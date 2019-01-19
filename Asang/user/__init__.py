import hashlib


def hash_password(password):
    h = hashlib.sha256(password.encode('utf-8'))
    password = h.hexdigest()
    return password
