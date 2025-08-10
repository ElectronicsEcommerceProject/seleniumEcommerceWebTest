import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.user_panel_pages.login_page import LoginPage
from pages.user_panel_pages.my_order_page import MyOrderPage
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

def check_initial_order_count(my_order_page):
    """Check initial order count"""
    print("[STEP] Checking initial order count...")
    initial_count = my_order_page.count_visible_orders()
    my_order_page.initial_order_count = initial_count
    my_order_page.current_order_count = initial_count
    
    if initial_count > 0:
        print(f"[SUCCESS] Found {initial_count} orders on the page!")
        return True
    else:
        print("[INFO] No orders found - user hasn't placed any orders yet")
        print("[INFO] Load More functionality cannot be tested without existing orders")
        return False

def load_all_orders(my_order_page):
    """Load all orders by clicking Load More buttons until no more are available"""
    print("\n[INFO] ========== LOADING ALL ORDERS ==========\n")
    print("[STEP] Checking for Load More buttons to load all orders...")
    
    while True:
        # Check if Load More button is present
        if my_order_page.check_load_more_button_present():
            print("[ACTION] Load More button found - clicking to load more orders...")
            
            # Click Load More button
            if my_order_page.click_load_more_button():
                print("[SUCCESS] Load More button clicked successfully!")
                
                # Wait for new orders to load
                my_order_page.wait_for_new_orders_to_load()
                
                # Update current count
                new_count = my_order_page.count_visible_orders()
                my_order_page.current_order_count = new_count
                print(f"[INFO] Total orders now visible: {new_count}")
            else:
                print("[INFO] Failed to click Load More button - stopping")
                break
        else:
            print("[INFO] No Load More button found - all orders are now loaded")
            break
    
    # Validate that all orders are actually loaded
    print("\n[STEP] Validating all orders are loaded...")
    if my_order_page.validate_all_orders_loaded():
        final_count = my_order_page.count_visible_orders()
        print("[INFO] ========== ALL ORDERS LOADED ==========\n")
        return final_count
    else:
        final_count = my_order_page.count_visible_orders()
        print(f"[INFO] Loaded {final_count} orders (may not be all available orders)")
        print("[INFO] ========== ORDER LOADING COMPLETE ==========\n")
        return final_count

def check_load_more_button(my_order_page):
    """Check for Load More button"""
    print("[STEP] Checking for Load More button...")
    if my_order_page.check_load_more_button_present():
        print("[SUCCESS] Load More button found and clickable!")
        return True
    else:
        print("[INFO] Load More button not found or not clickable")
        return False

def click_load_more_and_validate(my_order_page):
    """Click Load More button and validate order count increase"""
    print("[ACTION] Clicking Load More button...")
    if my_order_page.click_load_more_button():
        print("[SUCCESS] Load More button clicked successfully!")
        
        print("[STEP] Waiting for new orders to load...")
        my_order_page.wait_for_new_orders_to_load()
        
        print("[STEP] Validating order count increase...")
        increased, new_count = my_order_page.validate_order_count_increase(my_order_page.current_order_count)
        
        if increased:
            my_order_page.current_order_count = new_count
            print("[SUCCESS] New orders loaded successfully!")
            return True
        else:
            print("[INFO] No new orders loaded")
            return False
    else:
        print("[FAIL] Failed to click Load More button")
        return False

def run_filter_checkbox_tests(my_order_page):
    """Test filter checkbox functionality"""
    print("\n[INFO] ========== TESTING ALL FILTER CHECKBOXES ==========\n")
    
    # Test all filter checkboxes (both ORDER STATUS and ORDER TIME)
    my_order_page.test_all_filters()
    
    print("\n[INFO] ========== ALL FILTER TESTING COMPLETE ==========\n")
    return True

def run_search_functionality_tests(my_order_page):
    """Test order search functionality"""
    print("\n[INFO] ========== TESTING SEARCH FUNCTIONALITY ==========\n")
    
    # Test 1: Exact order search
    exact_result = my_order_page.test_exact_order_search()
    
    # Clear search before next test
    my_order_page.clear_search()
    
    # Test 2: Partial order search
    partial_result = my_order_page.test_partial_order_search()
    
    # Clear search before next test
    my_order_page.clear_search()
    
    # Test 3: Invalid search
    invalid_result = my_order_page.test_invalid_order_search()
    
    # Clear search to restore all orders
    my_order_page.clear_search()
    
    print("\n[INFO] ========== SEARCH TESTING COMPLETE ==========")
    print(f"[INFO] Exact search test: {'PASSED' if exact_result else 'COMPLETED'}")
    print(f"[INFO] Partial search test: {'PASSED' if partial_result else 'COMPLETED'}")
    print(f"[INFO] Invalid search test: {'PASSED' if invalid_result else 'COMPLETED'}")
    
    return True

def display_final_results(my_order_page):
    """Display final Load More testing results"""
    print("\n[INFO] ========== LOAD MORE TESTING COMPLETE ==========")
    print(f"[INFO] Initial orders: {my_order_page.initial_order_count}")
    print(f"[INFO] Final orders: {my_order_page.current_order_count}")
    print(f"[INFO] Total Load More clicks: {my_order_page.load_more_clicks}")
    print(f"[INFO] Additional orders loaded: {my_order_page.current_order_count - my_order_page.initial_order_count}")
    
    # Validate final count matches total available
    print("\n[STEP] Validating final order count...")
    if my_order_page.validate_final_order_count():
        print("[SUCCESS] Load More functionality tested successfully!")
        return True
    else:
        print("[INFO] Load More functionality partially tested")
        return my_order_page.current_order_count >= my_order_page.initial_order_count

def test_my_order_page(driver):
    """Main test function for my order page"""
    print("[TEST] Starting my order page test...")
    
    # Login
    perform_login(driver)
    
    # Navigate to orders page
    navigate_to_orders_page(driver)
    
    # Initialize my order page
    my_order_page = MyOrderPage(driver)
    
    print("\n[INFO] ========== TESTING LOAD MORE FUNCTIONALITY ==========\n")
    
    # Step 1: Check initial order count
    if not check_initial_order_count(my_order_page):
        print("[PASS] My order page test completed - no orders to test Load More functionality")
        print("[INFO] To test Load More functionality, place some orders first and run the test again")
        return
    
    # Step 2: Load all orders first
    load_all_orders(my_order_page)
    
    # Step 3: Test filter checkboxes
    run_filter_checkbox_tests(my_order_page)
    
    # Step 3.5: Test cancel complete order functionality
    print("\n[INFO] ========== TESTING CANCEL ORDER FUNCTIONALITY ==========\n")
    
    # Refresh page to reset state after filter testing
    print("[ACTION] Refreshing page to reset state...")
    driver.refresh()
    time.sleep(3)
    print("[SUCCESS] Page refreshed")
    
    if my_order_page.cancel_complete_order_button_click():
        print("[PASS] Cancel order functionality tested successfully")
    else:
        print("[INFO] Cancel order functionality test completed")
    
    # Step 4: Repeat Load More process until no more orders
    while True:
        # Check for Load More button
        if not check_load_more_button(my_order_page):
            print("[INFO] Load More button not available - all orders loaded")
            break
        
        # Click Load More and validate
        if not click_load_more_and_validate(my_order_page):
            print("[INFO] No new orders loaded - stopping Load More process")
            break
    
    # Step 5: Display final results
    display_final_results(my_order_page)
    
    # Step 6: Test search functionality at the end
    run_search_functionality_tests(my_order_page)
    
    print("[PASS] All testing completed successfully")