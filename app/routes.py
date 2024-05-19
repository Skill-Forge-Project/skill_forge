from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

# Import the password hashing library
import bcrypt

# Import the forms and models
from app.forms import LoginForm, RegistrationForm
from app.models import User

bp = Blueprint('main', __name__)

########### Routes handling user login/logout and registration ###########

# Define routes for login and register pages
@bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username==form.username.data) | (User.email==form.username.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in the user
            login_user(user, force=True)
            return redirect(url_for('main_page'))  # Redirect to the main page after login
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')
    return render_template('index.html', form=form)

# Route to handle the logout functionality
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
