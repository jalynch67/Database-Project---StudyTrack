from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Subject(db.Model):
    """Store a subject and its basic details."""

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    colour = db.Column(db.String(20), nullable=False, default="blue")
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    tasks = db.relationship(
        "StudyTask",
        backref="subject",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<Subject {self.name}>"


class StudyTask(db.Model):
    """Store a study task linked to a subject."""

    __tablename__ = "study_tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="medium")
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<StudyTask {self.title}>"
