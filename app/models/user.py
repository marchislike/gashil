import bcrypt
from flask import current_app

def create_user(user_id, password, nickname):
    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    user = {'user_id': user_id, 'password': password_hash, 'nickname': nickname}
    current_app.db.users.insert_one(user)

def verify_user(user_id, password):
    user = current_app.db.users.find_one({'user_id': user_id})
    if user:
        if bcrypt.checkpw(password.endcode('utf-8'), user['password']):
            return True
    return False