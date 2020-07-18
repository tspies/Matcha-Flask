import re

from flask import g, flash, redirect, url_for, request, render_template, session, current_app
from matcha         import bcrypt


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def validate_lib_login_form(form):

    user = query_db("SELECT * FROM users WHERE email=?", (form.email.data,), True)
    if user:
        check_password = bcrypt.check_password_hash(user['password'], form.password.data)
        if check_password:
            if user['verified']:
                set_session_values(user)
                query_db("UPDATE users SET last_online=? WHERE username=?", ("Online", user['username']))
                g.db.commit()
                flash(f"Welcome {user['username']}, you are logged in!", 'success')
            else:
                flash('You have not yet verified your email, please verify to continue', 'danger')
                return redirect(url_for('login'))
            return redirect(url_for('home'))
        else:
            flash("Password Incorrect", 'danger')
            return redirect(url_for('login'))
    else:
        flash("That email does not exist, please try another", 'danger')
        return redirect(url_for('login'))


def set_session_values(user):

    session['username'] = user['username']
    session['logged_in'] = True