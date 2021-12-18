from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser
from datetime import datetime
from Tables import Courses, Students, Reviews, StudentSchedule, Professors, CourseTimeSlots, app, db
from sqlalchemy.sql import text

@app.route("/", methods=["POST", "GET"])
def home():
  print('hello')
  if request.form.get("addStudent"):
    return url_for("addStudent")
  if request.form.get("addProfessor"):
    return url_for("addProfessor")
  if request.form.get("addCourse"):
    return url_for("addCourse")
  if request.form.get("editStudent"):
    return url_for("editStudent")
  if request.form.get("addCourseReview"):
    return url_for("addCourseReview")    
  if request.form.get("editProfessor"):
    return url_for("editProfessor")
  if request.form.get("editCourse"):
    return url_for("editCourse")
  if request.form.get("viewProfessor"):
    return url_for("viewProfessor")
  if request.form.get("viewCourses"):
    return url_for("viewCourses")
  if request.form.get("viewCourseReviews"):
    return url_for("viewCourseReviews")
  if request.form.get("viewStudentSchedule"):
    return url_for("viewStudentSchedule")
  if request.form.get("viewProfessorTable"):
    return url_for("viewProfessorTable")
  if request.form.get("editStudentSchedule"):
    return url_for("editStudentSchedule")
  if request.form.get("deleteEntry"):
    return url_for("deleteEntry")
  return render_template("index.html")

@app.route('/edit_student', methods=["GET", "POST"])
def editStudent():
  if request.method == "POST":
      data = request.form
      if data['id'] is not None and data['id'] != '':
          student = Students.query.filter_by(student_id = int(data['id'])).first()
          if student is not None:
            if data['name'] is not None and len(data['name']) > 0:
              student.name = data['name']
            if data['major'] is not None and len(data['major']) > 0:
              student.major = data['major']
            db.session.commit()
          else:
            return render_template("editStudent.html")
      return redirect(url_for('home'))
  else:
      return render_template("editStudent.html")

@app.route("/add_student", methods=["POST", "GET"])
def addStudent():
    if request.method == "POST":
      data = request.form
      # for name in data.keys():
      #     print(name)
      # print(data['enrolldate'])
      if Students.query.filter_by(student_id=int(data['id'])).first() is not None:
        return render_template("addStudent.html")
      student = Students(int(data['id']), data['name'], data['birthdate'], data['major'], data['enrolldate'])
      db.session.connection(execution_options={'isolation_level': 'READ UNCOMMITTED'})
      db.session.add(student)
      db.session.commit()
      return redirect(url_for('home'))
    else:
      return render_template("addStudent.html")

@app.route("/view_student", methods=["POST", "GET"])
def viewStudent():
    if request.method == "POST":
      data = request.form
      if request.form.get('student_check') and data['id'] is not None and data['id'] != '':
        id = int(request.form['id'])
        return redirect(url_for('viewStudentTable', id=id))
      elif request.form.get('major_check'):
        db.session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
        query_res = db.session.execute('select major, count(*) as num_students from Students group by major;')
        return render_template("viewMajorsTable.html", query_res=query_res)
      else:
        return render_template("viewStudent.html")
    else:
      return render_template("viewStudent.html")

@app.route("/view_student/<id>")
def viewStudentTable(id):
  db.session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
  if Students.query.filter_by(student_id=id).first() is not None:
    query_res = db.session.execute("select * from Students where student_id=:temp_id", {'temp_id':id}).fetchall()
    print(query_res[0][0])
    print(query_res[0][1])
    student = {}
    (student['student_id'], student['name'], student['birthdate'], student['major'], student['enrollment_date']) = query_res[0][0], query_res[0][1], query_res[0][2], query_res[0][3], query_res[0][4]
    return render_template("viewStudentTable.html", student=student)
  else:
    return redirect(url_for('viewStudent'))

@app.route("/add_professor", methods=["POST", "GET"])
def addProfessor():
    if request.method == "POST":
        data = request.form
        professor = Professors(int(data['id']), data['name'], data['dept'], data['joined'])
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("addProfessor.html")

@app.route("/edit_professor", methods=["POST", "GET"])
def editProfessor():
  if request.method == "POST":
      data = request.form
      if data['id'] is not None and data['id'] != '':
          professor = Professors.query.filter_by(prof_id = data['id']).first()
          if professor is not None:
            if data['dept'] is not None and len(data['dept']) > 0:
              professor.department = data['dept']
            if data['name'] is not None and len(data['name']) > 0:
              professor.name = data['name']
            if data['joined'] is not None and len(data['joined']) > 0:
              professor.join_date = data['joined']
            db.session.commit()
      return redirect(url_for('home'))
  else:
      return render_template("editProfessor.html")
  
