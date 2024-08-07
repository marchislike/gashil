from flask import Blueprint, request, jsonify, current_app, redirect, url_for, render_template, session
from app.models.user import create_user, check_duplicated_userId, verify_user
import logging

users_bp = Blueprint('users', __name__)
logger = logging.getLogger(__name__)

# 회원 가입
@users_bp.route('/users', methods=['POST'])
def join_user():
    payload = None
    try:
        payload = request.form.to_dict()
        user_id, password, nickname = payload['user_id'], payload['password'], payload['nickname']
        if not user_id or not password or not nickname:
            return render_template('./pages/join.html', error="필수 항목을 채워주세요.", form_data=payload)
        
        duplicated = check_duplicated_userId(user_id)
        if duplicated:
            return render_template('./pages/join.html', id_error="중복된 아이디예요.", form_data=payload)
        
        create_user(user_id, password, nickname)
        return redirect('/login')
    except Exception as e:
        logger.debug("Exception Error: %s", e) 
        return render_template('./pages/join.html', error="알 수 없는 에러가 발생했어요. 다시 시도해주세요😿", form_data=payload)

# 로그인
@users_bp.route('/users/login', methods=['POST'])
def login():
    payload = None
    try:
        payload = request.form.to_dict()
        user_id, password = payload['user_id'], payload['password']
        if not user_id or not password:
            return render_template('./pages/login.html', error="필수 항목을 채워주세요.", form_data=payload)
        
        verified = verify_user(user_id, password)
        if not verified:
            return render_template('./pages/login.html', error="아이디나 비밀번호가 일치하지 않습니다.", form_data=payload)
        
        session['user_id'] = user_id
        return render_template('/pages/main.html')
    except Exception as e:
        logger.debug("Exception Error: %s", e) 
        return render_template('./pages/login.html', error="알 수 없는 에러가 발생했어요. 다시 시도해주세요😿", form_data=payload) 


# 마이페이지 글 조회
@users_bp.route('/mypage', methods=['GET'])
def get_user_posts():
    user_id = session.get('user_id')
    try:
        # 내가 작성한 글
        authored_posts = list(current_app.db.posts.find({"user_id": user_id}))
        for post in authored_posts:
            post['_id'] = str(post['_id'])

        # 내가 참여를 누른 글
        participated_posts = list(current_app.db.posts.find({"participants": user_id}))
        for post in participated_posts:
            post['_id'] = str(post['_id'])

        posts = authored_posts + participated_posts
        return render_template('./pages/mypage.html', posts= posts ,user_id = user_id)
    
    except Exception as e:
        logger.debug("Exception Error: %s", e) 
        return render_template('./pages/mypage.html', error="알 수 없는 에러가 발생했어요. 다시 시도해주세요😿", user_id = session.get('user_id')) 
