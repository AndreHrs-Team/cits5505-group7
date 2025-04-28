from .view_routes import init_view_routes
from .api_routes import init_api_routes

def init_routes(app):
    init_view_routes(app)
    init_api_routes(app)