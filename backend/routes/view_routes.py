from flask import render_template


def init_view_routes(app):
    @app.route("/")
    @app.route("/index")
    def render_index_page():
        return render_template('index.html', title="Home")

    @app.route("/fitness")
    def render_fitness_page():
        return render_template('fitness/index.html', title="Fitness")

    @app.route("/finance")
    def render_finance_page():
        return render_template('finance/index.html', title="Fitness")
