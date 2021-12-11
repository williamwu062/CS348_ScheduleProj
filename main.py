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
		
class Reviews(db.Model):
	review_id = db.Column(db.Integer, primary_key=True)
	semester = db.Column(db.String(250))
	course_id = db.Column(db.Integer, db.ForeignKey("Courses.course_id"), nullable=False)
	review = db.Column(db.String(250))
	review_date = db.Column(db.DateTime, onupdate=datetime.now())
	student_id = db.Column(db.Integer, db.ForeignKey("Students.student_id"), nullable=False)
	
	def __init__(self, review_id, semester, course_id, review, review_date, student_id):
		self.review_id = review_id
		self.semester = semester
		self.course_id = course_id
		self.review = review
		self.review_date = review_date
		self.student_id = student_id


@app.route("/", methods=["POST", "GET"])
def home():
  print('hello')
  if request.form.get("addStudent"):
    return url_for("addStudent")
  if request.form.get("addProfessor"):
    return url_for("addProfessor")
  if request.form.get("addCourse"):
    return url_for("addCourse")
  if request.form.get("editCourse"):
    return url_for("editCourse")
  if request.form.get("viewCourses"):
    return url_for("viewCourses")
  if request.form.get("deleteEntry"):
    return url_for("deleteEntry")
  if request.form.get("viewCourseReviews"):
    return url_for("viewCourseReviews")
  if request.form.get("viewStudentSchedule"):
    return url_for("viewStudentSchedule")
  return render_template("index.html")

@app.route("/add_student", methods=["POST", "GET"])
def addStudent():
    if request.method == "POST":
        data = request.form
        for name in data.keys():
            print(name)
        print(data['enrolldate'])
        student = Students(int(data['id']), data['name'],
                           data['birthdate'], data['major'], data['enrolldate'])
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print('yo')
        return render_template("addStudent.html")


@app.route("/view_student", methods=["POST", "GET"])
def viewStudent():
    if request.method == "POST":
        id = int(request.form['id'])
        return redirect(url_for('viewStudentTable', id=id))
    else:
        return render_template("viewStudent.html")


@app.route("/<id>")
def viewStudentTable(id):
    return render_template("viewStudentTable.html", student=Students.query.filter_by(student_id=id).first())


@app.route("/add_professor")
def addProfessor():
    return render_template("addProfessor.html")


@app.route("/delete_entry")
def deleteEntry():
    return render_template("deleteEntry.html")


@app.route("/edit_course", methods=["POST", "GET"])
def editCourse():
    if request.method == "POST":
        data = request.form
        for name in data.keys():
            print(name)

        if data['id'] is not None and data['id'] != '':
            course = Courses.query.filter_by(course_id=data['id']).first()
            if course is not None:
              if data['department'] is not None and len(data['department']) > 0:
                course.department = data['department']
              if data['coursename'] is not None and len(data['coursename']) > 0:
                course.courseName = data['coursename']

        db.session.commit()
        return redirect(url_for('home'))
    else:
        print('yo')
        return render_template("editCourse.html")


@app.route("/add_course", methods=["POST", "GET"])
def addCourse():
  if request.method == "POST":
    data = request.form
    for name in data.keys():
      print(name)
    course = Courses(int(data['id']), data['department'], data['coursename'])
    db.session.add(course)
    db.session.commit()
    return redirect(url_for('home'))
  else:
    print('yo')
    return render_template("addCourse.html")
    
@app.route("/view_courses", methods=["POST", "GET"])
def viewCourses():
  if request.method == "POST":
    data = request.form
    department = data['department']
    courseName = data['coursename']

    groupBy = False
    if data.get('groupdept'):
      groupBy = True
      rawQuery = """SELECT department, sum(course_id) AS sumIDs FROM Courses GROUP BY department"""
      if data.get('alphabet'):
        rawQuery = rawQuery + """ ORDER BY department"""
        
    else:
      rawQuery = """SELECT * FROM Courses"""
      if courseName is not None and len(courseName) > 0:
        rawQuery = """SELECT * FROM Courses WHERE courseName=\"""" + courseName + """\""""
      if department is not None and len(department) > 0:
        rawQuery = """SELECT * FROM Courses WHERE department=\"""" + department + """\""""
        if courseName is not None and len(courseName) > 0:
          rawQuery = """SELECT * FROM Courses WHERE department=\"""" + department + """\" AND courseName=\"""" + courseName + """\""""
      if data.get('alphabet'):
        rawQuery = rawQuery + """ ORDER BY courseName"""
    
    queryResult = db.session.execute(rawQuery)

    courses = ""
    for row in queryResult:
      if groupBy:
        courses += "Department: " + row.department + ", Sum of IDs: " + str(row.sumIDs) + "\t"
      else:
        courses += "Course ID: " + str(row.course_id) + ", Course Name: " + row.courseName + ", Department: " + row.department + "\t"

    return render_template("viewCoursesList.html", courses=courses)

  else:
    return render_template("viewCourses.html")

@app.route("/view_course_reviews", methods=["POST", "GET"])
def viewCourseReviews():
	if request.method == "POST":
		#Get courseName that user put into the form
		data = request.form
		courseName = data['coursename']
		
		#Get the course_id associated with that courseName
		getCourseIDQuery = """SELECT course_id FROM Courses WHERE courseName=\"""" + courseName + """\""""
		result = db.session.execute(getCourseIDQuery).first()
		try:
			courseID = str(result.courseName)
		except AttributeError:
			returnString = "No course was found with that name."
			return render_template("viewCourseReviewsList.html", courseReviews=returnString)
			
		#Get course reviews associated with that course_id
		query = "SELECT * FROM Reviews AS R WHERE R.course_id = %s"
		result2 = db.session.execute(query, (courseID))
		
		courseReviews = ""
		#Collate course reviews into a string
		for row in result2:
			courseReviews += "Review ID: " + str(row.review_id) + ", Semester: " + str(row.semester) + ", Course ID: " + str(row.course_id) + ", Course Name: " + courseName + ", Review: " + str(row.review) + ", Review Date: " + str(row.review_date)
		
		return render_template("viewCourseReviewsList.html", courseReviews=courseReviews)
	else: 
		return render_template("viewCourseReviews.html")

@app.route("/view_student_schedule", methods=["POST", "GET"])
def viewStudentSchedule():
	
	return render_template("viewStudentSchedule.html")

if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)


  
