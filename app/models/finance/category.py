from datetime import datetime
from app import db


class Category(db.Model):
    __tablename__ = 'finance_categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # EXPENSE or INCOME
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), default='placeholder')
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # nullable for global categories
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    
    transactions = db.relationship('Transaction', back_populates='category')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'icon': self.icon,
            'user_id': self.user_id,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'deleted_at': int(self.updated_at.timestamp())
        }
