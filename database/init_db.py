import sqlite3



CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    salt BLOB NOT NULL,
    verifier BLOB NOT NULL
);