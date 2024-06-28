from datetime import datetime

from flask import Blueprint, jsonify, request

from config import db
from models.department import Department
from models.user import User

department_bp = Blueprint('department', __name__)


@department_bp.route('/company/department', methods=['GET'])
@department_bp.route('/company/department/<int:id>', methods=['GET'])
def get_department(id=None):
    if id is None:
        # 没有传递部门 ID，返回所有部门数据
        departments = Department.query.all()
    else:
        # 根据部门 ID 查询特定部门数据
        department = Department.query.get(id)
        if department is None:
            return jsonify({
                "success": False,
                "code": 404,
                "message": "部门不存在"
            }), 404

        # 将部门对象转换为 JSON 可序列化格式
        department_data = {
            "id": department.id,
            "pid": department.pid,
            "name": department.name,
            "code": department.code,
            "managerId": department.managerId,
            "managerName": department.managerName,
            "introduce": department.introduce,
        }
        return jsonify({
            "success": True,
            "code": 200,
            "data": department_data,
            "message": "获取部门数据成功"
        })

    # 转换数据库对象为 JSON 可序列化格式
    data = []
    for department in departments:
        department_data = {
            "id": department.id,
            "pid": department.pid,
            "name": department.name,
            "code": department.code,
            "managerId": department.managerId,
            "managerName": department.managerName,
            "introduce": department.introduce,
        }
        data.append(department_data)

    return jsonify({
        "success": True,
        "code": 200,
        "data": data,
        "message": "获取所有部门数据成功"
    })


@department_bp.route('/company/department', methods=['POST'])
def add_department():
    data = request.json
    code = data.get('code')
    introduce = data.get('introduce')
    managerId = data.get('managerId')
    name = data.get('name')
    pid = data.get('pid')

    manager = User.query.filter_by(id=managerId).first()
    managerName = manager.username if manager else None

    new_department = Department(
        code=code,
        introduce=introduce,
        managerId=managerId,
        managerName=managerName,
        name=name,
        pid=pid,
        createTime=datetime.now(),
    )
    try:
        db.session.add(new_department)
        db.session.commit()
        return {
            "success": True,
            "code": 200,
            "message": "部门新增成功"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "code": 500,
            "message": f"部门新增失败: {str(e)}"
        }
    finally:
        db.session.close()


@department_bp.route('/company/department/<int:id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get(id)
    if department is None:
        return jsonify({
            "success": False,
            "code": 404,
            "message": "部门不存在"
        }), 404

    data = request.json
    department.code = data.get('code', department.code)
    department.introduce = data.get('introduce', department.introduce)
    department.managerId = data.get('managerId', department.managerId)
    department.name = data.get('name', department.name)
    department.pid = data.get('pid', department.pid)
    department.managerName = User.query.get(data.get('managerId')).username if data.get('managerId') else None

    try:
        db.session.commit()
        return {
            "success": True,
            "code": 200,
            "message": "部门信息更新成功"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "code": 500,
            "message": f"部门信息更新失败: {str(e)}"
        }
    finally:
        db.session.close()


@department_bp.route('/company/department/<int:id>', methods=['DELETE'])
def delete_department(id):
    department = Department.query.get(id)
    if department is None:
        return jsonify({
            "success": False,
            "code": 404,
            "message": "部门不存在，无法删除"
        }), 404

    try:
        # Delete the department and its child departments recursively
        delete_recursive(department)
        db.session.commit()
        return {
            "success": True,
            "code": 200,
            "message": "部门删除成功"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "code": 500,
            "message": f"部门删除失败: {str(e)}"
        }
    finally:
        db.session.close()


def delete_recursive(department):
    # Delete child departments first
    child_departments = Department.query.filter_by(pid=department.id).all()
    for child in child_departments:
        delete_recursive(child)

    # Now delete the department itself
    db.session.delete(department)

    # Delete all associated data (assuming you have relationships defined in your models)
    related_data = User.query.filter_by(departmentId=department.id).all()
    for data in related_data:
        db.session.delete(data)
