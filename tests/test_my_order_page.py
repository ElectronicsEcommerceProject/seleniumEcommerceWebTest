import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
import time

load_dotenv()

print("[INFO] My Order Page Test Suite Initialized")
print("[INFO] Loading environment variables and dependencies")

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def perform_login(driver):
    """Handle login process"""
    print("[STEP] Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("[ACTION] Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("[ACTION] Entering credentials and logging in...")
    print(f"[INFO] Using email: {os.getenv('EMAIL')}")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("[STEP] Verifying login success...")
    time.sleep(2)
    if login_page.is_login_successful():
        print("[SUCCESS] Login successful!")
    else:
        print("[FAIL] Login failed - taking screenshot for debugging")
        driver.save_screenshot("login_failed_my_order.png")
        print(f"[INFO] Current page title: {driver.title}")
        assert False, "Login failed - could not proceed to my order test"

def navigate_to_orders_page(driver):
    """Navigate to the orders page"""
    print("[ACTION] Navigating to orders page...")
    driver.get("https://maalaxmi.store/#/profile/orders")
    time.sleep(2)
    print("[SUCCESS] Navigated to orders page successfully!")

def test_my_order_page(driver):
    """Main test function for my order page"""
    print("[TEST] Starting my order page test...")
    
    # Login
    perform_login(driver)
    
    # Navigate to orders page
    navigate_to_orders_page(driver)
    
    print("[PASS] My order page test completed successfully")