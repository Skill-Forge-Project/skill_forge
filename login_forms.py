'''
Login and Registration forms functionalities
'''
from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, EqualTo, DataRequired, ValidationError
import re

# Login Form
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
    
    if ValidationError:
        raise ValidationError(errors)
    

    

# Register Form
class RegistrationForm(FlaskForm):
    username = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'Username'})
    first_name = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'First name'})
    last_name = StringField('', [Length(min=4, max=25)], render_kw={'placeholder': 'Last name'})
    email = StringField('', [Email(), DataRequired()], render_kw={'placeholder': 'Email address'})    
    password = PasswordField('', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        validate_password], render_kw={'placeholder': 'Password'})
    confirm = PasswordField('', render_kw={'placeholder': 'Repeat password'})
    submit = SubmitField('Register')
    


# def validate_confirm_password(self, confirm_password):

