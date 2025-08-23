import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import time

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.admin_panel_pages.admin_login_page import LoginPage
from pages.admin_panel_pages.admin_order_management_page import AdminOrderManagementPage
from pages.admin_panel_pages.admin_dashboard_page import AdminDashboardPage


load_dotenv()


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_admin_order_management_page_verification(driver):
    """Test login and verify order management page"""
    login_page = LoginPage(driver)
    order_management_page = AdminOrderManagementPage(driver)
    
    print("🌐 Opening admin page...")
    driver.get("https://maalaxmi.store/#/admin")
    
    # Login first
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Logging in...")
    login_page.login(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    
    # Navigate to order management
    dashboard_page = AdminDashboardPage(driver)
    print("🔗 Navigating to Order Management...")
    order_management_page.navigate_to_order_management()
    
    assert order_management_page.verifying_orderManagement(), "Order Management page verification failed"
    
   