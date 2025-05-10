from flask import Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

api = Blueprint('api', __name__, url_prefix='/api')

# Remove or comment out the line below to break the circular import
# from . import auth_routes, data_routes, goal_routes, progress_routes, achievement_routes, share_routes, upload_routes, dashboard_routes

api = Blueprint('api', __name__, url_prefix='/api')

# Remove or comment out the line below to break the circular import
# from . import auth_routes, data_routes, goal_routes, progress_routes, achievement_routes, share_routes, upload_routes, dashboard_routes

db = SQLAlchemy()
migrate = Migrate()

# TODO: MOVE THE IMPORT PLACE FOR ROUTES
from app.models.education_event import EducationEvent
from app.routes.education_routes import bp as education_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main_bp, education_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(education_bp)

    return app


