from matcha.common_lib.query import query_db


def user_lib_get_user(username):
    user = query_db("SELECT * FROM users WHERE username=?", (username,), False, True)
    return user


def user_lib_get_interests(username):
    interests = query_db("SELECT * FROM interests WHERE username=? ", (username,), False, True)
    return interests

