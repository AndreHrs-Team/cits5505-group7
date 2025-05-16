import pytest
from flask import session
from app import create_app, db
from app.models.user import User
from app.models.goal import Goal
from app.models.activity import Activity
from app.models.weight import Weight
from app.models.sleep import Sleep
from app.models.heart_rate import HeartRate
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

@pytest.fixture
def test_activities(app, test_user):
    """Create test activity data"""
    with app.app_context():
        # Create today's step records
        today = datetime.now()
        activity = Activity(
            user_id=test_user,  # Now test_user is just the ID
            activity_type='steps',
            value=8000,
            total_steps=8000,
            timestamp=today
        )
        db.session.add(activity)
        
        # Create yesterday's step records
        yesterday = today - timedelta(days=1)
        activity2 = Activity(
            user_id=test_user,  # Now test_user is just the ID
            activity_type='steps',
            value=6000,
            total_steps=6000,
            timestamp=yesterday
        )
        db.session.add(activity2)
        db.session.commit()
        return [activity, activity2]

@pytest.fixture
def test_weights(app, test_user):
    """Create test weight data"""
    with app.app_context():
        # Create initial weight record
        today = datetime.now()
        weight1 = Weight(
            user_id=test_user,  # Now test_user is just the ID
            value=75.0,
            timestamp=today - timedelta(days=30)
        )
        db.session.add(weight1)
        
        # Create latest weight record
        weight2 = Weight(
            user_id=test_user,  # Now test_user is just the ID
            value=70.0,
            timestamp=today
        )
        db.session.add(weight2)
        db.session.commit()
        
        # Get the values to avoid detached instance issues
        weight_values = [weight1.value, weight2.value]
        db.session.expunge_all()
        
        return weight_values

@pytest.fixture
def authenticated_client(app, client, test_user):
    """Authenticate test client"""
    with app.app_context():
        # Get the user email based on the ID
        user = User.query.get(test_user)
        email = user.email
    
    # Login user
    client.post('/auth/login', data={
        'email': email,
        'password': 'TestPassword123'
    }, follow_redirects=True)
    
    return client

class TestGoalCreation:
    def test_create_steps_goal(self, app, test_user):
        """Test creating steps goal"""
        with app.app_context():
            # Create steps goal
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30)
            )
            db.session.add(goal)
            db.session.commit()
            
            # Verify goal has been created
            assert goal.id is not None
            assert goal.category == 'steps'
            assert goal.target_value == 10000
            assert goal.unit == 'steps'
            
            # Verify goal exists in database
            db_goal = Goal.query.get(goal.id)
            assert db_goal is not None
            assert db_goal.user_id == test_user
    
    def test_create_weight_goal(self, app, test_user, test_weights):
        """Test creating weight goal"""
        with app.app_context():
            # Create weight loss goal
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='weight',
                target_value=65.0,
                unit='kg',
                timeframe='monthly',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=60),
                progress_related=True,
                progress_baseline=test_weights[1]  # Use the value directly, not the object
            )
            db.session.add(goal)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify goal has been created
            assert goal.id is not None
            assert goal.category == 'weight'
            assert goal.target_value == 65.0
            assert goal.progress_baseline == 70.0  # Current weight set as baseline
            
            # Verify progress calculation
            # Current value should be the latest weight record
            assert goal.current_value == 70.0
            
            # Verify progress calculation (70 - 70) / (70 - 65) * 100 = 0%
            assert goal.calculate_progress() == 0
    
    def test_goal_api_routes(self, authenticated_client):
        """Test goal API routes"""
        # Access goal home page
        response = authenticated_client.get('/goals/')
        assert response.status_code == 200
        
        # Access create goal page
        response = authenticated_client.get('/goals/create')
        assert response.status_code == 200

