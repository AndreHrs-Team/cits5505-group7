from flask import jsonify, request
from controllers.user_controller import create_user


def init_user_routes(app):
    @app.route("/api/v1/users")
    def get_users():
        return jsonify({"message": "Get all users"})

    @app.route("/api/v1/users/<int:user_id>")
    def get_user(user_id):
        return jsonify({"message": f"Get user {user_id}"})

    @app.route("/api/v1/users", methods=['POST'])
    def create_new_user():
        data = request.get_json()
        try:
            user = create_user(data)
            return jsonify({
                "message": "User created successfully",
                "user_id": user.student_id
            }), 201
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 400
