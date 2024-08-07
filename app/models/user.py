import bcrypt
from pytz import timezone
from flask import current_app
from datetime import datetime

def check_duplicated_userId(user_id):
    user = current_app.db.users.find({'user_id': user_id})
    if list(user):
        return True
    return False

def create_user(user_id, password, nickname):
    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    current_time = datetime.now(timezone('Asia/Seoul'))
    user = {'user_id': user_id, 'password': password_hash, 'nickname': nickname, 'created_at':current_time, 'updated_at': current_time}
    return current_app.db.users.insert_one(user)

def verify_user(user_id, password):
    user = current_app.db.users.find_one({'user_id': user_id})
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return True
    return False