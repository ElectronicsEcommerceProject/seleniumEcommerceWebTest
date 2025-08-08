import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.login_page import LoginPage

load_dotenv()

print("[INFO] Login Test Suite Initialized")
print("[INFO] Loading environment variables and dependencies")


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login_valid(driver):
    print("[TEST] Starting login test...")
    print("[STEP] Navigating to website: https://maalaxmi.store/")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("[STEP] Opening sign-in modal...")
    login_page.open_sign_in_modal()
    
    print("[STEP] Entering credentials and attempting login...")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("[STEP] Verifying login success...")
    if login_page.is_login_successful():
        print("[PASS] Login test completed successfully")
    else:
        print("[FAIL] Login test failed - user not authenticated")
    
    assert login_page.is_login_successful(), "Login failed - expected element not found"

    