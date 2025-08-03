import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.main_zone_page import MainZonePage

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