import uuid
from extensions import db
from sqlalchemy.orm import relationship


class Boss(db.Model):
    __tablename__ = 'bosses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    boss_name = db.Column(db.String(100), nullable=False)
    boss_title = db.Column(db.String(100), nullable=False)
    boss_language = db.Column(db.String(50), nullable=False)
    boss_difficulty = db.Column(db.String(50), nullable=False)
    boss_specialty = db.Column(db.String(100), nullable=False)
    boss_description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __init__(self, boss_name, boss_title, boss_language, boss_difficulty, boss_specialty, boss_description=None):
        self.boss_name = boss_name
        self.boss_title = boss_title
        self.boss_language = boss_language
        self.boss_difficulty = boss_difficulty
        self.boss_specialty = boss_specialty
        self.boss_description = boss_description
    
    