from app import app
import users
import programs
import userprogram
import progress

from flask import render_template, redirect, request, session, make_response


@app.route("/")
def index():
    if not users.islogin():
        return render_template("index.html")
    else:
        if users.is_admin():
            return redirect("/adminmenu")
        return redirect("/usermenu")

@app.route("/adminmenu")
def adminmenu():
    if not users.islogin():
        return redirect("/")
    allow = False
    if users.is_admin():
        allow = True
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
    count = programs.countall()
    program = programs.getallprograms()
    return render_template("adminmenu.html", count=count, programs=program)

@app.route("/usermenu", methods=["GET", "POST"])
def usermenu():
    allow = False
    if users.islogin():
        allow = True
    if not allow:
        return redirect("/")
    if request.method == "GET":
        userid = users.usermenuid()
        count = userprogram.getprograms(userid)
        program = userprogram.getheadlinesandid(userid)
        return render_template("usermenu.html", count=count, programs=program)
    if request.method == "POST":
        userid = users.usermenuid()
        programid = request.form["program"]
        userprogramid = userprogram.returnid(userid, programid)
        return redirect("/")


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
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Käyttäjätunnuksen on oltava 3-20 pitkä")
        if len(password) < 6 or len(password) > 20:
            return render_template("error.html", message="Salasanan on oltava 6-20 merkkiä pitkä")
        if users.signuppost(username, password):
            userid = users.returnid(username)
            programid = programs.getfirstprogramid()
            if userprogram.createuserprogram(userid, programid):
                id = userprogram.returnid(userid, programid)
                if  progress.createprogress(id):
                    return redirect("/")
                else:
                    return render_template("error.html", message="Virhe luotaessa edistystoiminnallisuutta kunto-ohjelmallesi")
            else:
               return render_template("error.html", message="Ensimmäisen kunto-ohjelmasi luominen epäonnistui")
            return redirect("/")
        else:
            return render_template("error.html", message="Tunnuksen luominen epäonnistui")

@app.route("/program/<int:id>")
def program(id):
    if not users.islogin():
        return redirect("/") 
    allow = False
    if users.is_admin():
        allow = True
    if not allow:
        return redirect("/") 
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
    if not users.islogin():
        return redirect("/")
    allow = False
    if users.is_admin():
        allow = True
    userid = users.usermenuid()
    if userprogram.returnpictureallow(userid, id):
        allow = True
    if not allow:
        return redirect("/")
    try:
        data = programs.showpicture(id)
        response = make_response(bytes(data))
        response.headers.set("Content-Type","image/jpeg")
        return response
    except:
        return redirect("/")

@app.route("/usersprogram/<int:id>",methods=["GET", "POST"])
def usersprogram(id):
    if request.method == "GET":
        if not users.islogin():
            return redirect("/") 
        allow = False
        if users.is_admin():
            allow = True
        userid = users.usermenuid()
        if userprogram.returnallow(userid, id):
            allow = True
        if not allow:
            return redirect("/usermenu")
        try:
            userprogramid = id
            programid = userprogram.returnprogramid(id)
            content = programs.showprogram(programid)
            headline = programs.showheadline(programid)
            reps = progress.returnreps(id)
            percent = progress.returnpercent(id)
            times = progress.returntimes(id)
            message = " "
            if percent == 100:
                message = "Olet suorittanut ohjelman loppuun!"
            return render_template("usersprogram.html", userprogramid=userprogramid, content=content, headline=headline, reps=reps, times=times, percent=percent, picid=programid, message=message)
        except:
            return render_template("error.html", message="Tapahtui virhe ohjelmaa haettaessa")
    if request.method == "POST":
       if session["csrf_token"] != request.form["csrf_token"]:
           abort(403)
       programid = userprogram.returnprogramid(id)
       oldreps = progress.returnreps(id)
       oldtimes = progress.returntimes(id)
       totalreps = int(request.form["newreps"]) * int(request.form["newsets"])
       desiredreps = programs.getreps(programid)
       desiredtimes = programs.getreps(programid)
       newreps = oldreps + totalreps
       newtimes = oldtimes + 1
       percent = newreps/desiredreps*100
       if percent >100:
          newreps = 0
          newtimes=0
          percent = 0
       if progress.updateprogress(id, percent, newreps, newtimes):
           userprogramid = id
           programid = userprogram.returnprogramid(id)
           content = programs.showprogram(programid)
           headline = programs.showheadline(programid)
           reps = progress.returnreps(id)
           percent = progress.returnpercent(id)
           times = progress.returntimes(id)
           message = " "
           if percent == 100:
              message = "Olet suorittanut ohjelman loppuun!"
           return render_template("usersprogram.html", userprogramid=userprogramid, content=content, headline=headline, reps=reps, times=times, percent=percent, picid=programid, message=message)
       else:
           return render_template("error.html", message="Virhe edistyksen päivityksessä")

