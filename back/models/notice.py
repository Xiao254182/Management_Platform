from config import app, db


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(255))
    notice = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Notice {self.id}>"


with app.app_context():
    db.create_all()
