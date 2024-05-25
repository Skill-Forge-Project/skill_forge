from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, TextAreaField
from wtforms.validators import Email, Length, EqualTo, DataRequired, ValidationError, Regexp
import re

########### Login Form ###########
class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


def validate_password(form, password):
    errors = []
    if not re.search(r'[A-Z]', password.data):
        flash('Password must contain at least one uppercase letter', 'error')
        errors.append('Password must contain at least one uppercase letter')
    
    if len(password.data) < 10:
        flash('Password must be at least 10 characters long', 'error')
        errors.append('Password must be at least 10 characters long')

    if not re.search(r'\d', password.data):
        flash('Password must contain at least one digit', 'error')
        errors.append('Password must contain at least one digit')

    if not re.search(r'[!@#$%^&*()_+=\-{}\[\]:;,<.>?]', password.data):
        flash('Password must contain at least one special character', 'error')
        errors.append('Password must contain at least one special character')
    
    if form.confirm.data != password.data:
        flash('Passwords must match', 'error')
        errors.append('Passwords must match')
    
    if errors:
        raise ValidationError(errors)
    
    return password

    
########### Register Form ###########
class RegistrationForm(FlaskForm):
    username = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'Username'})
    first_name = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'First name'})
    last_name = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'Last name'})
    email = StringField('', [Email(), DataRequired()], render_kw={'placeholder': 'Email address'})    
    password = PasswordField('', validators=[
        DataRequired(),
        Length(min=10, message='Password must be at least 10 characters long.'),
        Regexp(re.compile(r'.*[A-Z].*'), message='Password must contain at least one uppercase letter.'),
        Regexp(re.compile(r'.*[0-9].*'), message='Password must contain at least one digit.'),
        Regexp(re.compile(r'.*[!@#$%^&*()_+=\-{}\[\]:;,<.>?].*'), message='Password must contain at least one special character.')
    ],
        render_kw={'placeholder': 'Password'})
    confirm = PasswordField('', render_kw={'placeholder': 'Repeat password'})
    submit = SubmitField('Register')
    
    
########### Password Reset Form ###########
class PasswordResetForm(FlaskForm):
    user_id = HiddenField('User ID')
    username = HiddenField('Username')
    token = HiddenField('Token')
    user_token = StringField('Token', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=10, message='Password must be at least 10 characters long.'),
        Regexp(re.compile(r'.*[A-Z].*'), message='Password must contain at least one uppercase letter.'),
        Regexp(re.compile(r'.*[0-9].*'), message='Password must contain at least one digit.'),
        Regexp(re.compile(r'.*[!@#$%^&*()_+=\-{}\[\]:;,<.>?].*'), message='Password must contain at least one special character.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    expiration_time = HiddenField('Expiration Time')
    submit = SubmitField('Reset Password')


########### Create New Quest Form - as Admin ###########
class QuestForm(FlaskForm):
    quest_name = StringField('Quest Name', validators=[DataRequired(), Length(max=100)])
    quest_language = SelectField('Quest Language', choices=[('Python', 'Python'), ('JavaScript', 'JavaScript'), ('Java', 'Java'), ('C#', 'C#')], validators=[DataRequired()])
    quest_difficulty = SelectField('Quest Difficulty', choices=[('Novice Quests', 'Novice Quests'), ('Adventurous Challenges', 'Adventurous Challenges'), ('Epic Campaigns', 'Epic Campaigns')], validators=[DataRequired()])
    quest_condition = TextAreaField('Quest Condition', validators=[DataRequired()])
    quest_inputs = TextAreaField('Inputs Samples', validators=[DataRequired()])
    quest_outputs = TextAreaField('Outputs Samples', validators=[DataRequired()])
    function_template = TextAreaField('Quest Template', validators=[DataRequired()])
    quest_unitests = TextAreaField('Quest Unit Tests - Not Obligatory')
    submit = SubmitField('Submit Quest')