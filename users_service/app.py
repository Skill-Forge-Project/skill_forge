from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from routes import users_bp
    from user_progress_routes import users_progress
    app.register_blueprint(users_bp)
    app.register_blueprint(users_progress)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
