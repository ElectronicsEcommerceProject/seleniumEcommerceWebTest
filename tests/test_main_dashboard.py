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
    assert dashboard_page.is_on_dashboard(), "Failed to navigate to the main dashboard"
    print("✅ Successfully on the main dashboard!")
    
    # print("🔍 Searching for products...")
    # dashboard_page.search_product("samsung")
    # print("⏳ Verifying search results...")
    # assert dashboard_page.get_search_results(), "Search results not found"
    # print("✅ Search results displayed successfully!")
    dashboard_page.apply_brand_filter()
    print("✅ Brand filter applied successfully!")
    time.sleep(240)


