import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import time

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.admin_panel_pages.admin_login_page import LoginPage
from pages.admin_panel_pages.admin_dashboard_page import AdminDashboardPage
from pages.admin_panel_pages.admin_banner_management_page import AdminBannerManagementPage

load_dotenv()


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_admin_banner_management_verification(driver):
    print("🌐 Opening admin page...")
    driver.get("https://maalaxmi.store/#/admin")
    
    # Login first
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Logging in...")
    login_page.login(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    
    # Navigate to banner management
    dashboard_page = AdminDashboardPage(driver)
    print("🔗 Navigating to Banner Management...")
    assert dashboard_page.navigate_to_banner_management(), "Failed to navigate to banner management"
    
    # Verify banner management page
    banner_page = AdminBannerManagementPage(driver)
    print("✅ Verifying banner management page...")
    
    assert banner_page.verifying_bannerManagement(), "Banner management page verification failed"
    print("✅ Banner management page verified successfully!")
    
    # Test edit button clicking
    print("✏️ Testing edit button clicking...")
    assert banner_page.clicking_edit_button(), "Edit button clicking failed"
    print("✅ Edit button clicking test completed!")
    
    # Test button clicking functionality
    print("🔘 Testing button clicking...")
    assert banner_page.clicking_button(), "Button clicking failed"
    print("✅ Button clicking test completed!")
    time.sleep(5)