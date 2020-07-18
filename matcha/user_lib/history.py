from flask import g
from matcha.common_lib.query import query_db

# def query_db(query, args=(), one=False, commit=False):
#     cur = g.db.execute(query, args)
#     if commit:
#         g.db.commit()
#         return
#     else:
#         rv = [dict((cur.description[idx][0], value)
#                    for idx, value in enumerate(row)) for row in cur.fetchall()]
#         return (rv[0] if rv else None) if one else rv


def log_history_moment(log_type, logging_user, notif_username, message):

    if log_type == 'wink':
        query_db("INSERT INTO history (log_username, notif_username, message, history_type) VALUES (?,?,?,?)",
                 (logging_user, notif_username, message, log_type), True)
    elif log_type == 'unwink':
        pass
    elif log_type == 'match':
        pass
    elif log_type == 'unmatch':
        pass

