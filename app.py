from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db  = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ingredients")
def list_ingredients():
    result = db.session.execute("SELECT id, name FROM ingredient")
    ingredients = result.fetchall()
    return render_template("ingredients.html", ingredients=ingredients)
    
@app.route("/new_ingredient")
def new_ingredient():
    return render_template("new_ingredient.html")

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    name = request.form["name"]
    sql = "INSERT INTO ingredient (name) VALUES (:name)"
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return redirect("/ingredients")
