from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import os

from functools import wraps #*데코레이터로 DB connection check
from .utils import check_required_fields

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.config["MONGO_URI"] = "mongodb+srv://kimwatson2026:whsdhkttms2026@gashil.yhejgv0.mongodb.net/?retryWrites=true&w=majority&appName=Gashil"
    app.config["DB_NAME"] = 'gashil'

    try:
        client = MongoClient(app.config["MONGO_URI"])
        app.db = client[app.config["DB_NAME"]]
    except errors.ServerSelectionTimeoutError as err:
        app.db = None
        
    def check_db_connection(db_check):
        @wraps(db_check)
        def decorated_function(*args, **kwargs): #kwargs: keyword 인자
            if app.db is None:
                return jsonify({"error": "DB 연결이 되어있지 않습니다."}), 500
            return db_check(*args, **kwargs)
        return decorated_function

    @app.route('/')
    def home():
        return render_template('index.html')
    

    @app.route('/posts', methods=['GET'])
    @check_db_connection
    def get_posts():
        try:
            posts = list(app.db.posts.find())
            for post in posts: #* Objectid를 사용하면서 MongoDB에서 json 직렬화가 가능하도록
                post['_id'] = str(post['_id'])
            return jsonify(posts), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/posts/<post_id>', methods=['GET'])
    @check_db_connection
    def get_post(post_id):
        try:
            post = app.db.posts.find_one({'_id': ObjectId(post_id)})
            if post:
                post['_id'] = str(post['_id'])
                return jsonify(post), 200
            else:
                return jsonify({"error": "게시글을 찾을 수 없습니다."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @app.route('/posts', methods=['POST'])
    @check_db_connection
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
            result = app.db.posts.insert_one(post)
            post['_id'] = str(result.inserted_id)
            return jsonify({"message": "게시글이 등록되었습니다.", "_id": str(result.inserted_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    #등록자 수정, 삭제

    @app.route('/posts/<post_id>', methods=['PUT'])
    @check_db_connection
    def update_post(post_id):
        try:
            data = request.get_json()
            update_fields = {key: value for key, value in data.items() if key != '_id'}
            required_fields = ["departure", "arrival", "date", "limit"]
            
            error_response = check_required_fields(required_fields, update_fields)
            if error_response:
                return error_response
            
            result = app.db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': update_fields})
            if result.matched_count:
                return jsonify({"message": "게시글이 수정되었습니다."}), 200
            else:
                return jsonify({"error": "이미 삭제된 게시글입니다."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/posts/<post_id>', methods=['DELETE'])
    @check_db_connection
    def delete_post(post_id):
        try:
            result = app.db.posts.delete_one({'_id': ObjectId(post_id)})
            if result.deleted_count:
                return jsonify({"message": "게시글이 삭제되었습니다."}), 200
            else:
                return jsonify({"error": "이미 삭제된 게시글입니다."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    return app
