from db import db
from flask import session
import os
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def islogin():
    if session["username"] == None:
        return False
    return True

def signuppost(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username,"password":hash_value, "role":"user"})
        db.session.commit()
    except:
        return False
    return True

def logout():
    del session["username"]
    del session["csrf_token"]

def usermenuid():
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    return result.fetchone()[0]


def is_admin():
    sql = "SELECT role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    if result.fetchone()[0] == 'admin':
        return True
    return False
