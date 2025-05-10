from app import db
from app.models.finance.transaction import Transaction
from app.models.finance.account import Account

class TransactionService:
    @staticmethod
    def delete_transaction(transaction_id, user_id):
        """Delete a transaction and update the account balance."""
        try:
            # Get the transaction
            transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
            if not transaction:
                return False, "Transaction not found"

            # Get the associated account
            account = Account.query.filter_by(id=transaction.account_id, user_id=user_id).first()
            if not account:
                return False, "Associated account not found"

            # Update account balance
            account.balance -= transaction.amount

            # Delete the transaction
            db.session.delete(transaction)
            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, str(e) 