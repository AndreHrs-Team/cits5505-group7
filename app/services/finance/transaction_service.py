from app import db
from app.models.finance.account import Account
from app.models.finance.category import Category
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
        
    
    @staticmethod
    def get_category_insight(user_id, days=28):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        result = db.session.query(
            Transaction.type,
            Category.name.label('category'),
            func.sum(Transaction.amount).label('total'),
            func.avg(Transaction.amount).label('average'),
            func.count(Transaction.amount).label('count')
        ).join(Category).filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date),
            Category.user_id.is_(None)
        ).group_by(Transaction.type, Category.name).all()

        return result
    
    @staticmethod
    def get_timeline_data(user_id, days=28):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        results = db.session.query(
            func.date(Transaction.date).label('day'),
            Transaction.type,
            func.sum(Transaction.amount).label('total')
        ).join(Category).filter(
            Transaction.user_id == user_id,
            Category.user_id.is_(None),
            Transaction.date.between(start_date, end_date)
        ).group_by(func.date(Transaction.date), Transaction.type).order_by(func.date(Transaction.date)).all()

        # Organize data by type
        data = {'labels': [], 'EXPENSE': [], 'INCOME': []}
        date_map = {}

        for r in results:
            # Ensure we use proper string format
            if isinstance(r.day, str):
                day = r.day
            else:
                day = r.day.strftime('%Y-%m-%d')

            if day not in date_map:
                date_map[day] = {'EXPENSE': 0, 'INCOME': 0}
            date_map[day][r.type] = float(r.total)  # Ensure it's serializable

        for day in sorted(date_map.keys()):
            data['labels'].append(day)
            data['EXPENSE'].append(date_map[day]['EXPENSE'])
            data['INCOME'].append(date_map[day]['INCOME'])

        return data

