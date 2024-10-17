from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_add_showtime():
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in your PATH

    try:
        # Navigate to the Add Showtime page
        driver.get("http://127.0.0.1:8000/showtimes/add/")

        # Wait for the Add Showtime page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(), "Add Showtime")]')))

        # Select a movie
        movie_select = driver.find_element(By.ID, "Mandakini")
        movie_select.click()
        movie_option = movie_select.find_element(By.XPATH, "//option[text()='Inception']")  # Replace 'Inception' with an actual movie title from your database
        movie_option.click()

        # Select a theatre
        theatre_select = driver.find_element(By.ID, "Bosco Theatre")
        theatre_select.click()
        theatre_option = theatre_select.find_element(By.XPATH, "//option[text()='Main Theatre']")  # Replace 'Main Theatre' with an actual theatre name from your database
        theatre_option.click()

        # Add a showtime
        showtime_input = driver.find_element(By.NAME, "showtime")
        showtime_input.send_keys("19:00")

        # Set start and end dates
        start_date_input = driver.find_element(By.ID, "start_date")
        start_date_input.send_keys("2023-12-25")

        end_date_input = driver.find_element(By.ID, "end_date")
        end_date_input.send_keys("2023-12-31")

        # Submit the form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for the success message or URL change
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "successMessage")))

        # Verify the success message
        success_message = driver.find_element(By.ID, "successMessage").text
        assert "Showtime added successfully" in success_message
        print("Test passed: Showtime added successfully.")

    except TimeoutException:
        print("Test failed: Showtime was not added.")

    finally:
        driver.quit()

# Call the function to run the test
test_add_showtime()