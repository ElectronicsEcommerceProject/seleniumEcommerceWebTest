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

def test_buy_now_page(driver):
    print("🌐 Opening website...")
    driver.get("https://maalaxmi.store/")
    
    login_page = LoginPage(driver)
    print("🔑 Opening sign-in modal...")
    login_page.open_sign_in_modal()
    print("📝 Entering credentials and logging in...")
    print(f"Using email: {os.getenv('EMAIL')}")
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    
    print("⏳ Verifying login success...")
    time.sleep(2)  # Additional wait
    if login_page.is_login_successful():
        print("✅ Login successful!")
    else:
        print("❌ Login failed - taking screenshot for debugging")
        driver.save_screenshot("login_failed_buy_now.png")
        print(f"Current page title: {driver.title}")
        assert False, "Login failed - could not proceed to buy now test"

    buy_now_page = BuyNowPage(driver)
    
    print("🛒 Clicking on product...")
    if buy_now_page.click_on_product():
        print("✅ Product clicked successfully!")
    else:
        print("❌ Failed to click on product")
        return
    print("📋 Getting product details...")
    product_details = buy_now_page.get_product_details()
    if product_details:
            print("✅ Product details retrieved successfully!")
            # Store in global variables
            global product_price, quantity_discount, bulk_discount
            product_price = product_details.get('price')
            quantity_discount = product_details.get('quantity_discount')
            bulk_discount = product_details.get('bulk_discount')
            
            # Parse discount details
            global quantity_discount_percentage, quantity_discount_quantity, bulk_discount_percentage, bulk_discount_quantity
            
            if quantity_discount:
                import re
                # Extract percentage (e.g., "10.00%")
                percentage_match = re.search(r'(\d+\.\d+)%', quantity_discount)
                quantity_discount_percentage = percentage_match.group(1) + '%' if percentage_match else None
                
                # Extract quantity (e.g., "2+" becomes 3)
                quantity_match = re.search(r'(\d+)\+', quantity_discount)
                quantity_discount_quantity = int(quantity_match.group(1)) + 1 if quantity_match else None
            
            if bulk_discount:
                # Extract percentage (e.g., "25.00%")
                percentage_match = re.search(r'(\d+\.\d+)%', bulk_discount)
                bulk_discount_percentage = percentage_match.group(1) + '%' if percentage_match else None
                
                # Extract quantity (e.g., "4+" becomes 5)
                quantity_match = re.search(r'(\d+)\+', bulk_discount)
                bulk_discount_quantity = int(quantity_match.group(1)) + 1 if quantity_match else None
            
            print(f"💰 Price: {product_price}")
            print(f"📊 Quantity Discount: {quantity_discount}")
            print(f"📦 Bulk Discount: {bulk_discount}")
            print(f"📊 Quantity Discount Percentage: {quantity_discount_percentage}")
            print(f"📊 Quantity Discount Quantity: {quantity_discount_quantity}")
            print(f"📦 Bulk Discount Percentage: {bulk_discount_percentage}")
            print(f"📦 Bulk Discount Quantity: {bulk_discount_quantity}")
    else:
            print("❌ Failed to get product details")
            return
        
    print("🔢 Getting quantity information...")
    min_quantity = buy_now_page.get_quantity_info()
    if min_quantity:
            print("✅ Quantity information retrieved successfully!")
            print(f"📊 Using min_quantity value: {min_quantity}")
    else:
            print("❌ Failed to get quantity information")
            return
        
    print("🔘 Clicking Set Custom Quantity button...")
    if buy_now_page.click_button("set_custom_quantity"):
        print("✅ Set Custom Quantity button clicked successfully!")
            
        print("✏️ Entering custom quantity...")
        if buy_now_page.get_input(min_quantity+1):
            print(f"✅ Custom quantity entered successfully! {min_quantity+1}")
        else:
            print("❌ Failed to enter custom quantity")
            return
            
    else:
        print("❌ Failed to click Set Custom Quantity button")
        return
    print("⚙️ Clicking Set button...")
    if buy_now_page.click_button("set"):
        print(f"✅ Set button clicked successfully! and updated quantity becomes {min_quantity+1}")
    else:
        print("❌ Failed to click Set button") 
        return
    
    #setting quantity to be below the minimum quantity...
    if buy_now_page.click_button("set_custom_quantity"):
        print("✅ Set Custom Quantity button clicked successfully!")
            
        print("✏️ Entering custom quantity...")
        if buy_now_page.get_input(min_quantity-1):
            print(f"✅ Custom quantity entered successfully! {min_quantity-1}")
        else:
            print("❌ Failed to enter custom quantity")
            return
            
    else:
        print("❌ Failed to click Set Custom Quantity button")
        return
    print("⚙️ Clicking Set button...")
    if buy_now_page.click_button("set"):
        print(f"✅ Set button clicked successfully! and updated quantity becomes {min_quantity-1}")
        # Handle alert
        try:
            time.sleep(1)  # Wait for alert to appear
            alert = driver.switch_to.alert
            alert_message = alert.text
            print(f"⚠️ Alert message: {alert_message}")
            alert.accept()  # Click OK on alert
            print("✅ Alert accepted")
        except Exception as e:
            print(f"❌ No alert found or error handling alert: {e}")
    else:
        print("❌ Failed to click Set button") 
        return
    
    #checking after increase in quantity to quantity_discount_quantity, bulk_discount_quantity the discount applied on price are correct or not
     # Calculate discount prices
    if product_price and quantity_discount_percentage and bulk_discount_percentage:
        price_value = float(product_price.replace('₹', '').replace(',', ''))
        # Extract numeric price value
                
                
        print(f"\n💰 Actual Price: ₹{price_value:.2f}")
                
        if quantity_discount_percentage:
        # Calculate total price after quantity discount
            discount_percent = float(quantity_discount_percentage.replace('%', ''))
            discounted_unit_price = price_value * (1 - discount_percent / 100)
            total_quantity_discount_price = discounted_unit_price * quantity_discount_quantity
            # Calculate saved amount for quantity discount
            actual_total_price_qty = price_value * quantity_discount_quantity
            quantity_saved_amount = actual_total_price_qty - total_quantity_discount_price
            print(f"📊 Total price after {quantity_discount_percentage} quantity discount for {quantity_discount_quantity} units: ₹{total_quantity_discount_price:.2f}")
            print(f"💰 Amount saved with quantity discount: ₹{quantity_saved_amount:.2f} (Original: ₹{actual_total_price_qty:.2f})")
                
        # Calculate total price after bulk discount
        if bulk_discount_percentage:
            bulk_percent = float(bulk_discount_percentage.replace('%', ''))
            discounted_bulk_unit_price = price_value * (1 - bulk_percent / 100)
            total_bulk_discount_price = discounted_bulk_unit_price * bulk_discount_quantity
            # Calculate saved amount for bulk discount
            actual_total_price_bulk = price_value * bulk_discount_quantity
            bulk_saved_amount = actual_total_price_bulk - total_bulk_discount_price
            print(f"📦 Total price after {bulk_discount_percentage} bulk discount for {bulk_discount_quantity} units: ₹{total_bulk_discount_price:.2f}")
            print(f"💰 Amount saved with bulk discount: ₹{bulk_saved_amount:.2f} (Original: ₹{actual_total_price_bulk:.2f})")
            
            # Compare with web prices
            print("\n🔍 Comparing calculated prices with web prices...")
            web_price_info = buy_now_page.get_web_price_info()
            
            if web_price_info:
                web_discounted = float(web_price_info['discounted_price'].replace('₹', '').replace(',', ''))
                web_original = float(web_price_info['original_price'].replace('₹', '').replace(',', ''))
                web_saved = float(web_price_info['savings'].replace('₹', '').replace(',', ''))
                
                print(f"🌐 Web discounted price: ₹{web_discounted:.2f}")
                print(f"🌐 Web original price: ₹{web_original:.2f}")
                print(f"🌐 Web savings: ₹{web_saved:.2f}")
                
                # Compare prices
                if abs(web_discounted - total_bulk_discount_price) < 0.01:
                    print("✅ Discounted price matches web price!")
                else:
                    print(f"❌ Discounted price mismatch: Calculated ₹{total_bulk_discount_price:.2f} vs Web ₹{web_discounted:.2f}")
                
                if abs(web_saved - bulk_saved_amount) < 0.01:
                    print("✅ Saved amount matches web savings!")
                else:
                    print(f"❌ Saved amount mismatch: Calculated ₹{bulk_saved_amount:.2f} vs Web ₹{web_saved:.2f}")
            else:
                print("❌ Failed to get web price information for comparison")
    