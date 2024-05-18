from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Enum
from sqlalchemy.orm import joinedload
from flask_bcrypt import Bcrypt  # Password hashing
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os, psycopg2, base64, subprocess, random, string, requests, json, re, secrets, datetime, eventlet
from login_forms import LoginForm, RegistrationForm
from email_functionality import send_welcome_mail, send_reset_email
# Import flask forms and validators
# Import test runners
from test_runners import run_python, run_javascript, run_java, run_csharp


# Load the env variables
load_dotenv()

app = Flask(__name__)

# Database authentication
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# The specific server ip address. Should be included in the .env file
srv_address = os.getenv("SERVER_IP_ADDR")

# Init the password hashing
bcrypt = Bcrypt(app)

# Init the database connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)
conn = psycopg2.connect(os.getenv('SQLALCHEMY_DATABASE_URI_DEV'))

socket = SocketIO(app)

# Init the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Register blueprints
from edit_quest_form import edit_quest_form_bp, ReportedQuest
from user_submit_quest import user_submit_quest_bp
from user_submit_quest import user_submit_dbsubmit_quest_bp
from user_submit_quest import approve_submited_quest_bp
from admin_submit_quest import quest_post_comment_bp
from admin_submit_quest import Quest
from user_submit_quest import SubmitedQuest
from user_solutions import SubmitedSolution
from user_achievements import Achievement, UserAchievement

# ----------------- User Functionality ----------------- #

# Define User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(10), primary_key=True)
    user_role = db.Column(Enum('User', 'Admin', name='user_role_enum'), default='User', nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    rank = db.Column(db.String(30), default="Novice Adventurer")
    avatar = db.Column(db.LargeBinary, default=None)
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(120), nullable=False)
    total_solved_quests = db.Column(db.Integer, default=0, nullable=False)
    total_python_quests = db.Column(db.Integer, default=0, nullable=False)
    total_java_quests = db.Column(db.Integer, default=0, nullable=False)
    total_javascript_quests = db.Column(db.Integer, default=0, nullable=False)
    total_csharp_quests = db.Column(db.Integer, default=0, nullable=False)
    total_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_approved_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_rejected_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_pending_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    facebook_profile = db.Column(db.String(120), default=" ")
    instagram_profile = db.Column(db.String(120), default=" ")
    github_profile = db.Column(db.String(120), default=" ")
    discord_id = db.Column(db.String(120), default=" ")
    linked_in = db.Column(db.String(120), default=" ")
    achievements = db.relationship('UserAchievement')
    is_banned = db.Column(db.Boolean, default=lambda: False)
    ban_date = db.Column(db.DateTime, nullable=True)
    ban_reason = db.Column(db.String(120), default=" ", nullable=True)
    user_online_status = db.Column(db.String(10), default="Offline", nullable=True)
    last_status_update = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)

    # Class constuctor
    def __init__(self, username, first_name, last_name, password, email, avatar=base64.b64encode(open('static/images/anvil.png', 'rb').read())):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.avatar = avatar
        self.generate_user_id()
        
    # Generate random UserID
    def generate_user_id(self):
        prefix = 'USR-'
        suffix_length = 6
        while True:
            suffix = ''.join(random.choices(string.digits, k=suffix_length))
            user_id = f"{prefix}{suffix}"
            if not User.query.filter_by(user_id=user_id).first():
                self.user_id = user_id
                break
    
    # Get the user_ID
    def get_id(self):
        return str(self.user_id)
    
    # Print the User info
    def get_userinfo(self):
        return f'User {self.username}\nID: {self.user_id}\nEmail: {self.email}\nRank: {self.rank}\nXP: {self.xp}XP.'

