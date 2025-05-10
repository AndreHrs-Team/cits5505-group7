from flask import flash, redirect, url_for, render_template
from app.forms.finance_forms import AccountForm
from app.services.finance.account_service import AccountService
from app.models.finance.account import Account

class AccountController:
    @staticmethod
    def handle_accounts_page(current_user, form=None):
        if form is None:
            form = AccountForm()

        # Get accounts for data table
        accounts = AccountService.get_user_accounts(current_user.id)

        if form.validate_on_submit():
            if form.id.data:  # Edit mode
                success, error = AccountService.update_account(form.id.data, current_user.id, form)
                flash_message = 'Account updated successfully!' if success else f'Error updating account: {error}'
            else:  # Create mode
                success, error = AccountService.create_account(current_user.id, form)
                flash_message = 'Account created successfully!' if success else f'Error creating account: {error}'
            
            flash(flash_message, 'success' if success else 'error')
            return redirect(url_for('finance.render_finance_accounts_page'))

        # Get chart data
        account_stats = AccountService.get_account_stats(current_user.id)
        
        chart_data = AccountController._prepare_chart_data(accounts, account_stats)
        return render_template('finance/finance_accounts.html.j2', 
                        form=form, 
                        chart_data=chart_data,
                        accounts=accounts)

    @staticmethod
    def _prepare_chart_data(accounts, account_stats):
        return {
            'labels': [account.name for account in accounts],
            'sum': [next((stat.sum for stat in account_stats if stat.account_id == account.id), 0) 
                   for account in accounts],
            'avg': [next((stat.avg for stat in account_stats if stat.account_id == account.id), 0) 
                   for account in accounts],
            'max': [next((stat.max for stat in account_stats if stat.account_id == account.id), 0) 
                   for account in accounts],
            'min': [next((stat.min for stat in account_stats if stat.account_id == account.id), 0) 
                   for account in accounts],
            'x_label': 'Accounts',
            'title': 'Account Activity (Last 28 Days)'
        }