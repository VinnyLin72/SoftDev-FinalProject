from flask import Flask, request, render_template, session, redirect, url_for, flash
from os import urandom
import db

app = Flask(__name__)
app.secret_key = urandom(32)

users = {"jaredasch":"pass"}

@app.route("/")
def index():
    try:
        db.create_table()
    except:
        pass
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.auth(username, password):
            return("welcome")
        else:
            flash('Please enter valid username and password')
            return redirect("/")
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/create_acc", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        username = request.form.get("username")
        # if username already exists
        if db.check_user(username):
            flash("This username has already been taken.")
            return redirect("/signup")
        password = request.form.get("password")
        pass2 = request.form.get("confirm-password")
        # if passwords do not match
        if password != pass2:
            flash("Passwords do not match.")
            return redirect("/signup")
        db.add_user(username, password)
        flash("Your account has succesfully been created.")
        return redirect("/")
    else: return "failed"



if __name__ == "__main__":
    app.debug = True;
    app.run()
