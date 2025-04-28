from flask import jsonify

def init_fitness_routes(app):
    @app.route("/api/v1/fitness")
    def get_fitnesses():
        return jsonify({"message": "Get all fitness"})

    @app.route("/api/v1/fitness/<int:user_id>")
    def get_fitness(user_id):
        return jsonify({"message": f"Get user {user_id}"})