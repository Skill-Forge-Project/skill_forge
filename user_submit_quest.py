from __main__ import app, db
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_login import login_required, current_user
import random, string
from app import User


# Define the database table for the submitted quests
class SubmitedQuest(db.Model):
    __tablename__ = 'user_submited_quests'
    quest_id = db.Column(db.String(10), primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    quest_name = db.Column(db.String(255), nullable=False)
    # solved_times = db.Column(db.Integer, default=0, nullable=True)
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
    logged_user_id = current_user.user_id
    logged_username = current_user.username
    print(logged_user_id)
    print(logged_username)
    
    # Create a new Quest object
    new_user_submitted_quest = SubmitedQuest(
        quest_id= quest_id,
        language=language,
        difficulty=difficulty,
        quest_name=quest_name,
        quest_author=logged_username, 
        quest_author_id=logged_user_id,
        status='Pending', # Default status is 'Pending
        date_added=datetime.now(),
        last_modified=datetime.now(),
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