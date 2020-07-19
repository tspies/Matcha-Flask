import sqlite3

from flask                                      import render_template, g, request, flash, session, redirect, url_for
from flask_socketio                             import send, emit

from matcha                                     import app, socketio
from matcha.browsing_lib.homepage_suggestions   import browsing_lib_get_suggested_user_profiles
from matcha.forms                               import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm, ProfileUpdateForm, AdminForm
from matcha.notification_lib.wink               import notification_lib_check_match
from matcha.user_lib.profile                    import user_lib_validate_profile_update_form, user_lib_populate_profle_update_form, \
                                                        user_lib_get_pictures, user_lib_create_wink, user_lib_unwink
from matcha.user_lib.get_user                   import user_lib_get_user, user_lib_get_interests
from matcha.validate_lib.email                  import validate_lib_email_verification, validate_lib_forgot_password, validate_lib_reset_password
from matcha.validate_lib.image                  import validate_lib_handle_picture_upload, validate_lib_update_profile_picture
from matcha.validate_lib.login                  import validate_lib_login_form
from matcha.validate_lib.logout                 import validate_lib_logout_user
from matcha.validate_lib.signup                 import validate_lib_signup_form, validate_lib_send_verification_email
from matcha.user_lib.create_user                import user_lib_create_user, user_lib_create_interests
from matcha.user_lib.block_user                 import user_lib_block_user
from matcha.common_lib.history                  import common_lib_get_history_logs, common_lib_log_history_moment
from matcha.common_lib.query                    import query_db
from matcha.browsing_lib.profile_view           import get_profile_data
from matcha.common_lib.blocking                 import common_lib_check_if_blocked, common_lib_filter_blocked_accounts
from matcha.admin_lib.validate_admin            import admin_lib_validate_login, admin_lib_logout_user
from matcha.admin_lib.requests                  import admin_lib_get_block_requests
clients = {}


# @socketio.on('like_notif', namespace="/like")
# def handle_like(message):
#     print(f"IN HANDLER username: {data['username']}")
#     username    = data['username']
#     room        = "room-" + username
#     emit('notifications', {"message": f"{session['username']} has winked at you!"}, room=room)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("database.db")
    return db

# <----------Socket Handlers---------->
@socketio.on('message')
def std_message(msg):
    print('Message ' + msg)
    send(msg, broadcast=True)


@socketio.on('connect_user')
def connect_user(data):
    username = data['username']
    clients[username] = request.sid
    print(" User " + username + " has connected to personal room.")
    print(clients)


@socketio.on('notification', namespace='/notification')
def handle_notification(data):
    return
    message = data['sender'] + data['message'] + "  -- " + data['recipient']
    recipient_sid = clients[data['recipient']]
    sender_sid = clients[data['sender']]
    emit('new_wink', message, room=recipient_sid)
    if notification_lib_check_match(data['recipient']):
        emit('new_match', message, room=recipient_sid)
        emit('new_match', message, room=sender_sid)


@socketio.on('private_message', namespace='/notification')
def handle_private_message(payload):
    recipient_sid = clients[payload['recipient']]
    message = payload['message']
    emit('new_private_message', message, room=recipient_sid)
# <----------End Socket Handlers----------->


# <----------App Routes---------->
@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = AdminForm()
    if 'admin' in session:
        if not session['admin']:
            if request.method == "POST":
                return admin_lib_validate_login(form)
    return render_template("admin_login.html", form=form)


@app.route('/admin_logout')
def admin_logout():

    flash('Logged Out of Admin portal', 'success')
    return admin_lib_logout_user()


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    block_requests = admin_lib_get_block_requests()
    return render_template("admin.html", block_requests=block_requests)


@app.route("/")
def splash():
    if 'logged_in ' in session:
        if session['logged_in']:
            return redirect(url_for('home'))
    session['logged_in'] = False
    session['admin'] = False
    return render_template("splash.html")


@app.route("/chat/<curr_username>/<username>", methods=['GET', 'POST'])
def chat(curr_username, username):
    return render_template("chat.html", curr_username=curr_username, username=username)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        if not session['logged_in']:
            form = LoginForm()
            if request.method == "POST":
                return validate_lib_login_form(form)
            return render_template("login.html", form=form)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if 'logged_in' in session:
        if not session['logged_in']:
            if request.method == "POST":
                if validate_lib_signup_form(form):
                    validate_lib_send_verification_email(form)
                    user_lib_create_user(form)
                    user_lib_create_interests(form.username.data)
                    return redirect(url_for('login'))
            return render_template('signup.html', form=form)
        else:
            return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@app.route("/logout")
