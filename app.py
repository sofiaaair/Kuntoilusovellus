from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/usermenu")
def usermenu():
    sql2 = "SELECT id FROM users WHERE username=:username"
    result2 = db.session.execute(sql2, {"username":session["username"]})
    userid = result2.fetchone()[0]
    sql = "SELECT COUNT(*) FROM programs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    count = result.fetchone()[0]
    sql = "SELECT id, headline FROM programs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    programs = result.fetchall()
    return render_template("usermenu.html", count=count, programs=programs)


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            return redirect("/usermenu")
        else:
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/signup",methods=["POST"])
def signupost():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/program/<int:id>")
def program(id):
    sql = "SELECT content FROM programs WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    content = result.fetchone()[0]
    return render_template("program.html", id=id, content=content)
