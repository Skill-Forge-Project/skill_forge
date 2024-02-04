
# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    # Get the user_ID
    def get_id(self):
        return str(self.id)
    
    # Print the User info
    def get_userinfo(self):
        return f'User {self.username}\nID: {self.id}\nEmail: {self.email}\nRank: {self.rank}\nXP: {self.xp}XP.'