#  Get the user's avatar, used in the comments section
@app.route('/get_avatar/<user_id>', methods=['GET'])
@login_required
def get_avatar(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    avatar = user.avatar
    return avatar

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Route to handle the user profile (self-open)
@app.route('/my_profile', methods=['POST', 'GET'])
@login_required
def open_user_profile():    
    # Get the User ID for the session
    user_id = current_user.user_id
    # Get the user's solved quests from the database
    user_solved_quests = SubmitedSolution.query.options(joinedload(SubmitedSolution.coding_quest)).all()
    # Get the user info from the database
    user = User.query.get(user_id)
    user.date_registered.strftime('%d-%m-%Y %H:%M:%S')
    # Get the user social media links
    user_facebook = User.query.get(user_id).facebook_profile
    user_instagram = User.query.get(user_id).instagram_profile
    user_github = User.query.get(user_id).github_profile
    user_discord = User.query.get(user_id).discord_id
    user_linked_in = User.query.get(user_id).linked_in
    # Get the user achievements
    user_achievements = UserAchievement.query.filter(UserAchievement.user_id==user_id).all()
    # Convert avatar binary data to Base64-encoded string
    avatar_base64 = base64.b64encode(user.avatar).decode('utf-8') if user.avatar else None
    # Get the last logged date
    user_status = User.query.get(user_id).user_online_status
    last_logged_date = User.query.get(user_id).last_status_update

    return render_template('user_profile.html', user=user, 
                           formatted_date=user.date_registered.strftime('%d-%m-%Y %H:%M:%S'), 
                           avatar=avatar_base64, 
                           user_solved_quests=user_solved_quests,
                           user_facebook=user_facebook,
                           user_instagram=user_instagram,
                           user_github=user_github,
                           user_discord=user_discord,
                           user_linked_in=user_linked_in,
                           user_achievements=user_achievements,
                           user_status=user_status,
                           last_logged_date=last_logged_date)

# Route to handle the user profile (self-open)
@app.route('/user_profile/<username>', methods=['POST', 'GET'])
@login_required
def open_user_profile_view(username):
    # Get the user info from the database
    user = User.query.filter_by(username=username).first()
    user_id = user.user_id
    # Convert avatar binary data to Base64-encoded string
    avatar_base64 = base64.b64encode(user.avatar).decode('utf-8') if user.avatar else None
    # Get the last logged date
    user_status = User.query.get(user_id).user_online_status
    last_logged_date = User.query.get(user_id).last_status_update
        
    if user:
        return render_template('user_profile_view.html', 
                               user=user, 
                               avatar=avatar_base64,
                               user_status=user_status,
                               last_logged_date=last_logged_date)
    else:
        # Handle the case where the user is not found
        return "User not found", 404


# Change the User avatar route
@app.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    # Get user ID from session or request parameters
    user_id = current_user.user_id
    if user_id is None:
        # Handle case where user is not logged in
        return redirect(url_for('login'))
    
    # Check if the avatar file is provided in the request
    if 'avatar' not in request.files:
        # Handle case where no file is uploaded
        flash('No avatar file uploaded', 'error')
        return redirect(request.url)
    
    # Get the uploaded file data
    avatar_file = request.files['avatar']
    
    # Read the file data as bytes
    avatar_data = avatar_file.read()
    
    # Update the user's avatar in the database
    user = User.query.get(user_id)
    user.avatar = avatar_data
    db.session.commit()
    
    # Redirect to the user profile page or any other page
    return redirect(url_for('open_user_profile'))


# Update User info route (Self-Update)
@app.route('/self_update', methods=['GET', 'POST'])
@login_required
def user_self_update():
    current_user_id = current_user.user_id
    new_first_name = request.form.get('change_first_name')
    new_last_name = request.form.get('change_last_name')
    new_email_address = request.form.get('change_email')
    fb_link = request.form.get('change_facebook')
    instagram_link = request.form.get('change_instagram')
    gh_link = request.form.get('change_github')
    discord_id = request.form.get('change_discord')
    linked_in_link = request.form.get('change_linkedin')
    user = User.query.get(current_user_id)
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email_address
    user.facebook_profile = fb_link
    user.instagram_profile = instagram_link
    user.github_profile = gh_link
    user.discord_id = discord_id
    user.linked_in = linked_in_link
    db.session.commit()
    return redirect(url_for('open_user_profile'))

# ----------------- User Functionality ----------------- #

# ----------------- Reset Password Functionality ----------------- #
class ResetToken(db.Model):
    __tablename__ = 'reset_tokens'
    user_id = db.Column(db.String(10), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(64), primary_key=True)
    expiration_time = db.Column(db.DateTime, nullable=False)
    
# Route to open the forgot password form
@app.route('/forgot_password')
def open_forgot_password():
    return render_template('forgot_password.html')

@app.route('/reset_password/<user_id>/<username>/<token>/<expiration_time>', methods=['GET', 'POST'])
def open_reset_password(token, user_id, username, expiration_time):
    return render_template('reset_password.html', token=token, user_id=user_id, username=username, expiration_time=expiration_time)

@app.route('/send_email_token', methods=['POST'])
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
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=60)
        new_token = ResetToken(user_id=user_id, username=username, user_email=user_mail, token=token, expiration_time=expiration_time)
        db.session.add(new_token)
        db.session.commit()

        # Send email with reset link containing the token
        send_reset_email(token, username, email, expiration_time)
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))
    flash('User with this email does not exist.', 'error')
    return redirect(url_for('open_forgot_password'))

