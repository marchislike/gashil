import logging
from flask import Blueprint, request, jsonify, current_app, redirect, url_for
from bson.objectid import ObjectId
from .utils import check_required_fields

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

posts_bp = Blueprint('posts', __name__)

# 조회
@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = list(current_app.db.posts.find())
        for post in posts:
            post['_id'] = str(post['_id'])
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@posts_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = current_app.db.posts.find_one({'_id': ObjectId(post_id)})
        if post:
            post['_id'] = str(post['_id'])
            return jsonify(post), 200
        else:
            return jsonify({"error": "게시글을 찾을 수 없습니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 등록
@posts_bp.route('/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        required_fields = ["departure", "arrival", "date", "limit"]
        error_response = check_required_fields(required_fields, data)
        if error_response:
            return error_response
        user_id = data['user_id']
        post = {
            "user_id": user_id,
            "departure": data['departure'],
            "arrival": data['arrival'],
            "date": data['date'],
            "memo": data['memo'],
            "limit": data['limit'],
            "current_count": 1,
            "participants": [user_id]
        }
        result = current_app.db.posts.insert_one(post)
        post['_id'] = str(result.inserted_id)
        
        
        logger.info(f"게시글이 등록되었습니다. post_id: {post['_id']}")
        
        # 리다이렉트 추가
        return redirect(url_for('routes.home'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 수정
@posts_bp.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        data = request.get_json()
        update_fields = {key: value for key, value in data.items() if key != '_id'}
        required_fields = ["departure", "arrival", "date", "limit"]
        error_response = check_required_fields(required_fields, update_fields)
        if error_response:
            return error_response
        result = current_app.db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': update_fields})
        if result.matched_count:
            logger.info(f"게시글 : {post_id}가 수정되었습니다.")
            
            # 리다이렉트 추가
            return redirect(url_for('routes.home'))
        else:
            return jsonify({"error": "이미 삭제된 게시글입니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 삭제
@posts_bp.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        result = current_app.db.posts.delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count:
            logger.info(f"게시글 : {post_id}가 삭제되었습니다.")
            
            # 리다이렉트 추가
            return redirect(url_for('routes.home'))
        else:
            return jsonify({"error": "이미 삭제된 게시글입니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

## 참여 여부 ##

@posts_bp.route('/posts/<post_id>/participation', methods=['PUT'])
def participate_post(post_id):
    try:
        data = request.get_json()
        #! 로그인 기능 구현 후 수정 세션으로 얻기(-)
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "로그인이 필요합니다."}), 401
        
        post = current_app.db.posts.find_one({'_id': ObjectId(post_id)})
        if not post:
            return jsonify({"error": "이미 삭제된 게시글입니다."}), 404

        # 참여인원이 최대 모집인원을 넘지 않도록 설정
        current_count = len(post.get('participants', []))
        limit = post.get('limit', 0)
        if current_count >= limit:
            return jsonify({"error": "참여 인원이 초과되었습니다."}), 400
        
        
        result = current_app.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$addToSet': {'participants': user_id}}
        )

        if result.matched_count:
            return jsonify({"message": "참여가 완료되었습니다."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@posts_bp.route('/posts/<post_id>/participation', methods=['DELETE'])
def cancel(post_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "로그인이 필요합니다."}), 400

        result = current_app.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$pull': {'participants': user_id}}
        )

        if result.matched_count:
            return jsonify({"message": "참여가 취소되었습니다."}), 200
        else:
            return jsonify({"error": "이미 삭제된 게시글입니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
