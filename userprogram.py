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



