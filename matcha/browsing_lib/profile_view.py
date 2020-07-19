from flask import session

from matcha.common_lib.query import query_db


def get_profile_data(username):

    profile_data = {}
    user_profile = query_db("SELECT * FROM users WHERE username=?", (username,), False, True)
    interests = query_db("SELECT * FROM interests WHERE username=?", (username,), False, True)
    matched = query_db("SELECT * from matches WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)",
                       (username, session['username'], session['username'], username), False, True)
    pictures = query_db("SELECT * FROM images WHERE username=?", (username,))
    winked = query_db("SELECT * FROM likes WHERE (user_liking=? AND user_liked=?)", (session['username'], username))

    print(matched)
    session_user = query_db("SELECT * FROM users WHERE username=?", (session['username'],), False, True)
    interest_list = []
    if 'id' in interests: interests.pop('id')
    if interests:
        for key, value in interests.items():
            if value == 1:
                interest_list.append(key)
    profile_data = {
        'session_user':     session_user,
        'user_profile':     user_profile,
        'interest_list':    interest_list,
        'pictures':         pictures,
        'matched':          matched,
        'winked':           winked
    }

    return profile_data