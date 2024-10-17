import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Automatically manage the ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.base_url = "http://localhost:8000"  # Ensure this is correct

 


    def test_admin_successful_login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login/")

        try:
            username = driver.find_element(By.NAME, "username")
            password = driver.find_element(By.NAME, "password")
            submit = driver.find_element(By.XPATH, "//button[@type='submit']")

            username.send_keys("tansya")  # Admin username
            password.send_keys("tansya@23")  # Admin password
            submit.click()

            # Wait for and verify successful admin login
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Admin Dashboard')]"))
            )
            self.assertIn("Admin Dashboard", driver.title)
            logger.info("Admin login test passed.")
        except Exception as e:
            logger.error(f"Error in test_admin_successful_login: {str(e)}")
            self.fail(f"Test failed: {str(e)}")
            
            

    def test_theatre_owner_successful_login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login/")

        try:
            username = driver.find_element(By.NAME, "username")
            password = driver.find_element(By.NAME, "password")
            submit = driver.find_element(By.XPATH, "//button[@type='submit']")

            username.send_keys("AlexThomas")  # Theatre owner username
            password.send_keys("alex12")  # Theatre owner password
            submit.click()

            # Wait for and verify successful theatre owner login
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Theatre Owner Dashboard')]"))
            )
            self.assertIn("Theatre Owner Dashboard", driver.title)
            logger.info("Theatre owner login test passed.")
        except Exception as e:
            logger.error(f"Error in test_theatre_owner_successful_login: {str(e)}")
            self.fail(f"Test failed: {str(e)}")
            
            
            
    def test_user_successful_login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login/")

        try:
            username = driver.find_element(By.NAME, "username")
            password = driver.find_element(By.NAME, "password")
            submit = driver.find_element(By.XPATH, "//button[@type='submit']")

            username.send_keys("Sonu")  # Replace with a valid user username
            password.send_keys("sonu12")  # Replace with a valid user password
            submit.click()

            # Wait for and verify successful login
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'User Dashboard')]"))
            )
            self.assertIn("User Dashboard", driver.title)
            logger.info("User login test passed.")
        except Exception as e:
            logger.error(f"Error in test_user_successful_login: {str(e)}")
            self.fail(f"Test failed: {str(e)}")


    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()