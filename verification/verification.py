import sqlite3
import hmac
from contextlib import closing
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

db_file = 'USERS.db'
VERIFIER_TOKEN = b'verifier_token'

class VaultNotFoundError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

def is_vault_initialized():
    with closing(sqlite3.connect(db_file)) as conn:
        row = conn.execute('''SELECT 1 FROM vault_meta WHERE id = 1''').fetchone()
        if row:
            return True
    return False

def derive_key(password: str, salt: bytes, iterations: int = 600_000) -> bytes:
    return hashlib.pbkdf2_hmac('sha256',
                               password.encode(),
                               salt,
                               iterations,
                               dklen=32)

def create_vault_user(password: str) -> bytes:
    salt = os.urandom(16)
    iterations = 600_000
    key = derive_key(password, salt, iterations)
    nonce = os.urandom(12)
    verifier = AESGCM(key).encrypt(nonce, VERIFIER_TOKEN, None)

    with closing(sqlite3.connect(db_file)) as conn:
        with conn:
            conn.execute('''INSERT INTO vault_meta(id, salt, verifier_nonce, verifier, kdf_iterations) 
                            VALUES (1,?,?,?,?)''', (salt, nonce, verifier, iterations))
    return key

def verify_vault_user(password: str) -> bytes:
    with closing(sqlite3.connect(db_file)) as conn:
        pass_info = conn.execute('''SELECT salt,
                                           verifier_nonce,
                                           verifier,
                                           kdf_iterations
                                    FROM vault_meta WHERE id = 1''').fetchone()

    if pass_info is None:
        raise VaultNotFoundError()

    salt, verifier_nonce, verifier, iterations = pass_info

    key = derive_key(password, salt, iterations)

    try:
        token = AESGCM(key).decrypt(verifier_nonce, verifier, None)
    except InvalidTag:
        raise  WrongPasswordError()
    if not hmac.compare_digest(token, VERIFIER_TOKEN):
        raise WrongPasswordError()
    return key