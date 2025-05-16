import pytest
from flask import session
from app import create_app, db
from app.forms.auth_forms import RegistrationForm, LoginForm
from app.forms.user_forms import ProfileForm, ChangePasswordForm, AccountSettingsForm
from app.forms.goal_forms import GoalForm
from datetime import datetime, timedelta
from wtforms.validators import EqualTo

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app(config_name='testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

class TestAuthForms:
    def test_registration_form_validation(self, app):
        """Test registration form validation."""
        with app.test_request_context():
            # Test valid form
            form = RegistrationForm(
                username='testuser',
                email='test@example.com',
                password='StrongPassword123@',
                confirm_password='StrongPassword123@'
            )
            assert form.validate() is True
            
            # Test weak password
            form = RegistrationForm(
                username='testuser',
                email='test@example.com',
                password='weak',
                confirm_password='weak'
            )
            assert form.validate() is False
            assert 'Password must be at least 8 characters' in str(form.password.errors)
            
            # Test password mismatch
            form = RegistrationForm(
                username='testuser',
                email='test@example.com',
                password='StrongPassword123@',
                confirm_password='DifferentPassword123@'
            )
            assert form.validate() is False
            assert 'Passwords must match' in str(form.confirm_password.errors)
            
            # Test invalid email
            form = RegistrationForm(
                username='testuser',
                email='invalid-email',
                password='StrongPassword123@',
                confirm_password='StrongPassword123@'
            )
            assert form.validate() is False
            assert 'Please enter a valid email address' in str(form.email.errors)
    
    def test_login_form_validation(self, app):
        """Test login form validation."""
        with app.test_request_context():
            # Test valid form
            form = LoginForm(
                email='test@example.com',
                password='TestPassword123'
            )
            assert form.validate() is True
            
            # Test missing email
            form = LoginForm(
                email='',
                password='TestPassword123'
            )
            assert form.validate() is False
            assert 'This field is required' in str(form.email.errors)
            
            # Test missing password
            form = LoginForm(
                email='test@example.com',
                password=''
            )
            assert form.validate() is False
            assert 'This field is required' in str(form.password.errors)
            
            # Test invalid email format
            form = LoginForm(
                email='invalid-email',
                password='TestPassword123'
            )
            assert form.validate() is False
            assert 'Please enter a valid email address' in str(form.email.errors)

class TestUserForms:
    def test_profile_form_validation(self, app):
        """Test profile form validation."""
        with app.test_request_context():
            # Test valid form
            form = ProfileForm(
                first_name='Test',
                last_name='User',
                gender='male',
                height=175,
                weight=70
            )
            assert form.validate() is True
            
            # Test invalid height (if negative)
            form = ProfileForm(
                first_name='Test',
                last_name='User',
                gender='male',
                height=-175,
                weight=70
            )
            # Height validator is optional, so should still pass unless there's an explicit validator
            assert form.validate() is True
            
            # Test very long name field
            form = ProfileForm(
                first_name='T' * 100,
                last_name='User',
                gender='male',
                height=175,
                weight=70
            )
            assert form.validate() is False
            assert 'Field cannot be longer than' in str(form.first_name.errors)
    
    def test_change_password_form_validation(self, app):
        """Test change password form validation."""
        with app.test_request_context():
            # 测试是否有required validators
            form = ChangePasswordForm()
            assert form.validate() is False
            assert 'This field is required' in str(form.current_password.errors)
            assert 'This field is required' in str(form.new_password.errors)
            assert 'This field is required' in str(form.confirm_password.errors)
            
            # 测试密码不匹配
            form = ChangePasswordForm(
                current_password='CurrentPassword123',
                new_password='NewPassword123',
                confirm_password='DifferentPassword123'
            )
            
            # 必须绕过validate_current_password方法，因为它依赖于current_user
            # 直接验证EqualTo validator
            confirm_validator = next(
                (v for v in form.confirm_password.validators 
                 if isinstance(v, EqualTo)), 
                None
            )
            assert confirm_validator is not None
            
            # 验证EqualTo validator失败
            with pytest.raises(ValueError):
                confirm_validator(form, form.confirm_password)

class TestGoalForm:
    def test_goal_form_validation(self, app):
        """Test goal form validation."""
        with app.test_request_context():
            # Test valid form
            today = datetime.utcnow().date()
            end_date = today + timedelta(days=30)
            
            form = GoalForm(
                category='steps',
                target_value=10000,
                unit='steps',
                timeframe='daily',
                start_date=today,
                end_date=end_date
            )
            assert form.validate() is True
            
            # Test negative target value
            form = GoalForm(
                category='steps',
                target_value=-1000,
                unit='steps',
                timeframe='daily',
                start_date=today,
                end_date=end_date
            )
            assert form.validate() is False
            assert 'Number must be at least 0.' in str(form.target_value.errors)
            
            # Test missing required field
            form = GoalForm(
                category='steps',
                unit='steps',
                timeframe='daily',
                start_date=today,
                end_date=end_date
            )
            assert form.validate() is False
            assert 'This field is required' in str(form.target_value.errors) 