@app.route("/view_professor", methods=["POST", "GET"])
def viewProfessor():
    if request.method == "POST":
        data = request.form
        date = data['date']
        date2 = data['date2']
        if(date is not None):
            if (data['dateOption'] == "before"):
                queryResult = Professors.query.filter(Professors.join_date < date).all()
            elif (data['dateOption'] == "after"):
                queryResult = Professors.query.filter(Professors.join_date > date).all()
            elif (data['dateOption'] == "between"):
                if(date2 is not None):
                    queryResult = Professors.query.filter(Professors.join_date > date).filter(Professors.join_date < date2).all()

        professors = ""
        for row in queryResult:
            professors += "Professor ID: " + \
                str(row.prof_id) + ", Name: " + \
                row.name + ", Department: " + row.department + ", Join Date: " + row.join_date + "\t"
        return render_template("viewProfessorTable.html", professors = professors)
    else:
        return render_template("viewProfessor.html")


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
        db.session.connection(execution_options={'isolation_level': 'READ UNCOMMITTED'})
        db.session.commit()

    return redirect(url_for('home'))
  else:
    print('yo')
    return render_template("editCourse.html")


@app.route("/add_course", methods=["POST", "GET"])
def addCourse():
    if request.method == "POST":
        data = request.form

        checkCourse = Courses.query.filter_by(course_id=int(data['id'])).first()
        checkProfessor = Professors.query.filter_by(
            prof_id=int(data['profID'])).first()
        if checkCourse is None and checkProfessor is not None:
            if data['coursename'] is not None and len(data['coursename']) > 0:
                if data['department'] is not None and len(data['department']) > 0:
                    if data['dayOfWeek'] is not None and len(data['dayOfWeek']) > 0:
                        course = Courses(
                            int(data['id']), data['department'], data['coursename'])
                        courseTimeSlot = CourseTimeSlots(
                            int(data['id']), data['dayOfWeek'], int(data['profID']))

                        db.session.connection(execution_options={'isolation_level': 'READ UNCOMMITTED'})
                        db.session.add(courseTimeSlot)
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
            queryResult = db.session.execute(rawQuery)
 
        else:
            rawQuery = """SELECT * FROM Courses"""
            if courseName is not None and len(courseName) > 0:
                rawQuery = """SELECT * FROM Courses WHERE courseName=:courseName"""
            if department is not None and len(department) > 0:
                rawQuery = """SELECT * FROM Courses WHERE department=:department"""
                if courseName is not None and len(courseName) > 0:
                    rawQuery = """SELECT * FROM Courses WHERE department=:department AND courseName=:courseName"""
            if data.get('alphabet'):
                rawQuery = rawQuery + """ ORDER BY courseName"""

            if courseName is not None and department is not None and len(courseName) > 0 and len(department) > 0:
                queryResult = db.session.execute(rawQuery, {'department':department, 'courseName':courseName}).fetchall()
                
            else:
                if courseName is not None and len(courseName) > 0:
                    queryResult = db.session.execute(rawQuery, {'courseName':courseName}).fetchall()
                elif department is not None and len(department) > 0:
                    queryResult = db.session.execute(rawQuery, {'department':department}).fetchall()
                else:
                    queryResult = db.session.execute(rawQuery)

        courses = ""
        for row in queryResult:
            if groupBy:
                courses += "Department: " + row.department + \
                    ", Sum of IDs: " + str(row.sumIDs) + "\t"
            else:
                courses += "Course ID: " + \
                    str(row.course_id) + ", Course Name: " + \
                    row.courseName + ", Department: " + row.department + "\t"

        return render_template("viewCoursesList.html", courses=courses)

    else:
        return render_template("viewCourses.html")

@app.route("/add_course_review", methods=["POST", "GET"])
def addCourseReview():
    if request.method == "POST":
        data = request.form
        if data['course_id'] is not None and data['review_id'] is not None:
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y")
            review = Reviews(review_id = data['review_id'], course_id = data['course_id'], semester = data['semester'], review = data['review'], review_date = date_time)
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        return render_template("addCourseReview.html")

@app.route("/view_course_reviews", methods=["POST", "GET"])
def viewCourseReviews():
    if request.method == "POST":
        # Get courseName that user put into the form
        data = request.form
        courseName = data['coursename']

        # Get the course_id associated with that courseName
        result = Courses.query.filter_by(courseName=courseName).first()
        courseID = 0
        try:
            courseID = result.course_id
        except AttributeError:
            returnString = "No course was found with that name."
            return render_template("viewCourseReviewsList.html", courseReviews=returnString)

        # Get course reviews associated with that course_id
        rawQuery = """SELECT * FROM Reviews AS R WHERE R.course_id=\"""" + \
            str(courseID) + """\""""
        result2 = db.session.execute(rawQuery)

        # Collate course reviews into a string
        courseReviews = ""
        for row in result2:
            courseReviews += "Review ID: " + str(row.review_id) + ", Semester: " + str(row.semester) + ", Course ID: " + str(
                row.course_id) + ", Course Name: " + courseName + ", Review: " + str(row.review) + ", Review Date: " + str(row.review_date) + "\t"

        if (courseReviews == ""):
            courseReviews = "No reviews have been written yet for course \'" + courseName + "\'"

        return render_template("viewCourseReviewsList.html", courseReviews=courseReviews)
    else:
        return render_template("viewCourseReviews.html")