@app.route("/createprogram",methods=["GET","POST"])
def createprogram():
    if request.method == "GET":
        if not users.islogin():
            return redirect("/") 
        allow = False
        if users.is_admin():
            allow = True
        if not allow:
            return redirect("/")
        userstosend = users.returnusernames()
        return render_template("createprograml.html", users=userstosend)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        try:
           int(request.form["sets"])
           int(request.form["times"])
           int(request.form["reps"])
        except ValueError:
            return render_template("error.html", message="Virheellinen syöttö kentässä toisto, sarja, tai treenkerrat, anna kyseiset kentät lukuina")
        file = request.files["file"]
        headline = request.form["headline"]
        content = request.form["content"]
        reps = int(request.form["reps"])*int(request.form["sets"])
        times = request.form["times"]
        user = request.form["user"]
        name = file.filename
        if not name.endswith(".jpg"):
            return render_template("error.html", message="Kuvan tulee olla .jpg -muotoa")
        data = file.read()
        if len(data) > 100*1024:
            return render_template("error.html", message="Kuva on liian iso")
        if programs.createprogram(headline,content,data,reps,times):
            userid = users.returnid(user)
            programid = programs.getid(headline, content)
        else:
            return render_template("error.html", message="Ohjelman luominen epäonnistui")
        if userprogram.createuserprogram(userid, programid):
            userprogramid = userprogram.returnid(userid, programid)
        else:
            return render_template("error.html", message="Virheellinen käyttäjätunnus tai ohjelma")
        if progress.createprogress(userprogramid):
            return redirect("/login")
        else:
            return render_template("error.html", message="Virhe käyttäjän edistystoimintoa luomisessa")

@app.route("/editprogram", methods=["GET", "POST"])
def editprogram():
    if request.method == "GET":
        if not users.islogin():
            return redirect("/")
        allow = False
        if users.is_admin():
            allow = True
        if not allow:
            return redirect("/")
        program = userprogram.getedituserprograms()
        programlist = programs.getallprograms()
        usernamelist = users.returnusernames()
        return render_template("editprogram.html", programs=program, programlist=programlist, usernamelist=usernamelist )
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        id = int(request.form["program"])
        if userprogram.setinvisible(id):
            return redirect("/editprogram")
        else:
            return render_template("error.html", message="Virhe ohjelmaa piilotettaessa")


@app.route("/edituser", methods=["GET", "POST"])
def edituser():
    if request.method == "GET":
        if not users.islogin():
            return redirect("/")
        allow = False
        if users.is_admin():
            allow = True
        if not allow:
            return redirect("/")
        program = userprogram.getedituserprograms()
        programlist = programs.getallprograms()
        usernamelist = users.returnusernames()
        return render_template("editprogram.html", programs=program, programlist=programlist, usernamelist=usernamelist)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        username = request.form["user"]
        programid = request.form["program"]
        userid = users.returnid(username)
        if userprogram.createuserprogram(userid, programid):
            id = userprogram.returnid(userid, programid)
            if progress.createprogress(id):
                return redirect("/edituser")
            else:
                return render_template("error.html", message="Virhe lisätessä edistyksenseurantaa ohjelmalle")
        else:
            return render_template("error.html", message="Virhe lisätessä ohjelmaa käyttäjälle")