class TestGoalProgress:
    def test_steps_goal_progress(self, app, test_user, test_activities):
        """Test steps goal progress update"""
        with app.app_context():
            # Create steps goal
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now()
            )
            db.session.add(goal)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify current value has been set
            assert goal.current_value == 8000  # Today's recorded steps
            
            # Verify progress calculation (8000 / 10000 * 100 = 80%)
            assert goal.calculate_progress() == 80
            
            # Goal not yet completed
            assert goal.completed is False
            
            # Add additional steps to complete the goal
            activity = Activity(
                user_id=test_user,  # Now test_user is just the ID
                activity_type='steps',
                value=3000,
                total_steps=3000,
                timestamp=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify current value has been updated
            assert goal.current_value == 11000  # Should be 8000 + 3000
            
            # Verify progress calculation (11000 / 10000 * 100 = 100%, but should be capped at 100%)
            assert goal.calculate_progress() == 100
            
            # Goal should be completed
            assert goal.completed is True
    
    def test_weight_goal_progress(self, app, test_user, test_weights):
        """Test weight goal progress update"""
        with app.app_context():
            # Create weight reduction goal (from 70kg to 65kg)
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='weight',
                target_value=65.0,
                unit='kg',
                timeframe='monthly',
                start_date=datetime.now(),
                progress_related=True,
                progress_baseline=70.0
            )
            db.session.add(goal)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify current value
            assert goal.current_value == 70.0
            assert goal.progress_baseline == 70.0
            
            # Verify initial progress (0%)
            assert goal.calculate_progress() == 0
            
            # Add new weight record (lost 2kg)
            new_weight = Weight(
                user_id=test_user,  # Now test_user is just the ID
                value=68.0,
                timestamp=datetime.now() + timedelta(days=1)
            )
            db.session.add(new_weight)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify current value has been updated
            assert goal.current_value == 68.0
            
            # Verify progress calculation ((70 - 68) / (70 - 65) * 100 = 40%)
            assert goal.calculate_progress() == 40
            
            # Add another weight record (reached target)
            final_weight = Weight(
                user_id=test_user,  # Now test_user is just the ID
                value=65.0,
                timestamp=datetime.now() + timedelta(days=2)
            )
            db.session.add(final_weight)
            db.session.commit()
            
            # Update goal progress
            GoalService.update_goal_progress(goal)
            
            # Verify current value has been updated
            assert goal.current_value == 65.0
            
            # Verify progress calculation ((70 - 65) / (70 - 65) * 100 = 100%)
            assert goal.calculate_progress() == 100
            
            # Goal should be completed
            assert goal.completed is True

class TestGoalManagement:
    def test_edit_goal(self, app, test_user):
        """Test editing a goal"""
        with app.app_context():
            # Create initial goal
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30)
            )
            db.session.add(goal)
            db.session.commit()
            
            # Edit goal
            original_id = goal.id
            goal.target_value = 12000
            goal.timeframe = 'weekly'
            goal.end_date = datetime.now() + timedelta(days=60)
            db.session.commit()
            
            # Verify goal has been updated
            updated_goal = Goal.query.get(original_id)
            assert updated_goal is not None
            assert updated_goal.target_value == 12000
            assert updated_goal.timeframe == 'weekly'
            assert (updated_goal.end_date - datetime.now()).days > 45  # About 60 days
    
    def test_delete_goal(self, app, test_user):
        """Test deleting a goal"""
        with app.app_context():
            # Create goal
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now()
            )
            db.session.add(goal)
            db.session.commit()
            
            goal_id = goal.id
            
            # Confirm goal exists
            assert Goal.query.get(goal_id) is not None
            
            # Delete goal
            db.session.delete(goal)
            db.session.commit()
            
            # Verify goal has been deleted
            assert Goal.query.get(goal_id) is None
    
    def test_goal_completion_date(self, app, test_user):
        """Test goal completion date"""
        with app.app_context():
            # Create goal
            goal = Goal(
                user_id=test_user,  # Now test_user is just the ID
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=datetime.now()
            )
            db.session.add(goal)
            db.session.commit()
            
            # Initially, goal is not completed
            assert goal.completed is False
            
            # Add enough steps to complete the goal
            activity = Activity(
                user_id=test_user,  # Now test_user is just the ID
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
            
            # Verify update date
            assert goal.updated_at is not None 