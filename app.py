from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from exceptions import RecipeError


app = Flask(__name__)
app.secret_key =getenv("SECRET_KEY")

from db import db
import users

def handle_recipe_error(e):
    return render_template("error.html", message=e)

app.register_error_handler(RecipeError, handle_recipe_error)

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
    users.create_user(username, password)
    return redirect("/")
    
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.login(username, password)
    return redirect("/")
   
@app.route("/logout")
def logout():
    users.logout()
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

@app.route("/delete_ingredient/<int:id>", methods=["POST"])
def delete_ingredient(id):
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    sql = "DELETE FROM ingredient WHERE id=:id AND owner_id=(SELECT id FROM users WHERE username=:username) RETURNING id"
    result = db.session.execute(sql, {"id":id, "username":session["username"]})
    deleted = result.fetchall()
    print(deleted)
    if len(deleted) != 1:
        return render_template("error.html", message="Ingredient does not exist or you don't have access to delete this ingredient")
    db.session.commit()
    return redirect("/ingredients")
    
@app.route("/new_recipe")
def new_recipe():
    return render_template("new_recipe.html")
    
@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    name = request.form["name"]
    description = request.form["description"]
    if len(name) > 100:
        return render_template("error.html", message="name of the recipe is too long")
    if len(description) > 5000:
        return render_template("error.html", message="description is too long")
    sql = "INSERT INTO recipe (name, description, owner_id) VALUES (:name, :description, (SELECT id FROM users WHERE username=:username))"
    db.session.execute(sql, {"name":name, "description":description, "username":session["username"]})
    db.session.commit()
    return redirect("/recipes")
   
@app.route("/recipes")
def list_recipes():
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    result = db.session.execute("SELECT id, name FROM recipe WHERE owner_id = (SELECT id FROM users WHERE username=:username)",
                                {"username":session["username"]})
    recipes = result.fetchall()
    return render_template("recipes.html", recipes=recipes)
    
@app.route("/delete_recipe/<int:id>", methods=["POST"])
def delete_recipe(id):
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    sql = "DELETE FROM recipe WHERE id=:id AND owner_id=(SELECT id FROM users WHERE username=:username) RETURNING id"
    result = db.session.execute(sql, {"id":id, "username":session["username"]})
    deleted = result.fetchall()
    print(deleted)
    if len(deleted) != 1:
        return render_template("error.html", message="Recipe does not exist or you don't have access to delete this recipe")
    db.session.commit()
    return redirect("/recipes")
    
@app.route("/recipe/<int:id>")
def show_recipe(id):
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    sql = "SELECT name, description, id FROM recipe WHERE id=:id AND owner_id=(SELECT id FROM users WHERE username=:username)"
    result = db.session.execute(sql, {"id":id, "username":session["username"]})
    recipe = result.fetchone()
    
    sql = "SELECT name, id FROM ingredient WHERE owner_id=(SELECT id FROM users WHERE username=:username)"
    result = db.session.execute(sql, {"username":session["username"]})
    all_ingredients = result.fetchall()
    
    sql = "SELECT id, amount, (SELECT name FROM ingredient WHERE id=ingredient_id) FROM recipe_ingredient WHERE recipe_id = :recipe_id"
    result = db.session.execute(sql, {"recipe_id":id})
    ingredients = result.fetchall()
    
    return render_template("recipe.html", name=recipe[0], description=recipe[1], id=recipe[2], all_ingredients=all_ingredients, ingredients=ingredients)

@app.route("/add_ingredient_to_recipe/<int:recipe_id>", methods=["POST"])
def add_ingredient_to_recipe(recipe_id):
    if not "username" in session:
        return render_template("error.html", message="You are not logged in")
    try:
        ingredient_id = int(request.form["ingredient"])
    except ValueError:
        raise RecipeError("Invalid ingredient id")

    try:    
        amount = int(request.form["amount"])
    except ValueError:
        raise RecipeError("Amount is not a numeric value")

    if amount <= 0:
        raise RecipeError("Amount needs to be positive number")

    #check that user owns the recipe and the ingredient
    
    print(repr(ingredient_id))
    print(repr(recipe_id))
    sql = "INSERT INTO recipe_ingredient (ingredient_id, recipe_id, amount) VALUES (:ingredient_id, :recipe_id, :amount)"
    db.session.execute(sql, {"ingredient_id":ingredient_id, "recipe_id":recipe_id, "amount":amount})
    db.session.commit()
    return redirect("/recipe/" + str(recipe_id))
