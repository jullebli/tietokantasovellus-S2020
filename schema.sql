CREATE TABLE recipe (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    description TEXT,
    owner_id INTEGER REFERENCES users (id)
);

CREATE TABLE ingredient (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    owner_id INTEGER REFERENCES users (id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

