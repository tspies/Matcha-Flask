from flask import g
from matcha import bcrypt
from matcha.common_lib.query import query_db


# def query_db(query, args=(), one=False):
#     cur = g.db.execute(query, args)
#     rv = [dict((cur.description[idx][0], value)
#                for idx, value in enumerate(row)) for row in cur.fetchall()]
#     return (rv[0] if rv else None) if one else rv


def user_lib_create_user(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    query_db("INSERT INTO users (username, email, password, verified, firstname, lastname) VALUES (?,?,?,?,?,?)",
             (form.username.data, form.email.data, hashed_password, False, form.firstname.data, form.lastname.data), True)


def user_lib_create_interests(username):
    query_db("INSERT INTO interests (username) VALUES (?)", (username,), True)
