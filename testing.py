from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver (make sure to replace 'path_to_chromedriver' with your actual path)
driver = webdriver.Chrome(executable_path="path_to_chromedriver")

# Set up test variables
BASE_URL = "http://104.197.128.246/"
USERNAME = "miner2@gmail.com"
PASSWORD = "Shadow1234"

try:
    # Open the application
    driver.get(BASE_URL)
    driver.maximize_window()

    # Test 1: Login Test
    print("Running Login Test...")
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "loginButton")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()

    # Wait until the dashboard page is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboard"))
    )
    print("Login Test Passed.")

    # Test 2: Navigate to Dashboard and Check Filter
    print("Running Dashboard Navigation Test...")
    driver.find_element(By.ID, "dashboard").click()

    # Wait for filter button to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "filter-btn"))
    )

    # Test 3: Apply Filter Test
    print("Running Filter Test...")
    driver.find_element(By.ID, "filter-btn").click()
    time.sleep(1)  # Small delay for the filter section to appear

    # Select options in filters (you can adjust values as needed)
    time_frame = driver.find_element(By.ID, "time_frame")
    time_frame.send_keys("Weekly")

    state_filter = driver.find_element(By.ID, "state-filter")
    state_filter.send_keys("Gujarat")

    zone_filter = driver.find_element(By.ID, "zone-filter")
    zone_filter.send_keys("West")

    # Apply the filter
    apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply Filter')]")
    apply_button.click()

    # Wait for the table to update and check the filtered result
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "minerTable"))
    )
    print("Filter Test Passed.")

except Exception as e:
    print("Test failed:", str(e))

finally:
    # Close the browser
    driver.quit()
