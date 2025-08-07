import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.main_zone_page import MainZonePage
import time

load_dotenv()

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def perform_login(driver):
    """Handle login process"""
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    print(f"Using email: {os.getenv('EMAIL')}")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    time.sleep(2)
    if login_page.is_login_successful():
        print("✅ Login successful!")
    else:
        print("❌ Login failed - taking screenshot for debugging")
        driver.save_screenshot("login_failed.png")
        print(f"Current page title: {driver.title}")
        assert False, "Login failed - could not proceed to zone test"

def click_category(zone_page):
    """Click on category to navigate to zone page"""
    print("💱 Clicking on category...")
    if zone_page.clicked_on_category():
        print("✅ Category clicked successfully!")
        return True
    else:
        print("❌ Failed to click category")
        return False

def verify_zone_page_access(zone_page):
    """Verify successful navigation to zone page"""
    print("Verifying if on zone page...")
    if zone_page.is_on_zone_page():
        print("✅ Successfully on the main zone!")
        return True
    else:
        print("❌ Failed to navigate to the main zone")
        return False

def check_brand_checkboxes(zone_page):
    """Check brand checkboxes status"""
    print("🔍 Checking brand checkboxes...")
    zone_page.check_brand_checkboxes()

def find_brand_names(zone_page):
    """Find and display brand names from search results"""
    print("🔍 Finding brand names from search results...")
    zone_page.found_brand_names()

def search_specific_brand(zone_page):
    """Search for a specific brand"""
    print("🔍 Searching for a specific brand...")
    if zone_page.search_brand_name("mi", "brand"):
        print("✅ Searched for brand successfully!")
        return True
    else:
        print("❌ Failed to search for brand")
        return False

def count_products(zone_page, url_pattern):
    """Count products on page"""
    print("🔍 Counting products on page...")
    zone_page.count_products_on_page(url_pattern)

def search_product(zone_page):
    """Search for a specific product"""
    zone_page.search_brand_name("satyamtest", "product")
    print("product search applied..")

def test_main_zone(driver):
    """Main test function that orchestrates all zone tests"""
    # Login
    perform_login(driver)
    
    # Initialize zone page
    zone_page = MainZonePage(driver)
    
    # Click category
    if not click_category(zone_page):
        return
    
    # Verify zone page access
    if not verify_zone_page_access(zone_page):
        return
    
    # Check brand checkboxes
    check_brand_checkboxes(zone_page)
    
    # Find brand names
    find_brand_names(zone_page)
    
    # Search specific brand
    if not search_specific_brand(zone_page):
        return
    
    # Find brand names after search
    find_brand_names(zone_page)
    
    # Count products
    url_pattern = "http://maalaxmi.store/uploads/product_images/media_file"
    count_products(zone_page, url_pattern)
    
    # Search product
    search_product(zone_page)
    
    # Count products after product search
    count_products(zone_page, url_pattern)