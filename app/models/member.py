import bcrypt
from flask import current_app

def create_user(user_id, password, nickname):
    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    user = {'user_id': user_id, 'password': password_hash, 'nickname': nickname}
    current_app.db.users.insert_one(user)
    