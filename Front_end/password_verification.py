import re


def password_authentecation(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$'
    if re.fullmatch(pattern, password):
        return True

    return False

