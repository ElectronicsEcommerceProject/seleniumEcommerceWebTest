import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import time

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.admin_panel_pages.admin_login_page import LoginPage
from pages.admin_panel_pages.admin_product_management_page import AdminProductManagementPage
from pages.admin_panel_pages.admin_dashboard_page import AdminDashboardPage


load_dotenv()


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_admin_product_management_page_verification(driver):
    """Test login and verify product management page"""
    login_page = LoginPage(driver)
    product_management_page = AdminProductManagementPage(driver)
    
    print("🌐 Opening admin page...")
    driver.get("https://maalaxmi.store/#/admin")
    
    # Login first
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Logging in...")
    login_page.login(os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    
    # Navigate to product management
    dashboard_page = AdminDashboardPage(driver)
    print("🔗 Navigating to Product Management...")
    product_management_page.navigate_to_product_management()
    
    assert product_management_page.verifying_productManagement(), "Product Management page verification failed"
    
    # Collect table counts before making searches
    product_management_page.collect_table_counts()
    
    # Search for test category
    product_management_page.search_test_category()
    
    # Search for test brand
    product_management_page.search_test_brand()
    
    # Search for test product
    product_management_page.search_test_product()
    
    # Search for test variant
    product_management_page.search_test_variant()
    
    # Search for test attribute
    product_management_page.search_test_attribute()
    
    # Print summary of all table data
    product_management_page.print_all_table_data()
