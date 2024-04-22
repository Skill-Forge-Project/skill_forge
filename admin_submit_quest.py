"""
This file handles the functionality for submiting a quest from the Admin Panel.
- Class:Quest is the model for the Quest table in the database.
- submit_quest function handles the form submission and updates the quest in the database.
"""



from __main__ import app, db
# from app import app, db # Use this instead of the above line for db migrations
from datetime import datetime
from flask import Blueprint, request, redirect, url_for
from sqlalchemy.dialects.postgresql import JSON
from flask_login import current_user, login_required
import random, string, base64

# Blueprint to handle posting new comment
quest_post_comment_bp = Blueprint('quest_post_comment', __name__)


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
    test_inputs = db.Column(db.Text, nullable=True)
    test_outputs = db.Column(db.Text, nullable=True)
    xp = db.Column(db.Enum('30', '60', '100', name='xp_points'), nullable=False)
    type = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    quest_comments = db.Column(JSON, default = [], nullable=True) # Store comments for the submited quests

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
    type = ''
    if request.form['quest_difficulty'] == 'Novice Quests':
        xp = 30
        type = 'Basic'
    elif request.form['quest_difficulty'] == 'Adventurous Challenges':
        xp = 60
        type = 'Basic'
    elif request.form['quest_difficulty'] == 'Epic Campaigns':
        xp = 100
        type = 'Basic'
    
    # Get the currently logged in user's username
    current_username = current_user.username
    
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a new Quest object
    new_quest = Quest(
        quest_id= quest_id,
        language=language,
        difficulty=difficulty,
        quest_name=quest_name,
        quest_author=current_username,
        date_added=current_time,
        last_modified=current_time,
        condition=quest_condition,
        function_template=function_template,
        unit_tests=unit_tests,
        test_inputs=quest_inputs,
        test_outputs=quest_outputs,
        type=type,
        xp=str(xp)
    )

    # Add the new quest to the database session
    db.session.add(new_quest)
    db.session.commit()

    # Redirect to a success page or main page
    return redirect(url_for('open_admin_panel'))



# Post new comment in comments sections
@login_required
@app.route('/quest_post_comment', methods=['POST'])
def quest_post_comment():
    quest_id = request.form['quest_id']
    all_quest_comments = eval(request.form['quest_comments'])
    comment = request.form['quest_comment']
    user_id = current_user.user_id
    user_role = current_user.user_role
    current_username = current_user.username
    user_avatar = base64.b64encode(current_user.avatar).decode('utf-8')
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Get the quest from the database
    quest = Quest.query.filter_by(quest_id=quest_id).first()
    
    # Append the new comment to the quest's comments list
    data = {
        'username': current_username,
        'user_id': user_id,
        'user_role': user_role,
        'user_avatar': user_avatar,
        'posted_at': current_time,
        'comment': comment
        }
    all_quest_comments.append(data)
    quest.quest_comments = all_quest_comments
    
    # Commit the changes to the database
    db.session.commit()
    
    # Redirect to the quest page
    return redirect(url_for('open_curr_quest', 
                            quest_id=quest.quest_id,
                            user_role=user_role,
                            user_avatar=user_avatar,
                            user_id=user_id))