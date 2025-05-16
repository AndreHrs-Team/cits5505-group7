import multiprocessing
from app import create_app
from app.init_db import create_admin_user
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TEST_USER = {
        "email": "admin@example.com",
        "password": "admin@123"
    }
    USE_AUTO_GENERATION = True

class TestUI(unittest.TestCase):
    def setUp(self):
        try:
            logger.info("Setting up test environment...")
            self.base_url = "http://localhost:5000"
            self.testApp = create_app(TestConfig)
            self.app_context = self.testApp.app_context()
            self.app_context.push()

            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            # Remove headless mode for debugging
            # chrome_options.add_argument("--headless=new")

            logger.info("Initializing Chrome WebDriver...")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.driver.implicitly_wait(10)

            logger.info("Starting Flask server...")
            self.server_thread = multiprocessing.Process(
                target=self.testApp.run,
                kwargs={'port': 5000, 'debug': False}  # Added debug=False
            )
            print('Create admin user')
            create_admin_user()
            self.server_thread.start()
            time.sleep(2)  # Increased wait time
            logger.info("Setup complete!")
            
        except Exception as e:
            logger.error(f"Setup failed: {str(e)}")
            raise

    def tearDown(self):
        try:
            logger.info("Cleaning up test environment...")
            if hasattr(self, 'driver'):
                self.driver.quit()
            if hasattr(self, 'server_thread'):
                self.server_thread.terminate()
                self.server_thread.join()
            if hasattr(self, 'app_context'):
                self.app_context.pop()
            logger.info("Cleanup complete!")
        except Exception as e:
            logger.error(f"Error in tearDown: {str(e)}")
            raise
        
    def test_login_form(self):
        """Test login form presence and functionality"""
        try:
            logger.info("Testing login form...")
            self.driver.get(f"{self.base_url}/auth/login")
            
            # Find login form elements using correct IDs from the HTML
            email_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            logger.info("Found form elements, attempting to input credentials...")
            
            # Test login with test credentials
            email_input.clear()  # Clear any existing text
            email_input.send_keys(TestConfig.TEST_USER["email"])
            
            password_input.clear()  # Clear any existing text
            password_input.send_keys(TestConfig.TEST_USER["password"])
            
            logger.info("Clicking submit button...")
            submit_button.click()
            
            # Wait for redirect or error message
            logger.info("Waiting for redirect...")
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(f"{self.base_url}/auth/login")
            )
            logger.info("Login test completed successfully")
            
        except Exception as e:
            logger.error(f"Error in test_login_form: {str(e)}")
            raise

if __name__ == "__main__":
    unittest.main()