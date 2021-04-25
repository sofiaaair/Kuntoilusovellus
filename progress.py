from db import db

def createprogress(userprogramid):
    try:
        sql = "INSERT INTO progress (userprogramid, percent, reps, times) VALUES (:userprogramid, :percent, :reps, :times)"
        db.session.execute(sql, {"userprogramid":userprogramid,"percent":0, "reps":0, "times":0})
        db.session.commit()
    except:
        return False
    return True

def returnid(userprogramid):
    sql = "SELECT id FROM progress WHERE userprogramid=:userprogramid"
    result = db.session.execute(sql, {"userprogramid":userprogramid})
    return result.fetchone()[0]