@app.route('/save_new_password', methods=['POST'])
@login_required
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
    if str(datetime.datetime.now()) > expiration_time:
        flash('Token has expired.', 'error')
        return redirect(url_for('open_reset_password', token=token, user_id=user_id, username=username, expiration_time=expiration_time))

    

    user = User.query.get(user_id)
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    used_token = ResetToken.query.filter_by(user_id=user_id, token=user_token).first()
    db.session.delete(used_token)
    db.session.commit()
    flash(f'Password for {username} successfully changed. Now you can log in with your new password.', 'success')
    return redirect(url_for('hello'))

# ----------------- Reset Password Functionality ----------------- #


# ----------------- Login and Register Functionality ----------------- #

# Define routes for login and register pages
@app.route('/', methods=['GET', 'POST'])
def login():    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username==form.username.data) | (User.email==form.username.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in the user
            login_user(user, force=True)
            user.user_online_status = 'Online'
            user.last_status_update = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for('main_page'))  # Redirect to the main page after login
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')
    return render_template('index.html', form=form)

# Route to handle the logout functionality
@app.route('/logout')
@login_required
def logout():
    user = User.query.get(current_user.user_id)
    user.user_online_status = 'Offline'
    user.last_status_update = datetime.datetime.now()
    db.session.commit()
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email or username is already in use
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('Email or username already in use', 'error')
            return redirect(url_for('register'))
        
        # Create a new user
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



# Update user status in PostgreSQL
# def update_user_status(user_id, status):
#     current_time = datetime.datetime.now()
#     current_status = UserStatus.filter_by(user_id=user_id).first()
#     if current_status:
#         update_status = UserStatus(user_id=user_id, status=status, last_updated=current_time)
#         db.session.add(update_status)
#         db.session.commit()
#     else:
#         new_status = UserStatus(user_id=user_id, status=status, last_updated=current_time)
#         db.session.add(new_status)
#         db.session.commit()

# @socket.on('connect')
# def connect():
#     user_id = current_user.user_id
#     update_user_status(user_id, 'Online')
#     emit('status_update', {'user_id': user_id, 'status': 'Online'}, broadcast=True)


# @socket.on('disconnect')
# def disconnect():
#     user_id = current_user.user_id
#     update_user_status(user_id, 'Offline')
#     emit('status_update', {'user_id': user_id, 'status': 'Offline'}, broadcast=True)
    
    
# Flask-SocketIO events
# @socketio.on('connect')
# def handle_connect():
#     user_id = current_user.user_id
#     if user_id:
#         update_user_status(user_id, 'online')
#         socketio.emit('status_update', {'user_id': user_id, 'status': 'online'}, broadcast=True)


# @socketio.on('disconnect')
# def handle_disconnect():
#     user_id = current_user.user_id
#     if user_id:
#         update_user_status(user_id, 'offline')
#         socketio.emit('status_update', {'user_id': user_id, 'status': 'offline'}, broadcast=True)

# ----------------- Login and Register Functionality ----------------- #

with app.app_context():
    # Create the database tables
    db.create_all()


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/main')
@login_required
def main_page():
    with open('main_page_title', 'r') as file:
        title_content = file.read()
    with open('main_page_info', 'r') as file:
        content = file.read()  
    server_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('main.html', server_time=server_time, title_content=title_content, content=content)


# Redirect to the Admin Panel (Admin Role in the database is needed)
@app.route('/admin_panel')
@login_required
def open_admin_panel():
    # Retrieve all quests from the database
    all_quests = Quest.query.all()
    all_submited_quests = SubmitedQuest.query.all()
    # Get the User ID for the session
    logged_user_id = current_user.user_id
    # Get the user object with the User ID from the session
    currently_logged_user = User.query.get(logged_user_id)
    # Get all reported quests
    all_reported_quests = ReportedQuest.query.all()
    # Get all users (this is needed so we can extract the name of the user who has reported a quest)
    all_users = User.query.all()
    # Get all admins (this is needed so we can create a dropdown menu in the `Check Reports` table)
    all_admins = User.query.filter_by(user_role='Admin').all()
    if currently_logged_user.user_role == "Admin":
        return render_template('admin_panel.html', 
        all_quests=all_quests, 
        all_submited_quests=all_submited_quests, 
        reported_quests=all_reported_quests,
        all_users=all_users,
        all_admins=all_admins)
    
    return redirect(url_for('login'))

