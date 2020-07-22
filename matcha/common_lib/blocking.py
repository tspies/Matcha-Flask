from flask import session

from matcha.common_lib.query import query_db


def common_lib_filter_blocked_accounts(sexuals):

    blocked_accounts = query_db("SELECT * FROM blocked_accounts WHERE user_blocking=?", (session['username'],))
    blocked_names_list = []

    for sexual in sexuals:
        for blocked_account in blocked_accounts:
            if sexual['username'] == blocked_account['blocked_user']:
                blocked_names_list.append(blocked_account['blocked_user'])

    return blocked_names_list


def common_lib_check_if_blocked(username):

    check_blocked = query_db("SELECT * FROM blocked_accounts WHERE user_blocking=? AND blocked_user=?",
                             (username, session['username']))

    return True if check_blocked else False