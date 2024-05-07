'''
This file handles the User achievemnts functionality.
'''

from __main__ import app, db
# from app import db # Use this instead of the above line for db migrations
from datetime import datetime
from flask import Blueprint, request, redirect, url_for
from sqlalchemy.dialects.postgresql import JSON
from flask_login import current_user, login_required
import random, string, base64


# BLueprint to handle the generate achievement functionality
generate_achievemnt_bp = Blueprint('generate_achievemnt', __name__)

# Define the Achievement model
class Achievement(db.Model):
    __tablename__ = 'achievements'
    achievement_id = db.Column(db.String(100), primary_key=True)
    achievement_name = db.Column(db.String(100), unique=True, nullable=False)
    achievement_description = db.Column(db.String(255), nullable=False)
    achievement_picture = db.Column(db.String(20), nullable=False)
    language = db.Column(db.String(100), nullable=True)
    quests_number_required = db.Column(db.Integer, nullable=True)

# Define the UserAchievement model to track achievements earned by users
class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_achievement_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(100),nullable=False)
    achievement_id = db.Column(db.String(100), db.ForeignKey('achievements.achievement_id'), nullable=False)
    earned_on = db.Column(db.DateTime, nullable=False, default=datetime.now)


# Generate achievements for the user
def generate_achievemnt(user_id, language, quest_nr):

    # Get the user's username
    username = current_user.username

    # Check if the achievement already exists
    achievement = Achievement.query.filter_by(Achievement.language==language, quest_nr==Achievement.points, ).all()
    
    db.session.add(achievement)
    db.session.commit()
    # Check if the user already has the achievement
    user_achievement = UserAchievement.query.filter_by(user_id=user_id, achievement_id=achievement.achievement_id).first()

    if not user_achievement:
        # Create the user achievement
        user_achievement = UserAchievement(user_achievement_id=base64.urlsafe_b64encode(f'{user_id}{achievement.achievement_id}'.encode()).decode().rstrip('='),
                                            user_id=user_id,
                                            username=username,
                                            achievement_id=achievement.achievement_id)
        db.session.add(user_achievement)
        db.session.commit()

    return user_achievement