from flask import g, session


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def browsing_lib_get_suggested_user_profiles(current_user_object):
    suggestions = query_db("SELECT * FROM users WHERE NOT username=?", (session['username'],))
    return suggestions