import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.admin_panel_pages.admin_login_page import LoginPage
from pages.admin_panel_pages.admin_login_page import LoginPage
from pages.admin_panel_pages.admin_dashboard_page import AdminDashboardPage

load_dotenv()


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_admin_dashboard_verification(driver):
    print("🌐 Opening admin page...")
    driver.get("https://maalaxmi.store/#/admin")
    
    # Login first
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Logging in...")
    login_page.login(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    
    # Verify dashboard
    admin_dashboard = AdminDashboardPage(driver)
    print("✅ Verifying admin dashboard page...")
    
    assert admin_dashboard.verifying_adminDashboard(), "Admin dashboard verification failed"
    print("✅ Admin dashboard verified successfully!")
    
    # Test button functionality
    print("🔘 Testing button functionality...")
    admin_dashboard.checking_button_working()
    print("✅ Button testing completed!")