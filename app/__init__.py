from flask import Flask, redirect, url_for, render_template, flash, jsonify
from config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required
from flask_socketio import SocketIO, emit, disconnect
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime, timedelta
# Import database instance
from app.database.db_init import db
from app.models import User


migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, manage_session=False, ping_timeout=10, ping_interval=5)
    csrf.init_app(app)
    
    # Apply ProxyFix to handle the reverse proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    
    # Import routes
    from app.routes import routes, user_routes, user_submited_solutions, quests_routes, user_submit_quest_routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(user_routes.bp_usr)
    app.register_blueprint(user_submit_quest_routes.bp_usq)
    app.register_blueprint(user_submited_solutions.bp_uss)
    app.register_blueprint(quests_routes.bp_qst)
    
    # Import websockets
    # Define ping timeout and ping interval (in seconds)
    # socketio = socketio(app, ping_timeout=10, ping_interval=5)
    from app.sockets import handle_connect, handle_disconnect, handle_status_update_request

    ########### Routes handling error codes responds ###########
    # Custom error handler for Unauthorized (404) error
    @app.errorhandler(401)
    def unauthorized_error(error):
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('main.login'))
    
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
        user = User.query.get(user_id)
        return user
    
    @app.route('/get_user_status/user_id')
    def get_user_status(user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return jsonify(status=user.user_online_status, last_logged_date=user.last_status_update.strftime('%d-%m-%Y %H:%M') if user.last_status_update else None)
        return jsonify(status='Offline', last_logged_date=None)
        
    return app
