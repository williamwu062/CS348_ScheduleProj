from types import MethodDescriptorType
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["post", "get"])
def home():
  if request.form.get("s_signup"):
    return url_for("s_signup")
  if request.form.get("s_login"):
    return url_for("s_login")
  return render_template("index.html")

@app.route("/student_signup", methods=["post", "get"])
def s_signup():
  if request.method == "post":
    user_details = request.form
  else:
    return render_template("student_signup.html")

@app.route("/student_login")
def s_login():
  return render_template("student_login.html")

if __name__ == "__main__":
  app.run(debug=True)