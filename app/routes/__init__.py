from flask import Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

api = Blueprint('api', __name__, url_prefix='/api')

# Remove or comment out the line below to break the circular import
# from . import auth_routes, data_routes, goal_routes, progress_routes, achievement_routes, share_routes, upload_routes, dashboard_routes

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)  

    # register blueprints
    from app.routes import api
    app.register_blueprint(api)

    return app
