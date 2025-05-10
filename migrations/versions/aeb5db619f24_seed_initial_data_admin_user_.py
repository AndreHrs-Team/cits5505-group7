"""Seed initial data (admin user, achievements)

Revision ID: aeb5db619f24
Revises: 01e71d5b5eb0
Create Date: 2025-05-11 00:10:51.871582

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean, Integer, DateTime, Text, Float
import datetime
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = 'aeb5db619f24'
down_revision = '01e71d5b5eb0'
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

achievements_table = table('achievements',
    column('name', String),
    column('description', String),
    column('category', String),
    column('icon', String),
    column('level', String),
    column('condition_type', String),
    column('condition_value', Float),
    column('trigger_type', String),
    column('created_at', DateTime),
)


def upgrade():
    now = datetime.datetime.utcnow()

    # Seed admin user
    op.execute(
        users_table.insert().values(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin@123'),
            created_at=now,
            updated_at=now,
            last_login=None,
            is_active=True,
            is_admin=True,
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
    
    # Seed achievements
    achievements = [
        # Steps
        {"name": "First Steps", "description": "Record your first 1,000 steps", "category": "steps", "icon": "walking", "level": "bronze", "condition_type": "milestone", "condition_value": 1000, "trigger_type": "progress"},
        {"name": "Daily Walker", "description": "Reach 5,000 steps in a day", "category": "steps", "icon": "shoe-prints", "level": "silver", "condition_type": "milestone", "condition_value": 5000, "trigger_type": "progress"},
        {"name": "Power Walker", "description": "Reach 10,000 steps in a day", "category": "steps", "icon": "person-walking", "level": "gold", "condition_type": "milestone", "condition_value": 10000, "trigger_type": "progress"},
        
        # Weight
        {"name": "Weight Tracker", "description": "Record your first weight measurement", "category": "weight", "icon": "weight", "level": "bronze", "condition_type": "milestone", "condition_value": 1, "trigger_type": "progress"},
        {"name": "Weight Goal Setter", "description": "Set your first weight goal", "category": "weight", "icon": "bullseye", "level": "silver", "condition_type": "goal", "condition_value": 1, "trigger_type": "goal"},
        {"name": "Weight Goal Achiever", "description": "Achieve your first weight goal", "category": "weight", "icon": "trophy", "level": "gold", "condition_type": "goal", "condition_value": 1, "trigger_type": "goal"},
        
        # Heart Rate
        {"name": "Heart Monitor", "description": "Record your first heart rate measurement", "category": "heart_rate", "icon": "heart-pulse", "level": "bronze", "condition_type": "milestone", "condition_value": 1, "trigger_type": "progress"},
        {"name": "Heart Rate Explorer", "description": "Record heart rate for 7 consecutive days", "category": "heart_rate", "icon": "heart", "level": "silver", "condition_type": "streak", "condition_value": 7, "trigger_type": "progress"},
        {"name": "Heart Rate Master", "description": "Record heart rate for 30 consecutive days", "category": "heart_rate", "icon": "heart-circle", "level": "gold", "condition_type": "streak", "condition_value": 30, "trigger_type": "progress"},
        
        # Sleep
        {"name": "Sleep Tracker", "description": "Record your first sleep data", "category": "sleep", "icon": "moon", "level": "bronze", "condition_type": "milestone", "condition_value": 1, "trigger_type": "progress"},
        {"name": "Sleep Regular", "description": "Record sleep for 7 consecutive days", "category": "sleep", "icon": "bed", "level": "silver", "condition_type": "streak", "condition_value": 7, "trigger_type": "progress"},
        {"name": "Sleep Expert", "description": "Record sleep for 30 consecutive days", "category": "sleep", "icon": "stars", "level": "gold", "condition_type": "streak", "condition_value": 30, "trigger_type": "progress"},
        
        # General
        {"name": "Data Enthusiast", "description": "Record data in all categories (weight, heart rate, steps, sleep)", "category": "general", "icon": "chart-line", "level": "bronze", "condition_type": "milestone", "condition_value": 1, "trigger_type": "combined"},
        {"name": "Goal Setter", "description": "Set goals in all categories", "category": "general", "icon": "list-check", "level": "silver", "condition_type": "goal", "condition_value": 1, "trigger_type": "goal"},
        {"name": "Goal Master", "description": "Achieve goals in all categories", "category": "general", "icon": "crown", "level": "gold", "condition_type": "goal", "condition_value": 1, "trigger_type": "goal"},
    ]

    for item in achievements:
        item["created_at"] = now

    op.bulk_insert(achievements_table, achievements)

def downgrade():
    op.execute("DELETE FROM users WHERE username = 'admin'")
    
    names = [
        "First Steps", "Daily Walker", "Power Walker",
        "Weight Tracker", "Weight Goal Setter", "Weight Goal Achiever",
        "Heart Monitor", "Heart Rate Explorer", "Heart Rate Master",
        "Sleep Tracker", "Sleep Regular", "Sleep Expert",
        "Data Enthusiast", "Goal Setter", "Goal Master"
    ]
    formatted = "', '".join(names)
    op.execute(f"DELETE FROM achievements WHERE name IN ('{formatted}')")