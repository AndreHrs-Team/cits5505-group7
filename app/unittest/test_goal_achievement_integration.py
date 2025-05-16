import pytest
from flask import session
from app import create_app, db
from app.models.user import User
from app.models.goal import Goal
from app.models.achievement import Achievement, UserAchievement
from app.models.activity import Activity
from app.models.weight import Weight
from app.services.goal_service import GoalService
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Create and configure Flask application for testing"""
    app = create_app(config_name='testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Return test client"""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create test user"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com', height=175)
        user.set_password('TestPassword123')
        db.session.add(user)
        db.session.commit()
        
        # Get user ID to avoid detached instance issues
        user_id = user.id
        db.session.expunge_all()
        
        # Return the user ID instead of the user object
        return user_id

class TestGoalAchievementIntegration:
    def test_goal_creation_with_steps(self, app, test_user):
        """Test goal creation and steps data addition"""
        with app.app_context():
            # Create a goal
            goal = Goal(
                user_id=test_user,
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now()
            )
            db.session.add(goal)
            db.session.commit()
            
            # Confirm goal exists
            assert goal.id is not None
            assert goal.completed is False
            
            # Add enough steps to complete the goal
            activity = Activity(
                user_id=test_user,
                activity_type='steps',
                value=10000,
                total_steps=10000,
                timestamp=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify goal is completed
            assert goal.completed is True
    
    def test_multiple_users_with_goals(self, app):
        """Test multi-user goal system"""
        with app.app_context():
            # Create two users
            user1 = User(username='user1', email='user1@example.com')
            user1.set_password('Password123')
            db.session.add(user1)
            
            user2 = User(username='user2', email='user2@example.com')
            user2.set_password('Password123')
            db.session.add(user2)
            db.session.commit()
            
            # Create goals for each user
            goal1 = Goal(
                user_id=user1.id,
                category='steps',
                target_value=8000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now()
            )
            db.session.add(goal1)
            
            goal2 = Goal(
                user_id=user2.id,
                category='weight',
                target_value=70,
                unit='kg',
                timeframe='monthly',
                start_date=datetime.now(),
                progress_related=True,
                progress_baseline=75.0
            )
            db.session.add(goal2)
            db.session.commit()
            
            # Add user1's steps data
            activity = Activity(
                user_id=user1.id,
                activity_type='steps',
                value=9000,
                total_steps=9000,
                timestamp=datetime.now()
            )
            db.session.add(activity)
            
            # Add user2's weight data
            weight = Weight(
                user_id=user2.id,
                value=70.0,
                timestamp=datetime.now()
            )
            db.session.add(weight)
            db.session.commit()
            
            # Update progress for both users' goals
            GoalService.update_goal_progress(goal1)
            GoalService.update_goal_progress(goal2)
            
            # Verify goal progress
            assert goal1.completed is True  # User1's steps goal is completed
            assert goal2.calculate_progress() == 100  # User2's weight goal has reached 100%