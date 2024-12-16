from flask import Blueprint
from controllers.UserController import login_user, register_user, getUser
from auth import token_required

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/user/<user_id>', methods=['GET'])(token_required(getUser))
user_bp.route('/login', methods=['POST'])(login_user)
user_bp.route('/register', methods=['POST'])(register_user)
