
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login_valid(driver):
    driver.get("https://maalaxmi.store/")

    # Wait for the "Sign In" button to be clickable
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='text-sm font-medium' and text()='Sign In']"))
    )
    sign_in_button.click()

    # Wait for the email input field to appear in the modal
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_input.send_keys("testuser@example.com")

    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpass")
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

    WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
    assert "dashboard" in driver.current_url
