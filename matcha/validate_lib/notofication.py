from flask import g, session
from matcha.common_lib.query import query_db

def validate_lib_check_match(username):
    match_check = query_db("SELECT * FROM matches WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)", (session['username'], username, username, session['username']))
    return True if match_check else False