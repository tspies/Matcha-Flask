from flask import session

from matcha.common_lib.query import query_db


def common_lib_filter_blocked_accounts(profiles):

    blocked_accounts = query_db("SELECT * FROM blocked_accounts WHERE user_blocking=?", (session['username'],))
    blocked_names_list = []

    for profile in profiles:
        for blocked_account in blocked_accounts:
            if profile['username'] == blocked_account['blocked_user']:
                blocked_names_list.append(blocked_account['blocked_user'])

    return blocked_names_list


def common_lib_check_if_blocked(username):
    return False