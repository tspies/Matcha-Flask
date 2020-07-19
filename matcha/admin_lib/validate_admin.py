from flask import session, flash, url_for, redirect

from matcha import bcrypt
from matcha.common_lib.query import query_db


def admin_lib_validate_login(form):
    user = query_db("SELECT * FROM users WHERE email=? AND user_type='admin'", (form.email.data,), False, True)
    if user:
        check_password = bcrypt.check_password_hash(user['password'], form.password.data)
        if check_password:
            set_session_values(user)
            flash(f"Welcome {user['username']}, you are logged into the Admin Portal!", 'success')
            return redirect(url_for('admin'))
        else:
            flash("Password Incorrect", 'danger')
            return redirect(url_for('admin_login'))
    else:
        flash("Invalid Admin Login Details", 'danger')
        return redirect(url_for('admin_login'))


def set_session_values(user):

    session['admin'] = user['username']


def admin_lib_logout_user():

    session.pop('admin', None)

    return redirect(url_for('splash'))
