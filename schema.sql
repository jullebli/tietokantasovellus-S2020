CREATE TABLE recipe (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    description TEXT
);

CREATE TABLE ingredient (
    id SERIAL PRIMARY KEY, 
    name TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

