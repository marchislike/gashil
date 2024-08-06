from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import os

def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.config["MONGO_URI"] = "mongodb+srv://kimwatson2026:whsdhkttms2026@gashil.yhejgv0.mongodb.net/?retryWrites=true&w=majority&appName=Gashil"
    app.config["DB_NAME"] = 'gashil'

    try:
        client = MongoClient(app.config["MONGO_URI"])
        app.db = client[app.config["DB_NAME"]]
    except errors.ServerSelectionTimeoutError as err:
        app.db = None

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/posts', methods=['GET'])
    def get_posts():
        try:
            posts = list(app.db.posts.find())
            posts = convert_objectid_to_str(posts)
            return jsonify(posts), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/posts', methods=['POST'])
    def create_post():
        try:
            data = request.get_json()
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
            return jsonify({"message": "파티원 모집글이 성공적으로 등록되었습니다.", "_id": str(result.inserted_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    #참석 여부 -- 
    
    
    
    
    
    #등록자 수정, 삭제

    @app.route('/posts/<post_id>', methods=['PUT'])
    def update_post(post_id):
        try:
            if app.db is None:
                raise errors.ServerSelectionTimeoutError("Database not connected")
            data = request.get_json()
            update_fields = {k: v for k, v in data.items() if k != '_id'}
            result = app.db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': update_fields})
            if result.matched_count:
                return jsonify({"message": "게시글이 수정되었습니다."}), 200
            else:
                return jsonify({"error": "Post not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/posts/<post_id>', methods=['DELETE'])
    def delete_post(post_id):
        try:
            if app.db is None:
                raise errors.ServerSelectionTimeoutError("Database not connected")
            result = app.db.posts.delete_one({'_id': ObjectId(post_id)})
            if result.deleted_count:
                return jsonify({"message": "게시글이 성공적으로 삭제되었습니다."}), 200
            else:
                return jsonify({"error": "Post not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
