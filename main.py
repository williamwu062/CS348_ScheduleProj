from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser
from datetime import datetime
from Tables import Courses, Students, Reviews, StudentSchedule, app, db

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
  if request.form.get("editStudentSchedule"):
    return url_for("editStudentSchedule")
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
    
    checkCourse = Courses.query.filter_by(course_id=data['id']).first()
    if checkCourse is None:
      if data['coursename'] is not None and len(data['coursename']) > 0:
        if data['department'] is not None and len(data['department']) > 0:
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
		result = Courses.query.filter_by(courseName=courseName).first()
		courseID = 0
		try:
			courseID = result.course_id
		except AttributeError:
			returnString = "No course was found with that name."
			return render_template("viewCourseReviewsList.html", courseReviews=returnString)
			
		#Get course reviews associated with that course_id
		rawQuery = """SELECT * FROM Reviews AS R WHERE R.course_id=\"""" + str(courseID) + """\""""
		result2 = db.session.execute(rawQuery)
		
		#Collate course reviews into a string
		courseReviews = ""
		for row in result2:
			courseReviews += "Review ID: " + str(row.review_id) + ", Semester: " + str(row.semester) + ", Course ID: " + str(row.course_id) + ", Course Name: " + courseName + ", Review: " + str(row.review) + ", Review Date: " + str(row.review_date) + "\t"
		
		if (courseReviews == ""):
			courseReviews = "No reviews have been written yet for course \'" + courseName + "\'"
			
		return render_template("viewCourseReviewsList.html", courseReviews=courseReviews)
	else: 
		return render_template("viewCourseReviews.html")

@app.route("/view_student_schedule", methods=["POST", "GET"])
def viewStudentSchedule():
	if request.method == "POST":
		#Get student_id that user put into the form
		data = request.form
		studentID = data['id']
		
		#Get course_ids associated with the schedule of the student with that student_id
		result = StudentSchedule.query.filter_by(student_id=studentID)
		num_results = len(result.all())
		print("num_results =", num_results)
		if (num_results == 0):
			returnString = "No schedule exists for student with id " + str(studentID)
			print(returnString)
			return render_template("viewStudentScheduleList.html", studentSchedule=returnString)
		
		#Get courses associated with each course_id, collate into a string
		studentSchedule = ""
		for row in result:
			result2 = Courses.query.filter_by(course_id=row.course_id).first()
			try:
				studentSchedule += "Course ID: " + str(result2.course_id) + ", Department: " + str(result2.department) + ", Course Name: " + str(result2.courseName) + "\t"
			except:
				pass
		
		if (studentSchedule == ""):
			studentSchedule = "No valid courses have been added to this student's schedule"
		
		return render_template("viewStudentScheduleList.html", studentSchedule=studentSchedule)
	else:	
		return render_template("viewStudentSchedule.html")
	
@app.route("/edit_student_schedule", methods=["POST", "GET"])
def editStudentSchedule():
	if request.method == "POST":
		#Get form information that the user inputted
		data = request.form
		studentID = data['studentid']
		courseID = data['courseid']
		adding = data['options'] == "Add"
		deleting = data['options'] == "Delete"
		
		#If adding a course to a student's schedule
		if (adding == True):
			
			studentCourse = StudentSchedule(student_id=int(studentID), course_id=int(courseID))
			db.session.add(studentCourse)
			db.session.commit()
			print("Successfully added tuple", studentCourse, " to StudentSchedule table")
		#If deleting a course from a student's schedule
		else:
			try:
				StudentSchedule.query.filter_by(student_id=studentID, course_id=courseID).delete()
				db.session.commit()
				print("Successfully deleted course with id", courseID, " from student's schedule")
			except:
				print("Ran into error trying to delete course with id", courseID, " from this student's schedule")
				pass
				
		return redirect(url_for('home'))
	if request.method == "GET":
		return render_template("editStudentSchedule.html")
		
if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)


  
