from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from flask_bcrypt import Bcrypt  # Password hashing
from flask_login import LoginManager, UserMixin, login_user, login_required
from dotenv import load_dotenv
import os, psycopg2, base64, subprocess, unittest, random, string
from datetime import datetime
from login_forms import LoginForm, RegistrationForm

# Load the env variables
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Init the password hashing
bcrypt = Bcrypt(app)

# Init the database connection
db = SQLAlchemy(app)
conn = psycopg2.connect(os.getenv('SQLALCHEMY_DATABASE_URI'))

# Init the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Define User model
class User(db.Model):
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

# Class for storing the quests(exercises)
class Quest(db.Model):
    __tablename__ = 'coding_quests'
    quest_id = db.Column(db.String(10), primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    quest_name = db.Column(db.String(255), nullable=False)
    solved_times = db.Column(db.Integer, default=0, nullable=True)
    quest_author = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    condition = db.Column(db.Text, nullable=False)
    function_template = db.Column(db.Text, nullable=False)
    unit_tests = db.Column(db.Text, nullable=False)
    xp = db.Column(db.Enum('30', '60', '100', name='xp_points'), nullable=False)

    def __repr__(self):
        return f"QuestID={self.quest_id}, Quest Name='{self.quest_name}', Language='{self.language}', Difficulty='{self.difficulty}', XP='{self.xp}'"
    
# Submit new quest as admin from the admin panel
@app.route('/submit_quest', methods=['GET', 'POST'])
def submit_quest():
    language = request.form['quest_language']
    difficulty = request.form['quest_difficulty']
    quest_name = request.form['quest_name']
    quest_condition = request.form['quest_condition']
    function_template = request.form['function_template']
    unit_tests = request.form['quest_unitests']
    


    # Generate random suffix
    suffix_length = 6
    suffix = ''.join(random.choices(string.digits, k=suffix_length))
    # Determine prefix based on language
    if request.form['quest_language'] == 'Python':
        prefix = 'PY-'
    elif request.form['quest_language'] == 'Java':
        prefix = 'JV-'
    elif request.form['quest_language'] == 'JavaScript':
        prefix = 'JS-'
    elif request.form['quest_language'] == 'C#':
        prefix = 'CS-'
    else:
        prefix = 'UNK-'  # Default prefix for unknown languages
    # Construct quest ID
    quest_id = f"{prefix}{suffix}"
    
    # Assing XP points based on difficulty
    xp = 0
    if request.form['quest_difficulty'] == 'Novice Quests':
        xp = 30
    elif request.form['quest_difficulty'] == 'Adventurous Challenges':
        xp = 60
    elif request.form['quest_difficulty'] == 'Epic Campaigns':
        xp = 100
    
    print(language, difficulty, quest_name, quest_condition, function_template, unit_tests, xp)
    
    # Create a new Quest object
    new_quest = Quest(
        quest_id= quest_id,
        language=language,
        difficulty=difficulty,
        quest_name=quest_name,
        quest_author='Your Author',  # Replace with actual author name
        date_added=datetime.now(),
        last_modified=datetime.now(),
        condition=quest_condition,
        function_template=function_template,
        unit_tests=unit_tests,
        xp=str(xp)
    )

    # Add the new quest to the database session
    db.session.add(new_quest)
    db.session.commit()

    # Redirect to a success page or main page
    return redirect(url_for('open_admin_panel'))

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
        user = User.query.filter_by(username=form.username.data).first()
        
        # Create session for the user. This is needed for the login manager and for reading the data from the database
        session['user_id'] = user.user_id
        
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
@login_required
@app.route('/admin_panel')
def open_admin_panel():
    return render_template('admin_panel.html')

@login_required
@app.route('/user_profile')
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

# Change from template to real page!!!! Redirect to the table with all tasks
@login_required
@app.route('/table_template')
def open_table_template():
    # Retrieve all quests from the database
    all_quests = Quest.query.all()
    print(all_quests)
    return render_template('table_template.html', quests=all_quests)


# Change from template to real page!!!!
@login_required
@app.route('/quest/<quest_id>')
def open_curr_task(quest_id):
    # Retrieve the specific quest from the database, based on the quest_id
    quest = Quest.query.get(quest_id)
    return render_template('curr_task_template.html', quest=quest)


# # # # # # # # # # # # Python Tests Verify # # # # # # # # # # # #
# Route to handle solution submission
@login_required
@app.route('/submit-solution', methods=['POST'])
def submit_solution():
    user_code = request.form.get('user_code')
    unit_tests = request.form.get('unit_tests')
    total_code = user_code + '\n\n' + unit_tests
    try:
        user_output = subprocess.check_output(['./venv/bin/python3.11', '-c', total_code], text=True)
    except subprocess.CalledProcessError as e:
        user_output = e.output
    print(f'The output of the user code is: {user_output}')
    return user_output




if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host = '0.0.0.0', port = '5000')
