from db import db
from flask import session
import os



def createprogram(headline,content,data):
    try:
        sql = "INSERT INTO program (headline, content, data) VALUES (:headline,:content,:data)"
        db.session.execute(sql, {"headline":headline,"content":content,"data":data})
        db.session.commit()
    except:
        return False
    return True

def getprograms(userid):
    sql = "SELECT COUNT(*) FROM user_program WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchone()[0]

def getheadlines(userid):
    sql = "SELECT program.headline FROM program JOIN user_program ON program.id = user_program.programid JOIN users ON user_program.userid = users.id WHERE users.id=:userid"
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
