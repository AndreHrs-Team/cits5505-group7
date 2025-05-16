from flask import flash, redirect, url_for, render_template
from app.forms.finance_forms import TransactionForm
from app.services.finance.transaction_service import TransactionService
from app.models.finance.account import Account
from app.models.finance.category import Category

class TransactionController:
    @staticmethod
    def handle_transaction_page(current_user, form=None):
        accounts = Account.query.filter_by(user_id=current_user.id).all()
        categories = Category.query.filter(
            (Category.user_id == current_user.id) | (Category.user_id == None)
        ).all()

        if form is None:
            form = TransactionForm()
        
        # Always set the choices
        form.account_id.choices = [(account.id, account.name) for account in accounts]
        form.category_id.choices = [(category.id, category.name) for category in categories]

        if form.validate_on_submit():
            account = Account.query.get(form.account_id.data)
            if not account:
                flash('Account not found!', 'error')
                return redirect(url_for('finance.render_finance_page'))

            # Check if this is an edit (has ID) or new transaction
            if form.id.data:
                success, result = TransactionService.update_transaction(
                    form.id.data, current_user.id, account, form)
                flash_message = 'Transaction updated successfully!' if success else f'Error updating transaction: {result}'
            else:
                success, result = TransactionService.create_transaction(
                    current_user.id, account, form)
                if success:
                    if result < 0:
                        flash_message = f'Warning: {account.name} has a negative balance of {result:.2f}. Please check your transactions.'
                    else:
                        flash_message = 'Transaction created successfully!'
                else:
                    flash_message = f'Error creating transaction: {result}'

            flash(flash_message, 'success' if success else 'error')
            return redirect(url_for('finance.render_finance_page'))

        # Get transactions for data table
        transactions = TransactionService.get_user_transactions(current_user.id)
        
        # Get chart data
        transaction_stats = TransactionService.get_transaction_stats(current_user.id)
        chart_data = TransactionController._prepare_chart_data(transaction_stats)
        categories_dict = {c.id: c for c in categories}
        accounts_dict = {a.id: a for a in accounts}
        
        return render_template('finance/finance_transaction.html.j2',
                            form=form,
                            categories_dict=categories_dict,
                            accounts_dict=accounts_dict,
                            transactions=transactions,
                            chart_data=chart_data)

    @staticmethod
    def _prepare_chart_data(transaction_stats):
        types = ['EXPENSE', 'INCOME']
        return {
            'labels': types,
            'sum': [next((stat.sum for stat in transaction_stats if stat.type == type), 0) 
                   for type in types],
            'avg': [next((stat.avg for stat in transaction_stats if stat.type == type), 0) 
                   for type in types],
            'max': [next((stat.max for stat in transaction_stats if stat.type == type), 0) 
                   for type in types],
            'min': [next((stat.min for stat in transaction_stats if stat.type == type), 0) 
                   for type in types],
            'x_label': 'Transaction Types',
            'title': 'Transaction Summary (Last 28 Days)'
        }
    

    @staticmethod
    def handle_insight_page(current_user):
        insight_data = TransactionService.get_category_insight(current_user.id)
        timeline_data = TransactionService.get_timeline_data(current_user.id)

        insight = {'EXPENSE': [], 'INCOME': []}
        for row in insight_data:
            insight[row.type].append({
                'category': row.category,
                'total': round(row.total, 2),
                'average': round(row.average, 2),
                'count': row.count
            })

        return render_template('finance/finance_insight.html.j2',
                            insight=insight,
                            timeline_data=timeline_data)
