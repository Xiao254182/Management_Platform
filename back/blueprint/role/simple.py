from flask import Blueprint, jsonify

from models.user import User

simple_bp = Blueprint('simple', __name__)


@simple_bp.route('/user/simple', methods=['GET'])
def user_simple():
    try:
        # Query all Simple objects from the database
        user_data = User.query.all()

        # Serialize data into JSON-compatible format
        data = []
        for user in user_data:
            data.append({
                "id": user.id,
                "username": user.username
            })

        # Prepare response data
        response_data = {
            "success": True,
            "code": 200,
            "data": data,
            "message": "获取员工简单列表成功"
        }
        return jsonify(response_data)

    except Exception as e:
        # Handle exceptions, log errors, etc.
        response_data = {
            "success": False,
            "code": 500,
            "message": f"获取员工简单列表失败: {str(e)}"
        }
        return jsonify(response_data)