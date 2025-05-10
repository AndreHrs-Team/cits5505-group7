from datetime import datetime
from app import db


class Account(db.Model):
    """Model for financial accounts."""
    __tablename__ = 'finance_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # bank, wallet, etc.
    note = db.Column(db.Text)
    balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relationships
    transactions = db.relationship('Transaction', back_populates='account')
    user = db.relationship('User', backref=db.backref(
        'finance_accounts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'note': self.note,
            'balance': self.balance,
            'currency': self.currency,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'deleted_at': int(self.updated_at.timestamp())
        }

    def __repr__(self):
        return f'<Account {self.name}>'