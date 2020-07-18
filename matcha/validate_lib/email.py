import re

from flask              import g, flash, redirect, url_for, render_template, current_app, request, session
from matcha             import bcrypt
from flask_mail         import Message
from itsdangerous       import URLSafeTimedSerializer

from matcha import mail


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def validate_lib_email_verification(token):

    username = decode_token(token)
    check = query_db("SELECT * FROM users WHERE username=?", (username,), True)
    if check:
        update_verified(username)
        flash("Email verified! Please login to continue.", 'success')
        return redirect(url_for('login'))
    else:
        flash("There seems to be an error with your token, would you like s to resend the token?", 'danger')
    return render_template("verification.html")


def update_verified(username):
    query_db("UPDATE users SET verified=? WHERE username=?", (True, username))
    g.db.commit()


def decode_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        decoded_token = serializer.loads(
            token,
            salt='email-confirm-salt',
            max_age=3600
        )
        return decoded_token
    except ValueError as e:
        return False


def validate_lib_forgot_password(form):
    if not check_valid_email(form.email.data):
        return render_template("forgot_password.html", form=form)
    else:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(form.email.data, salt='email-confirm-salt')
        message = Message(subject="Matcha Password Reset",
                          body=f"You have requested to reset your password, please click on the following link to reset your password: http://127.0.0.1:5000{url_for('reset_password', token=token)}",
                          recipients=[form.email.data])
        mail.send(message)
        flash("We have sent you a link to reset your password, please click on it to reset your password.", 'success')
        if 'logged_in' in session:
            session.pop('logged_in')
        if 'username' in session:
            session.pop('username')
        return redirect(url_for('login'))


def check_valid_email(email):

    if not re.search("@", email):
        flash("Please use a valid email address, with a '@' symbol.", 'danger')
        return False
    elif not query_db("SELECT * FROM users WHERE email=?", (email,),  True):
        flash("A user with that email address does not exist, please try again.", 'danger')
        return False
    else:
        return True


def validate_lib_reset_password(form, token):
    decoded_token = decode_token(token)
    if decoded_token:
        if decoded_token == form.email.data:

            if not check_valid_email(form.email.data):
                return render_template("reset_password.html", form=form, token=token)
            if not valid_password(form.password.data):
                flash(
                    "Password is Invlaid please use a password between 6 and 15 character with at least one number, special character, one uppler case letter and on lower case letter with no spaces",
                    'danger')
                return render_template("reset_password.html", form=form, token=token)
            if not form.password.data == form.pswd_confirm.data:
                flash("Password and Confirm password do not match", 'danger')
                return render_template("reset_password.html", form=form, token=token)
            set_new_password(form)
            return redirect(url_for('login'))
        else:
            flash('The entered email is incorrect', 'danger')
    else:
        flash("There seems to be a problem with your token, please try again.", 'danger')
    return render_template("reset_password.html", form=form, token=token)


def valid_password(password):
    valid = False

    while 1:
        if len(password) < 6 or len(password) > 15:
            break
        elif not re.search("[a-z]", password):
            break
        elif not re.search("[0-9]", password):
            break
        elif not re.search("[A-Z]", password):
            break
        elif not re.search("[!@#$%^&*()]", password):
            break
        elif re.search("\s", password):
            break
        else:
            valid = True
            break
    return valid


def set_new_password(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    query_db("UPDATE users SET password=? WHERE email=?", (hashed_password, form.email.data,), True)
    flash("Password has been updated", 'success')
    g.db.commit()











