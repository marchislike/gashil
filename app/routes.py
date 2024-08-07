from flask import Blueprint, render_template, session,redirect

routes_bp = Blueprint('routes', __name__)

# USER
@routes_bp.route('/')
def home():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('./pages/main.html')

@routes_bp.route('/join')
def join_page():
    return render_template('./pages/join.html')

@routes_bp.route('/login')
def login_page():
    if session.get('user_id'):
        return redirect('/')
    return render_template('./pages/login.html')

# POST
@routes_bp.route('/posts/new')
def new_post_page():
    return render_template('./pages/new.html', title='글쓰기')

@routes_bp.route('/posts/<post_id>')
def edit_post_page():
    return render_template('')
