import uuid
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from services import set_avatar


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_role = db.Column(db.String(50), nullable=False, default='User')
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_banned = db.Column(db.Boolean, default=False, nullable=False)
    banned_date = db.Column(db.DateTime, nullable=True)
    ban_reason = db.Column(db.String(120), default="", nullable=True)
    about_me = db.Column(db.Text, default="", nullable=True)
    user_online_status = db.Column(db.String(10), default="Offline", nullable=True)
    last_seen_date = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    
    # Gamification fields
    xp_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    rank = db.Column(db.String(50), default='Novice')
    
    # Quests fields
    total_solved_quests = db.Column(db.Integer, default=0, nullable=False)
    total_python_quests = db.Column(db.Integer, default=0, nullable=False)
    total_java_quests = db.Column(db.Integer, default=0, nullable=False)
    total_javascript_quests = db.Column(db.Integer, default=0, nullable=False)
    total_csharp_quests = db.Column(db.Integer, default=0, nullable=False)
    total_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_approved_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_rejected_submited_quests = db.Column(db.Integer, default=0, nullable=False)
    total_pending_submited_quests = db.Column(db.Integer, default=0, nullable=False)

    # Social media fields
    facebook_profile = db.Column(db.String(120), default="", nullable=True)
    instagram_profile = db.Column(db.String(120), default="", nullable=True)
    github_profile = db.Column(db.String(120), default="", nullable=True)
    discord_id = db.Column(db.String(120), default="", nullable=True)
    linked_in = db.Column(db.String(120), default="", nullable=True)

    def __init__(self, username, first_name, last_name, email, password, avatar=set_avatar("assets/img/quest_approved.png")):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.avatar = avatar

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_avatar(self, avatar):
        self.avatar = avatar