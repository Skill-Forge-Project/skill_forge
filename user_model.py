
# Define User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0, nullable=False)
    rank = db.Column(db.String(50), default='Novice Adventurer', nullable=False)
    
    # Class constuctor
    def __init__(self, username, first_name, last_name, password, email, xp, rank):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.xp = xp
        self.rank = rank
    
    # Get the user_ID
    def get_id(self):
        return str(self.id)
    
    # Print the User info
    def get_userinfo(self):
        return f'User {self.username}\nID: {self.id}\nEmail: {self.email}\nRank: {self.rank}\nXP: {self.xp}XP.'
