from db import db
from flask import session
import users
import progress
import os

def createuserprogram(userid, programid):
    try:
        sql = "INSERT INTO user_program (userid, programid) VALUES (:userid, :programid)"
        db.session.execute(sql, {"userid":userid, "programid":programid})
        db.session.commit()
    except:
        return False
    return True

def returnid(userid, programid):
    sql = "SELECT id FROM user_program WHERE userid=:userid AND programid=:programid"
    result = db.session.execute(sql, {"userid":userid, "programid":programid})
    return result.fetchone()[0]

def getprograms(userid):
    sql = "SELECT COUNT(*) FROM user_program WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchone()[0]

def getheadlinesandid(userid):
    sql = "SELECT user_program.id, program.headline FROM user_program JOIN program ON program.id = user_program.programid WHERE user_program.userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchall()

def returnprogramid(id):
    sql = "SELECT programid FROM user_program WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def returnallow(userid, id):
    sql = "SELECT id FROM user_program WHERE id=:id AND userid=:userid"
    result = db.session.execute(sql, {"id":id, "userid":userid})
    if result.fetchone() != None:
        return True
    else:
        return False
