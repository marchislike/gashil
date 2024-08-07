from flask import Blueprint, request, jsonify, current_app
import datetime
from .utils import check_required_fields, check_db_connection
import bcrypt

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
@check_db_connection
def create_user():
    try:
        data = request.get_json()
        required_fields = ["user_id", "password", "nickname"]
        error_response = check_required_fields(required_fields, data)
        if error_response:
            return error_response

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        current_time = datetime.datetime.utcnow()
        user = {
            "user_id": data['user_id'],
            "password_hash": hashed_password,
            "nickname": data['nickname'],
            "created_at": current_time,
            "updated_at": current_time
        }
        result = current_app.db.users.insert_one(user)
        return jsonify({"message": "회원가입이 완료되었습니다.", "user_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


## 사용자 프로필에서 글 모음 조회
@users_bp.route('/users/<user_id>/posts', methods=['GET'])
@check_db_connection
def get_user_posts(user_id):
    try:
        # 내가 작성한 글
        authored_posts = list(current_app.db.posts.find({"user_id": user_id}))
        for post in authored_posts:
            post['_id'] = str(post['_id'])

        # 내가 참여를 누른 글
        participated_posts = list(current_app.db.posts.find({"participants": user_id}))
        for post in participated_posts:
            post['_id'] = str(post['_id'])

        response = {
            "authored_posts": authored_posts,
            "participated_posts": participated_posts
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