def logout():
    return validate_lib_logout_user()


@app.route('/home')
def home():
    if session.get('logged_in'):
        current_user_object = user_lib_get_user(session['username'])
        if current_user_object['complete'] != 'False':
            suggested_profiles = browsing_lib_get_suggested_user_profiles(current_user_object)
            print(suggested_profiles)
            blocked_name_list = common_lib_filter_blocked_accounts(suggested_profiles)
            return render_template("home.html", suggestions=suggested_profiles, username=session['username'], blocked_list=blocked_name_list)
        else:
            flash('Please complete your profile to continue', 'danger')
            return redirect(url_for('profile_update'))
    return redirect(url_for('splash'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == "POST":
        return validate_lib_forgot_password(form)
    return render_template('forgot_password.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if request.method == "POST":
        return validate_lib_reset_password(form, token)
    return render_template("reset_password.html", form=form, token=token)


@app.route('/not_verified')
def unverified():
    return render_template("unverified.html")


@app.route('/verification/<token>')
def verification(token):
    return validate_lib_email_verification(token)


@app.route('/profile_update', methods=['GET', 'POST'])
def profile_update():
    if 'logged_in' in session:
        if session['logged_in']:
            if request.method == "POST":
                form = ProfileUpdateForm()
                user = user_lib_get_user(session['username'])
                interests = request.form.getlist('interest')
                pictures = user_lib_get_pictures(session['username'])
                return user_lib_validate_profile_update_form(form, user, interests, pictures)
            else:
                form = ProfileUpdateForm()
                user = user_lib_get_user(session['username'])
                interests = user_lib_get_interests(session['username'])
                form = user_lib_populate_profle_update_form(form, user, interests)
                pictures = user_lib_get_pictures(session['username'])
            return render_template("profile_update.html", form=form, user=user, interests=interests, pictures=pictures)
    return redirect(url_for('splash'))


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if 'logged_in' in session:
        if session['logged_in']:
            if request.method == 'POST':
                validate_lib_handle_picture_upload(request)
                return redirect(url_for('profile_update'))
    return redirect(url_for('splash'))


@app.route('/update_profile_pic_pictures')
def update_profile_picture_pictures():
    pictures = user_lib_get_pictures(session['username'])
    return render_template("update_profile_picture.html", pictures=pictures)


@app.route('/update_profile_picture/<filename>')
def update_profile_picture(filename):
    validate_lib_update_profile_picture(filename)
    return redirect(url_for('profile_update'))


@app.route('/profile_view/<username>')
def profile_view(username):

    profile = get_profile_data(username)

    if profile['user_profile']:

        common_lib_log_history_moment('profile_view', session['username'], username, "You viewed " + username + "'s profile")
        if not common_lib_check_if_blocked(username):
            common_lib_log_history_moment('profile_view', username, session['username'], session['username'] + " viewed your profile, why dont you check their profile out?")

        return render_template("profile_view.html",
                               winked=profile['winked'],
                               user=profile['user_profile'],
                               session_user=profile['session_user'],
                               interests=profile['interest_list'],
                               matched=profile['matched'],
                               pictures=profile['pictures'])
    else:
        flash('That user does not exist', 'danger')
        return redirect(url_for('home'))


@app.route('/wink/<username>', methods=['GET', 'POST'])
def wink(username):
    already_liked = query_db("SELECT * FROM likes WHERE user_liking=? AND user_liked=?",
                             (session['username'], username), False, True)
    if already_liked:
        flash("Hey! You have already winked at this person , wait for then to wink back at you.", 'danger')
        return redirect(url_for('profile_view', username=username))
    else:
        return user_lib_create_wink(username)


@app.route('/unwink/<username>', methods=['GET', 'POST'])
def unwink(username):
    return user_lib_unwink(username)


@app.route('/history')
def history():
    if 'logged_in' in session:
        if session['logged_in']:
            history_logs = common_lib_get_history_logs()
            return render_template('history.html', history_logs=history_logs, username=session['username'])


@app.route('/block_user/<username>', methods=['GET', 'POST'])
def block_user(username):
    if 'logged_in' in session:
        if session['logged_in']:
            user_lib_block_user(username)
            return redirect(url_for('home'))


@app.route('/notification', methods=['GET', 'POST'])
def notifications():
    return render_template('notifications.html')
