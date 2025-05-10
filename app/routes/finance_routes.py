from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app import db
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
    # Get all transactions for the user
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    # Get all accounts for the user
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    
    # Get all categories
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    # Calculate summary statistics
    total_income = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == current_user.id, Transaction.amount > 0)\
        .scalar() or 0
        
    total_expense = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == current_user.id, Transaction.amount < 0)\
        .scalar() or 0
        
    net_balance = total_income + total_expense
    
    return render_template(
        'finance/transactions.html.j2',
        transactions=transactions,
        accounts=accounts,
        categories=categories,
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance
    )

@bp.route('/account/adjust', methods=['PUT'])
@login_required
def create_adjustment_transaction():
    data = request.get_json()
    account_id = data.get('account_id')
    new_balance = data.get('new_balance')
    
    if not account_id or new_balance is None:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
    account = Account.query.filter_by(id=account_id, user_id=current_user.id).first()
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
        
    # Create adjustment transaction
    adjustment_amount = new_balance - account.balance
    transaction = Transaction(
        amount=adjustment_amount,
        description='Balance adjustment',
        account_id=account_id,
        user_id=current_user.id,
        date=datetime.utcnow()
    )
    
    # Update account balance
    account.balance = new_balance
    
    try:
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    success, error = TransactionService.delete_transaction(transaction_id, current_user.id)
    if success:
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    return jsonify({'error': error}), 400

@bp.route('/accounts', methods=['GET', 'POST'])
@login_required
def render_finance_accounts_page():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(
            name=form.name.data,
            balance=form.balance.data,
            currency=form.currency.data,
            user_id=current_user.id
        )
        try:
            db.session.add(account)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('finance.render_finance_accounts_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
    
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('finance/accounts.html.j2', form=form, accounts=accounts)

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
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        try:
            db.session.add(category)
            db.session.commit()
            flash('Category created successfully!', 'success')
            return redirect(url_for('finance.render_finance_categories_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating category: {str(e)}', 'error')
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('finance/categories.html.j2', form=form, categories=categories)

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
    return render_template('finance/finance_insight.html.j2')

