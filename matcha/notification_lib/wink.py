import sqlite3

from flask import g, session, current_app


def connect_db():
    return sqlite3.connect(current_app.config['DATABASE'])


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def notification_lib_check_match(username):
    connection = connect_db()
    match_check = connection.execute("SELECT * FROM matches WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)", (session['username'], username, username, session['username']))
    # match_check = query_db("SELECT * FROM matches WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)", (session['username'], username, username, session['username']))
    return True if match_check else False