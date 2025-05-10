from app import db
from app.models.finance.account import Account
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.finance.transaction import Transaction

class AccountService:
    @staticmethod
    def create_account(user_id, form):
        try:
            account = Account(
                user_id=user_id,
                name=form.name.data,
                type=form.type.data,
                balance=form.balance.data,
                note=form.note.data
            )
            db.session.add(account)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_account_stats(user_id, days=28):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        return db.session.query(
            Transaction.account_id,
            func.sum(Transaction.amount).label('sum'),
            func.avg(Transaction.amount).label('avg'),
            func.max(Transaction.amount).label('max'),
            func.min(Transaction.amount).label('min')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date)
        ).group_by(Transaction.account_id).all()

    @staticmethod
    def get_user_accounts(user_id):
        return Account.query.filter_by(
            user_id=user_id,
            deleted_at=None
        ).all()

    @staticmethod
    def update_account(account_id, user_id, form):
        try:
            account = Account.query.filter_by(id=account_id,
                user_id=user_id,
                deleted_at=None).first()
            if not account:
                return False, "Account not found"

            account.name = form.name.data
            account.type = form.type.data
            account.note = form.note.data
            account.balance = form.balance.data

            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_account(account_id, user_id):
        try:
            account = Account.query.filter_by(
                id=account_id,
                user_id=user_id,
                deleted_at=None
            ).first()

            if not account:
                return False, "Account not found"

            account.deleted_at = datetime.now()
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)