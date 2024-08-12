from flask import Flask, render_template, request, jsonify, current_app, session
from pymongo import MongoClient, errors
from .posts import posts_bp
from .users import users_bp
from .routes import routes_bp
import os


def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder=os.path.join(os.getcwd(), 'static'))
    app.config["MONGO_URI"] = "mongodb+srv://[username]:[password]@gashil.yhejgv0.mongodb.net/?retryWrites=true&w=majority&appName=Gashil"
    app.config["DB_NAME"] = 'gashil'
    app.secret_key = 'super_ultra_mega_SECRET_for_real'

    try:
        client = MongoClient(app.config["MONGO_URI"])
        app.db = client[app.config["DB_NAME"]]
    except errors.ServerSelectionTimeoutError as err:
        app.db = None

    @app.before_request
    def before_request():
        if current_app.db is None:
            return jsonify({"error": "DB 연결이 되어있지 않습니다."}), 500

        excluded_paths = ['/join']
        if any(request.path.startswith(path) for path in excluded_paths):
            return

    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(routes_bp)
    
    return app
