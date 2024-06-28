from flask import Blueprint, jsonify
from models.notice import Notice

notice_bp = Blueprint('notice', __name__)


@notice_bp.route('/home/notice', methods=['GET'])
def home_notice():
    notices = Notice.query.all()

    data = []
    for notice in notices:
        notice_data = {
            "icon": notice.icon,
            "notice": notice.notice,
            "createTime": notice.createTime.strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(notice_data)

    response_data = {
        "success": True,
        "code": 200,
        "data": data,
        "message": "执行成功"
    }
    return jsonify(response_data)
