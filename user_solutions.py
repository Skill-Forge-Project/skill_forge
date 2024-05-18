"""
This file handles the functionality for creating a new record when user submits his/her solution. 
All quests are stored in a single database table, and each solution has a unique ID.
No matter which language is the quest OR if the solution is correct, partially correct or incorrect, the solution is stored in the database.

- class: SubmitedSolution provides the structure for the database table and defines the columns and the rules for the table.
- coding_quets inits the relantionship with the Quest table(coding_quests).
"""


from __main__ import app, db
# from app import app, db # Use this instead of the above line for db migrations
from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from datetime import datetime

# Define the structure of the user_submited_solutions table.
class SubmitedSolution(db.Model):
    __tablename__ = 'user_submited_solutions'
    submission_id = db.Column(db.String(20), primary_key=True) # Unique ID for each submission.
    quest_id = db.Column(db.String(20), db.ForeignKey('coding_quests.quest_id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user_code = db.Column(db.Text, nullable=True)
    successful_tests = db.Column(db.Integer, default=0, nullable=True)
    unsuccessful_tests = db.Column(db.Integer, default=0, nullable=True)
    quest_passed = db.Column(db.Boolean, nullable=True)
    
    # Define the relationship between the user_submited_solutions and coding_quests table.
    coding_quest = db.relationship('Quest')


# Route to handle the view solution page.
@login_required
@app.route('/view_solution/<solution_id>', methods=['GET'])
def open_view_solution(solution_id):
    
    # Get the user's desired solution based on the solution_id
    user_solved_quest = SubmitedSolution.query.filter_by(submission_id=solution_id).options(joinedload(SubmitedSolution.coding_quest)).first()

    return render_template('view_solution.html', user_solved_quest=user_solved_quest)