import random
import string
import base64
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
from app import db


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

    # Class constuctor
    def __init__(self, username, first_name, last_name, password, email, avatar=base64.b64encode(open('static/images/anvil.png', 'rb').read())):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
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