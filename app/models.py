import random
import string
import base64
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from app.database.db_init import db



########### Define the User model ###########
class User(UserMixin, db.Model):
    __tablename__ = 'users'        
    user_id = db.Column(db.String(10), primary_key=True)
    user_role = db.Column(Enum('User', 'Admin', name='user_role_enum'), default='User', nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    rank = db.Column(db.String(30), default="Novice Adventurer")
    avatar = db.Column(db.LargeBinary, default=None)
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(120), nullable=False)
    total_solved_quests = db.Column(db.Integer, default=0, nullable=False)
    total_python_quests = db.Column(db.Integer, default=0, nullable=False)
    total_java_quests = db.Column(db.Integer, default=0, nullable=False)
    total_javascript_quests = db.Column(db.Integer, default=0, nullable=False)
    total_csharp_quests = db.Column(db.Integer, default=0, nullable=False)
    total_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_approved_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_rejected_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_pending_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    facebook_profile = db.Column(db.String(120), default=" ")
    instagram_profile = db.Column(db.String(120), default=" ")
    github_profile = db.Column(db.String(120), default=" ")
    discord_id = db.Column(db.String(120), default=" ")
    linked_in = db.Column(db.String(120), default=" ")
    achievements = db.relationship('UserAchievement')
    is_banned = db.Column(db.Boolean, default=lambda: False)
    ban_date = db.Column(db.DateTime, nullable=True)
    ban_reason = db.Column(db.String(120), default=" ", nullable=True)
    user_online_status = db.Column(db.String(10), default="Offline", nullable=True)
    last_status_update = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)

    def __init__(self, username, first_name, last_name, password, email, avatar=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        if avatar is None:
            with open('./static/images/anvil.png', 'rb') as f:
                self.avatar = base64.b64encode(f.read())
        else:
            self.avatar = avatar
        self.generate_user_id()
        
    # Generate random UserID
    def generate_user_id(self):
        prefix = 'USR-'
        suffix_length = 6
        while True:
            suffix = ''.join(random.choices(string.digits, k=suffix_length))
            user_id = f"{prefix}{suffix}"
            if not User.query.filter_by(user_id=user_id).first():
                self.user_id = user_id
                break
    
    # Get the user_ID
    def get_id(self):
        return str(self.user_id)
    
    # Print the User info
    def get_userinfo(self):
        return f'User {self.username}\nID: {self.user_id}\nEmail: {self.email}\nRank: {self.rank}\nXP: {self.xp}XP.'


########### Define the model for reset password tokens ###########
class ResetToken(db.Model):
    __tablename__ = 'reset_tokens'
    user_id = db.Column(db.String(10), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(64), primary_key=True)
    expiration_time = db.Column(db.DateTime, nullable=False)
    
    

########### Define the Achievement model ###########
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

########### Define the UserAchievement model to track achievements earned by users ###########
class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_achievement_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(100),nullable=False)
    achievement_id = db.Column(db.String(100), db.ForeignKey('achievements.achievement_id'), nullable=False)
    earned_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # Define the relationship with the Achievement model
    achievement = relationship("Achievement", back_populates="user_achievements")



########### Define the Quest model ###########
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

########### Define the SubmitedQuest model - Quest submited by the user ###########
# Define the database table for the submitted quests
class SubmitedQuest(db.Model):
    __tablename__ = 'user_submited_quests'
    quest_id = db.Column(db.String(10), primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    quest_name = db.Column(db.String(255), nullable=False)
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
    comments=db.Column(JSON, default = [], nullable=True) # Store comments for the submited quests
    

########### Define the ReportedQuest model - Quest reported by the user ###########
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
    
    # Specify the foreign keys explicitly
    reported_quest = db.relationship("Quest", foreign_keys=[quest_id], backref="reported_quests")
    user_reporter = db.relationship("User", foreign_keys=[report_user_id], backref="reported_quests")
    admin = db.relationship("User", foreign_keys=[admin_assigned], backref="assigned_reports")


########### Define the SubmitedSolution model - the submited quest solutions by the users ###########
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
