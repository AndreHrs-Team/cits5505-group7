from flask import jsonify

def init_user_routes(app):
    @app.route("/api/v1/users")
    def get_users():
        return jsonify({"message": "Get all users"})

    @app.route("/api/v1/users/<int:user_id>")
    def get_user(user_id):
        return jsonify({"message": f"Get user {user_id}"})