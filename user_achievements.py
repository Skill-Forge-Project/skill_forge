'''
 - This file handles the User achievemnts functionality.
 - class:Achievement - This class is used to define the Achievement model.
 - class:UserAchievement - This class is used to define the UserAchievement model to track achievements earned by users.
'''

from __main__ import app, db
# from app import db # Use this instead of the above line for db migrations
from datetime import datetime
from sqlalchemy.orm import relationship


# Define the Achievement model
class Achievement(db.Model):
    __tablename__ = 'achievements'
    achievement_id = db.Column(db.String(100), primary_key=True)
    achievement_name = db.Column(db.String(100), unique=True, nullable=False)
    achievement_description = db.Column(db.String(255), nullable=False)
    achievement_picture = db.Column(db.String(40), nullable=False)
    language = db.Column(db.String(100), nullable=True)
    quests_number_required = db.Column(db.Integer, nullable=True)
    
    # Define the relationship with the UserAchievement model
    user_achievements = relationship("UserAchievement", back_populates="achievement")

# Define the UserAchievement model to track achievements earned by users
class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_achievement_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(100),nullable=False)
    achievement_id = db.Column(db.String(100), db.ForeignKey('achievements.achievement_id'), nullable=False)
    earned_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # Define the relationship with the Achievement model
    achievement = relationship("Achievement", back_populates="user_achievements")