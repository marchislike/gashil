import logging
from flask import Blueprint, request, jsonify, current_app, redirect, url_for,render_template,session
from bson.objectid import ObjectId
from .utils import check_required_fields
from app.models.post import save_update_post
from datetime import datetime
from pytz import timezone

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

posts_bp = Blueprint('posts', __name__)

# 조회
@posts_bp.route('/', methods=['GET'])
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    try:
        posts = list(current_app.db.posts.find({"date": {"$gt": datetime.now(timezone('Asia/Seoul'))}}))
        for post in posts:
            post['_id'] = str(post['_id'])
            post['date'] = post['date'].strftime("%Y년 %m월 %d일 %H:%M")
        return render_template('./pages/main.html', posts= posts, user_id = user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 글(조회, 수정, 삭제) 버튼 핸들러
@posts_bp.route('/posts/form-handler', methods=['POST'])
def handle_post_buttons():
    data = request.form.to_dict()
    action = data.get('action')
    
    try:
        if action == 'edit':
            return render_template('./pages/new.html', post=data, title='수정하기' )
        elif action == 'delete':
            return delete_post(data)
        elif action == 'cancel':
            return cancel_participation(data)
        elif action == 'participate':
            return participate_post(data)
        else:
            return redirect('/')
    except Exception as e:
        logger.debug("Exception Error: %s", e)
        return redirect('/')


# 업데이트 핸들러
@posts_bp.route('/posts', methods=['POST'])
def update_create_post():
    try:
        data = request.form.to_dict()
        departure, destination, date, rides_limit, _id = data.get('departure'),data.get('destination'),data.get('date'),data.get('rides_limit'),data.get('_id')
        if not departure or not destination or not date or not rides_limit:
            return render_template('./pages/new.html', error="필수 항목을 채워주세요.", post=data)
            
        # 수정    
        if _id:
            update_fields = {key: value for key, value in data.items() if key != '_id'}
            update_fields['date'] =  datetime.strptime(date, "%Y년 %m월 %d일 %H:%M")
            result = current_app.db.posts.update_one({'_id': ObjectId(_id)}, {'$set': update_fields})
            if result.matched_count:
                logger.info(f"게시글 : {_id}가 수정되었습니다.")
            return redirect('/')
        
        # 등록
        else:
            user_id = session['user_id']
            print(type(date), date)
            post = {
                "user_id": user_id,
                "departure":departure,
                "destination": destination,
                "date": datetime.strptime(date, "%Y년 %m월 %d일 %H:%M"),
                "memo": data['memo'],
                "rides_limit": rides_limit,
                "current_count": 1,
                "participants": [user_id]
            }
            print(post)
            created = save_update_post(post)
            if created:
                return redirect('/')
    except Exception as e:
        logger.debug("Exception Error: %s", e) 
        return render_template('./pages/new.html', error="알 수 없는 에러가 발생했어요. 다시 시도해주세요😿", post=data)
    


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

def cancel_participation(post_id):
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
