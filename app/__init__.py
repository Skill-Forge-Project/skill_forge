from flask import Flask, redirect, url_for, render_template
from config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
# Import database instance
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
    
    # Import sockets
    from app.sockets import handle_connect, handle_disconnect, handle_heartbeat, handle_request_user_status
    # Import routes
    from app.routes import routes, user_routes, user_submited_solutions, quests_routes, user_submit_quest_routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(user_routes.bp_usr)
    app.register_blueprint(user_submit_quest_routes.bp_usq)
    app.register_blueprint(user_submited_solutions.bp_uss)
    app.register_blueprint(quests_routes.bp_qst)

    ########### Routes handling error codes responds ###########
    # Custom error handler for Not Found (404) error
    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('not_found'))

    @app.route('/not_found')
    def not_found():
        return render_template('404.html')

    with app.app_context():
        db.create_all()
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(user_id)
    
    return app
