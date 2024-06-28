from config import db, app


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    name = db.Column(db.String(255))
    code = db.Column(db.String(20))
    managerId = db.Column(db.Integer)
    managerName = db.Column(db.String(255))
    introduce = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Department {self.name}>"


with app.app_context():
    db.create_all()
