from app import db
from app.models.finance.account import Account
from app.models.finance.transaction import Transaction

class AccountService:
    @staticmethod
    def delete_account(account_id, user_id):
        """Delete an account and all its associated transactions."""
        try:
            # Get the account
            account = Account.query.filter_by(id=account_id, user_id=user_id).first()
            if not account:
                return False, "Account not found"

            # Delete all associated transactions
            Transaction.query.filter_by(account_id=account_id).delete()

            # Delete the account
            db.session.delete(account)
            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, str(e) 