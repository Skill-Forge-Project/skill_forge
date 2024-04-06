from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Enum, ARRAY
from flask_bcrypt import Bcrypt  # Password hashing
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from dotenv import load_dotenv
import os, psycopg2, base64, subprocess, unittest, random, string, requests
from datetime import datetime
from login_forms import LoginForm, RegistrationForm
# Import test runner
from test_runners import run_python, run_javascript, run_java, run_csharp



# Load the env variables
load_dotenv()

app = Flask(__name__)


app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# The specific server ip address. Should be included in the .env file
srv_address = os.getenv("SERVER_IP_ADDR")

# Init the password hashing
bcrypt = Bcrypt(app)

# Init the database connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)
conn = psycopg2.connect(os.getenv('SQLALCHEMY_DATABASE_URI_DEV'))

# Init the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Register blueprints
from edit_quest_form import edit_quest_form_bp
from user_submit_quest import user_submit_quest_bp
from user_submit_quest import user_submit_dbsubmit_quest_bp
from user_submit_quest import approve_submited_quest_bp
from admin_submit_quest import Quest # handle as Blueprint!!!
from user_submit_quest import SubmitedQuest # handle as Blueprint!!!

# Define User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(10), primary_key=True)
    user_role = db.Column(Enum('User', 'Admin', name='user_role_enum'), default='User', nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    rank = db.Column(db.String(30), default="Novice Adventurer")
    avatar = db.Column(db.LargeBinary, default=None)
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(120), nullable=False)
    total_solved_quests = db.Column(db.Integer, default=0)
    total_python_quests = db.Column(db.Integer, default=0)
    total_java_quests = db.Column(db.Integer, default=0)
    total_javascript_quests = db.Column(db.Integer, default=0)
    total_csharp_quests = db.Column(db.Integer, default=0)
    total_submited_quests = db.Column(db.Integer, default=0)
    total_approved_submited_quests = db.Column(db.Integer, default=0)
    total_rejected_submited_quests = db.Column(db.Integer, default=0)
    total_pending_submited_quests = db.Column(db.Integer, default=0)
    
    # Class constuctor
    def __init__(self, username, first_name, last_name, password, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
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


# Update user information form
@login_required
@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    user_first_name = request.form['first_name']



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    # Create the database tables
    db.create_all()

# App route for Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        repeat_password = request.form['confirm']

        # Check if passwords match
        if password != repeat_password:
            return render_template('register.html', error='Passwords do not match')

        # Check if the email or username is already in use
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            return render_template('register.html', error='Email or username already in use')

        # Create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.')

    return render_template('register.html', form=form)


# App route for Login
@app.route('/', methods=['GET', 'POST'])
def login():    
    form = LoginForm()
    if form.validate_on_submit():
        print("Validation succesful!")
        user = User.query.filter((User.username==form.username.data) | (User.email==form.username.data)).first()
        
        if user:
            # Create session for the user. This is needed for the login manager and for reading the data from the database
            session['user_id'] = user.user_id
        else:
            # Return some error!!!!!!
            pass
        
        # Log in the user
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, force = True)
            return redirect(url_for('main_page'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('index.html', form=form)


@app.route('/')
def hello():
    return render_template('index.html')

@login_required
@app.route('/main')
def main_page():
    return render_template('main.html')


# Redirect to the Admin Panel (Admin Role in the database is needed)
@app.route('/admin_panel')
@login_required
def open_admin_panel():
    
    # Retrieve all quests from the database
    all_quests = Quest.query.all()
    all_submited_quests = SubmitedQuest.query.all()

    # Get the User ID for the session
    logged_user_id = session['user_id']

    # Get the user object with the User ID from the session
    currently_logged_user = User.query.get(logged_user_id)

    if currently_logged_user.user_role == "Admin":
        return render_template('admin_panel.html', all_quests=all_quests, all_submited_quests=all_submited_quests)
    
    return redirect(url_for('login'))

# Route to handle the user profile (self-open)
@login_required
@app.route('/my_profile', methods=['POST', 'GET'])
def open_user_profile():
    # If user is not logged in, redirect to login page
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get the User ID for the session
    user_id = session['user_id']
    
    # Get the user info from the database
    user = User.query.get(user_id)
    user.date_registered.strftime('%d-%m-%Y %H:%M:%S')
    
    # Convert avatar binary data to Base64-encoded string
    avatar_base64 = base64.b64encode(user.avatar).decode('utf-8') if user.avatar else None

    return render_template('user_profile.html', user=user, formatted_date=user.date_registered.strftime('%d-%m-%Y %H:%M:%S'), avatar=avatar_base64)

# Route to handle the user profile (self-open)
@login_required
@app.route('/user_profile/<username>', methods=['POST', 'GET'])
def open_user_profile_view(username):
    # Get the user info from the database
    user = User.query.filter_by(username=username).first()
    user.date_registered.strftime('%d-%m-%Y %H:%M:%S')
    # Convert avatar binary data to Base64-encoded string
    avatar_base64 = base64.b64encode(user.avatar).decode('utf-8') if user.avatar else None
    if user:
        # Render the user profile template with the user data
        return render_template('user_profile_view.html', user=user, avatar=avatar_base64)
    else:
        # Handle the case where the user is not found
        return "User not found", 404



# Change the User avatar route
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    # Get user ID from session or request parameters
    user_id = session.get('user_id') or request.form.get('user_id')
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
@login_required
@app.route('/self_update', methods=['GET', 'POST'])
def user_self_update():
    current_user_id = current_user.user_id
    new_first_name = request.form.get('change_first_name')
    new_last_name = request.form.get('change_last_name')
    new_email_address = request.form.get('change_email')
    
    user = User.query.get(current_user_id)
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email_address
    db.session.commit()
    return redirect(url_for('open_user_profile'))

# App Routes to tasks
@login_required
@app.route('/python_tasks')
def open_python_tasks():
    return render_template('python_tasks.html')

@login_required
@app.route('/js_tasks')
def open_js_tasks():
    return render_template('js_tasks.html')

@login_required
@app.route('/java_tasks')
def open_java_tasks():
    return render_template('java_tasks.html')

@login_required
@app.route('/c_sharp_tasks')
def open_csharp_tasks():
    return render_template('c_sharp_tasks.html')

# Redirect to the table with all tasks. Change from template to real page!!!! 
@login_required
@app.route('/table_template')
def open_table_template():
    # Retrieve all quests from the database
    all_quests = Quest.query.all()
    all_users = User.query.all()
    return render_template('table_template.html', quests=all_quests, users=all_users)

# Open Quest for submitting. Change from template to real page!!!!
@login_required
@app.route('/quest/<quest_id>')
def open_curr_quest(quest_id):
    # Retrieve the specific quest from the database, based on the quest_id
    quest = Quest.query.get(quest_id)
    return render_template('curr_task_template.html', quest=quest)


# Route to handle solution submission
@login_required
@app.route('/submit-solution', methods=['POST'])
def submit_solution():
    user_id = current_user.user_id
    username = current_user.username
    current_quest_language = request.form.get('quest_language')
    current_quest_type = request.form.get('quest_type')
    current_quest_id = request.form.get('quest_id')
    print(f"Current quest type is: {current_quest_type}")
    
    # Handle the simple quests testing
    if current_quest_type == 'Basic':
        user_code = request.form.get('user_code')
        quest_inputs = [eval(x) for x in request.form.get('quest_inputs').split("\r\n")]
        quest_outputs = [eval(x) for x in request.form.get('quest_outputs').split("\r\n")]

        # Handle the code runner exection based on the Quest language
        if current_quest_language == 'Python':
            successful_tests, unsuccessful_tests, message = run_python.run_code(user_code, quest_inputs, quest_outputs)
            return jsonify({'successful_tests': successful_tests, 'unsuccessful_tests': unsuccessful_tests, 'message': message})

        elif current_quest_language == 'JavaScript':
            user_code = request.form.get('user_code')
            quest_inputs = [eval(x) for x in request.form.get('quest_inputs').split("\r\n")]
            quest_outputs = [eval(x) for x in request.form.get('quest_outputs').split("\r\n")]
            successful_tests, unsuccessful_tests, message = run_javascript.run_code(user_code, quest_inputs, quest_outputs)
            return jsonify({'successful_tests': successful_tests, 'unsuccessful_tests': unsuccessful_tests, 'message': message})
        
        elif current_quest_language == 'Java':
            successful_tests, unsuccessful_tests, message = run_java.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)
            return jsonify({'successful_tests': successful_tests, 'unsuccessful_tests': unsuccessful_tests, 'message': message})
        
        elif current_quest_language == 'C#':
            user_output = run_csharp.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)
            return user_output
        
    # Handle the advanced quests testing (requires unit tests)
    elif current_quest_type == 'Advanced':
        print(f'Current Languange is: {current_quest_language}')
        if current_quest_language == 'Python':
            # # # # # # # # # # # # Python Tests Verify # # # # # # # # # # # #
            user_code = request.form.get('user_code')
            unit_tests = request.form.get('unit_tests')
            total_code = user_code + '\n\n' + unit_tests
            try:
                user_output = subprocess.check_output(['./venv/bin/python3.11', '-c', total_code], text=True)
            except subprocess.CalledProcessError as e:
                user_output = e.output
            print(f'The output of the user code is: {user_output}')
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
    app.run(debug=True, host = '0.0.0.0', port = os.getenv("DEBUG_PORT"))

