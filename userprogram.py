from db import db
from flask import session
import users
import progress
import os

def createuserprogram(userid, programid):
    try:
        sql = "INSERT INTO user_program (userid, programid, visible) VALUES (:userid, :programid, :visible)"
        db.session.execute(sql, {"userid":userid, "programid":programid, "visible":1})
        db.session.commit()
    except:
        return False
    return True

def returnid(userid, programid):
    sql = "SELECT id FROM user_program WHERE userid=:userid AND programid=:programid AND visible=:visible"
    result = db.session.execute(sql, {"userid":userid, "programid":programid, "visible":1})
    return result.fetchone()[0]

def getprograms(userid):
    sql = "SELECT COUNT(*) FROM user_program WHERE userid=:userid AND visible=:visible"
    result = db.session.execute(sql, {"userid":userid, "visible":1})
    return result.fetchone()[0]

def getedituserprograms():
    sql = "SELECT user_program.id, program.headline, users.username FROM user_program JOIN program on user_program.programid = program.id JOIN users ON user_program.userid = users.id WHERE user_program.visible = 1"
    result = db.session.execute(sql)
    return result.fetchall()

def getheadlinesandid(userid):
    sql = "SELECT user_program.id, program.headline FROM user_program JOIN program ON program.id = user_program.programid WHERE user_program.userid=:userid AND user_program.visible=:visible"
    result = db.session.execute(sql, {"userid":userid, "visible":1})
    return result.fetchall()

def returnprogramid(id):
    sql = "SELECT programid FROM user_program WHERE id=:id AND visible=:visible"
    result = db.session.execute(sql, {"id":id, "visible":1})
    return result.fetchone()[0]

def returnallow(userid, id):
    sql = "SELECT id FROM user_program WHERE id=:id AND userid=:userid AND visible=:visible"
    result = db.session.execute(sql, {"id":id, "userid":userid, "visible":1})
    if result.fetchone() != None:
        return True
    else:
        return False

def returnpictureallow(userid, programid):
    sql = "SELECT id FROM user_program WHERE userid=:userid AND programid=:programid AND visible=:visible"
    result = db.session.execute(sql, {"userid":userid, "programid":programid, "visible":1})
    if result.fetchone() != None:
        return True
    else:
        return False

def setinvisible(id):
    try:
        sql = "UPDATE user_program SET visible = 0 WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False
