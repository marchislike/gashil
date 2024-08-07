from flask import Blueprint, jsonify, current_app
from .utils import check_db_connection

mypage_bp = Blueprint('mypage', __name__)

@mypage_bp.route('/mypage/<user_id>', methods=['GET'])
@check_db_connection
def get_user_profile(user_id):
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
