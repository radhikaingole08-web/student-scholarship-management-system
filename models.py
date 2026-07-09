from datetime import datetime
from db import db


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    year_of_study = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Scholarship(db.Model):
    __tablename__ = "scholarships"

    scholarship_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    last_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Open")
    application_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    __tablename__ = "applications"

    application_id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.student_id'),
        nullable=False
    )

    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey('scholarships.scholarship_id'),
        nullable=False
    )

    status = db.Column(db.String(20), default="Pending")

class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)