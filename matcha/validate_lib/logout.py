from datetime import datetime

from flask import session, redirect, url_for, g


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def validate_lib_logout_user():
    mydate = datetime.now()
    formateddate = mydate.strftime("%d-%m-%Y\n%H:%M:%S")
    query_db("UPDATE users SET last_online=? WHERE username=?", (formateddate, session['username']))
    g.db.commit()
    session.pop('username', None)
    session.pop('logged_in', None)

    return redirect(url_for('splash'))