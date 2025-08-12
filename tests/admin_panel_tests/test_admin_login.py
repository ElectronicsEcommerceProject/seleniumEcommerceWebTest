import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.admin_panel_pages.admin_login_page import LoginPage

load_dotenv()


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login_valid(driver):
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/#/admin")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    login_page.login(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    
    print("⏳ Verifying login success...")
    if login_page.is_login_successful():
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")
    
    assert login_page.is_login_successful(), "Login failed - expected element not found"

    