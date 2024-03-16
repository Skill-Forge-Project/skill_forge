from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


# Register Form
class RegistrationForm(FlaskForm):
    username = StringField('', [validators.Length(min=4, max=25)], render_kw={'placeholder': 'Username'})
    first_name = StringField('', [validators.Length(min=4, max=25)], render_kw={'placeholder': 'First name'})
    last_name = StringField('', [validators.Length(min=4, max=25)], render_kw={'placeholder': 'Last name'})
    email = StringField('', [validators.Email()], render_kw={'placeholder': 'Email address'})
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={'placeholder': 'Password'})
    confirm = PasswordField('', render_kw={'placeholder': 'Repeat password'})
    submit = SubmitField('Register')