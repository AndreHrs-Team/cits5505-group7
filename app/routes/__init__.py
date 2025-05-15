import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'warning'


def create_app(config_object='config.Config'):
    """
    Application factory: create and configure the Flask app.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints
    from app.routes.main_routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.education_routes import bp as education_bp
    app.register_blueprint(education_bp)

    return app


# import models so Alembic can detect them
from app.models.education_event import EducationEvent
