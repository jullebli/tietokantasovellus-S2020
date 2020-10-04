# Database application for recipes

## Introduction

The application is a database application where the user can create and read recipes. 

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
- (user can search for recipes based on an ingredient/ingredients)
- (user can search for a recipe based on a string)
- (user can search for recipes based on tags)
- (user can determine if user's recipes are public or private)
- (user gets the locations of the ingredients that are listed in Foodie.fi)


## Database structure

At least four tables are needed:

- recipe
  - id, name, desciption
- recipe_ingredient
  - id, recipe_id, ingredient_id, amount
- ingredient
  - id, name, (price, EAN code?, location in an S-group's store (that you can get from Foodie.fi)?)
- user
  - id, username, password, (privilege level?)

Additional tables may be added if there is enough time. For example

- tag
  - id, name
- recipe_tag
  - id, recipe_id, tag_id

## Heroku

https://radiant-depths-05859.herokuapp.com/

## Status

Many of the functions have been added. Search functions, ability to remove an ingredient from a recipe and more functional navigation are missing.
