import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).with_name("vault.db")

def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''PRAGMA foreign_keys = ON''')
    return conn


SCHEMA = '''
    -- Vault-ის პარამეტრები (ერთი სტრიქონი). საიდუმლო არაფერია:
    -- salt და iterations გასაღების გამოსაყვანად Master Password-მდე იკითხება.
    CREATE TABLE IF NOT EXISTS vault_meta(
    id INTEGER PRIMARY KEY AUTOINCREMENT CHECK(id  = 1),
    salt BLOB NOT NULL,
    kdf_iterations INTEGER NOT NULL,
    verifier       BLOB    NOT NULL
    );
    
    -- კატეგორიები
    CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    );
    -- პაროლები
    CREATE TABLE IF NOT EXISTS passwords (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id         INTEGER
                        REFERENCES categories(id) ON DELETE SET NULL,
    meta_enc            BLOB    NOT NULL,  -- title, username, url, notes, strength
    secret_enc          BLOB    NOT NULL,  -- მხოლოდ პაროლი
    created_at          INTEGER NOT NULL,  -- unix timestamp
    updated_at          INTEGER NOT NULL,
    password_changed_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_passwords_category ON passwords(category_id);
    -- ფაილები: მეტამონაცემი და შიგთავსი ცალკე ცხრილებში,
    -- რომ სიის წაკითხვისას დიდი ბლობები არ ჩაიტვირთოს
    CREATE TABLE IF NOT EXISTS files (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    meta_enc   BLOB    NOT NULL,  -- სახელი, ზომა, რეალური ტიპი, SHA-256, ენტროპია, risk score
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
    );
 
    CREATE TABLE IF NOT EXISTS file_data (
    file_id  INTEGER PRIMARY KEY
             REFERENCES files(id) ON DELETE CASCADE,
    data_enc BLOB NOT NULL        -- დაშიფრული ფაილის ბაიტები
    );
'''

def InitDB() -> None:
    with closing(connect()) as conn, conn:
        conn.executescript(SCHEMA)



