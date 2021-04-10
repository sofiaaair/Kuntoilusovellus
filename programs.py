from db import db

def getprograms(userid):
    sql = "SELECT COUNT(*) FROM programs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchone()[0]

def getheadlines(userid):
    sql = "SELECT id, headline FROM programs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchall()

def showprogram(id):
    sql = "SELECT content FROM programs WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def getallprograms():
    sql = "SELECT id, headline FROM programs"
    result = db.session.execute(sql)
    return result.fetchall()

def countall():
    sql = "SELECT COUNT(*) FROM programs"
    result = db.session.execute(sql)
    return result.fetchone()[0]

def createprogram(headline, content, userid):
    try:
        sql = "INSERT INTO programs (headline, content, userid) VALUES (:headline,:content,:userid)"
        db.session.execute(sql, {"headline:":headline,"content:":content, "userid":userid})
        db.session.commit()
    except:
        return False
    return True
