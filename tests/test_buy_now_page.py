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
    else:
        print("❌ Failed to click on product")
        return
    print("📋 Getting product details...")
    details_xpath = "//div[contains(@class, 'mt-3') and contains(@class, 'p-3') and contains(@class, 'bg-gray-50')]"
    if buy_now_page.get_product_details(details_xpath):
            print("✅ Product details retrieved successfully!")
    else:
            print("❌ Failed to get product details")
            return
        
    print("🔢 Getting quantity information...")
    quantity_input_xpath = "//input[@type='number' and contains(@class, 'w-16')]"
    min_quantity = buy_now_page.get_quantity_info(quantity_input_xpath)
    if min_quantity:
            print("✅ Quantity information retrieved successfully!")
            print(f"📊 Using min_quantity value: {min_quantity}")
    else:
            print("❌ Failed to get quantity information")
            return
        
    print("🔘 Clicking Set Custom Quantity button...")
    button_xpath = "//button[contains(text(), 'Set Custom Quantity')]"
    if buy_now_page.click_button(button_xpath):
        print("✅ Set Custom Quantity button clicked successfully!")
            
        print("✏️ Entering custom quantity...")
        input_xpath = "//input[@type='number' and @placeholder='Enter quantity']"
        if buy_now_page.get_input(input_xpath, min_quantity+1):
            print(f"✅ Custom quantity entered successfully! {min_quantity+1}")
        else:
            print("❌ Failed to enter custom quantity")
            return
            
    else:
        print("❌ Failed to click Set Custom Quantity button")
        return
    print("⚙️ Clicking Set button...")
    set_button_xpath = "//button[contains(text(), 'Set')]"
    if buy_now_page.click_button(set_button_xpath):
        print(f"✅ Set button clicked successfully! and updated quantity becomes {min_quantity+1}")
    else:
        print("❌ Failed to click Set button") 
    