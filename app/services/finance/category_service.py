from app import db
from app.models.finance.category import Category
from app.models.finance.transaction import Transaction
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.user import User

class CategoryService:
    @staticmethod
    def create_category(user_id, form):
        try:
            category = Category(
                user_id=None if form.is_global.data else user_id,
                type=form.type.data,
                name=form.name.data
            )
            db.session.add(category)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_category_stats(user_id, days=28):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return db.session.query(
            Category.id,
            Category.name,
            Category.type,
            func.sum(Transaction.amount).label('sum'),
            func.avg(Transaction.amount).label('avg'),
            func.max(Transaction.amount).label('max'),
            func.min(Transaction.amount).label('min')
        ).join(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date)
        ).group_by(Category.id).all()
    
    @staticmethod
    def get_user_categories(user_id):
        return Category.query.filter(
            (Category.user_id == user_id) | (Category.user_id == None)
        ).all()

    @staticmethod
    def update_category(category_id, user_id, form):
        try:
            category = Category.query.get(category_id)
            if not category:
                return False, "Category not found"
            
            # Check if user has permission to edit
            if category.user_id is None and not User.query.get(user_id).is_admin:
                return False, "You don't have permission to edit global categories"

            category.name = form.name.data
            category.type = form.type.data
            # Add this line to handle global category toggle
            category.user_id = None if form.is_global.data else user_id
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_category(category_id, user_id):
        try:
            category = Category.query.get(category_id)
            if not category:
                return False, "Category not found"
            
            # Check if user has permission to edit
            if category.user_id is None and not User.query.get(user_id).is_admin:
                return False, "You don't have permission to edit global categories"
            
            db.session.delete(category)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)