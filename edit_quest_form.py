"""
This file handles the functionality for editing a quest from the Admin Panel.
- edit_quest_db function handles the form submission and updates the quest in the database.
- open_edit_quest route opens the quest for editing from the Admin Panel.
- edit_quest_form_bp is Blueprint which makes available the routes from the main app.
- the `ReportedQuest` class is the table which stores the reported quests from the users
"""

from __main__ import app, db
# from app import app, db # Use this instead of the above line for db migrations
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_login import login_required, current_user
import random, string
from sqlalchemy.dialects.postgresql import JSON
from admin_submit_quest import Quest
from sqlalchemy import ForeignKey

# Blueprint to handle opening of specific quest from the database fro editing
edit_quest_form_bp = Blueprint('open_edit_quest', __name__)


# The class which will store the reported quests from the users
class ReportedQuest(db.Model):
    __tablename__ = 'reported_quests'
    report_id = db.Column(db.String(20), primary_key=True)
    quest_id = db.Column(db.String(10), ForeignKey('coding_quests.quest_id'), nullable=False)
    report_status = db.Column(db.Enum('In Progress', 'Resolved', 'Not Resolved', name='repost_status'), nullable=False)
    report_user_id = db.Column(db.String(10), ForeignKey('users.user_id'), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    report_reason = db.Column(db.Text, nullable=True)
    admin_assigned = db.Column(db.String(10), ForeignKey('users.user_id'), nullable=True)

# Handle quest edit from the Admin Panel
@app.route('/edit_quest_db', methods=['GET', 'POST'])
def edit_quest_db():
    quest_id = request.form['quest_id']
    quest_name = request.form['quest_name']
    quest_language = request.form['quest_language']
    quest_difficulty = request.form['quest_difficulty']
    quest_condition = request.form['quest_condition']
    function_template = request.form['function_template']
    unit_tests = request.form['quest_unitests']
    input_tests = request.form['quest_test_inputs']
    output_tests = request.form['quest_test_outputs']
    
    quest = Quest.query.get(quest_id)
    reported_quest = ReportedQuest.query.get(quest_id)
    print(quest)
    print(reported_quest.report_status)
    if quest:
        quest.quest_name = quest_name
        quest.language = quest_language
        quest.difficulty = quest_difficulty
        quest.condition = quest_condition
        quest.function_template = function_template
        quest.unit_tests = unit_tests
        quest.input_tests = input_tests
        quest.output_tests = output_tests

        # If this is True it means that the user is editing a reported quest (there is a chosen radion button)
        if request.form.get('progress_option'):
            print(request.form.get('progress_option'))
            report_progress = request.form.get('progress_option')
            reported_quest.report_status = report_progress

            if report_progress == 'Resolved':
                db.session.delete(reported_quest)
        
        db.session.commit()
        
        return redirect(url_for('open_admin_panel'))
    else:
        return 'Quest not found!', 404


# Open Quest for editing from the Admin Panel
@login_required
@app.route('/edit_quest/<quest_id>')
def open_edit_quest(quest_id):
    # Retrieve the specific quest from the database, based on the quest_id
    quest = Quest.query.get(quest_id)
    return render_template('edit_quest.html', quest=quest)


# Open Reported Quest for editing from the Admin Panel
@login_required
@app.route('/edit_reported_quest/<quest_id>')
def open_edit_reported_quest(quest_id):
    quest = Quest.query.get(quest_id)
    reported_quest = ReportedQuest.query.get(quest_id)
    return render_template('edit_reported_quest.html', quest=quest, reported_quest=reported_quest)


# Route to handle `Report Quest` Button
@login_required
@app.route('/report_quest/<curr_quest_id>')
def report_quest(curr_quest_id):
    quest = Quest.query.get(curr_quest_id)
    
    # Generate random suffix
    suffix_length = 16
    suffix = ''.join(random.choices(string.digits, k=suffix_length))
    prefix = 'REP-'
    report_id = f"{prefix}{suffix}"
    # Construct quest ID
    while ReportedQuest.query.filter_by(report_id=report_id).first():
        # If it exists, generate a new submission_id
        suffix = ''.join(random.choices(string.digits, k=suffix_length))
        report_id = f"{prefix}{suffix}"
    
    # # Get the current time
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save the submission to the database
    new_reported_quest = ReportedQuest(
        quest_id=quest.quest_id,
        report_id=report_id,
        report_status = 'Not Resolved',
        report_user_id = current_user.user_id,
        report_reason = 'nothing for now',  # This needs to be changed
        admin_assigned = 'USR-751694'  # This needs to be changed
    )

    # Add the new submission to the database session
    db.session.add(new_reported_quest)
    db.session.commit()
    
    return redirect(url_for('open_curr_quest', quest_id=curr_quest_id))