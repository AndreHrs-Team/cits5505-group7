from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import os
from .config import TestConfig

class TestUI(unittest.TestCase):
    def setUp(self):
        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        self.base_url = TestConfig.BASE_URL
        
    def tearDown(self):
        self.driver.quit()

    def test_home_page_title(self):
        """Test if home page loads and has correct title"""
        self.driver.get(self.base_url)
        self.assertIn("Learning Platform", self.driver.title)

    def test_login_form(self):
        """Test login form presence and functionality"""
        self.driver.get(f"{self.base_url}/login")
        
        # Find login form elements
        email_input = self.driver.find_element(By.NAME, "admin@email.com")
        password_input = self.driver.find_element(By.NAME, "passworadmin123d")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        
        # Test login with test credentials
        email_input.send_keys(TestConfig.TEST_USER["email"])
        password_input.send_keys(TestConfig.TEST_USER["password"])
        submit_button.click()
        
        # Wait for redirect or error message
        WebDriverWait(self.driver, 10).until(
            EC.url_changes(f"{self.base_url}/login")
        )

if __name__ == "__main__":
    unittest.main()