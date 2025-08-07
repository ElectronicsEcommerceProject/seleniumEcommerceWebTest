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

def test_main_zone(driver):
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    print(f"Using email: {os.getenv('EMAIL')}")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    time.sleep(2)  # Additional wait
    if login_page.is_login_successful():
        print("✅ Login successful!")
    else:
        print("❌ Login failed - taking screenshot for debugging")
        driver.save_screenshot("login_failed.png")
        print(f"Current page title: {driver.title}")
        assert False, "Login failed - could not proceed to zone test"

    zone_page = MainZonePage(driver)
    
    print("💱 Clicking on category...")
    if zone_page.clicked_on_category():
        print("✅ Category clicked successfully!")
    else:
        print("❌ Failed to click category")
        return
    
    print("Verifying if on zone page...")
    if zone_page.is_on_zone_page():
        print("✅ Successfully on the main zone!")
    else:
        print("❌ Failed to navigate to the main zone")
        return
    
    print("🔍 Checking brand checkboxes...")
    zone_page.check_brand_checkboxes()
    
    print("🔍 Finding brand names from search results...")
    zone_page.found_brand_names()
    
    print("🔍 Searching for a specific brand...")
    if zone_page.search_brand_name("mi", "brand"):
        print("✅ Searched for brand successfully!")
    else:
        print("❌ Failed to search for brand")
        return
    zone_page.found_brand_names()
    print("🔍 Counting products on page...")
    url_pattern = "http://maalaxmi.store/uploads/product_images/media_file"
    zone_page.count_products_on_page(url_pattern)
    zone_page.search_brand_name("satyamtest", "product")
    print("product search applied..")
    zone_page.count_products_on_page(url_pattern)