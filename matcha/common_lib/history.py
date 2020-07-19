from flask import session
from .query import query_db
from datetime import datetime
from .blocking import common_lib_check_if_blocked


def common_lib_log_history_moment(log_type, logging_user, notif_username, message):

    mydate = datetime.now()
    formated_datenow = mydate.strftime("%d-%m-%Y\n%H:%M:%S")

    query_db("INSERT INTO history (log_username, notif_username, message, history_type, logged_timestamp ) VALUES (?,?,?,?,?)",
             (logging_user, notif_username, message, log_type, formated_datenow), True)


def common_lib_get_history_logs():

    history_logs = query_db("SELECT * FROM history WHERE log_username=?", (session['username'],))
    return history_logs
