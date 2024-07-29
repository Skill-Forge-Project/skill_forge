
from flask import Flask, redirect, url_for, render_template, flash, jsonify
from config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required, login_user, user_loaded_from_header
from flask_socketio import SocketIO, emit, disconnect
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime, timedelta
# Import database instance
from app.database.db_init import db
from app.models import User
# Import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO(manage_session=True)
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, manage_session=False, ping_timeout=10, ping_interval=5, cors_allowed_origins="*", logger=True, engineio_logger=True)
    csrf.init_app(app)
    
    # Apply ProxyFix to handle the reverse proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    
    # Import routes
    from app.routes import routes, user_routes, user_submited_solutions, quests_routes, user_submit_quest_routes, guild_routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(user_routes.bp_usr)
    app.register_blueprint(user_submit_quest_routes.bp_usq)
    app.register_blueprint(user_submited_solutions.bp_uss)
    app.register_blueprint(quests_routes.bp_qst)
    app.register_blueprint(guild_routes.bp_guild)
    
    # Import websockets
    # Define ping timeout and ping interval (in seconds)
    # from app.sockets import handle_connect, handle_disconnect, handle_status_update_request

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
    
    @app.before_request
    def update_last_activity():
        if current_user.is_authenticated:
            current_user.last_status_update = datetime.now()
            if current_user.user_online_status != "Online":
                current_user.user_online_status = "Online"
        db.session.commit()
            
    def check_inactive_users():
        with app.app_context():
            timeout = datetime.now() - timedelta(seconds=5)
            inactive_users = User.query.filter(User.user_online_status == 'Online', User.last_status_update < timeout).all()
            for user in inactive_users:
                user.user_online_status = 'Offline'
                db.session.commit()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_inactive_users, trigger="interval", seconds=10)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
        
    return app
