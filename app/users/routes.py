from flask import request, jsonify, render_template
from . import users_bp

@users_bp.route('/', methods=['GET, POST'])
def login_route():
    if request.method == 'GET':
        return render_template('./pages/login.html')
        