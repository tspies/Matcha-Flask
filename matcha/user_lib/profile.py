import re

from flask import render_template, session, flash, redirect, url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from matcha import mail
from matcha.common_lib.history import common_lib_log_history_moment
from matcha.common_lib.query import query_db

# def query_db(query, args=(), commit=False, one=False):
#     cur = g.db.execute(query, args)
#     if commit:
#         g.db.commit()
#     else:
#         rv = [dict((cur.description[idx][0], value)
#                    for idx, value in enumerate(row)) for row in cur.fetchall()]
#         return (rv[0] if rv else None) if one else rv


def user_lib_validate_profile_update_form(form, user, post_form_interests, pictures):
    interest_list = ['travelling', 'exercise', 'movies', 'dancing', 'cooking', 'outdoors', 'pets', 'photography', 'sports']
    update_interests = []

    for interest in interest_list:
        if interest in post_form_interests:
            update_interests.append(1)
        else:
            update_interests.append(0)
    new_username = False
    new_email = False
    form.likes.data = user['likes']
    form.matches.data = user['matches']
    form.fame.data = user['fame']

    if not form.username.data == user['username']:
        new_username = True
        username = query_db("SELECT * FROM users WHERE username = ?", (form.username.data,), False, True)
        if username:
            flash("That username is already in use, please choose another one.", 'danger')
            return render_template("profile_update.html",  form=form, user=user)

    if not form.email.data == user['email']:
        new_email = True
        if re.search("@", form.email.data):
            email = query_db("SELECT * FROM users WHERE email = ?", (form.email.data,), False, True)
            if email:
                flash("That email is already in in use, plese choose another one.", 'danger')
                return render_template("profile_update.html",  form=form, user=user)
        else:
            flash("Please us a valid email address, with a '@' symbol.", 'danger')
            return render_template("profile_update.html", form=form, user=user)

    if new_username and new_email:
        query_db("UPDATE users SET username=?, email=?, gender=?, sex_orientation=? WHERE username=?",
                 (form.username.data, form.email.data, form.gender.data, form.sex_orientation.data, user['username']), True)
        query_db("UPDATE interests SET username=? WHERE username=?",
                 (form.username.data, session['username']), True)
        query_db(
            "UPDATE interests SET travelling=?, exercise=?, movies=?, dancing=?, cooking=?, outdoors=?, pets=?, photography=?, sports=? WHERE username=?",
            (update_interests[0], update_interests[1], update_interests[2], update_interests[3], update_interests[4],
             update_interests[5], update_interests[6], update_interests[7], update_interests[8], form.username.data), True)
        flash("Username and email updated, please click the link in the verification email we sent you to re-verify your account.", 'success')
        pop_session_values(form)
        send_verification_email(form)
        return redirect(url_for('login'))

    elif new_username:
        query_db("UPDATE users SET username=?, gender=?, sex_orientation=? WHERE username=?",
                 (form.username.data, form.gender.data, form.sex_orientation.data, session['username']), True)
        query_db("UPDATE interests SET username=? WHERE username=?",
                 (form.username.data, session['username']), True)
        query_db(
            "UPDATE interests SET travelling=?, exercise=?, movies=?, dancing=?, cooking=?, outdoors=?, pets=?, photography=?, sports=? WHERE username=?",
            (update_interests[0], update_interests[1], update_interests[2], update_interests[3], update_interests[4],
             update_interests[5], update_interests[6], update_interests[7], update_interests[8], form.username.data), True)
        flash("Username updated!", 'success')
        set_session_values(form)
        return redirect(url_for('profile_update'))

    elif new_email:
        query_db("UPDATE users SET email=?, gender=?, sex_orientation=? WHERE username=?",
                 (form.email.data, form.gender.data, form.sex_orientation.data, session['username']), True)
        flash("Email updated, please click the link in the verification email we sent you to re-verify your account.", 'success')
        pop_session_values()
        send_verification_email(form)
        return redirect(url_for('login'))

    query_db("UPDATE users SET gender=?, sex_orientation=?, bio=?, firstname=?, lastname=?, age=?, complete=? WHERE username=?",
             (form.gender.data, form.sex_orientation.data, form.bio.data, form.firstname.data, form.lastname.data, form.age.data, 'True', session['username']), True)

    query_db(
        "UPDATE interests SET travelling=?, exercise=?, movies=?, dancing=?, cooking=?, outdoors=?, pets=?, photography=?, sports=? WHERE username=?",
        (update_interests[0], update_interests[1], update_interests[2], update_interests[3], update_interests[4],
         update_interests[5], update_interests[6], update_interests[7], update_interests[8], session['username']), True)

    return redirect(url_for('profile_update', form=form, user=user, pictures=pictures))


