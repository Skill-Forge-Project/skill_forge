'''
This file handles the User achievemnts functionality.
'''

from __main__ import app, db
# from app import app, db # Use this instead of the above line for db migrations
from datetime import datetime
from flask import Blueprint, request, redirect, url_for
from sqlalchemy.dialects.postgresql import JSON
from flask_login import current_user, login_required
import random, string, base64


# Define the Achievement model
class Achievement(db.Model):
    __tablename__ = 'achievements'
    achievement_id = db.Column(db.String(100), primary_key=True)
    achievement_name = db.Column(db.String(100), unique=True, nullable=False)
    achievement_description = db.Column(db.String(255), nullable=False)
    achievement_picture = db.Column(db.String(20), nullable=False)

# Define the UserAchievement model to track achievements earned by users
class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_achievement_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    username = db.Column(db.String(100),db.ForeignKey('user.username'),nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.achievement_id'), nullable=False)
    earned_on = db.Column(db.DateTime, nullable=False, default=datetime.now)