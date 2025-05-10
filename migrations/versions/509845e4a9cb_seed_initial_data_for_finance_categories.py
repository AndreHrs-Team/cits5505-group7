"""seed initial data for finance categories

Revision ID: 509845e4a9cb
Revises: aeb5db619f24
Create Date: 2025-05-11 00:33:45.766303

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean, Integer, DateTime, Text, Float
import datetime

# revision identifiers, used by Alembic.
revision = '509845e4a9cb'
down_revision = 'aeb5db619f24'
branch_labels = None
depends_on = None

# Define finance_categories table for use in op.bulk_insert
finance_categories_table = table('finance_categories',
    column('type', String),
    column('name', String),
    column('description', String),
    column('icon', String),
    column('user_id', Integer),
    column('created_at', DateTime),
    column('updated_at', DateTime),
)

def upgrade():
    now = datetime.datetime.utcnow()

    income_categories = [
        "Allowance",
        "Salary",
        "Cashback",
        "Bonus",
        "Other"
    ]

    expense_categories = [
        "Food",
        "Transportation",
        "Groceries",
        "Self Development",
        "Household",
        "Accomodation",
        "Apparel",
        "Beauty",
        "Health",
        "Education",
        "Gift",
        "Hobby",
        "Telephone Bill",
        "Entertainment",
        "Other"
    ]

    rows = []

    for name in income_categories:
        rows.append({
            "type": "INCOME",
            "name": name,
            "description": f"{name} income category",
            "icon": "placeholder",
            "user_id": None,
            "created_at": now,
            "updated_at": now,
        })

    for name in expense_categories:
        rows.append({
            "type": "EXPENSE",
            "name": name,
            "description": f"{name} expense category",
            "icon": "placeholder",
            "user_id": None,
            "created_at": now,
            "updated_at": now,
        })

    op.bulk_insert(finance_categories_table, rows)

def downgrade():
    op.execute("""
        DELETE FROM finance_categories
        WHERE user_id IS NULL
          AND name IN (
              'Allowance', 'Salary', 'Cashback', 'Bonus', 'Other',
              'Food', 'Transportation', 'Groceries', 'Self Development',
              'Household', 'Accomodation', 'Apparel', 'Beauty', 'Health',
              'Education', 'Gift', 'Hobby', 'Telephone Bill',
              'Entertainment'
          )
    """)