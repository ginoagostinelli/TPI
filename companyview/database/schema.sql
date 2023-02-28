DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL ,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);


DROP TABLE IF EXISTS favorite;

CREATE TABLE favorite (
    id_user INTEGER NOT NULL ,
    id_company TEXT not null 
);
