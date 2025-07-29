import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.driver_setup import get_driver
from pages.login_page import LoginPage


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login_valid(driver):
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    login_page.open_sign_in_modal()
    login_page.login("satyamgrandmaster@gmail.com", "satyamtest")

    