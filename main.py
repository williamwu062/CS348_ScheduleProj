from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser

app = Flask(__name__)
password = groupprojectpassword
dbname = project
project_id = 

db = SQLAlchemy(app)

class Students(db.model):
  student_id = db.Column(db.Integer, primary_key = True, nullable = False)
  name = db.Column(db.String(250), nullable = False)
  birthdate = db.Column(db.String(250), nullable = False, unique = False)
  major = db.Column(db.String(250), nullable = True)
  enrollment_date = db.Column(db.Integer, nullable = False)

@app.route("/", methods=["post", "get"])
def home():
  if request.form.get("addStudent"):
    return url_for("addStudent")
  if request.form.get("addProfessor"):
    return url_for("addProfessor")
  if request.form.get("deleteEntry"):
    return url_for("deleteEntry")
  return render_template("index.html")

@app.route("/add_student")
def addStudent():
  return render_template("addStudent.html")

@app.route("/add_professor")
def addProfessor():
  return render_template("addProfessor.html")
	
@app.route("/delete_entry")
def deleteEntry():
  return render_template("deleteEntry.html")

if __name__ == "__main__":
  app.run(debug=True)