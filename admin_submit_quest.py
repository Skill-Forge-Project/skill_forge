from __main__ import app, db
from datetime import datetime
from flask import request, redirect, url_for, render_template, session
from flask_login import login_required, current_user
import random, string



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