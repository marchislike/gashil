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
    post_id = data.get('_id')
    user_id = session['user_id']
    
    try:
        if action == 'edit':
            return render_template('./pages/new.html', post=data, title='수정하기' )
        elif action == 'delete':
            return delete_post(post_id)
        elif action == 'cancel':
            return cancel_participation(post_id, user_id)
        elif action == 'participate':
            return participate_post(post_id, user_id)
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
        return redirect('/')
    except Exception as e:
        logger.debug("Exception Error: %s", e)
        return redirect('/')
    

def participate_post(post_id, user_id):
    try:
        post = current_app.db.posts.find_one({'_id': ObjectId(post_id)})
        if not post:
            logger.info(f"이미 삭제된 게시글입니다.")
            return redirect('/')
        
        # 참여인원이 최대 모집인원을 넘지 않도록 설정
        current_count = len(post.get('participants', []))
        rides_limit = int(post.get('rides_limit', 0))
        if current_count >= rides_limit:
            logger.info(f"참여인원이 최대 모집인원을 넘습니다.")
            return redirect('/')
        result = current_app.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$addToSet': {'participants': user_id},
             '$inc': {'current_count': 1}
            },
        )

        if result.matched_count:
            return redirect('/mypage')
    except Exception as e:
        logger.debug("Exception Error: %s", e)
        return redirect('/')

def cancel_participation(post_id, user_id):
    try:
        result = current_app.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$pull': {'participants': user_id},
              '$inc': {'current_count': -1}}
        )
        if result.matched_count:
            logger.info(f"게시글 : {post_id}의 참여가 취소되었습니다.")
            return redirect('/')
    except Exception as e:
        logger.debug("Exception Error: %s", e)
        return redirect('/')
