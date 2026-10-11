import sqlite3
from contextlib import closing

db_path = "USERS.db"

def InitDB():
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute('''PRAGMA foreign_keys=ON''')
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS vault_meta (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            salt BLOB NOT NULL,
            verifier_nonce BLOB NOT NULL,
            verifier BLOB NOT NULL,
            kdf_iterations INTEGER NOT NULL DEFAULT 600000)''')

