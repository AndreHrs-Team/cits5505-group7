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
        return render_template('finance/finance_transaction.html', title="Finance - Transaction")

    @app.route("/finance/accounts")
    def render_finance_accounts_page():
        return render_template('finance/finance_accounts.html', title="Finance - Accounts")

    @app.route("/finance/categories")
    def render_finance_categories_page():
        return render_template('finance/finance_categories.html', title="Finance - Categories")

    @app.route("/finance/insight")
    def render_finance_insight_page():
        return render_template('finance/finance_insight.html', title="Finance - Insight")