@app.route("/view_student_schedule", methods=["POST", "GET"])
def viewStudentSchedule():
    if request.method == "POST":
        # Get student_id that user put into the form
        data = request.form
        studentID = data['id']

        # Get course_ids associated with the schedule of the student with that student_id
        result = StudentSchedule.query.filter_by(student_id=studentID)
        num_results = len(result.all())
        print("num_results =", num_results)
        if (num_results == 0):
            returnString = "No schedule exists for student with id " + \
                str(studentID)
            print(returnString)
            return render_template("viewStudentScheduleList.html", studentSchedule=returnString)

        # Get courses associated with each course_id, collate into a string
        studentSchedule = ""
        for row in result:
            result2 = Courses.query.filter_by(course_id=row.course_id).first()
            try:
                studentSchedule += "Course ID: " + str(result2.course_id) + ", Department: " + str(
                    result2.department) + ", Course Name: " + str(result2.courseName) + "\t"
            except:
                pass

        if (studentSchedule == ""):
            studentSchedule = "No valid courses have been added to this student's schedule"

        return render_template("viewStudentScheduleList.html", studentSchedule=studentSchedule)
    else:
        return render_template("viewStudentSchedule.html")


@app.route("/create_student_schedule", methods=["POST", "GET"])
def createStudentSchedule():
    if request.method == "POST":
        data = request.form
        studentID = data['studentID'].split()

        # IDs must be separated by ' ' in frontend
        courseIDs = data['courseIDs'].split()

        if Students.query.filter_by(student_id=int(studentID)).first() is not None:
          for id in courseIDs:
            if Courses.query.filter_by(course_id=int(id)).first() is not None:
                scheduleClass = StudentSchedule(int(studentID), int(id))

                db.session.connection(execution_options={'isolation_level': 'READ UNCOMMITTED'})
                db.session.add(scheduleClass)
                db.session.commit()
        return redirect(url_for('home'))
    else:
        print('yo')
        return render_template("addCourse.html")


@app.route("/edit_student_schedule", methods=["POST", "GET"])
def editStudentSchedule():
    if request.method == "POST":
        # Get form information that the user inputted
        data = request.form
        studentID = data['studentid']
        courseID = data['courseid']
        adding = data['options'] == "Add"
        deleting = data['options'] == "Delete"
        result = ""

        # If adding a course to a student's schedule
        if (adding == True):
            checkCourse = Courses.query.filter_by(course_id=courseID).first()
            if checkCourse is not None:
                checkAlreadyEnrolled = StudentSchedule.query.filter_by(
                    student_id=studentID, course_id=courseID).first()
                if checkAlreadyEnrolled is not None:
                    result = "Student is already enrolled in course with id " + \
                        str(courseID) + ", did not add course"
                    return render_template("editStudentScheduleLanding.html", studentScheduleLanding=result)
                studentCourse = StudentSchedule(
                    student_id=int(studentID), course_id=int(courseID))
                db.session.add(studentCourse)
                db.session.commit()
                result = "Successfully added course with id " + \
                    str(courseID) + \
                    " to the schedule of student with id " + str(studentID)
                return render_template("editStudentScheduleLanding.html", studentScheduleLanding=result)
            else:
                result = "No course exists with id " + \
                    str(courseID) + ", could not add to student schedule"
                return render_template("editStudentScheduleLanding.html", studentScheduleLanding=result)
        # If deleting a course from a student's schedule
        else:
            try:
                checkStudentCourse = StudentSchedule.query.filter_by(
                    student_id=studentID, course_id=courseID).first()
                if checkStudentCourse is not None:
                    StudentSchedule.query.filter_by(
                        student_id=studentID, course_id=courseID).delete()
                    db.session.commit()
                    result = "Successfully deleted course with id " + \
                        str(courseID) + " from student's schedule"
                    return render_template("editStudentScheduleLanding.html", studentScheduleLanding=result)
                else:
                    result = "Course with id " + \
                        str(courseID) + \
                        " did not exist in this student's schedule, nothing to delete"
                    return render_template("editStudentScheduleLanding.html", studentScheduleLanding=result)
            except:
                result = "Ran into error trying to delete course with id " + \
                    str(courseID) + " from this student's schedule. Contact server owner for more information."
                return render_template("editStudentScheduleLanding.html", studentScheduleLanding=result)
                pass

    if request.method == "GET":
        return render_template("editStudentSchedule.html")

@app.route("/delete_entry", methods=["POST", "GET"])
def deleteEntry():
    if request.method == "POST":
        data = request.form
        id = data['id']
        if(data['deleteOption'] == "student"):
            record = Students.query.filter_by(student_id = id).first()
            db.session.delete(record)
            db.session.commit()
        elif(data['deleteOption'] == "professor"):
            record = Professors.query.filter_by(prof_id = id).first()
            db.session.delete(record)
            db.session.commit()
        elif(data['deleteOption'] == "course"):
            record = Courses.query.filter_by(course_id = id).first()
            db.session.delete(record)
            db.session.commit()
        elif(data['deleteOption'] == "review"):
            record = Reviews.query.filter_by(review_id = id).first()
            db.session.delete(record)
            db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("deleteEntry.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)