"""
This file handles the functionality for submiting a new quest as a regular user.
- Class:SubmitedQuest defines the database table for the submitted quests and the database columns and columns properties. Updates only with db migration!!!
- open_user_submit_quest route opens the user submit quest page.
- user_submit_quest route handles the form submission and commits the new quest to the database.
- open_submited_quest route opens the specified quest for editing from the Admin Panel.
"""

from __main__ import app, db
# from app import app, db # Use this instead of the above line for db migrations
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_login import login_required, current_user
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import IntegrityError
import random, string, json
from admin_submit_quest import Quest


# Blueprint to handle opening of specific submited quest
user_submit_quest_bp = Blueprint('open_submited_quest', __name__)
# Blueprint to handle the commit of the submited quest into the database
user_submit_dbsubmit_quest_bp = Blueprint('user_submit_quest', __name__)
# Blueprint to handle the approval of the submited quest and adding it to the database(class Quests)
approve_submited_quest_bp = Blueprint('approve_submited_quest', __name__)

# Define the database table for the submitted quests
class SubmitedQuest(db.Model):
    __tablename__ = 'user_submited_quests'
    quest_id = db.Column(db.String(10), primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    quest_name = db.Column(db.String(255), nullable=False)
    quest_author = db.Column(db.String(255), nullable=False)
    quest_author_id = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', name='quest_submit_status'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    condition = db.Column(db.Text, nullable=False)
    function_template = db.Column(db.Text, nullable=False)
    unit_tests = db.Column(db.Text, nullable=True)
    test_inputs = db.Column(db.Text, nullable=True)
    test_outputs = db.Column(db.Text, nullable=True)
    xp = db.Column(db.Enum('30', '60', '100', name='xp_points'), nullable=False)
    type = db.Column(db.Enum('Basic', 'Advanced', name='quest_type'), nullable=True)
    comments=db.Column(JSON, default = "[]", nullable=True) # Store comments for the submited quests


# Redirect to the user submit quest page
@login_required
@app.route('/user_submit_quest')
def open_user_submit_quest():
    return render_template('user_submit_quest.html')

# Submit new quest as a regular user
@login_required
@app.route('/user_submit_quest', methods=['GET', 'POST'])
def user_submit_quest():
    language = request.form['quest_language']
    difficulty = request.form['quest_difficulty']
    quest_name = request.form['quest_name']
    quest_condition = request.form['quest_condition']
    function_template = request.form['function_template']
    unit_tests = request.form['quest_unitests']
    quest_inputs = request.form['quest_inputs']
    quest_outputs = request.form['quest_outputs']
    
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
    quest_type = ''
    if request.form['quest_difficulty'] == 'Novice Quests':
        xp = 30
        quest_type = 'Basic'
    elif request.form['quest_difficulty'] == 'Adventurous Challenges':
        xp = 60
        quest_type = 'Basic'
    elif request.form['quest_difficulty'] == 'Epic Campaigns':
        xp = 100
        quest_type = 'Basic'
    elif request.form['quest_difficulty'] == 'Abyssal Trials':
        quest_type = 'Advanced'
        
    # Define default state for the quest (Pending)
    state = 'Pending'
    
    # Get the User ID for the session
    current_user_id = current_user.user_id
    current_username = current_user.username
    
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a new Quest object
    new_user_submitted_quest = SubmitedQuest(
        quest_id= quest_id,
        language=language,
        difficulty=difficulty,
        quest_name=quest_name,
        quest_author=current_username, 
        quest_author_id=current_user_id,
        status='Pending', # Default status is 'Pending
        date_added=current_time,
        last_modified=current_time,
        condition=quest_condition,
        function_template=function_template,
        unit_tests=unit_tests,
        test_inputs=quest_inputs,
        test_outputs=quest_outputs,
        type=quest_type,
        xp=str(xp)
    )
    
    # Add the new quest to the database session
    db.session.add(new_user_submitted_quest)
    db.session.commit()
    
    return redirect(url_for('open_user_submit_quest'))


# Open User Submited Quest for editing from the Admin Panel
@login_required
@app.route('/open_submited_quest/<quest_id>')
def open_submited_quest(quest_id):
    submited_quest = SubmitedQuest.query.filter_by(quest_id=quest_id).first()
    return render_template('edit_submited_quest.html', submited_quest=submited_quest)

# Route to Approve the Submited Quest to the database class Quests
@login_required
@app.route('/approve_submited_quest', methods=['GET', 'POST'])
def approve_submited_quest():
    # Read the values from the HTML form to pass to the Class constructor
    submited_quest_id = request.form['submited_quest_id']
    submited_quest_name = request.form['submited_quest_name']
    submited_quest_language = request.form['submited_quest_language']
    submited_quest_difficulty = request.form['submited_quest_difficulty']
    submited_quest_author = request.form['submited_quest_author']
    submited_quest_date_added=request.form['submited_quest_date_added']
    submited_quest_condition = request.form['submited_quest_condition']
    submited_function_template = request.form['submited_function_template']
    submited_quest_unit_tests = request.form['submited_quest_unitests']
    submited_quest_inputs = request.form['submited_quest_inputs']
    submited_quest_outputs = request.form['submited_quest_outputs']
    
    print(f'Submited Quest Difficulty: {submited_quest_difficulty}')
    # Assing XP points based on difficulty
    xp = 0
    type = ''
    if request.form['submited_quest_difficulty'] == 'Novice Quests':
        xp = 30
        type = 'Basic'
    elif request.form['submited_quest_difficulty'] == 'Adventurous Challenges':
        xp = 60
        type = 'Basic'
    elif request.form['submited_quest_difficulty'] == 'Epic Campaigns':
        xp = 100
        type = 'Basic'
    
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_quest = Quest(
        quest_id=submited_quest_id,
        language=submited_quest_language,
        difficulty=submited_quest_difficulty,
        quest_name=submited_quest_name,
        quest_author=submited_quest_author,
        date_added=submited_quest_date_added,
        last_modified=current_time,
        condition=submited_quest_condition,
        function_template=submited_function_template,
        unit_tests=submited_quest_unit_tests,
        test_inputs=submited_quest_inputs,
        test_outputs=submited_quest_outputs,
        xp=str(xp),
        type=type
    )
    db.session.add(new_quest)
    # db.session.delete(submited_quest) Instead of delete, change the status to 'Approved' and disable the buttons for Approve/Request Changes
    db.session.commit()
    print("Quest was submitted successfully!")
    return redirect(url_for('open_admin_panel'))


# Post new comment in comments sections
@login_required
@app.route('/post_comment', methods=['POST'])
def post_comment():
    submited_quest_id = request.form['submited_quest_id']
    all_comments = eval(request.form['submited_quest_comments'])
    comment = request.form['submited_quest_comment']
    user_id = current_user.user_id
    username = current_user.username
    
    print(all_comments)
    
    # Get the current time
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    created_at = current_time
    
    current_quest = SubmitedQuest.query.filter_by(quest_id=submited_quest_id).first()
    data = {'username': username, 'user_id': user_id, 'posted_at': created_at, 'comment': comment}
    all_comments.append(data)
    current_quest.comments = all_comments
    print(current_quest.comments)
    
    db.session.commit()
    
    return render_template('edit_submited_quest.html', submited_quest=current_quest)