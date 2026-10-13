import sqlite3
import hmac
from contextlib import closing
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from  init_db import connect

VERIFIER_TOKEN = b'verifier_token'
KDF_ITERATIONS = 600_000
SALT_SIZE = 16
NONCE_SIZE = 12

class VaultNotFoundError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

class VaultAlreadyExistsError(Exception):
    pass

def is_vault_initialized():
    with closing(connect()) as conn:
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
    if is_vault_initialized():
        raise VaultAlreadyExistsError()
    salt = os.urandom(SALT_SIZE)
    iterations = KDF_ITERATIONS
    key = derive_key(password, salt, iterations)
    nonce = os.urandom(NONCE_SIZE)
    verifier = nonce + AESGCM(key).encrypt(nonce, VERIFIER_TOKEN, None)

    with closing(connect()) as conn:
        with conn:
            conn.execute('''INSERT INTO vault_meta(id, salt, kdf_iterations, verifier) 
                            VALUES (1,?,?,?)''', (salt, iterations, verifier))
    return key

def verify_vault_user(password: str) -> bytes:
    with closing(connect()) as conn:
        pass_info = conn.execute('''SELECT salt,
                                           kdf_iterations,
                                           verifier
                                    FROM vault_meta WHERE id = 1''').fetchone()

    if pass_info is None:
        raise VaultNotFoundError()

    salt, iterations, blob = pass_info
    nonce = blob[:12]
    ciphertext = blob[12:]

    key = derive_key(password, salt, iterations)

    try:
        token = AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise  WrongPasswordError()
    if not hmac.compare_digest(token, VERIFIER_TOKEN):
        raise WrongPasswordError()
    return key