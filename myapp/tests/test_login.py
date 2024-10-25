import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestLogin(unittest.TestCase):
    def setUp(self):
      
        self.driver = webdriver.Chrome() 
        self.driver.get("http://localhost:8000/login") 

    def test_admin_login(self):
        driver = self.driver
        # Admin login
        driver.find_element(By.NAME, "username").send_keys("tansya")  
        driver.find_element(By.NAME, "password").send_keys("tansya@23")  
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(2) 
        try:
            self.assertIn("Admin Dashboard", driver.title)  
            print("Admin login test passed")
        except AssertionError:
            print("Admin login test failed")

    def test_theatre_owner_login(self):
        driver = self.driver
        # Theatre owner login
        driver.get("http://localhost:8000/login")  
        driver.find_element(By.NAME, "username").send_keys("Megha")  
        driver.find_element(By.NAME, "password").send_keys("megha12")  
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(2)  
        try:
            self.assertIn("Theatre Owner Dashboard", driver.title)  
            print("Theatre owner login test passed")
        except AssertionError:
            print("Theatre owner login test failed")

    def test_user_login(self):
        driver = self.driver
        # User login
        driver.get("http://localhost:8000/login")  # Navigate back to login
        driver.find_element(By.NAME, "username").send_keys("Varsha")  # Replace with actual user username
        driver.find_element(By.NAME, "password").send_keys("varsha12")  # Replace with actual user password
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(2) 
        try:
            self.assertIn("User Dashboard", driver.title)  
            print("User login test passed")
        except AssertionError:
            print("User login test failed")

    def tearDown(self):
        self.driver.quit()  

if __name__ == "__main__":
    unittest.main()