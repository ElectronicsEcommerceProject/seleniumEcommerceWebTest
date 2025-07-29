import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login_valid(driver):
    driver.get("https://maalaxmi.store/")

    wait = WebDriverWait(driver, 10)


    # Wait until element is ready for interaction
    sign_in_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='text-sm font-medium' and text()='Sign In']"))
    )

    # Hover action
    hover = ActionChains(driver).move_to_element(sign_in_button)
    hover.perform()
    print("✅ Hovered over the 'Sign In' button")

    # Wait and click the "Login" button using button text
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']"))
    )
    login_button.click()                           

    # Wait for the email input field
    email_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_input.send_keys("satyamgrandmaster@gmail.com")

    # Safe wait for password field using name attribute
    try:
        password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("satyamtest")
    except TimeoutException:
        pytest.fail("❌ Password input field not found on the page.")

    # Wait and click the Login button using its full class attributes
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
            "button.w-full.bg-blue-600.text-white.py-2.rounded-md.text-sm.font-medium.hover\\:bg-blue-700.transition-all.px-4"))
    )
    login_button.click()

    