import pytest
import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from pymongo import MongoClient

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = "mongodb://localhost:27017/testDatabase"
    app.config['DB_NAME'] = "testDatabase"
    client = MongoClient(app.config["MONGO_URI"])
    app.db = client[app.config['DB_NAME']]
    with app.test_client() as client:
        with app.app_context():
            app.db.users.drop()
            app.db.posts.drop()  # 테스트 전에 데이터베이스 초기화
            yield client

def test_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_post(client):
    response = client.post('/posts', json={
        'user_id': 'user_id_1',
        'departure': '기숙사',
        'arrival': '대전역',
        'date': '2024-08-01T10:00:00Z',
        'memo': '짐이 많습니다.',
        'limit': 4
    })
    assert response.status_code == 201  # 오타 수정
    data = response.get_json()
    assert data['message'] == '파티원 모집글이 성공적으로 등록되었습니다.'

    # DB에 post가 있는지 확인
    response = client.get('/posts')
    posts = response.get_json()
    assert len(posts) == 1
    assert posts[0]['departure'] == '기숙사'
    assert posts[0]['arrival'] == '대전역'
    assert posts[0]['current_count'] == 1

# 수정
def test_update_post(client):
    response = client.post('/posts', json={
        'user_id': 'user_id_1',
        'departure': '기숙사',
        'arrival': '대전역',
        'date': '2024-08-01T10:00:00Z',
        'memo': '짐이 많습니다.',
        'limit': 4
    })
    assert response.status_code == 201
    post_id = response.get_json()['_id']

    update_data = {
        'departure': '기숙사',
        'arrival': '서울역',
        'memo': '수정된 메모'
    }

    response = client.put(f'/posts/{post_id}', json=update_data)
    assert response.status_code == 200
    assert response.get_json()['message'] == '게시글이 수정되었습니다.'

    response = client.get('/posts')
    posts = response.get_json()
    assert len(posts) == 1
    assert posts[0]['arrival'] == '서울역'
    assert posts[0]['memo'] == '수정된 메모'

# 삭제
def test_delete_post(client):
    response = client.post('/posts', json={
        'user_id': 'user_id_1',
        'departure': '기숙사',
        'arrival': '대전역',
        'date': '2024-08-01T10:00:00Z',
        'memo': '짐이 많습니다.',
        'limit': 4
    })
    assert response.status_code == 201
    post_id = response.get_json()['_id']

    response = client.delete(f'/posts/{post_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == '게시글이 성공적으로 삭제되었습니다.'

    response = client.get('/posts')
    posts = response.get_json()
    assert len(posts) == 0
