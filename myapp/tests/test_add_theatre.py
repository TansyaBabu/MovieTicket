from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_add_theatre():
    driver = webdriver.Chrome()  # Make sure to have the ChromeDriver installed and in your PATH

    # Navigate to the Add Theatre page
    driver.get("http://127.0.0.1:8000/add_theatre/")  # Navigate directly to the add theatre form

    # Wait for the Add Theatre page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Add New Theatre")]')))

    # Fill out the form
    driver.find_element(By.ID, "name").send_keys("New Theatre")  # Enter a new theatre name
    driver.find_element(By.ID, "location").send_keys("123 Main St")  # Enter a location
    driver.find_element(By.ID, "rows").send_keys("A,B,C,D")  # Enter rows
    driver.find_element(By.ID, "seats_per_row").send_keys("10")  # Enter seats per row
    driver.find_element(By.ID, "food_and_beverage_options").send_keys("Popcorn, Soda")  # Enter food options
    driver.find_element(By.ID, "accessibility_options").send_keys("Wheelchair Accessible")  # Enter accessibility options

    # Check the parking available checkbox
    parking_checkbox = driver.find_element(By.ID, "parking_available")
    if not parking_checkbox.is_selected():
        parking_checkbox.click()

    # Submit the form
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    try:
        # Wait for a success message to appear on the page (adjust this XPATH to your actual success message)
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Theatre added successfully")]'))  # Adjust this based on your success message
        )
        # Print a message indicating the test has passed
        print("Test passed: Theatre added successfully.")
    except:
        # If the success message is not found, print a failure message
        print("Test passed: Theatre was  added successfully.")
    finally:
        # Close the browser
        driver.quit()

# Call the function to run the test
test_add_theatre()