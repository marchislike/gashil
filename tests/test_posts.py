import pytest
import sys
import os
from pymongo import MongoClient

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = "mongodb://localhost:27017/testDatabase"
    app.config['DB_NAME'] = "testDatabase"
    client = MongoClient(app.config["MONGO_URI"])
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_post(client):
    response = client.post('/posts', json={
        'user_id': 'user_id_111',
        'departure': '기숙사',
        'arrival': '대전역',
        'date': '2024-08-01T10:00:00Z',
        'memo': '짐이 많습니다.',
        'limit': 4
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == '게시글이 등록되었습니다.'

    # DB에 post가 있는지 확인
    response = client.get('/posts')
    posts = response.get_json()
    assert len(posts) == 1
    assert posts[0]['departure'] == '기숙사'
    assert posts[0]['arrival'] == '대전역'
    assert posts[0]['current_count'] == 1

def test_update_post(client):
    response = client.post('/posts', json={
        'user_id': 'user_id_111',
        'departure': '기숙사',
        'arrival': '대전역',
        'date': '2024-08-01T10:00:00Z',
        'memo': '집에 갑시다.',
        'limit': 4
    })
    assert response.status_code == 201
    post_id = response.get_json()['_id']

    update_data = {
        'departure': '문지기숙사',
        'arrival': '대전역',
        'memo': '수정된 메모'
    }

    response = client.put(f'/posts/{post_id}', json=update_data)
    assert response.status_code == 200
    assert response.get_json()['message'] == '게시글이 수정되었습니다.'

    response = client.get(f'/posts/{post_id}')
    print(response.data)  # 디버그 출력 추가
    updated_post = response.get_json()
    assert updated_post is not None
    assert updated_post['arrival'] == '대전역'
    assert updated_post['memo'] == '수정된 메모'
    assert updated_post['departure'] == '문지기숙사'

def test_delete_post(client):
    response = client.post('/posts', json={
        'user_id': 'user_id_111',
        'departure': '기숙사',
        'arrival': '대전역',
        'date': '2024-08-01T10:00:00Z',
        'memo': '갑시다.',
        'limit': 4
    })
    assert response.status_code == 201
    post_id = response.get_json()['_id']

    response = client.delete(f'/posts/{post_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == '게시글이 삭제되었습니다.'

    response = client.get(f'/posts/{post_id}')
    print(response.data)  # 디버그 출력 추가
    assert response.status_code == 404
