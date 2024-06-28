from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from config import db

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mobile = data.get('mobile')
    password = data.get('password')

    # 假设验证成功后
    if mobile == "13800000002" and password == "hm#qd@23!":
        # 创建访问令牌
        access_token = create_access_token(identity=mobile)

        response_data = {
            'message': 'Login successful',
            'success': True,
            'code': 200,
            'data': access_token,
        }
        return jsonify(response_data)
    else:
        # 处理验证失败情况
        response_data = {
            'message': 'Invalid credentials',
            'success': False,
            'code': 401
        }
        return jsonify(response_data), 401
