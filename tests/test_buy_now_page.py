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

# Global variables to store product details
product_price = None
quantity_discount = None
bulk_discount = None
quantity_discount_percentage = None
quantity_discount_quantity = None
bulk_discount_percentage = None
bulk_discount_quantity = None

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def perform_login(driver):
    """Handle login process"""
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    print(f"Using email: {os.getenv('EMAIL')}")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    time.sleep(2)
    if login_page.is_login_successful():
        print("✅ Login successful!")
    else:
        print("❌ Login failed - taking screenshot for debugging")
        driver.save_screenshot("login_failed_buy_now.png")
        print(f"Current page title: {driver.title}")
        assert False, "Login failed - could not proceed to buy now test"

def click_product(buy_now_page):
    """Click on product"""
    print("🛒 Clicking on product...")
    if buy_now_page.click_on_product():
        print("✅ Product clicked successfully!")
        return True
    else:
        print("❌ Failed to click on product")
        return False

def get_and_parse_product_details(buy_now_page):
    """Get and parse product details"""
    print("📋 Getting product details...")
    product_details = buy_now_page.get_product_details()
    if product_details:
        print("✅ Product details retrieved successfully!")
        
        global product_price, quantity_discount, bulk_discount
        global quantity_discount_percentage, quantity_discount_quantity, bulk_discount_percentage, bulk_discount_quantity
        
        product_price = product_details.get('price')
        quantity_discount = product_details.get('quantity_discount')
        bulk_discount = product_details.get('bulk_discount')
        
        import re
        if quantity_discount:
            percentage_match = re.search(r'(\d+\.\d+)%', quantity_discount)
            quantity_discount_percentage = percentage_match.group(1) + '%' if percentage_match else None
            quantity_match = re.search(r'(\d+)\+', quantity_discount)
            quantity_discount_quantity = int(quantity_match.group(1)) + 1 if quantity_match else None
        
        if bulk_discount:
            percentage_match = re.search(r'(\d+\.\d+)%', bulk_discount)
            bulk_discount_percentage = percentage_match.group(1) + '%' if percentage_match else None
            quantity_match = re.search(r'(\d+)\+', bulk_discount)
            bulk_discount_quantity = int(quantity_match.group(1)) + 1 if quantity_match else None
        
        print(f"💰 Price: {product_price}")
        print(f"📊 Quantity Discount: {quantity_discount}")
        print(f"📦 Bulk Discount: {bulk_discount}")
        print(f"📊 Quantity Discount Percentage: {quantity_discount_percentage}")
        print(f"📊 Quantity Discount Quantity: {quantity_discount_quantity}")
        print(f"📦 Bulk Discount Percentage: {bulk_discount_percentage}")
        print(f"📦 Bulk Discount Quantity: {bulk_discount_quantity}")
        return True
    else:
        print("❌ Failed to get product details")
        return False

def get_quantity_info(buy_now_page):
    """Get quantity information"""
    print("🔢 Getting quantity information...")
    min_quantity = buy_now_page.get_quantity_info()
    if min_quantity:
        print("✅ Quantity information retrieved successfully!")
        print(f"📊 Using min_quantity value: {min_quantity}")
        return min_quantity
    else:
        print("❌ Failed to get quantity information")
        return None

def set_custom_quantity_above_min(buy_now_page, min_quantity):
    """Set custom quantity above minimum"""
    print("🔘 Clicking Set Custom Quantity button...")
    if buy_now_page.click_button("set_custom_quantity"):
        print("✅ Set Custom Quantity button clicked successfully!")
        
        print("✏️ Entering custom quantity...")
        if buy_now_page.get_input(min_quantity+1):
            print(f"✅ Custom quantity entered successfully! {min_quantity+1}")
        else:
            print("❌ Failed to enter custom quantity")
            return False
    else:
        print("❌ Failed to click Set Custom Quantity button")
        return False
    
    print("⚙️ Clicking Set button...")
    if buy_now_page.click_button("set"):
        print(f"✅ Set button clicked successfully! and updated quantity becomes {min_quantity+1}")
        return True
    else:
        print("❌ Failed to click Set button")
        return False

def set_custom_quantity_below_min(buy_now_page, min_quantity, driver):
    """Set custom quantity below minimum and handle alert"""
    if buy_now_page.click_button("set_custom_quantity"):
        print("✅ Set Custom Quantity button clicked successfully!")
        
        print("✏️ Entering custom quantity...")
        if buy_now_page.get_input(min_quantity-1):
            print(f"✅ Custom quantity entered successfully! {min_quantity-1}")
        else:
            print("❌ Failed to enter custom quantity")
            return False
    else:
        print("❌ Failed to click Set Custom Quantity button")
        return False
    
    print("⚙️ Clicking Set button...")
    if buy_now_page.click_button("set"):
        print(f"✅ Set button clicked successfully! and updated quantity becomes {min_quantity-1}")
        
        # Handle alert
        try:
            time.sleep(1)
            alert = driver.switch_to.alert
            alert_message = alert.text
            print(f"⚠️ Alert message: {alert_message}")
            alert.accept()
            print("✅ Alert accepted")
        except Exception as e:
            print(f"❌ No alert found or error handling alert: {e}")
        return True
    else:
        print("❌ Failed to click Set button")
        return False

