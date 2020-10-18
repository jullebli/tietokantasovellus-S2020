# Database application for recipes

## Introduction

The application is a database application where the user can create and read own recipes. 

## Use cases

At least the following use cases will be supported (not yet supported or optional use cases are in parenthesis):

- user logs in
- user logs out
- user creates an ingredient
- user deletes an ingredient
- user creates a recipe
- user adds an ingredient to a recipe
- user removes an ingredient from recipe
- user removes a recipe

## Database structure

Database contains tables:

- recipe
  - id, name, desciption
- recipe_ingredient
  - id, recipe_id, ingredient_id, amount
- ingredient
  - id, name
- user
  - id, username, password

## Heroku

https://radiant-depths-05859.herokuapp.com/

## Status

Functions listed in the Use cases section has been added. Given more time I would have separated the code more to different modules, the ablity to read public recipes and added CSS styling. Currently there are some open security issues: there is no CSR protection and access control is lacking when adding an ingredient to a recipe.
