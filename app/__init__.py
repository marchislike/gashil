from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, errors
from .utils import check_db_connection
from .posts import posts_bp
from .mypage import mypage_bp
from .users import users_bp
from .routes import routes_bp
import os


def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates')) #cwd - current working directory 현재 작업 절대경로 반환
    app.config["MONGO_URI"] = "mongodb+srv://kimwatson2026:whsdhkttms2026@gashil.yhejgv0.mongodb.net/?retryWrites=true&w=majority&appName=Gashil"
    app.config["DB_NAME"] = 'gashil'

    try:
        client = MongoClient(app.config["MONGO_URI"])
        app.db = client[app.config["DB_NAME"]]
    except errors.ServerSelectionTimeoutError as err:
        app.db = None

    @app.route('/')
    def home():
        return render_template('layout.html')
    
    app.register_blueprint(posts_bp)
    app.register_blueprint(mypage_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(routes_bp)
    
    return app