from flask import g
from matcha.common_lib.query import query_db

# def query_db(query, args=(), one=False):
#     cur = g.db.execute(query, args)
#     rv = [dict((cur.description[idx][0], value)
#                for idx, value in enumerate(row)) for row in cur.fetchall()]
#     return (rv[0] if rv else None) if one else rv


def user_lib_get_user(username):
    user = query_db("SELECT * FROM users WHERE username=?", (username,), False, True)
    return user


def user_lib_get_interests(username):
    interests = query_db("SELECT * FROM interests WHERE username=? ", (username,), False, True)
    return interests

