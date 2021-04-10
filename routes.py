from app import app
import users
import programs
from flask import render_template, redirect, request, session


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/adminmenu")
def adminmenu():
    allow = False
    if users.is_admin():
        allow = True
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
    count = programs.countall()
    program = programs.getallprograms()
    return render_template("adminmenu.html", count=count, programs=program)

@app.route("/usermenu")
def usermenu():
    userid = users.usermenuid()
    count = programs.getprograms(userid)
    program = programs.getheadlines(userid)
    return render_template("usermenu.html", count=count, programs=program)


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if users.islogin():
            if users.is_admin(): 
                return redirect("/adminmenu")
            else:
                return redirect("/usermenu")
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            if users.is_admin():
                return redirect("/adminmenu")
            else:
                return redirect("/usermenu")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup",methods=["GET","POST"])
def signupost():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.signuppost(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Tunnuksen luominen epäonnistui")

@app.route("/program/<int:id>")
def program(id):
    content = programs.showprogram(id)
    return render_template("program.html", id=id, content=content)



@app.route("/createprogram", methods=["GET", "POST"])
def createprogram():
    if request.method == "GET":
        allow = False
        if users.is_admin():
            allow = True
        if not allow:
            return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
        return render_template("createprograml.html")
    if request.method == "POST":
        allow = False
        if users.is_admin():
            allow = True
        if not allow:
            return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
        headline = request.form["headline"]
        content = request.form["content"]
        userid = request.form["userid"]
        if programs.createprogram(headline, content, userid):
            return redirect("/login")
        else:
            return render_template("error.html", message="Virhe lisäyksessä")

