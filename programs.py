from db import db
from flask import session
import os



def createprogram(headline,content,data,reps,times):
    try:
        sql = "INSERT INTO program (headline, content, reps, times, data) VALUES (:headline,:content,:reps,:times,:data)"
        db.session.execute(sql, {"headline":headline,"content":content,"reps":reps,"times":times,"data":data})
        db.session.commit()
    except:
        return False
    return True

def getheadlines(userid):
    sql = "SELECT program.headline, program.id FROM program JOIN user_program ON program.id = user_program.programid WHERE user_program.userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchall()

def showprogram(id):
    sql = "SELECT content FROM program WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def showheadline(id):
    sql = "SELECT headline FROM program WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def showpicture(id):
    sql = "SELECT data FROM program WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def getallprograms():
    sql = "SELECT id, headline FROM program"
    result = db.session.execute(sql)
    return result.fetchall()

def countall():
    sql = "SELECT COUNT(*) FROM program"
    result = db.session.execute(sql)
    return result.fetchone()[0]

def ifexist(id):
    sql = "SELECT content FROM program  WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    content = result.fetchone()
    if content == None:
        return False
    else:
        return True

def getid(headline, content):
    sql = "SELECT id FROM program WHERE headline=:headline AND content=:content"
    result = db.session.execute(sql, {"headline":headline, "content":content})
    return result.fetchone()[0]

def getreps(id):
    sql = "SELECT reps FROM program WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def gettimes(id):
    sql = "SELECT times FROM program WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def getfirstprogramid():
    sql = "SELECT MIN(id) FROM program GROUP BY id"
    result = db.session.execute(sql)
    return result.fetchone()[0]

