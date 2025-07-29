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
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    login_page.login("satyamgrandmaster@gmail.com", "satyamtest")
    
    print("⏳ Verifying login success...")
    if login_page.is_login_successful():
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")
    
    assert login_page.is_login_successful(), "Login failed - expected element not found"

    