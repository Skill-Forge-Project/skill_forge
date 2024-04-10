"""
This file handles the functionality for creating a new record when user submits his/her solution. 
All quests are stored in a single database table, and each solution has a unique ID.
No matter which language is the quest OR if the solution is correct, partially correct or incorrect, the solution is stored in the database.

- class: SubmitedSolution provides the structure for the database table and defines the columns and the rules for the table.
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

class SubmitedSolution(db.Model):
    __tablename__ = 'user_submited_solutions'
    submission_id = db.Column(db.String(20), primary_key=True) # Unique ID for each submission.
    quest_id = db.Column(db.String(20), db.ForeignKey('coding_quests.quest_id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_code = db.Column(db.Text, nullable=True)
    successful_tests = db.Column(db.Integer, default=0, nullable=True)
    unsuccessful_tests = db.Column(db.Integer, default=0, nullable=True)
    quest_passed = db.Column(db.Boolean, nullable=True)
