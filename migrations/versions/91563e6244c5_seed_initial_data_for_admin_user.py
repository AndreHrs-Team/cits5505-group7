"""seed initial data for admin user

Revision ID: 91563e6244c5
Revises: 509845e4a9cb
Create Date: 2025-05-11 00:34:50.140187

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float, DateTime
import datetime


# revision identifiers, used by Alembic.
revision = '91563e6244c5'
down_revision = '509845e4a9cb'
branch_labels = None
depends_on = None

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

    accounts = [
        {
            "user_id": 1,
            "name": "Commbank",
            "type": "bank",
            "note": "",
            "balance": 100.0,
            "currency": "AUD",
            "created_at": now,
            "updated_at": now
        },
        {
            "user_id": 1,
            "name": "Visa Credit Card",
            "type": "credit",
            "note": "",
            "balance": 0.0,
            "currency": "AUD",
            "created_at": now,
            "updated_at": now
        },
        {
            "user_id": 1,
            "name": "Cash",
            "type": "wallet",
            "note": "",
            "balance": 100.0,
            "currency": "AUD",
            "created_at": now,
            "updated_at": now
        }
    ]

    op.bulk_insert(finance_accounts_table, accounts)


def downgrade():
    op.execute("""
        DELETE FROM finance_accounts
        WHERE user_id = 1
        AND name IN ('Commbank', 'Visa Credit Card', 'Cash')
    """)
