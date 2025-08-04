import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from utils.driver_setup import get_driver
from pages.login_page import LoginPage
from pages.buy_now_page import BuyNowPage
import time

load_dotenv()

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_buy_now_page(driver):
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    assert login_page.is_login_successful(), "Login failed - could not proceed to buy now test"
    print("✅ Login successful!")

    buy_now_page = BuyNowPage(driver)
    
    print("🛒 Clicking on product...")
    product_xpath = "//h3[contains(text(), 'Redbon fast charger')]"
    if buy_now_page.click_on_product(product_xpath):
        print("✅ Product clicked successfully!")
        
        print("📋 Getting product details...")
        details_xpath = "//div[contains(@class, 'mt-3') and contains(@class, 'p-3') and contains(@class, 'bg-gray-50')]"
        if buy_now_page.get_product_details(details_xpath):
            print("✅ Product details retrieved successfully!")
        else:
            print("❌ Failed to get product details")
        
        print("🔢 Getting quantity information...")
        quantity_input_xpath = "//input[@type='number' and contains(@class, 'w-16')]"
        if buy_now_page.get_quantity_info(quantity_input_xpath):
            print("✅ Quantity information retrieved successfully!")
        else:
            print("❌ Failed to get quantity information")
        
    else:
        print("❌ Failed to click on product")
        return
    
