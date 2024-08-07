from flask import Blueprint

member_bp = Blueprint('members', __name__)

from . import routes