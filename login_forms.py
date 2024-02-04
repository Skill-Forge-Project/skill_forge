from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


# Register Form
class RegistrationForm(FlaskForm):
    username = StringField('username', [validators.Length(min=4, max=25)])
    first_name = StringField('first_name', [validators.Length(min=4, max=25)])
    last_name = StringField('last_name', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Email()])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('repeat_password')
    submit = SubmitField('register')