import re, secrets, os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
# Import the mail functions
from app.mailtrap import send_reset_email, send_welcome_mail
# Import the database instance
from app.database.db_init import db
# Import the forms and models
from app.forms import LoginForm, RegistrationForm
from app.models import User, ResetToken

bp = Blueprint('main', __name__)

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

########### Routes handling user login/logout and registration ###########
# Define routes for login and register pages
@bp.route('/', methods=['GET', 'POST'])
def login():
    # Import the bcrypt instance
    from app import bcrypt
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username==form.username.data) | (User.email==form.username.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in the user
            login_user(user, force=True)
            return redirect(url_for('main.main_page'))  # Redirect to the main page after login
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')
    return render_template('index.html', form=form)

# Route to handle the logout functionality
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

# Handle the registration route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email or username is already in use
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('Email or username already in use', 'error')
            return redirect(url_for('register'))
        
        # Create a new user
        # Import the bcrypt instance
        from app import bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email=form.email.data, username=form.username.data, 
                        first_name=form.first_name.data, last_name=form.last_name.data, 
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        send_welcome_mail(form.email.data, form.username.data)
        flash('Your account has been created! You are now able to log in.', 'success ')
        return redirect(url_for('login'))  # Redirect to the login page after successful registration
    return render_template('register.html', form=form)

########### Routes handling password reset functionality ###########
# Route to open the forgot password form
@bp.route('/forgot_password')
def open_forgot_password():
    return render_template('forgot_password.html')

@bp.route('/reset_password/<user_id>/<username>/<token>/<expiration_time>', methods=['GET', 'POST'])
def open_reset_password(token, user_id, username, expiration_time):
    return render_template('reset_password.html', token=token, user_id=user_id, username=username, expiration_time=expiration_time)

@bp.route('/send_email_token', methods=['POST'])
def send_email_token():
    email = request.form.get('email_address')
    if len(email) == 0:
        flash('Please provide an email address.', 'error')
        return redirect(url_for('open_forgot_password'))
    
    user_mail = request.form.get('email_address')
    current_user = User.query.filter_by(email=user_mail).first()
    if current_user:
        user_id = User.query.filter_by(email=email).first().user_id
        username = User.query.filter_by(email=email).first().username
        # Generate a unique token
        token = secrets.token_urlsafe(32)
        # Calculate expiration time (60 minutes from now)
        expiration_time = datetime.now() + timedelta(minutes=60)
        new_token = ResetToken(user_id=user_id, username=username, user_email=user_mail, token=token, expiration_time=expiration_time)
        db.session.add(new_token)
        db.session.commit()

        # Send email with reset link containing the token
        send_reset_email(token, username, email, expiration_time)
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    flash('User with this email does not exist.', 'error')
    return redirect(url_for('open_forgot_password'))

@bp.route('/save_new_password', methods=['POST'])
def update_new_password():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    token = request.form.get('token')
    user_token = request.form.get('user_token')
    new_password = request.form.get('password')
    confirm_password = request.form.get('confirm')
    expiration_time = request.form.get('expiration_time')

    if new_password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if user_token is None or user_token != token:
        flash('Invalid token.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if not new_password or not confirm_password:
        flash('Please provide a password.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if len(new_password) < 10:
        flash('Password must be at least 10 characters long.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if not re.search(r'[A-Z]', new_password):
        flash('Password must contain at least one uppercase letter.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if not re.search(r'\d', new_password):
        flash('Password must contain at least one digit.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if not re.search(r'[!@#$%^&*()_+=\-{}\[\]:;,<.>?]', new_password):
        flash('Password must contain at least one special character.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    if str(datetime.now()) > expiration_time:
        flash('Token has expired.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))

    

    user = User.query.get(user_id)
    # Import the bcrypt instance
    from app import bcrypt
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    used_token = ResetToken.query.filter_by(user_id=user_id, token=user_token).first()
    db.session.delete(used_token)
    db.session.commit()
    flash(f'Password for {username} successfully changed. Now you can log in with your new password.', 'success')
    return redirect(url_for('hello'))

########### Routes handling main apge ###########
# Open the main page
@bp.route('/home')
@login_required
def main_page():
    title_path = os.path.join(base_dir, '../main_page_title')
    info_path = os.path.join(base_dir, '../main_page_info')
    try:
        with open(title_path, 'r') as file:
            title_content = file.read().strip()
    except FileNotFoundError:
        title_content = "Default Title"
    try:
        with open(info_path, 'r') as file:
            content = file.read().strip()
    except FileNotFoundError:
        content = "Default Content"
        
    server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('homepage.html', server_time=server_time, title_content=title_content, content=content)