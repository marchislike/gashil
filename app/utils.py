from flask import jsonify, current_app
from functools import wraps #*데코레이터로 DB connection check

HTTP_BAD_REQUEST = 400

def check_required_fields(required_fields, data):
    # 필수 필드 중 데이터에 없거나 None인 필드를 찾음
    invalid_fields = [field for field in required_fields if field not in data or data[field] is None]
    if invalid_fields:
        error_message = f"필수 항목을 채워주세요!: {', '.join(invalid_fields)}"
        return jsonify({"error": error_message}), HTTP_BAD_REQUEST
    return None
    
def check_db_connection(db_check):
    @wraps(db_check)
    def decorated_function(*args, **kwargs): #kwargs: keyword 인자
        if current_app.db is None:
            return jsonify({"error": "DB 연결이 되어있지 않습니다."}), 500
        return db_check(*args, **kwargs)
    return decorated_function
