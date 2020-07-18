import re
from flask              import flash, g, session, current_app
from matcha             import mail
from flask_mail         import Message
from itsdangerous       import URLSafeTimedSerializer


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def validate_lib_signup_form(form):
    valid = True

    username = query_db("SELECT * FROM users WHERE username = ?", (form.username.data,))
    email = query_db("SELECT * FROM users WHERE email = ?", (form.email.data,))
    if username:
        flash("That username is already in use, please choose another one.", 'danger')
        return False
    if not form.firstname.data or not form.lastname.data:
        flash("Please provide a first and last name", 'danger')
        return False
    if email:
        flash("That email is already in in use, plese choose another one.", 'danger')
        return False
    if not re.search("@", form.email.data):
        flash("Please us a valid email address, with a '@' symbol.", 'danger')
        return False
    if not valid_password(form.password.data):
        flash("Password is Invlaid please use a password between 6 and 15 character with at least one number, special character, one uppler case letter and on lower case letter with no spaces", 'danger')
        return False
    if not form.password.data == form.pswd_confirm.data:
        flash("Password and Confirm password do not match", 'danger')
        return False

    if valid:
        set_session_values(form)
    return valid


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


def set_session_values(form):

    session['username'] = form.username.data
    # session['logged_in'] = True


def validate_lib_send_verification_email(form):

    serialize = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serialize.dumps(form.username.data, salt='email-confirm-salt')

    message = Message(subject="Matcha Verification",
                      body=f"Thanks for signing up, please click on the following link to complete your registration: http://127.0.0.1:5000/verification/{token}",
                      recipients=[form.email.data])
    mail.send(message)
    flash("You have Signed up, please click the link in the email we have sent you to verify your account.", 'success')

