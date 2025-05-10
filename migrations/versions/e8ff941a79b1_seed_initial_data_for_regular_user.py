"""seed initial data for regular user

Revision ID: e8ff941a79b1
Revises: 91563e6244c5
Create Date: 2025-05-11 00:34:56.596798

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean, Integer, DateTime, Text, Float
import datetime
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = 'e8ff941a79b1'
down_revision = '91563e6244c5'
branch_labels = None
depends_on = None

users_table = table('users',
    column('id', Integer),
    column('username', String),
    column('email', String),
    column('password_hash', String),
    column('created_at', DateTime),
    column('updated_at', DateTime),
    column('last_login', DateTime),
    column('is_active', Boolean),
    column('is_admin', Boolean),
    column('first_name', String),
    column('last_name', String),
    column('gender', String),
    column('birth_date', DateTime),
    column('height', Float),
    column('weight', Float),
    column('default_share_privacy', String),
    column('default_share_modules', Text),
    column('default_share_template', String),
    column('default_share_expiry', Integer),
)

finance_accounts_table = table('finance_accounts',
    column('user_id', Integer),
    column('name', String),
    column('type', String),
    column('note', String),
    column('balance', Float),
    column('currency', String),
    column('created_at', DateTime),
    column('updated_at', DateTime),
)

def upgrade():
    now = datetime.datetime.utcnow()

    # Seed regular user
    op.execute(
        users_table.insert().values(
            id=2,
            username='user',
            email='user@example.com',
            password_hash=generate_password_hash('user@123'),
            created_at=now,
            updated_at=now,
            last_login=None,
            is_active=True,
            is_admin=False,
            first_name=None,
            last_name=None,
            gender=None,
            birth_date=None,
            height=None,
            weight=None,
            default_share_privacy='overview',
            default_share_modules='["dashboard","heartrate","activity","weight","sleep","goals","achievements"]',
            default_share_template='social',
            default_share_expiry=7
        )
    )

    # Seed finance accounts
    accounts = [
        {
            "user_id": 2,
            "name": "NAB",
            "type": "bank",
            "note": "",
            "balance": 100.0,
            "currency": "AUD",
            "created_at": now,
            "updated_at": now
        },
        {
            "user_id": 2,
            "name": "Mastercard CC",
            "type": "credit",
            "note": "",
            "balance": 0.0,
            "currency": "AUD",
            "created_at": now,
            "updated_at": now
        },
        {
            "user_id": 2,
            "name": "Cash",
            "type": "wallet",
            "note": "",
            "balance": 300.0,
            "currency": "AUD",
            "created_at": now,
            "updated_at": now
        }
    ]

    op.bulk_insert(finance_accounts_table, accounts)


def downgrade():
    op.execute("DELETE FROM users WHERE username = 'user'")
    op.execute("""
        DELETE FROM finance_accounts
        WHERE user_id = 2
        AND name IN ('NAB', 'Mastercard CC', 'Cash')
    """)
    
