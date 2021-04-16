CREATE TABLE program (
    id SERIAL PRIMARY KEY,
    headline TEXT,
    content TEXT,
    data BYTEA
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT
);

CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    userprogramid INTEGER,
    percent NUMERIC,
    content TEXT
);

CREATE TABLE user_program (
    id SERIAL PRIMARY KEY,
    userid INTEGER references users,
    programid INTEGER references program,
    progressid INTEGER references progress
);


