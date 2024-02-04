from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Password hashing
from flask_login import LoginManager, UserMixin, login_user, login_required
from dotenv import load_dotenv
import os

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

# Init the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


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
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        # Check if the username or email already exists
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username or email already exists. Please choose different ones.', 'danger')
        else:
            # Hash the password with bcrypt
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            # Create a new user and add it to the database
            new_user = User(username=username, first_name = first_name, last_name = last_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            # return redirect(url_for('index'))
    return render_template('register.html', form=form)


# App route for Login
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Form called")
    if form.validate_on_submit():
        print("Validation succesful!")
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("Login Succesful!")
            login_user(user, force = True)
            flash('Login successful!', 'success')
            print("Redirect me!")
            return redirect(url_for('main_page'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('index.html', form=form)


@app.route('/')
def hello():
    return render_template('index.html')

# App Routes to tasks
@app.route('/python_tasks')
def open_python_tasks():
    return render_template('python_tasks.html')

@app.route('/js_tasks')
def open_js_tasks():
    return render_template('js_tasks.html')

@app.route('/java_tasks')
def open_java_tasks():
    return render_template('java_tasks.html')

@app.route('/c_sharp_tasks')
def open_csharp_tasks():
    return render_template('c_sharp_tasks.html')

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host = '0.0.0.0', port = '5000')
    app.run()
