from flask import jsonify

from .fitness import init_fitness_routes
from .users import init_user_routes


def init_api_routes(app):
    @app.route("/api/v1/heartbeat/ping")
    def heart_beat():
        return jsonify({"message": "pong!"})
    
    init_fitness_routes(app)
    init_user_routes(app)