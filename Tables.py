from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Scheduler.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(250))
    courseName = db.Column(db.String(250))

    def __init__(self, course_id, department, courseName):
        self.course_id = course_id
        self.department = department
        self.courseName = courseName

class Professors(db.Model):
    prof_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    department = db.Column(db.String(250))
    join_date = db.Column(db.String(250))

    def __init__(self, prof_id, name, department, join_date):
        self.prof_id = prof_id
        self.department = department
        self.name = name
        self.join_date = join_date

class CourseTimeSlots(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey(Courses.course_id), nullable=False, primary_key=True)
    dayOfWeek = db.Column(db.String(250), primary_key=True)
    prof_id = db.Column(db.Integer, db.ForeignKey(Professors.prof_id), nullable=False, primary_key=True)

    def __init__(self, course_id, dayOfWeek, prof_id):
        self.course_id = course_id
        self.dayOfWeek = dayOfWeek
        self.prof_id = prof_id


class Students(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birthdate = db.Column(db.String(250))
    major = db.Column(db.String(250))
    enrollment_date = db.Column(db.String(250))

    def __init__(self, student_id, name, birthdate, major, enrollment_date):
        self.student_id = student_id
        self.name = name
        self.birthdate = birthdate
        self.major = major
        self.enrollment_date = enrollment_date
		
class Professors(db.Model):
    professor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    department = db.Column(db.String(250))
    join_date = db.Column(db.String(250))

    def __init__(self, professor_id, name, department, join_date):
        self.professor_id = professor_id
        self.name = name
        self.department = department
        self.join_date = join_date

class Reviews(db.Model):
	review_id = db.Column(db.Integer, primary_key=True)
	semester = db.Column(db.String(250))
	course_id = db.Column(db.Integer, db.ForeignKey(Courses.course_id), nullable=False)
	review = db.Column(db.String(250))
	review_date = db.Column(db.DateTime, onupdate=datetime.now())
	student_id = db.Column(db.Integer, db.ForeignKey(Students.student_id), nullable=False)
	
	def __init__(self, review_id, semester, course_id, review, review_date, student_id):
		self.review_id = review_id
		self.semester = semester
		self.course_id = course_id
		self.review = review
		self.review_date = review_date
		self.student_id = student_id
		
class StudentSchedule(db.Model):
	student_id = db.Column(db.Integer, db.ForeignKey(Students.student_id), nullable=False, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey(Courses.course_id), nullable=False, primary_key=True)
	
	def __init__(self, student_id, course_id):
		self.student_id = student_id
		self.course_id = course_id    