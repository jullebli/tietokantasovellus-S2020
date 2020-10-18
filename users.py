from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy
from db import db
from flask import session
from exceptions import RecipeError


def create_user(username, password):
    if len(password) < 8:
        raise RecipeError("Password is too short")
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password_hash) VALUES (:username,:password_hash)"
    try:
        db.session.execute(sql, {"username":username,"password_hash":hash_value})
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise RecipeError("User already exists")

def login(username, password):
    sql = "SELECT password_hash FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user == None:
        raise RecipeError("Login failed, user does not exist")   
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            return
        else:
            raise RecipeError("Wrong password")
    