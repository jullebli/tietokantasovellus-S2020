from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key =getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db  = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")
    
@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    
    #TODO check if user already exists, error.html
    
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password_hash) VALUES (:username,:password_hash)"
    db.session.execute(sql, {"username":username,"password_hash":hash_value})
    db.session.commit()
    return redirect("/");
    
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if user == None:
        
        return render_template("error.html", message="Login failed, user does not exist")
    
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong password")
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/ingredients")
def list_ingredients():
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    result = db.session.execute("SELECT id, name FROM ingredient WHERE owner_id = (SELECT id FROM users WHERE username=:username)",
                                {"username":session["username"]})
    ingredients = result.fetchall()
    return render_template("ingredients.html", ingredients=ingredients)
    
@app.route("/new_ingredient")
def new_ingredient():
    return render_template("new_ingredient.html")

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    name = request.form["name"]
    sql = "INSERT INTO ingredient (name, owner_id) VALUES (:name, (SELECT id FROM users WHERE username=:username))"
    db.session.execute(sql, {"name":name, "username":session["username"]})
    db.session.commit()
    return redirect("/ingredients")
