'''
Login and Registration forms functionalities
'''
from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, EqualTo, DataRequired
import re

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')

# Register Form
class RegistrationForm(FlaskForm):
    username = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'Username'})
    first_name = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'First name'})
    last_name = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'Last name'})
    email = StringField('', [Email(), DataRequired()], render_kw={'placeholder': 'Email address'})
    password = PasswordField('', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ], render_kw={'placeholder': 'Password'})
    confirm = PasswordField('', render_kw={'placeholder': 'Repeat password'})
    submit = SubmitField('Register')
    
    def validate_password(self, password):
        if not re.search(r'[A-Z]', password.data):
            flash('Password must contain at least one uppercase letter', 'error')
        
        if len(password.data) < 10:
            flash('Password must be at least 10 characters long', 'error')

        if not re.search(r'\d', password.data):
            flash('Password must contain at least one digit', 'error')

        if not re.search(r'[!@#$%^&*()_+=\-{}\[\]:;,<.>?]', password.data):
            flash('Password must contain at least one special character', 'error')
    
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            flash('Passwords do not match', 'error')
