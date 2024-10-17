# test_register.py
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

class RegisterTest(unittest.TestCase):

    def setUp(self):
        # Automatically manage the ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.base_url = "http://localhost:8000"  # Ensure this is correct

    def test_successful_registration(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register/")  # Adjust this if necessary

        try:
            # Fill in the registration form
            driver.find_element(By.NAME, "username").send_keys("Sonu")
            driver.find_element(By.NAME, "email").send_keys("sonusebastian751@gmail.com")
            driver.find_element(By.NAME, "phone").send_keys("9562451299")
            driver.find_element(By.NAME, "address").send_keys("Thevarkkatil")
            driver.find_element(By.NAME, "password").send_keys("Sonu12")
            driver.find_element(By.NAME, "confirm_password").send_keys("Sonu12")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            # Wait for successful registration confirmation
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Registration Successful')]"))  # Adjust this based on your success message
            )
            self.assertIn("Registration Successful", driver.page_source)
            logger.info("Successful registration test passed.")
        except Exception as e:
            logger.error(f"Error in test_successful_registration: {str(e)}")
            self.fail(f"Test failed: {str(e)}")


   

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()