from extensions import db

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    deadline = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))