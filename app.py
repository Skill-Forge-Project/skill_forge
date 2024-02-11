from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Password hashing
from flask_login import LoginManager, UserMixin, login_user, login_required
from dotenv import load_dotenv
import os, psycopg2, base64
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
    user_id = db.Column(db.Integer, primary_key=True)
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
    
    # Get the user_ID
    def get_id(self):
        return str(self.user_id)
    
    # Print the User info
    def get_userinfo(self):
        return f'User {self.username}\nID: {self.user_id}\nEmail: {self.email}\nRank: {self.rank}\nXP: {self.xp}XP.'


class Quest(db.Model):
    __tablename__ = 'coding_quests'
    task_id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    quest_name = db.Column(db.String(255), nullable=False)
    quest_author = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    condition = db.Column(db.Text, nullable=False)
    function_template = db.Column(db.Text, nullable=False)
    unit_tests = db.Column(db.Text, nullable=False)
    xp = db.Column(db.Enum('30', '60', '100', name='xp_points'), nullable=False)

    def __repr__(self):
        return f"<Quest(task_id={self.task_id}, quest_name='{self.quest_name}', language='{self.language}', difficulty='{self.difficulty}', xp='{self.xp}')>"
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

# Change from template to real page!!!!
@login_required
@app.route('/table_template')
def open_table_template():
    return render_template('table_template.html')

# Load all the quests from the database
@login_required
@app.route('/quests')
def quests():
    # Retrieve all quests from the database
    all_quests = Quest.query.all()
    return render_template('quests.html', quests=all_quests)

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host = '0.0.0.0', port = '5000')
