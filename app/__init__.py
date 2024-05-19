from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt  # Password hashing

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    bcrypt = Bcrypt(app)
    
    from app import routes, models
    app.register_blueprint(routes.bp)
    
    return app
