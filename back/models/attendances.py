from config import db, app


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workNumber = db.Column(db.String(255))
    day01 = db.Column(db.String(255))
    day02 = db.Column(db.String(255))
    day03 = db.Column(db.String(255))
    day04 = db.Column(db.String(255))
    day05 = db.Column(db.String(255))
    day06 = db.Column(db.String(255))
    day07 = db.Column(db.String(255))
    day08 = db.Column(db.String(255))
    day09 = db.Column(db.String(255))
    day10 = db.Column(db.String(255))
    day11 = db.Column(db.String(255))
    day12 = db.Column(db.String(255))
    day13 = db.Column(db.String(255))
    day14 = db.Column(db.String(255))
    day15 = db.Column(db.String(255))
    day16 = db.Column(db.String(255))
    day17 = db.Column(db.String(255))
    day18 = db.Column(db.String(255))
    day19 = db.Column(db.String(255))
    day20 = db.Column(db.String(255))
    day21 = db.Column(db.String(255))
    day22 = db.Column(db.String(255))
    day23 = db.Column(db.String(255))
    day24 = db.Column(db.String(255))
    day25 = db.Column(db.String(255))
    day26 = db.Column(db.String(255))
    day27 = db.Column(db.String(255))
    day28 = db.Column(db.String(255))
    day29 = db.Column(db.String(255))
    day30 = db.Column(db.String(255))
    day31 = db.Column(db.String(255))

    def __repr__(self):
        return f"<Attendances {self.id}>"


with app.app_context():
    db.create_all()
