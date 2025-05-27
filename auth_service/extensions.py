from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
