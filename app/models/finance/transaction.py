from datetime import datetime
from app import db
from datetime import datetime


class Transaction(db.Model):
    """Model for financial transactions."""
    __tablename__ = 'finance_transactions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # EXPENSE or INCOME
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'finance_accounts.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'finance_categories.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(255))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    account = db.relationship('Account', back_populates='transactions')
    category = db.relationship('Category', back_populates='transactions')
    user = db.relationship('User', backref=db.backref(
        'finance_transactions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'user_id': self.user_id,
            'account': self.account.to_dict(),
            'category': self.category.to_dict(),
            'account_id': self.account_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'date': int(self.date.timestamp()),
            'date_obj': self.date.strftime('%Y-%m-%dT%H:%M'),
            'title': self.title,
            'note': self.note,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp())
        }

    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount}>'