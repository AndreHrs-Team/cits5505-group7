from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.utils.decorators import admin_required
from app.utils.cache_utils import invalidate_dashboard_cache

bp = Blueprint('finance', __name__, url_prefix='/finance')


@bp.route('/')
@login_required
def render_finance_page():
    return render_template('finance/finance_transaction.html', title="Finance - Transaction")


@bp.route('/accounts')
@login_required
def render_finance_accounts_page():
    return render_template('finance/finance_accounts.html', title="Finance - Accounts")


@bp.route('/categories')
@login_required
def render_finance_categories_page():
    return render_template('finance/finance_categories.html', title="Finance - Categories")


@bp.route('/insight')
@login_required
def render_finance_insight_page():
    return render_template('finance/finance_insight.html', title="Finance - Insight")
