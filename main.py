from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["post", "get"])
def home():
  if request.form.get("s_student_add"):
    return url_for("s_student_add")
  if request.form.get("s_professor_add"):
    return url_for("s_professor_add")
  if request.form.get("s_delete_entry"):
    return url_for("s_delete_entry")
  return render_template("index.html")

@app.route("/student_add")
def s_student_add():
  return render_template("student_add.html")

@app.route("/professor_add")
def s_professor_add():
  return render_template("professor_add.html")
	
@app.route("/delete_entry")
def s_delete_entry():
  return render_template("delete_entry.html")

if __name__ == "__main__":
  app.run(debug=True)