from datetime import datetime

from flask import Blueprint, request, jsonify

from config import db
from models.department import Department

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
def profile():
    response_data = {
        "success": True,
        "code": 200,
        "data": {
            "roles": {
                "menus": [
                    "department",
                    "employee",
                    "approval",
                    "attendance",
                ],
            },
            "companyId": "1",
            "company": "xx学院",
            "userId": 1,
            "mobile": "13800000002",
            "username": "管理员",
            "staffPhoto": "https://heimahr.itheima.net/defaultHead.png",
            "departmentName": "云计算技术与应用",
            "departmentId": 1,
        },
        "message": "获取资料成功"
    }
    # Check if the department with id=1 already exists
    existing_department = Department.query.filter_by(id=1).first()

    if not existing_department:
        # Create a new department object
        main_department = Department(
            id=1,
            pid=0,
            name="云计算技术与应用",
            code="YJSJSYYY",
            managerId=0,
            managerName="管理员",
            introduce="根",
            createTime=datetime.now(),
        )

        # Add new department to the database session
        db.session.add(main_department)
        db.session.commit()
    return jsonify(response_data)
