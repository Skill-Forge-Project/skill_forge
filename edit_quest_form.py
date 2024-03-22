"""
This file handles the functionality for editing a quest from the Admin Panel.
- edit_quest_db function handles the form submission and updates the quest in the database.
- open_edit_quest route opens the quest for editing from the Admin Panel.
- edit_quest_form_bp is Blueprint which makes available the routes from the main app.
"""

from __main__ import app, db
# from app import app, db # Use this instead of the above line for db migrations
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_login import login_required, current_user
import random, string
from admin_submit_quest import Quest
from user_submit_quest import SubmitedQuest

# Blueprint to handle opening of specific quest from the database fro editing
edit_quest_form_bp = Blueprint('open_edit_quest', __name__)


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
    print(quest)
    if quest:
        quest.quest_name = quest_name
        quest.language = quest_language
        quest.difficulty = quest_difficulty
        quest.condition = quest_condition
        quest.function_template = function_template
        quest.unit_tests = unit_tests
        quest.input_tests = input_tests
        quest.output_tests = output_tests
        
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