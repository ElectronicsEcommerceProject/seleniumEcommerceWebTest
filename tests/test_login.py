
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
    driver.get('https://example.com/login')
    login_page = LoginPage(driver)
    login_page.login('testuser', 'testpass')
    assert 'dashboard' in driver.current_url
