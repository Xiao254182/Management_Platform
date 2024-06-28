from flask import Blueprint, jsonify, request
from config import db
from models.department import Department
from models.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['POST'])
def create_user():
    # 解析请求中的 JSON 数据
    data = request.json

    # 创建新用户
    new_user = User(
        username=data.get('username'),
        mobile=data.get('mobile'),
        workNumber=data.get('workNumber'),
        departmentId=data.get('departmentId')
    )

    # 将新用户添加到数据库会话中
    db.session.add(new_user)
    db.session.commit()

    # 构建返回的 JSON 数据结构
    response_data = {
        "success": True,
        "code": 201,
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "mobile": new_user.mobile,
            "workNumber": new_user.workNumber,
            "departmentId": new_user.departmentId,
        },
        "message": "成功创建新用户"
    }
    return jsonify(response_data), 200


@user_bp.route('/user', methods=['GET'])
def get_all_users():
    # 获取查询参数
    departmentId = request.args.get('departmentId', type=int)
    page = request.args.get('page', default=1, type=int)
    pagesize = request.args.get('pagesize', default=10, type=int)
    keyword = request.args.get('keyword', type=str)
    print(keyword)
    # 构建查询
    query = User.query
    if departmentId == 1:
        if keyword:
            query = query.filter(User.username.like(f"%{keyword}%"))
            print(keyword)
        else:
            query = query.filter()
    elif departmentId:
        query = query.filter_by(departmentId=departmentId)

    # 分页处理
    pagination = query.paginate(page=page, per_page=pagesize, error_out=False)
    users = pagination.items

    # 构建返回的 JSON 数据结构
    rows = []
    for user in users:
        # 查询部门名称
        department = Department.query.filter_by(id=user.departmentId).first()

        # 构建每个用户的数据行
        row = {
            "id": user.id,
            "username": user.username,
            "mobile": user.mobile,
            "workNumber": user.workNumber,
            "departmentId": user.departmentId,
            "departmentName": department.name if department else None,
        }
        rows.append(row)

    response_data = {
        "success": True,
        "code": 200,
        "data": {
            "total": pagination.total,
            "rows": rows
        },
        "message": "获取员工列表成功"
    }
    return jsonify(response_data)


@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    # 查询用户
    user = User.query.get_or_404(id)

    # 构建返回的 JSON 数据结构
    response_data = {
        "success": True,
        "code": 200,
        "data": {
            "id": user.id,
            "username": user.username,
            "mobile": user.mobile,
            "workNumber": user.workNumber,
            "departmentId": user.departmentId,
        },
        "message": "获取员工信息成功"
    }
    return jsonify(response_data)


@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    # 查询用户
    user = User.query.get_or_404(id)

    related_data = User.query.filter_by(username=user.username).all()
    for data in related_data:
        db.session.delete(data)
    # 删除用户
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "成功删除用户"
    })


@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    # 查询用户
    user = User.query.get_or_404(id)

    # 解析请求中的 JSON 数据
    data = request.json

    # 更新用户信息
    user.username = data.get('username', user.username)
    user.mobile = data.get('mobile', user.mobile)
    user.workNumber = data.get('workNumber', user.workNumber)
    user.departmentId = data.get('departmentId', user.departmentId)

    # 提交更新到数据库
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "成功更新用户信息"
    })
