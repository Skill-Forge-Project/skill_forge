from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


# Register Form
class RegistrationForm(FlaskForm):
    username = StringField('Username:', [validators.Length(min=4, max=25)])
    first_name = StringField('First Name:', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name:', [validators.Length(min=4, max=25)])
    email = StringField('Email:', [validators.Email()])
    password = PasswordField('Password:', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:')
    submit = SubmitField('Register')