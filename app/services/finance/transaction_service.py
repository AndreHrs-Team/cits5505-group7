from app import db
from app.models.finance.account import Account
from app.models.finance.transaction import Transaction
from sqlalchemy import func
from datetime import datetime, timedelta

class TransactionService:
    @staticmethod
    def create_transaction(user_id, account, form):
        try:
            amount = form.amount.data
            if form.type.data == 'EXPENSE':
                account.balance -= amount
            else:
                account.balance += amount

            transaction = Transaction(
                user_id=user_id,
                type=form.type.data,
                account_id=form.account_id.data,
                category_id=form.category_id.data,
                amount=amount,
                date=form.date.data,
                title=form.title.data,
                note=form.note.data
            )
            
            db.session.add(transaction)
            db.session.commit()
            return True, account.balance
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_transaction_stats(user_id, days=28):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return db.session.query(
            Transaction.type,
            func.sum(Transaction.amount).label('sum'),
            func.avg(Transaction.amount).label('avg'),
            func.max(Transaction.amount).label('max'),
            func.min(Transaction.amount).label('min')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date)
        ).group_by(Transaction.type).all()
    

    @staticmethod
    def get_user_transactions(user_id):
        return Transaction.query.filter(
            (Transaction.user_id == user_id) | (Transaction.user_id == None)
        ).all()

    @staticmethod
    def update_transaction(transaction_id, user_id, account, form):
        try:
            transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
            if not transaction:
                return False, "Transaction not found"
            
            previous_amount = transaction.amount
            if form.type.data == 'EXPENSE':
                account.balance += previous_amount
            else:
                account.balance -= previous_amount

            amount = form.amount.data
            if form.type.data == 'EXPENSE':
                account.balance -= amount
            else:
                account.balance += amount

            transaction.user_id = user_id
            transaction.type = form.type.data
            transaction.account_id = form.account_id.data
            transaction.category_id = form.category_id.data
            transaction.amount = amount
            transaction.date = form.date.data
            transaction.title = form.title.data
            transaction.note = form.note.data
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_transaction(transaction_id, user_id):
        try:
            transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
            
            if not transaction:
                return False, "Transaction not found"
            
            account = Account.query.filter_by(id=transaction.account_id, user_id=user_id).first()
            
            previous_amount = transaction.amount
            if transaction.type == 'EXPENSE':
                account.balance += previous_amount
            else:
                account.balance -= previous_amount
            
            db.session.delete(transaction)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)