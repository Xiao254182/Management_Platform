from datetime import date

from flask import Blueprint, jsonify, request

from config import db
from models.attendances import Attendance
from models.department import Department
from models.user import User

attendances_bp = Blueprint('attendances', __name__)


@attendances_bp.route('/attendances', methods=['GET'])
def attendances():
    params = request.args.to_dict()
    department_name = params.get('departmentName')
    state_id = params.get('stateID')

    users_query = User.query
    if department_name:
        users_query = users_query.join(Department, User.departmentId == Department.id).filter(
            Department.name == department_name)

    users = users_query.all()

    # Fetch attendance records for the current month if not initialized
    for user in users:
        attendance_records = Attendance.query.filter_by(workNumber=user.workNumber).first()

        if not attendance_records:
            attendance_records = Attendance(workNumber=user.workNumber)
            db.session.add(attendance_records)
            db.session.commit()

    # Update attendance status for dates prior to current day
    current_day = date.today().day
    attendances = Attendance.query.all()

    for attendance in attendances:
        for day_number in range(1, 32):
            day_column = f"day{day_number:02}"
            if day_number < current_day:
                if getattr(attendance, day_column) is None or getattr(attendance, day_column) == '未考勤':
                    setattr(attendance, day_column, 7)

    db.session.commit()

    # Prepare response data based on stateID
    rows = []

    for user in users:
        attendance_records = Attendance.query.filter_by(workNumber=user.workNumber).first()
        department = Department.query.filter_by(id=user.departmentId).first()
        if state_id:
            try:
                state_ids = [int(id.strip()) for id in state_id.split(',')]
            except ValueError:
                pass
        else:
            state_ids = []
        attendance_data = []
        for day in range(1, 32):
            day_key = f"day{day:02}"
            day_value = getattr(attendance_records, day_key)
            if day_value is not None and day_value != 7:
                if state_ids:
                    day_value = int(day_value)
                    if day_value in state_ids:
                        attendance_data.append({
                            "day": f"202406{day:02}",
                            "adtStatu": day_value
                        })
                    else:
                        slot = 7
                        attendance_data.append({
                            "day": f"202406{day:02}",
                            "adtStatu": slot
                        })
                else:
                    try:
                        day_value = int(day_value)
                    except ValueError:
                        pass
                    attendance_data.append({
                        "day": f"202406{day:02}",
                        "adtStatu": day_value
                    })

        row = {
            "id": user.id,
            "userId": user.id,
            "username": user.username,
            "mobile": user.mobile,
            "workNumber": user.workNumber,
            "departmentId": user.departmentId,
            "departmentName": department.name if department else None,
            "attendanceRecord": attendance_data
        }
        # Filter rows based on stateID
        rows.append(row)

    response_data = {
        "success": True,
        "code": 200,
        "data": {
            "data": {
                "total": len(rows),
                "rows": rows
            },
            "tobeTaskCount": 0,
            "monthOfReport": 6,
            "yearOfReport": 2024
        },
        "message": "执行成功"
    }
    return jsonify(response_data)


@attendances_bp.route('/attendances/<int:id>', methods=['PUT'])
def update_attendance(id):
    # Fetch attendance record by id
    attendance = Attendance.query.get_or_404(id)

    # Assuming you receive updated data in JSON format from the client
    request_data = request.get_json()

    # Extract day from request_data
    day = request_data['day']

    # Extract last two digits from day
    day_suffix = day[-2:]

    # Update each day's status based on the received data
    for day_number in range(1, 32):
        day_key = f"day{day_number:02}"  # Ensure day number is formatted with leading zeros
        day_key_suffix = day_key[-2:]

        if day_key_suffix == day_suffix:
            # Update attendance record for this specific day
            setattr(attendance, day_key, request_data['adtStatu'])

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Attendance record updated successfully"
    })
