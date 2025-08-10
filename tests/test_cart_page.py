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

def extract_product_info(cart_page):
    """Extract product information"""
    print("[ACTION] Extracting product information...")
    time.sleep(2)  # Wait for page to load
    
    if cart_page.get_product_info():
        print("[SUCCESS] Product information extracted and stored successfully!")
        return True
    else:
        print("[FAIL] Failed to extract product information")
        return False

def click_set_custom_quantity(cart_page):
    """Click Set Custom Quantity button"""
    print("[ACTION] Clicking Set Custom Quantity button...")
    if cart_page.set_custom_quantity_button_click():
        print("[SUCCESS] Set Custom Quantity button clicked successfully!")
        return True
    else:
        print("[FAIL] Failed to click Set Custom Quantity button")
        return False

def set_bulk_quantity(cart_page):
    """Set quantity for bulk discount"""
    print("[ACTION] Setting bulk discount quantity...")
    if cart_page.set_bulk_discount_quantity():
        print("[SUCCESS] Bulk discount quantity set successfully!")
        return True
    else:
        print("[FAIL] Failed to set bulk discount quantity")
        return False

def show_pricing_summary(cart_page):
    """Display pricing summary"""
    print("[ACTION] Displaying pricing summary...")
    if cart_page.display_pricing_summary():
        print("[SUCCESS] Pricing summary displayed successfully!")
        return True
    else:
        print("[FAIL] Failed to display pricing summary")
        return False

def validate_pricing(cart_page):
    """Validate pricing calculations"""
    print("[ACTION] Validating pricing calculations...")
    if cart_page.validate_pricing_calculations():
        print("[SUCCESS] Pricing validation completed successfully!")
        return True
    else:
        print("[FAIL] Failed to validate pricing calculations")
        return False

def test_login_and_click_product(driver):
    """Main test function for cart page"""
    print("[TEST] Starting cart page test...")
    
    # Login
    cart_page = perform_login(driver)
    
    # Click product
    assert click_product(cart_page), "Failed to click any product"
    
    # Extract product info
    extract_product_info(cart_page)
    
    # Click Set Custom Quantity button
    click_set_custom_quantity(cart_page)
    
    # Set bulk discount quantity
    set_bulk_quantity(cart_page)
    
    # Display pricing summary
    show_pricing_summary(cart_page)
    
    # Validate pricing calculations
    validate_pricing(cart_page)
    
    print("[PASS] Cart page test completed successfully")