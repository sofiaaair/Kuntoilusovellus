CREATE TABLE program (
    id SERIAL PRIMARY KEY,
    headline TEXT,
    content TEXT,
    reps INTEGER,
    times INTEGER,
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
    content TEXT,
    reps INTEGER,
    times INTEGER
);

CREATE TABLE user_program (
    id SERIAL PRIMARY KEY,
    userid INTEGER references users,
    programid INTEGER references program,
    visible INTEGER
);


