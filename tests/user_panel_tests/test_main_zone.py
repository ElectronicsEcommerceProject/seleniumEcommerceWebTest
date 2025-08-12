import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.user_panel_pages.login_page import LoginPage
from pages.user_panel_pages.main_zone_page import MainZonePage
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
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    assert login_page.is_login_successful(), "Login failed - could not proceed to zone test"
    print("✅ Login successful!")

    zone_page = MainZonePage(driver)
    
    print("💱 Clicking on category...")
    category_xpath = "/html/body/div/div/div[1]/header/nav/div/div[2]/button[1]"
    if zone_page.clicked_on_category(category_xpath):
        print("✅ Category clicked successfully!")
    else:
        print("❌ Failed to click category")
        return
    
    print("Verifying if on zone page...")
    zone_xpath = "//span[normalize-space()='Price -- High to Low']"
    if zone_page.is_on_zone_page(zone_xpath):
        print("✅ Successfully on the main zone!")
    else:
        print("❌ Failed to navigate to the main zone")
        return
    
    print("🔍 Checking brand checkboxes...")
    labels_xpath = "//div[contains(@class, 'max-h-40') and contains(@class, 'overflow-y-auto') and contains(@class, 'custom-scrollbar')]//label[input[@type='checkbox']]"
    zone_page.check_brand_checkboxes(labels_xpath)
    
    print("🔍 Finding brand names from search results...")
    brand_labels_xpath = "//div[contains(@class, 'max-h-40') and contains(@class, 'overflow-y-auto') and contains(@class, 'custom-scrollbar')]//label"
    zone_page.found_brand_names(brand_labels_xpath)
    
    
    
    print("🔍 Searching for a specific brand...")
    search_box_xpath = "//input[@placeholder='Search brands...']"
    if zone_page.search_brand_name("mi", search_box_xpath):
        print("✅ Searched for brand successfully!")
    else:
        print("❌ Failed to search for brand")
        return
    zone_page.found_brand_names(brand_labels_xpath)
    print("🔍 Counting products on page...")
    url_pattern = "http://maalaxmi.store/uploads/product_images/media_file"
    zone_page.count_products_on_page(url_pattern)
    zone_page.search_brand_name("satyamtest", "//input[@placeholder='🔍 Search products (auto-search after 1.5s or press Enter)...']")
    print("product search applied..")
    zone_page.count_products_on_page(url_pattern)