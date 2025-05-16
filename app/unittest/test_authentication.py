import pytest
from flask import session
from app import create_app, db
from app.models.user import User
from werkzeug.security import check_password_hash

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
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
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

class TestUserAuthentication:
    def test_register_user(self, client):
        """Test user registration with valid data."""
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123',
            'confirm_password': 'StrongPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # 测试成功注册后被重定向到登录页面
        assert b'Login - HealthTrack' in response.data
        
        # Verify user was added to database
        with client.application.app_context():
            user = User.query.filter_by(username='testuser').first()
            assert user is not None
            assert user.email == 'test@example.com'

    def test_register_validation(self, client):
        """Test validation during registration."""
        # Test with weak password
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'weak',
            'confirm_password': 'weak'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # 测试简单的密码验证 - 这取决于服务器端的实现
        
        # Test with mismatched passwords
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123',
            'confirm_password': 'DifferentPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Passwords do not match' in response.data
        
        # Test with existing username
        with client.application.app_context():
            user = User(username='existinguser', email='existing@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/auth/register', data={
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'StrongPassword123',
            'confirm_password': 'StrongPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Username or email already exists' in response.data

    def test_login_valid(self, client):
        """Test login with valid credentials."""
        # Create a test user
        with client.application.app_context():
            user = User(username='logintest', email='login@example.com')
            user.set_password('TestPassword123')
            db.session.add(user)
            db.session.commit()
        
        # Test login
        response = client.post('/auth/login', data={
            'email': 'login@example.com',
            'password': 'TestPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # 成功登录后会重定向到仪表板
        assert b'Dashboard - HealthTrack' in response.data
        
        # Check that user is logged in
        with client.session_transaction() as sess:
            assert '_user_id' in sess

    def test_login_invalid(self, client):
        """Test login with invalid credentials."""
        # Create a test user
        with client.application.app_context():
            user = User(username='logintest', email='login@example.com')
            user.set_password('TestPassword123')
            db.session.add(user)
            db.session.commit()
        
        # Test with incorrect password
        response = client.post('/auth/login', data={
            'email': 'login@example.com',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid email or password' in response.data
        
        # Test with non-existent user
        response = client.post('/auth/login', data={
            'email': 'nonexistent@example.com',
            'password': 'TestPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid email or password' in response.data

    def test_logout(self, client):
        """Test user logout."""
        # Create and login a test user
        with client.application.app_context():
            user = User(username='logouttest', email='logout@example.com')
            user.set_password('TestPassword123')
            db.session.add(user)
            db.session.commit()
        
        client.post('/auth/login', data={
            'email': 'logout@example.com',
            'password': 'TestPassword123'
        })
        
        # Test logout
        response = client.get('/auth/logout', follow_redirects=True)
        
        assert response.status_code == 200
        # 注销后重定向到登录页面
        assert b'Login - HealthTrack' in response.data
        
        # Verify session is cleared
        with client.session_transaction() as sess:
            assert '_user_id' not in sess

    def test_password_reset_request(self, client):
        """Test password reset request."""
        # Create a test user
        with client.application.app_context():
            user = User(username='resettest', email='reset@example.com')
            user.set_password('TestPassword123')
            db.session.add(user)
            db.session.commit()
        
        # Test password reset request
        response = client.post('/auth/reset_password_request', data={
            'email': 'reset@example.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # 请求重置密码后会显示一个消息并重定向到登录页面
        assert b'Login - HealthTrack' in response.data
        
        # Test with non-existent email
        response = client.post('/auth/reset_password_request', data={
            'email': 'nonexistent@example.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should not reveal if email exists or not for security
        assert b'Login - HealthTrack' in response.data

    def test_protected_routes(self, client):
        """Test access to protected routes."""
        # Try to access a protected route without login
        response = client.get('/dashboard', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please log in to access this page' in response.data
        
        # Login and try again
        with client.application.app_context():
            user = User(username='protectedtest', email='protected@example.com')
            user.set_password('TestPassword123')
            db.session.add(user)
            db.session.commit()
        
        client.post('/auth/login', data={
            'email': 'protected@example.com',
            'password': 'TestPassword123'
        })
        
        response = client.get('/dashboard', follow_redirects=True)
        assert response.status_code == 200
        # Should now have access to the dashboard content
        assert b'Dashboard - HealthTrack' in response.data 