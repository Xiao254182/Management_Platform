from config import db, app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    mobile = db.Column(db.String(20))
    workNumber = db.Column(db.String(20))
    departmentId = db.Column(db.Integer)
    def __repr__(self):
        return f"<User {self.username}>"


with app.app_context():
    db.create_all()
