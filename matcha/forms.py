from wtforms import SubmitField, PasswordField, BooleanField, StringField, TextAreaField, SelectField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import IntegerField

GENDER_TYPES = ['Male', 'Female', 'Transgender', 'Gender Neutral', 'Non-Binary', 'Agender', 'Pangender', 'Genderqueer',
                'Two-Spirit', 'Third Gender']
SEX_ORIENTATION = ['Bisexual', 'Heterosexual', 'Homosexual']


class LoginForm(FlaskForm):
    email = StringField('Email:')
    submit = SubmitField('Log In')
    password = PasswordField('Password')
    remember = BooleanField("Remember Me")


class SignupForm(FlaskForm):
    email = StringField('Email:')
    username = StringField('Username:')
    firstname = StringField('Firstname:')
    lastname = StringField('Lastname:')
    password = PasswordField('Password:')
    pswd_confirm = PasswordField('Confirm Password:')
    submit = SubmitField('Signup')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email:')
    submit = SubmitField('Send Reset Link')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email:')
    password = PasswordField('New Pssword:')
    pswd_confirm = PasswordField('Confirm Password:')
    submit = SubmitField('Send Reset Link')


class ProfileUpdateForm(FlaskForm):
    username = StringField('Username')
    firstname = StringField('Firstname:')
    profile_pic = StringField()
    lastname = StringField('Lastname:')
    email = StringField('Email:')
    age = IntegerField('Age:')
    likes = IntegerField('Likes:')
    matches = IntegerField('Matches:')
    bio = TextAreaField('Bio:')
    gender = SelectField('Gender:', choices=GENDER_TYPES, default='')
    sex_orientation = SelectField('Sexual Orientation', choices=SEX_ORIENTATION, default='Bisexual')
    fame = IntegerField('Fame:')
    geo_location = StringField('Location:')
    bio = TextAreaField('Bio:')

    submit = SubmitField('Update Profile')

    travelling = BooleanField('Travelling')
    exercise = BooleanField('Exercise')
    movies = BooleanField('Movies')
    dancing = BooleanField('Dancing')
    cooking = BooleanField('Cooking')
    outdoors = BooleanField('Outdoors')
    pets = BooleanField('Pets')
    photography = BooleanField('Photography')
    sports = BooleanField('Sports')
