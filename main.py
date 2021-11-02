from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Students(db.Model):
  student_id = db.Column(db.Integer, primary_key = True)
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
    

@app.route("/", methods=["POST", "GET"])
def home():
  print('hello')
  if request.form.get("addStudent"):
    return url_for("addStudent")
  if request.form.get("addProfessor"):
    return url_for("addProfessor")
  if request.form.get("deleteEntry"):
    return url_for("deleteEntry")
  return render_template("index.html")

@app.route("/add_student", methods=["POST", "GET"])
def addStudent():
  if request.method == "POST":
    data = request.form
    for name in data.keys():
      print(name)
    print(data['enrolldate'])
    student = Students(int(data['id']), data['name'], data['birthdate'], data['major'], data['enrolldate'])
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
  return render_template("viewStudentTable.html", student=Students.query.filter_by(student_id = id).first())


@app.route("/add_professor")
def addProfessor():
  return render_template("addProfessor.html")
	
@app.route("/delete_entry")
def deleteEntry():
  return render_template("deleteEntry.html")

if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)