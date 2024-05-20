from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from app.database.db_init import db


migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from app.routes import routes, user_routes, user_submited_solutions, quests_routes, user_submit_quest_routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(user_routes.bp_usr)
    app.register_blueprint(user_submit_quest_routes.bp_usq)
    app.register_blueprint(user_submited_solutions.bp_uss)
    app.register_blueprint(quests_routes.bp_qst)

    with app.app_context():
        db.create_all()
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import inside the function
        return User.query.get(user_id)
    
    return app