def calculate_and_compare_prices(buy_now_page):
    """Calculate discount prices and compare with web prices"""
    if product_price:
        # Get current quantity from browser
        current_quantity = buy_now_page.get_current_quantity()
        if not current_quantity:
            print("❌ Failed to get current quantity from browser")
            return
            
        price_value = float(product_price.replace('₹', '').replace(',', ''))
        print(f"\n💰 Unit Price: ₹{price_value:.2f}")
        print(f"🔢 Current Quantity in Browser: {current_quantity}")
        
        # Determine which discount applies based on current quantity
        discount_percent = 0
        discount_type = "No discount"
        
        if bulk_discount_percentage and current_quantity >= bulk_discount_quantity:
            discount_percent = float(bulk_discount_percentage.replace('%', ''))
            discount_type = f"Bulk discount ({bulk_discount_percentage})"
        elif quantity_discount_percentage and current_quantity >= quantity_discount_quantity:
            discount_percent = float(quantity_discount_percentage.replace('%', ''))
            discount_type = f"Quantity discount ({quantity_discount_percentage})"
        
        # Calculate prices based on current quantity
        original_total_price = price_value * current_quantity
        discounted_unit_price = price_value * (1 - discount_percent / 100)
        discounted_total_price = discounted_unit_price * current_quantity
        saved_amount = original_total_price - discounted_total_price
        
        print(f"🏷️ Applied Discount: {discount_type}")
        print(f"💰 Calculated for {current_quantity} units:")
        print(f"  - Original Total Price: ₹{original_total_price:.2f} ({current_quantity} x ₹{price_value:.2f})")
        print(f"  - Discounted Total Price: ₹{discounted_total_price:.2f} ({current_quantity} x ₹{discounted_unit_price:.2f})")
        print(f"  - Amount Saved: ₹{saved_amount:.2f}")
        
        # Compare with web prices
        print(f"\n🔍 Comparing calculated prices with web prices (for {current_quantity} units):")
        web_price_info = buy_now_page.get_web_price_info()
        
        if web_price_info:
            web_discounted = float(web_price_info['discounted_price'].replace('₹', '').replace(',', ''))
            web_original = float(web_price_info['original_price'].replace('₹', '').replace(',', ''))
            web_saved = float(web_price_info['savings'].replace('₹', '').replace(',', ''))
            
            print(f"🌐 Web prices for {current_quantity} units:")
            print(f"  - Web original price: ₹{web_original:.2f}")
            print(f"  - Web discounted price: ₹{web_discounted:.2f}")
            print(f"  - Web savings: ₹{web_saved:.2f}")
            
            if abs(web_discounted - discounted_total_price) < 0.01:
                print(f"✅ Discounted price matches web price for {current_quantity} units!")
            else:
                print(f"❌ Discounted price mismatch for {current_quantity} units: Calculated ₹{discounted_total_price:.2f} vs Web ₹{web_discounted:.2f}")
            
            if abs(web_saved - saved_amount) < 0.01:
                print(f"✅ Saved amount matches web savings for {current_quantity} units!")
            else:
                print(f"❌ Saved amount mismatch for {current_quantity} units: Calculated ₹{saved_amount:.2f} vs Web ₹{web_saved:.2f}")
        else:
            print("❌ Failed to get web price information for comparison")

def test_buy_now_page(driver):
    """Main test function that orchestrates all buy now tests"""
    # Login
    perform_login(driver)
    
    # Initialize buy now page
    buy_now_page = BuyNowPage(driver)
    
    # Click product
    if not click_product(buy_now_page):
        return
    
    # Get and parse product details
    if not get_and_parse_product_details(buy_now_page):
        return
    
    # Get quantity information
    min_quantity = get_quantity_info(buy_now_page)
    if not min_quantity:
        return
    
    # Set custom quantity above minimum
    if not set_custom_quantity_above_min(buy_now_page, min_quantity):
        return
    
    # Set custom quantity below minimum
    if not set_custom_quantity_below_min(buy_now_page, min_quantity, driver):
        return
    
    # Test price calculation with current quantity (after alert, quantity should be back to minimum)
    print("\n📊 ========== TESTING PRICE CALCULATION ==========\n")
    
    # Wait for page to stabilize after alert
    time.sleep(2)
    
    print(f"🔢 Testing with current quantity after alert...")
    calculate_and_compare_prices(buy_now_page)
    
    # Try to test quantity discount scenario
    print(f"\n🔢 Attempting to test quantity discount scenario...")
    try:
        # Refresh page to reset state
        driver.refresh()
        time.sleep(3)
        
        # Set quantity for quantity discount testing
        if quantity_discount_quantity and buy_now_page.click_button("set_custom_quantity"):
            if buy_now_page.get_input(quantity_discount_quantity):
                if buy_now_page.click_button("set"):
                    print(f"✅ Quantity set to {quantity_discount_quantity} for quantity discount testing!")
                    time.sleep(2)
                    calculate_and_compare_prices(buy_now_page)
                    
                    # Test bulk discount scenario
                    print(f"\n🔢 Testing bulk discount scenario...")
                    if bulk_discount_quantity and buy_now_page.click_button("set_custom_quantity"):
                        if buy_now_page.get_input(bulk_discount_quantity):
                            if buy_now_page.click_button("set"):
                                print(f"✅ Quantity set to {bulk_discount_quantity} for bulk discount testing!")
                                time.sleep(2)
                                calculate_and_compare_prices(buy_now_page)
    except Exception as e:
        print(f"❌ Error in discount testing: {e}")
        print("Testing with current quantity as fallback...")
        calculate_and_compare_prices(buy_now_page)
    
    print("\n📊 ========== PRICE TESTING COMPLETE ==========\n")
    