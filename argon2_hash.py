from argon2 import PasswordHasher


def hash(plain_pw):
    return PasswordHasher().hash(plain_pw)


def verify_hash(hash, plain_pw):
    try:
        PasswordHasher().verify(hash, plain_pw)
    except Exception:
        return False
    else:
        return True
