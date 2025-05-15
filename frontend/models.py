from flask_login import UserMixin

from . import db


class Administrator(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Professor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    classes = db.relationship("Class", back_populates="professor")


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    credits = db.Column(db.Integer)

    classes = db.relationship(
        "Class", secondary="student_class", back_populates="students"
    )


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    course_name = db.Column(db.String(100))
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"))

    professor = db.relationship("Professor", back_populates="classes")
    students = db.relationship(
        "Student", secondary="student_class", back_populates="classes"
    )


class Student_Class(db.Model):
    __tablename__ = "student_class"

    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), primary_key=True)