def user_lib_populate_profle_update_form(form, user, interests):

    form.bio.data               = user['bio']
    form.age.data               = user['age']
    form.fame.data              = user['fame']
    form.email.data             = user['email']
    form.likes.data             = user['likes']
    form.gender.data            = user['gender']
    form.matches.data           = user['matches']
    form.username.data          = user['username']
    form.lastname.data          = user['lastname']
    form.firstname.data         = user['firstname']
    form.profile_pic.data       = user['profile_pic']
    form.sex_orientation.data   = user['sex_orientation']

    form.pets.data              = interests['pets']
    form.sports.data            = interests['sports']
    form.movies.data            = interests['movies']
    form.dancing.data           = interests['dancing']
    form.cooking.data           = interests['cooking']
    form.exercise.data          = interests['exercise']
    form.outdoors.data          = interests['outdoors']
    form.travelling.data        = interests['travelling']
    form.photography.data       = interests['photography']

    return form


def user_lib_get_pictures(username):
    pictures = query_db("SELECT * FROM images WHERE username=?", (username,))
    return pictures


def user_lib_create_wink(username):
    query_db("INSERT INTO likes (user_liking, user_liked) VALUES (?,?)",
             (session['username'], username), True)
    flash("You have winked at " + username, 'success')
    common_lib_log_history_moment('wink', session['username'], username, 'You winked at ' + username)
    common_lib_log_history_moment('wink', username, session['username'], session['username'] + ' winked at you!')

    history = query_db("SELECT * FROM history")
    print(history)
    query_db("UPDATE users SET likes=likes+1 WHERE username=?", (username,), True)
    check_if_users_match(username)
    query_db("UPDATE users SET fame = ((likes + matches + 1) * 100) WHERE username=?", (username,), True)
    query_db("UPDATE users SET fame = ((likes + matches + 1) * 100) WHERE username=?", (session['username'],), True)
    return redirect(url_for('profile_view', username=username))


def user_lib_unwink(username):
    query_db("DELETE FROM likes WHERE (user_liking=? AND user_liked=?)", (session['username'], username), True)
    query_db("UPDATE users SET likes=likes-1 WHERE username=?", (username,), True)
    flash("You have un-winked " + username, 'success')

    common_lib_log_history_moment('unwink', session['username'], username, 'You unwinked ' + username)
    common_lib_log_history_moment('unwink', username, session['username'], session['username'] + ' unwinked you! :(')

    match_check = query_db("SELECT * FROM matches WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)",
              (session['username'], username, username, session['username']))

    if match_check:
        user_1 = query_db("SELECT * FROM matches WHERE user_1=? AND user_2=?", (session['username'], username))
        user_2 = query_db("SELECT * FROM matches WHERE user_1=? AND user_2=?", (username, session['username']))
        if user_1:
            query_db("DELETE FROM matches WHERE user_1=? AND user_2=?", (session['username'], username), True)

        if user_2:
            query_db("DELETE FROM matches WHERE user_1=? AND user_2=?", (username, session['username']), True)

        testmatch = query_db("SELECT * FROM matches")
        print(testmatch)
        query_db("UPDATE users SET matches=matches-1 WHERE username=?", (session['username'],), True)
        query_db("UPDATE users SET matches=matches-1 WHERE username=?", (username,), True)

        common_lib_log_history_moment('unmatch', session['username'], username, 'You unmatched with ' + username)
        common_lib_log_history_moment('unmatch', username, session['username'], session['username'] + ' unmatched with you! :(')

        flash("You have unmatched from " + username, 'success')

    query_db("UPDATE users SET fame = ((likes + matches + 1) * 100) WHERE username=?", (username,), True)
    query_db("UPDATE users SET fame = ((likes + matches + 1) * 100) WHERE username=?", (session['username'],), True)
    return redirect(url_for('profile_view', username=username))


def check_if_users_match(username):
    user_1 = query_db("SELECT * FROM likes WHERE user_liking=? and user_liked=?", (session['username'], username))
    user_2 = query_db("SELECT * FROM likes WHERE user_liking=? and user_liked=?", (username, session['username']))
    match_check = query_db("SELECT * FROM matches WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)", (session['username'], username, username, session['username']))

    if user_1 and user_2 and not match_check:
        flash("You and " + username + " have matched! You can now chat.", 'success')

        common_lib_log_history_moment('match', session['username'], username, 'You matched with ' + username + '<3')
        common_lib_log_history_moment('match', username, session['username'], session['username'] + ' matched with you! <3')

        query_db("INSERT INTO matches (user_1, user_2) VALUES (?,?)", (session['username'], username), True)
        query_db("UPDATE users SET matches=matches+1 WHERE username=?", (session['username'],), True)
        query_db("UPDATE users SET matches=matches+1 WHERE username=?", (username,), True)


def set_session_values(form):

    session['username'] = form.username.data


def pop_session_values():

    session.pop('username')
    session.pop('logged_in')


def send_verification_email(form):

    serialize = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serialize.dumps(form.username.data, salt='email-confirm-salt')

    message = Message(subject="Matcha Verification",
                      body=f"You have updated your email, please click on the following link to complete your registration: http://127.0.0.1:5000/verification/{token}",
                      recipients=["tspies.game@gmail.com"])
    mail.send(message)
    flash("You have Signed up, please click the link in the email we have sent you to verify your account.", 'success')