import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.cart_page import CartPage
import time

load_dotenv()

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def perform_login(driver):
    """Handle login process"""
    print("[STEP] Opening website...")
    driver.get("https://maalaxmi.store/")
    
    cart_page = CartPage(driver)
    print("[ACTION] Opening sign-in modal...")
    cart_page.open_sign_in_modal()
    print("[ACTION] Entering credentials and logging in...")
    print(f"[INFO] Using email: {os.getenv('EMAIL')}")
    cart_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("[STEP] Verifying login success...")
    time.sleep(2)
    if cart_page.is_login_successful():
        print("[SUCCESS] Login successful!")
        return cart_page
    else:
        print("[FAIL] Login failed")
        assert False, "Login failed - could not proceed"

def click_product(cart_page):
    """Click on any product"""
    print("[ACTION] Clicking on a product...")
    if cart_page.click_any_product():
        print("[SUCCESS] Product clicked successfully!")
        return True
    else:
        print("[INFO] Failed to click product, trying by index...")
        if cart_page.click_product_by_index(0):
            print("[SUCCESS] Product clicked by index!")
            return True
        else:
            print("[FAIL] Failed to click any product")
            return False

def test_login_and_click_product(driver):
    """Main test function for cart page"""
    print("[TEST] Starting cart page test...")
    
    # Login
    cart_page = perform_login(driver)
    
    # Click product
    assert click_product(cart_page), "Failed to click any product"
    
    print("[PASS] Cart page test completed successfully")