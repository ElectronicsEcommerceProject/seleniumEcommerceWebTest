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


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_dashboard_navigation(driver):
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    assert login_page.is_login_successful(), "Login failed - could not proceed to dashboard test"
    print("✅ Login successful!")

    dashboard_page = MainDashboardPage(driver)
    print("Verifying if on dashboard...")
    dashboard_xpath = "//button[contains(text(),'Buttonphone')]"
    assert dashboard_page.is_on_dashboard(dashboard_xpath), "Failed to navigate to the main dashboard"
    print("✅ Successfully on the main dashboard!")
    
    print("🔍 Searching for products...")
    search_box_selector = "input[placeholder='Search for products...']"
    dashboard_page.search_product("samsung", search_box_selector)
    print("⏳ Verifying search results...")
    results_selector = "[class*='product'], [class*='item'], [class*='card']"
    assert dashboard_page.get_search_results(results_selector), "Search results not found"
    print("✅ Search results displayed successfully!")
    
    is_cleared = dashboard_page.clear_search(search_box_selector)
    if is_cleared:
        print("✅ Search box cleared successfully!")
    else:
        print("❌ Search box not cleared properly")
        return 
    
    filter_xpath = "//*[@id='root']/div/div[4]/div/div[1]/button[4]"
    dashboard_page.apply_brand_filter(filter_xpath)
    print("✅ Brand filter applied successfully!")
    
    brand_xpath = "//div[contains(@class, 'text-blue-600') and contains(@class, 'bg-blue-50') and contains(text(), 'Vivo')]"
    wait_xpath = "//div[contains(@class, 'text-blue-600') and contains(@class, 'bg-blue-50')]"
    product_count = dashboard_page.count_products_by_brand(brand_xpath, wait_xpath)
    print(f"📊 Found {product_count} Vivo products")

    print("🔄 Refreshing page...")
    dashboard_page.refresh_page()
    
    print("🖼️ Finding images with specific URL pattern...")
    url_pattern = "http://maalaxmi.store/uploads/product_images/media_file"
    image_count = dashboard_page.find_images_with_url_pattern(url_pattern)
    print(f"📊 Found {image_count} images with pattern: {url_pattern}")
    
    print("🔄 Clicking Load More button...")
    if dashboard_page.click_button_by_text("Load More"):
        print("✅ Load More button clicked successfully!")
    else:
        print("❌ Load More button not found or not clickable")
    
   