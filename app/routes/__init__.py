import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# extensions
db = SQLAlchemy()
migrate = Migrate()

# (Optional) API blueprint placeholder
api_bp = Blueprint('api', __name__, url_prefix='/api')

def create_app(config_object='config.Config'):
    """
    Create and configure the Flask application.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_path = os.path.join(base_dir, '..', 'frontend', 'templates')
    static_path = os.path.join(base_dir, '..', 'frontend', 'static')

    app = Flask(
        __name__,
        template_folder=templates_path,
        static_folder=static_path
    )
    app.config.from_object(config_object)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.routes.education_routes import bp as education_bp
    app.register_blueprint(education_bp, url_prefix='/education')

    # if you have API routes, register api_bp here:
    # app.register_blueprint(api_bp)

    return app