# Redirect to the table with all tasks. Change from template to real page!!!! 
@app.route('/quests_table/<language>', methods=['GET'])
@login_required
def open_quests_table(language):
    # Retrieve all quests from the database
    all_quests = Quest.query.filter(Quest.language == language).all()
    # Retrieve all users from the database
    all_users = User.query.all()
    return render_template('table_template.html', quests=all_quests, users=all_users, language=language)

# Open Quest for submitting. Change from template to real page!!!!
@app.route('/quest/<quest_id>', methods=['GET'])
@login_required
def open_curr_quest(quest_id):
    # Retrieve the specific quest from the database, based on the quest_id
    quest = Quest.query.get(quest_id)
    user_avatar = base64.b64encode(current_user.avatar).decode('utf-8')
    user_role = current_user.user_role
    return render_template('curr_task_template.html', 
                           quest=quest, 
                           user_avatar=user_avatar,
                           user_role=user_role)

# Route to handle solution submission
@app.route('/submit-solution', methods=['POST'])
@login_required
def submit_solution():
    user_id = current_user.user_id
    username = current_user.username
    user_xp_points = current_user.xp
    current_quest_language = request.form.get('quest_language')
    current_quest_type = request.form.get('quest_type')
    current_quest_id = request.form.get('quest_id')
    current_quest_difficulty = request.form.get('quest_difficulty')
    # Handle the simple quests testing
    if current_quest_type == 'Basic':
        user_code = request.form.get('user_code')
        quest_inputs = [eval(x) for x in request.form.get('quest_inputs').split("\r\n")]
        quest_outputs = [eval(x) for x in request.form.get('quest_outputs').split("\r\n")]
        # Handle the code runner exection based on the Quest language
        if current_quest_language == 'Python':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_python.run_code(user_code, quest_inputs, quest_outputs)

        elif current_quest_language == 'JavaScript':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_javascript.run_code(user_code, quest_inputs, quest_outputs)
                    
        elif current_quest_language == 'Java':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_java.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)

        elif current_quest_language == 'C#':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_csharp.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)
        
        # Submit new solution to the database
        quest_id = request.form['quest_id']
        user_id = current_user.user_id
        user_code = request.form['user_code']
        successful_tests = successful_tests
        unsuccessful_tests = unsuccessful_tests
        quest_passed = True if unsuccessful_tests == 0 else False
        
        # Generate random suffix
        suffix_length = 16
        suffix = ''.join(random.choices(string.digits, k=suffix_length))
        prefix = 'SUB-'
        submission_id = f"{prefix}{suffix}"
        # Construct quest ID
        while SubmitedSolution.query.filter_by(submission_id=submission_id).first():
            # If it exists, generate a new submission_id
            suffix = ''.join(random.choices(string.digits, k=suffix_length))
            submission_id = f"{prefix}{suffix}"
                
        # Check if the user already solved the particular quest and IF NOT add XP points, count the quest and update users stats
        solution = SubmitedSolution.query.filter_by(user_id=user_id, quest_id=quest_id, quest_passed=True).first()
        update_user_stats = False
        if not solution or solution == None:
            update_user_stats = True
        current_datetime = datetime.datetime.now()
        
        # Save the submission to the database
        new_submission = SubmitedSolution(
            submission_id=submission_id,
            user_id=user_id,
            quest_id=quest_id,
            submission_date=current_datetime,
            user_code=user_code,
            successful_tests=successful_tests,
            unsuccessful_tests=unsuccessful_tests,
            quest_passed=quest_passed
        )
        
        # Add the new submission to the database session
        db.session.add(new_submission)
        db.session.commit()
        
        # Handle the leveling of the user
        # Update succesfully solved quests
        if update_user_stats:
            current_quest_number = 0
            if unsuccessful_tests == 0:
                current_user.total_solved_quests += 1
                if current_quest_language == "Python":
                    current_user.total_python_quests += 1
                    current_quest_number = current_user.total_python_quests
                elif current_quest_language == "JavaScript":
                    current_user.total_javascript_quests += 1
                    current_quest_number = current_user.total_python_quests
                elif current_quest_language == "Java":
                    current_user.total_java_quests += 1
                    current_quest_number = current_user.total_python_quests
                elif current_quest_language == "C#":
                    current_user.total_csharp_quests += 1
                    current_quest_number = current_user.total_python_quests

                
                # Update the user XP
                if current_quest_difficulty == "Novice Quests":
                    current_user.xp += 30
                elif current_quest_difficulty == "Adventurous Challenges":
                    current_user.xp += 60
                elif current_quest_difficulty == "Epic Campaigns":
                    current_user.xp += 100
            
                # Update the user XP level and rank
                with open('levels.json', 'r') as levels_file:
                    leveling_data = json.load(levels_file)

                for level in leveling_data:
                    for level_name, level_stats in level.items():
                        if level_stats['min_xp'] <= user_xp_points <= level_stats['max_xp']:
                            current_user.level = level_stats['level']
                            current_user.rank = level_name
                            break            

            
            # Generate achievement for the user    
            achievement = Achievement.query.filter(
                Achievement.language == current_quest_language,
                Achievement.quests_number_required == current_quest_number).all()
            achievement_id = Achievement.query.filter(Achievement.achievement_id == achievement[0].achievement_id).first().achievement_id
            if achievement:
                # Generate random suffix
                suffix_length = 16
                suffix = ''.join(random.choices(string.digits, k=suffix_length))
                prefix = 'USR-ACHV-'
                user_achievement_id = f"{prefix}{suffix}"
                while UserAchievement.query.filter_by(user_achievement_id=user_achievement_id).first():
                    # If it exists, generate a new submission_id
                    suffix = ''.join(random.choices(string.digits, k=suffix_length))
                    user_achievement_id = f"{prefix}{suffix}"
                    
                user_achievement = UserAchievement(
                                    user_achievement_id=user_achievement_id,
                                    user_id=user_id,
                                    username=username,
                                    achievement_id=achievement_id,
                                    earned_on=datetime.datetime.now())
                db.session.add(user_achievement)
            db.session.commit()

        
        # Return the results of the tests and the final message to the frontend
        return jsonify({
            'successful_tests': successful_tests,
            'unsuccessful_tests': unsuccessful_tests,
            'message': message,
            'zero_test_input': zero_tests[0],
            'zero_test_output': zero_tests[1],
            'zero_test_result': zero_tests_outputs[0],
            'zero_test_error': zero_tests_outputs[1]
        })
    
    # Handle the advanced quests testing (requires unit tests)
    elif current_quest_type == 'Advanced':
        if current_quest_language == 'Python':
            # # # # # # # # # # # # Python Tests Verify # # # # # # # # # # # #
            user_code = request.form.get('user_code')
            unit_tests = request.form.get('unit_tests')
            total_code = user_code + '\n\n' + unit_tests
            try:
                user_output = subprocess.check_output(['./venv/bin/python3.11', '-c', total_code], text=True)
            except subprocess.CalledProcessError as e:
                user_output = e.output
            return user_output
        
        elif current_quest_language == 'JavaScript':
        # # # # # # # # # # # # JavaScript Tests Verify # # # # # # # # # # # #
            try:
                user_code = request.form.get('user_code')
                unit_tests = request.form.get('unit_tests')
                
                ############# KEEP THIS CODE JUST IN CASE. IT'S WORKING BUT NEEDS TO BE JSON-FIED ##########################
                # print(user_code)
                # command = [
                #     'curl', 
                #     '-X', 'POST', 
                #     '-H', 'Content-Type: application/json', 
                #     # '-d', f'{{"code": "{user_code}", "unit_tests": "{unit_tests}"}}', 
                #     '-d', f'{{"code": "{user_code}"}}',
                #     'http://192.168.0.169:3000/execute'
                # ]
                # result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
                # print(result.stdout)
                # print(result.stderr)
                # return result.stdout
                #############################################################################################################
                
                server_url = f"http://{srv_address}:3000/execute"
                response = requests.post(server_url, json={'code': user_code})
                result = response.json()['result']
                return jsonify({'result': result})
            except Exception as e:
                print(f'An unexpected error occurred: {e}')
                return e
                
        elif current_quest_language == 'Java':
        # # # # # # # # # # # # JavaScript Tests Verify # # # # # # # # # # # #
            pass
        elif current_quest_language == 'C#':
        # # # # # # # # # # # # JavaScript Tests Verify # # # # # # # # # # # #
            pass
        
        
if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    socket.run(app, debug=True, host = '0.0.0.0', port=os.getenv("DEBUG_PORT"))
    # app.run(debug=True, host = '0.0.0.0', port = os.getenv("DEBUG_PORT"))

