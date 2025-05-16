from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app import db
from app.controllers.finance.account_controller import AccountController
from app.controllers.finance.category_controller import CategoryController
from app.controllers.finance.transaction_controller import TransactionController
from app.forms.finance_forms import AccountForm, CategoryForm, TransactionForm
from app.models.finance.account import Account
from app.models.finance.category import Category
from app.models.finance.transaction import Transaction
from app.services.finance.account_service import AccountService
from app.services.finance.category_service import CategoryService
from app.services.finance.transaction_service import TransactionService
from app.utils.decorators import admin_required
from app.utils.cache_utils import invalidate_dashboard_cache
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('finance', __name__, url_prefix='/finance')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def render_finance_page():
    return TransactionController.handle_transaction_page(current_user)

@bp.route('/account/adjust', methods=['PUT'])
@login_required
def create_adjustment_transaction():
    data = request.get_json()
    success, result = AccountController.handle_balance_adjustment(current_user, data)

    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': result}), 400

@bp.route('/transactions/<int:transacction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transacction_id):
    success, error = TransactionService.delete_transaction(transacction_id, current_user.id)
    if success:
        return jsonify({'message': 'Account deleted successfully'}), 200
    return jsonify({'error': error}), 400

@bp.route('/accounts', methods=['GET', 'POST'])
@login_required
def render_finance_accounts_page():
    return AccountController.handle_accounts_page(current_user)

@bp.route('/accounts/<int:account_id>', methods=['DELETE'])
@login_required
def delete_account(account_id):
    success, error = AccountService.delete_account(account_id, current_user.id)
    if success:
        return jsonify({'message': 'Account deleted successfully'}), 200
    return jsonify({'error': error}), 400

@bp.route('/categories', methods=['GET', 'POST'])
@login_required
def render_finance_categories_page():
    return CategoryController.handle_categories_page(current_user)

@bp.route('/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    success, error = CategoryService.delete_category(category_id, current_user.id)
    if success:
        return jsonify({'message': 'Category deleted successfully'}), 200
    return jsonify({'error': error}), 400

@bp.route('/insight')
@login_required
def render_finance_insight_page():
    return TransactionController.handle_insight_page(current_user)

