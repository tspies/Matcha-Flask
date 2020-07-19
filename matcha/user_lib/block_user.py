from flask import session, flash
from matcha.common_lib.query import query_db
from matcha.common_lib.history import common_lib_log_history_moment


def user_lib_block_user(username):

    already_blocked = query_db("SELECT * FROM blocked_accounts WHERE user_blocking=? AND blocked_user=?", (session['username'], username))

    if not already_blocked:
        flash('Block request has been sent to admin for review', 'success')
        common_lib_log_history_moment('block request', session['username'], username, 'You have submitted a request to block ' + username)
        query_db("INSERT INTO blocked_accounts (user_blocking, blocked_user) VALUES (?,?)", (session['username'], username), True)
    else:
        flash('You have already submitted a blocking request, please wait for admin to review your request', 'danger')

    test_blocked = query_db("SELECT * FROM blocked_accounts")
    print(test_blocked)