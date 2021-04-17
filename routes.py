from app import app
import users
import programs
from flask import render_template, redirect, request, session, make_response


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
    allow = False
    if users.islogin():
        allow = True
    if not allow:
        return render_template("error.html", message="Virheelliset käyttäjätunnukset")
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
        else:
            return redirect("/")
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
        if len(username) < 3 or len(username) > 50:
            return render_template("error.html", message="Käyttäjätunnuksen on oltava 3-50 pitkä")
        if len(password) < 6 or len(password) > 20:
            return render_template("error.html", message="Salasanan on oltava 6-20 merkkiä pitkä")
        if users.signuppost(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Tunnuksen luominen epäonnistui")

@app.route("/program/<int:id>")
def program(id):
    exist = False
    if programs.ifexist(id):
        exist = True
    if not exist:
        return render_template("error.html", message="Treeniohjelmaa ei löydy")
    headline = programs.showheadline(id)
    content = programs.showprogram(id)
    return render_template("program.html", id=id, content=content, headline=headline)

@app.route("/programpic/<int:id>")
def programpic(id):
    data = programs.showpicture(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type","image/jpeg")
    return response

@app.route("/usersprogram/<int:id>")
def usersprogram(id):
    #TO DO
    return render_template("usersprogram.html", id=id, content=content, headline=headline, reps=reps, times=times, percent=percent)

@app.route("/createprogram",methods=["GET","POST"])
def createprogram():
    if request.method == "GET":
        allow = False
        if users.is_admin():
            allow = True
        if not allow:
            return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
        return render_template("createprograml.html")
    if request.method == "POST":
        file = request.files["file"]
        headline = request.form["headline"]
        content = request.form["content"]
        reps = request.form["reps"]
        sets = request.form["sets"]
        times = request.form["times"]
        name = file.filename
        if not name.endswith(".jpg"):
            return render_template("error.html", message="Kuvan tulee olla .jpg -muotoa")
        data = file.read()
        if len(data) > 100*1024:
            return render_template("error.html", message="Kuva on liian iso")
        if programs.createprogram(headline,content,data):
            return redirect("/login")
        else:
            return render_template("error.html", message="Virhe lisäyksessä")

