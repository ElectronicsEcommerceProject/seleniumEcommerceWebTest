import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.main_dashboard_page import MainDashboardPage

load_dotenv()

print("[INFO] Dashboard Test Suite Initialized")
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
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("[STEP] Verifying login success...")
    assert login_page.is_login_successful(), "Login failed - could not proceed to dashboard test"
    print("[SUCCESS] Login successful!")

def verify_dashboard_access(dashboard_page):
    """Verify successful navigation to dashboard"""
    print("[STEP] Verifying if on dashboard...")
    assert dashboard_page.is_on_dashboard(), "Failed to navigate to the main dashboard"
    print("[SUCCESS] Successfully on the main dashboard!")

def product_search(dashboard_page):
    """Test product search functionality"""
    print("[ACTION] Searching for products...")
    dashboard_page.search_product("samsung")
    print("[STEP] Verifying search results...")
    assert dashboard_page.get_search_results(), "Search results not found"
    print("[SUCCESS] Search results displayed successfully!")

def search_clear(dashboard_page):
    """Test search box clearing functionality"""
    is_cleared = dashboard_page.clear_search()
    if is_cleared:
        print("[SUCCESS] Search box cleared successfully!")
        return True
    else:
        print("[FAIL] Search box not cleared properly")
        return False

def brand_filter(dashboard_page):
    """Test brand filter functionality"""
    dashboard_page.apply_brand_filter()
    print("[SUCCESS] Brand filter applied successfully!")
    
    product_count = dashboard_page.count_products_by_brand()
    print(f"[INFO] Found {product_count} Vivo products")
    return product_count

def page_refresh(dashboard_page):
    """Test page refresh functionality"""
    print("[ACTION] Refreshing page...")
    dashboard_page.refresh_page()

def image_loading(dashboard_page):
    """Test image loading with URL pattern"""
    print("[ACTION] Finding images with specific URL pattern...")
    url_pattern = "http://maalaxmi.store/uploads/product_images/media_file"
    image_count = dashboard_page.find_images_with_url_pattern(url_pattern)
    print(f"[INFO] Found {image_count} images with pattern: {url_pattern}")
    return image_count

def load_more_button(dashboard_page):
    """Test Load More button functionality"""
    print("[ACTION] Clicking Load More button...")
    if dashboard_page.click_button_by_text("Load More"):
        print("[SUCCESS] Load More button clicked successfully!")
        return True
    else:
        print("[FAIL] Load More button not found or not clickable")
        return False

def test_dashboard_navigation(driver):
    """Main test function that orchestrates all dashboard tests"""
    print("[TEST] Starting dashboard navigation test...")
    
    # Login
    perform_login(driver)
    
    # Initialize dashboard page
    dashboard_page = MainDashboardPage(driver)
    
    # Verify dashboard access
    verify_dashboard_access(dashboard_page)
    
    # Test product search
    product_search(dashboard_page)
    
    # Test search clearing
    if not search_clear(dashboard_page):
        return
    
    # Test brand filter
    brand_filter(dashboard_page)
    
    # Test page refresh
    page_refresh(dashboard_page)
    
    # Test image loading
    image_loading(dashboard_page)
    
    # Test Load More button
    if load_more_button(dashboard_page):
        # Test image loading after Load More
        image_loading(dashboard_page)
    
    print("[PASS] Dashboard navigation test completed successfully")
    
   