from config import app, db

from blueprint.user.profile import profile_bp
from blueprint.attendances.attendances import attendances_bp
from blueprint.dashboard.notice import notice_bp
from blueprint.department.department import department_bp
from blueprint.role.simple import simple_bp
from blueprint.user.login import login_bp
from blueprint.user.user import user_bp

app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(department_bp)
app.register_blueprint(simple_bp)
app.register_blueprint(attendances_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
