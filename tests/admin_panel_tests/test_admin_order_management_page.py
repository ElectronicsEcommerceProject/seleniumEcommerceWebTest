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
    time.sleep(5)
    
    # Login first
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    time.sleep(2)
    print("📝 Logging in...")
    login_page.login(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    
    # Navigate to order management
    dashboard_page = AdminDashboardPage(driver)
    print("🔗 Navigating to Order Management...")
    order_management_page.navigate_to_order_management()
    
    # assert order_management_page.verifying_orderManagement(), "Order Management page verification failed"
    
    # # Count all order items with pagination
    # total_items = order_management_page.count_all_order_items_with_pagination()
    # print(f"Found {total_items} total order items.")
    # assert total_items == 38, f"Expected 38 total order items, but found {total_items}"


    # # Get the total orders count from the header
    # header_count = order_management_page.get_total_orders_from_header()
    # print(f"Header count: {header_count}")
    
    # # Compare header count with table count (using total_items already calculated)
    # order_management_page.compare_header_and_table_counts(header_count, total_items)
    
    # Get all pending orders across all pages
    pending_orders = order_management_page.get_pending_orders_with_pagination()
    print(f"\n📊 Found {len(pending_orders)} pending orders in total")
    
    # Get pending orders count from dashboard and compare
    dashboard_pending_count = order_management_page.get_pending_orders_count_from_dashboard()
    print(f"Dashboard pending count: {dashboard_pending_count}")
    order_management_page.compare_dashboard_and_actual_pending_counts(dashboard_pending_count, len(pending_orders))
    
    # Get all shipped orders across all pages
    shipped_orders = order_management_page.get_shipped_orders_with_pagination()
    print(f"\n📊 Found {len(shipped_orders)} shipped orders in total")
    
    # Get shipped orders count from dashboard and compare
    dashboard_shipped_count = order_management_page.get_shipped_orders_count_from_dashboard()
    print(f"Dashboard shipped count: {dashboard_shipped_count}")
    order_management_page.compare_dashboard_and_actual_shipped_counts(dashboard_shipped_count, len(shipped_orders))