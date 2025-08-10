from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

class CartPage:
    """Page object for the Cart page."""
    
    # Global variables
    product_price = None
    quantity_discount_percentage = None
    quantity_discount_unit = None
    bulk_discount_percentage = None
    bulk_discount_unit = None
    entered_quantity = None
    pre_cart_final_price = None
    pre_cart_savings = None
    
    # Locators
    SIGN_IN_BUTTON = (By.XPATH, "//span[@class='text-sm font-medium' and text()='Sign In']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'].w-full.bg-gradient-to-r.from-blue-600.to-blue-700")
    LOGIN_SUCCESS_INDICATOR = (By.XPATH, "//button[contains(text(),'Buttonphone')]")
    PRODUCT_ELEMENTS = (By.XPATH, "//div[contains(@class, 'w-full p-3') and contains(@class, 'bg-white rounded-xl shadow-lg') and contains(@class, 'cursor-pointer')]")
    PRODUCT_INFO_SECTION = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]")
    PRICE_INFO = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]//span[text()='Price:']/following-sibling::span")
    SKU_INFO = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]//span[text()='SKU:']/following-sibling::span")
    MIN_ORDER_QTY = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]//span[text()='Min. Order Qty:']/following-sibling::span")
    QUANTITY_DISCOUNT = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]//span[text()='Quantity Discount:']/following-sibling::span")
    BULK_DISCOUNT = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]//span[text()='Bulk Discount:']/following-sibling::span")
    SET_CUSTOM_QUANTITY_BUTTON = (By.XPATH, "//button[contains(@class, 'text-blue-600') and contains(text(), 'Set Custom Quantity')]")
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number' and @placeholder='Enter quantity']")
    SET_BUTTON = (By.XPATH, "//button[contains(@class, 'bg-blue-600') and text()='Set']")
    TOTAL_PRICE_SECTION = (By.XPATH, "//div[contains(@class, 'mt-3 p-3 bg-gray-50 rounded-lg')]//span[text()='Total Price:']/following-sibling::div")
    FINAL_PRICE = (By.XPATH, "//span[contains(@class, 'text-xl font-bold text-green-600')]")
    ORIGINAL_PRICE = (By.XPATH, "//span[contains(@class, 'line-through')]")
    SAVINGS_AMOUNT = (By.XPATH, "//span[contains(@class, 'text-green-600') and contains(text(), 'Save')]")
    PRICE_BREAKDOWN = (By.XPATH, "//div[contains(@class, 'text-sm text-gray-600') and contains(text(), '×')]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@class, 'bg-orange-600') and contains(text(), 'ADD TO CART')]")
    SHOPPING_CART_HEADING = (By.XPATH, "//h1[contains(@class, 'text-xl') and contains(text(), 'Shopping Cart')]")
    REMOVE_BUTTONS = (By.XPATH, "//button[contains(@class, 'text-red-600') and text()='Remove']")
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(), 'Your cart is empty')]")
    CART_ITEM_PRICE = (By.XPATH, "//span[@class='font-semibold text-base sm:text-lg']")
    CART_ITEM_DISCOUNT = (By.XPATH, "//span[@class='text-xs text-green-600']")
    CART_ITEM_QUANTITY = (By.XPATH, "//span[contains(@class, 'px-2 py-1 min-w-[32px] text-center text-sm')]")
    CART_ITEM_TOTAL = (By.XPATH, "//span[@class='font-semibold text-sm sm:text-base whitespace-nowrap']")
    CART_BULK_DISCOUNT_TEXT = (By.XPATH, "//div[contains(@class, 'text-green-600') and contains(text(), 'Bulk discount applied')]")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open_sign_in_modal(self):
        """Open the sign-in modal by hovering and clicking login."""
        sign_in_button = self.wait.until(EC.presence_of_element_located(self.SIGN_IN_BUTTON))
        hover = ActionChains(self.driver).move_to_element(sign_in_button)
        hover.perform()
        
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()

    def login(self, email, password):
        """Perform login with email and password."""
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.send_keys(email)
        
        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        password_input.send_keys(password)
        
        login_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        login_button.click()
        
    def is_login_successful(self):
        """Check if login was successful."""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.LOGIN_SUCCESS_INDICATOR))
            return True
        except:
            return False
    
    def click_any_product(self):
        """Click the first available product."""
        try:
            product = self.wait.until(EC.element_to_be_clickable(self.PRODUCT_ELEMENTS))
            actions = ActionChains(self.driver)
            actions.move_to_element(product).click().perform()
            return True
        except:
            return False
    
    def click_product_by_index(self, index=0):
        """Click product by specific index."""
        try:
            products = self.driver.find_elements(*self.PRODUCT_ELEMENTS)
            if len(products) > index:
                actions = ActionChains(self.driver)
                actions.move_to_element(products[index]).click().perform()
                return True
            return False
        except:
            return False
    
    def get_product_info(self):
        """Extract and store product information in class variables."""
        try:
            print("[INFO] Extracting product information...")
            
            # Wait for product info section to load
            self.wait.until(EC.presence_of_element_located(self.PRODUCT_INFO_SECTION))
            
            # Extract and store price
            try:
                CartPage.product_price = self.driver.find_element(*self.PRICE_INFO).text
            except:
                CartPage.product_price = "Not found"
            
            # Extract Quantity Discount
            try:
                qty_discount = self.driver.find_element(*self.QUANTITY_DISCOUNT).text
                if qty_discount != "Not found":
                    # Extract percentage (e.g., "10.00% off on 2+ units")
                    percentage_match = re.search(r'(\d+\.\d+)%', qty_discount)
                    unit_match = re.search(r'(\d+\+) units', qty_discount)
                    CartPage.quantity_discount_percentage = percentage_match.group(1) + "%" if percentage_match else "Not found"
                    CartPage.quantity_discount_unit = unit_match.group(1) + " units" if unit_match else "Not found"
                else:
                    CartPage.quantity_discount_percentage = "Not found"
                    CartPage.quantity_discount_unit = "Not found"
            except:
                CartPage.quantity_discount_percentage = "Not found"
                CartPage.quantity_discount_unit = "Not found"
            
            # Extract Bulk Discount
            try:
                bulk_discount = self.driver.find_element(*self.BULK_DISCOUNT).text
                if bulk_discount != "Not found":
                    # Extract percentage (e.g., "25.00% off on 4+ units")
                    percentage_match = re.search(r'(\d+\.\d+)%', bulk_discount)
                    unit_match = re.search(r'(\d+\+) units', bulk_discount)
                    CartPage.bulk_discount_percentage = percentage_match.group(1) + "%" if percentage_match else "Not found"
                    CartPage.bulk_discount_unit = unit_match.group(1) + " units" if unit_match else "Not found"
                else:
                    CartPage.bulk_discount_percentage = "Not found"
                    CartPage.bulk_discount_unit = "Not found"
            except:
                CartPage.bulk_discount_percentage = "Not found"
                CartPage.bulk_discount_unit = "Not found"
            
            # Print all extracted information
            print(f"[INFO] Product Price: {CartPage.product_price}")
            print(f"[INFO] Quantity Discount Percentage: {CartPage.quantity_discount_percentage}")
            print(f"[INFO] Quantity Discount Unit: {CartPage.quantity_discount_unit}")
            print(f"[INFO] Bulk Discount Percentage: {CartPage.bulk_discount_percentage}")
            print(f"[INFO] Bulk Discount Unit: {CartPage.bulk_discount_unit}")
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not extract product info: {e}")
            return False
    
    def set_custom_quantity_button_click(self):
        """Click the Set Custom Quantity button."""
        try:
            print("[ACTION] Looking for Set Custom Quantity button...")
            button = self.wait.until(EC.element_to_be_clickable(self.SET_CUSTOM_QUANTITY_BUTTON))
            
            # Scroll to button and click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)
            button.click()
            print("[SUCCESS] Set Custom Quantity button clicked successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Could not click Set Custom Quantity button: {e}")
            return False
    
    def set_bulk_discount_quantity(self):
        """Set quantity to bulk_discount_unit+1 to apply bulk discount."""
        try:
            # Calculate quantity for bulk discount
            if CartPage.bulk_discount_unit and CartPage.bulk_discount_unit != "Not found":
                # Extract number from "4+ units" format
                unit_match = re.search(r'(\d+)', CartPage.bulk_discount_unit)
                if unit_match:
                    bulk_qty = int(unit_match.group(1)) + 1
                    CartPage.entered_quantity = bulk_qty
                    print(f"[ACTION] Setting quantity to {bulk_qty} to apply bulk discount...")
                    
                    # Find and fill quantity input
                    quantity_input = self.wait.until(EC.element_to_be_clickable(self.QUANTITY_INPUT))
                    quantity_input.clear()
                    quantity_input.send_keys(str(bulk_qty))
                    print(f"[SUCCESS] Entered quantity: {bulk_qty}")
                    
                    # Click Set button
                    set_button = self.wait.until(EC.element_to_be_clickable(self.SET_BUTTON))
                    set_button.click()
                    print("[SUCCESS] Set button clicked successfully")
                    return True
                else:
                    print("[ERROR] Could not parse bulk discount unit")
                    return False
            else:
                print("[ERROR] Bulk discount unit not available")
                return False
        except Exception as e:
            print(f"[ERROR] Could not set bulk discount quantity: {e}")
            return False
    
    def display_pricing_summary(self):
        """Display complete pricing summary after quantity is set."""
        try:
            print("[INFO] Extracting pricing summary...")
            time.sleep(2)  # Wait for price calculation
            
            # Print entered quantity
            if CartPage.entered_quantity:
                print(f"[INFO] Entered Quantity: {CartPage.entered_quantity}")
            
            # Extract final price
            try:
                final_price = self.driver.find_element(*self.FINAL_PRICE).text
                CartPage.pre_cart_final_price = float(re.search(r'[₹]([\d,]+\.?\d*)', final_price).group(1).replace(',', ''))
                print(f"[INFO] Final Price: {final_price}")
            except:
                CartPage.pre_cart_final_price = 0
                print("[INFO] Final Price: Not found")
            
            # Extract original price
            try:
                original_price = self.driver.find_element(*self.ORIGINAL_PRICE).text
                print(f"[INFO] Original Price: {original_price}")
            except:
                print("[INFO] Original Price: Not found")
            
            # Extract savings
            try:
                savings = self.driver.find_element(*self.SAVINGS_AMOUNT).text
                CartPage.pre_cart_savings = float(re.search(r'[₹]([\d,]+\.?\d*)', savings).group(1).replace(',', ''))
                print(f"[INFO] {savings}")
            except:
                CartPage.pre_cart_savings = 0
                print("[INFO] Savings: Not found")
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not extract pricing summary: {e}")
            return False
    
    def validate_pricing_calculations(self):
        """Validate pricing calculations and discounts."""
        try:
            print("[INFO] Validating pricing calculations...")
            
            # Extract numeric values
            product_price_num = float(re.search(r'[₹]([\d,]+\.?\d*)', CartPage.product_price).group(1).replace(',', '')) if CartPage.product_price != "Not found" else 0
            entered_qty = CartPage.entered_quantity if CartPage.entered_quantity else 0
            bulk_discount_percent = float(re.search(r'([\d.]+)', CartPage.bulk_discount_percentage).group(1)) if CartPage.bulk_discount_percentage != "Not found" else 0
            
            # Get displayed prices
            try:
                original_price_text = self.driver.find_element(*self.ORIGINAL_PRICE).text
                original_price_num = float(re.search(r'[₹]([\d,]+\.?\d*)', original_price_text).group(1).replace(',', ''))
            except:
                print("[ERROR] Could not extract original price for validation")
                return False
            
            try:
                final_price_text = self.driver.find_element(*self.FINAL_PRICE).text
                final_price_num = float(re.search(r'[₹]([\d,]+\.?\d*)', final_price_text).group(1).replace(',', ''))
            except:
                print("[ERROR] Could not extract final price for validation")
                return False
            
            try:
                savings_text = self.driver.find_element(*self.SAVINGS_AMOUNT).text
                savings_num = float(re.search(r'[₹]([\d,]+\.?\d*)', savings_text).group(1).replace(',', ''))
            except:
                print("[ERROR] Could not extract savings for validation")
                return False
            
            # Validation 1: Quantity × Product Price = Original Price
            expected_original = product_price_num * entered_qty
            if abs(expected_original - original_price_num) < 0.01:
                print(f"[SUCCESS] ✅ Quantity calculation correct: {entered_qty} × ₹{product_price_num} = ₹{original_price_num}")
            else:
                print(f"[FAIL] ❌ Quantity calculation incorrect: {entered_qty} × ₹{product_price_num} = ₹{expected_original}, but got ₹{original_price_num}")
            
            # Validation 2: Bulk Discount Calculation
            expected_discount = original_price_num * (bulk_discount_percent / 100)
            expected_final = original_price_num - expected_discount
            
            if abs(expected_discount - savings_num) < 0.01 and abs(expected_final - final_price_num) < 0.01:
                print(f"[SUCCESS] ✅ Bulk discount calculation correct: {bulk_discount_percent}% on ₹{original_price_num} = Save ₹{savings_num}, Final ₹{final_price_num}")
            else:
                print(f"[FAIL] ❌ Bulk discount calculation incorrect: Expected save ₹{expected_discount}, final ₹{expected_final}, but got save ₹{savings_num}, final ₹{final_price_num}")
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not validate pricing calculations: {e}")
            return False
    
    def add_to_cart_button_click(self):
        """Click ADD TO CART button with quantity validation."""
        try:
            print("[ACTION] Looking for ADD TO CART button...")
            
            # Find ADD TO CART button
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON))
            button_text = add_to_cart_button.text
            
            # Extract quantity from button text (e.g., "ADD TO CART (5)")
            button_qty_match = re.search(r'\((\d+)\)', button_text)
            if button_qty_match:
                button_qty = int(button_qty_match.group(1))
                
                # Compare with entered quantity
                if CartPage.entered_quantity and button_qty == CartPage.entered_quantity:
                    print(f"[SUCCESS] ✅ Quantity validation passed: Button shows ({button_qty}) matches Entered Quantity: {CartPage.entered_quantity}")
                else:
                    print(f"[WARNING] ⚠️ Quantity mismatch: Button shows ({button_qty}) but Entered Quantity: {CartPage.entered_quantity}")
            
            # Click the button
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
            time.sleep(1)
            add_to_cart_button.click()
            print("[SUCCESS] ADD TO CART button clicked successfully")
            
            # Handle alert
            try:
                print("[INFO] Waiting for cart alert...")
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"[INFO] Alert message: {alert_text}")
                
                # Check if item already exists in cart
                if "Item already exist in cart" in alert_text:
                    alert.accept()
                    print("[INFO] Item already in cart - clearing cart first...")
                    if self.clear_existing_cart():
                        print("[INFO] Cart cleared - returning to product page to retry...")
                        self.driver.back()  # Go back to product page
                        time.sleep(3)
                        return "retry"  # Signal to retry the process
                    return False
                else:
                    alert.accept()  # Click OK
                    print("[SUCCESS] Alert accepted successfully")
            except Exception as e:
                print(f"[WARNING] No alert appeared or could not handle alert: {e}")
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not click ADD TO CART button: {e}")
            return False
    
    def verify_on_cart_page(self):
        """Verify if user is on the cart page."""
        try:
            print("[ACTION] Verifying if on cart page...")
            print("[INFO] Waiting for page navigation to complete...")
            time.sleep(5)  # Wait longer for page to load
            
            # Wait for Shopping Cart heading with longer timeout
            print("[INFO] Looking for Shopping Cart heading...")
            cart_heading = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.SHOPPING_CART_HEADING)
            )
            heading_text = cart_heading.text
            
            if "Shopping Cart" in heading_text:
                print(f"[SUCCESS] ✅ Successfully navigated to cart page: '{heading_text}' found")
                return True
            else:
                print(f"[FAIL] ❌ Not on cart page: Expected 'Shopping Cart' but found '{heading_text}'")
                return False
        except Exception as e:
            print(f"[ERROR] Could not verify cart page: {e}")
            print(f"[INFO] Current page URL: {self.driver.current_url}")
            print(f"[INFO] Current page title: {self.driver.title}")
            return False
    
    def clear_existing_cart(self):
        """Navigate to cart and remove all items."""
        try:
            print("[ACTION] Navigating to cart page to clear existing items...")
            self.driver.get("https://maalaxmi.store/#/cart")
            time.sleep(3)
            
            # Find and click all Remove buttons
            while True:
                try:
                    remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
                    if not remove_buttons:
                        print("[INFO] No more Remove buttons found")
                        break
                    
                    print(f"[INFO] Found {len(remove_buttons)} Remove button(s)")
                    # Click the first Remove button
                    remove_buttons[0].click()
                    print("[SUCCESS] Clicked Remove button")
                    time.sleep(2)  # Wait for item to be removed
                    
                except Exception as e:
                    print(f"[INFO] No more items to remove: {e}")
                    break
            
            # Check for empty cart message
            try:
                empty_message = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.EMPTY_CART_MESSAGE)
                )
                print(f"[SUCCESS] ✅ Cart cleared successfully: '{empty_message.text}' found")
                return True
            except:
                print("[INFO] Empty cart message not found, but removal process completed")
                return True
                
        except Exception as e:
            print(f"[ERROR] Could not clear cart: {e}")
            return False
    
    def retry_add_to_cart_process(self):
        """Retry the complete add to cart process after clearing cart."""
        try:
            print("[INFO] ========== RETRYING ADD TO CART PROCESS ==========\n")
            
            # Step 1: Click Set Custom Quantity button
            if not self.set_custom_quantity_button_click():
                return False
            
            # Step 2: Set bulk discount quantity
            if not self.set_bulk_discount_quantity():
                return False
            
            # Step 3: Display pricing summary
            if not self.display_pricing_summary():
                return False
            
            # Step 4: Validate pricing
            if not self.validate_pricing_calculations():
                return False
            
            # Step 5: Try add to cart again
            result = self.add_to_cart_button_click()
            if result == "retry":
                print("[ERROR] Still getting duplicate item error after clearing cart")
                return False
            
            return result
        except Exception as e:
            print(f"[ERROR] Could not retry add to cart process: {e}")
            return False
    
    def validate_cart_item_details(self):
        """Compare cart item details with pre-cart values."""
        try:
            print("[INFO] ========== VALIDATING CART ITEM DETAILS ==========\n")
            time.sleep(3)  # Wait for cart page to load
            
            # Extract cart item details
            try:
                cart_price = self.driver.find_element(*self.CART_ITEM_PRICE).text
                cart_price_num = float(re.search(r'[₹]([\d,]+\.?\d*)', cart_price).group(1).replace(',', ''))
                print(f"[INFO] Cart Item Price: {cart_price}")
            except:
                print("[ERROR] Could not extract cart item price")
                return False
            
            try:
                cart_discount = self.driver.find_element(*self.CART_ITEM_DISCOUNT).text
                cart_discount_num = float(re.search(r'[₹]([\d,]+\.?\d*)', cart_discount).group(1).replace(',', ''))
                print(f"[INFO] Cart Item Discount: {cart_discount}")
            except:
                print("[ERROR] Could not extract cart item discount")
                return False
            
            try:
                cart_quantity = int(self.driver.find_element(*self.CART_ITEM_QUANTITY).text)
                print(f"[INFO] Cart Item Quantity: {cart_quantity}")
            except:
                print("[ERROR] Could not extract cart item quantity")
                return False
            
            try:
                cart_total = self.driver.find_element(*self.CART_ITEM_TOTAL).text
                cart_total_num = float(re.search(r'[₹]([\d,]+\.?\d*)', cart_total).group(1).replace(',', ''))
                print(f"[INFO] Cart Item Total: {cart_total}")
            except:
                print("[ERROR] Could not extract cart item total")
                return False
            
            try:
                bulk_discount_text = self.driver.find_element(*self.CART_BULK_DISCOUNT_TEXT).text
                bulk_percentage_match = re.search(r'([\d.]+)%', bulk_discount_text)
                cart_bulk_percentage = float(bulk_percentage_match.group(1)) if bulk_percentage_match else 0
                print(f"[INFO] Cart Bulk Discount: {bulk_discount_text}")
            except:
                print("[ERROR] Could not extract cart bulk discount")
                return False
            
            # Get pre-cart values from stored class variables
            product_price_num = float(re.search(r'[₹]([\d,]+\.?\d*)', CartPage.product_price).group(1).replace(',', '')) if CartPage.product_price != "Not found" else 0
            entered_qty = CartPage.entered_quantity if CartPage.entered_quantity else 0
            pre_cart_bulk_percent = float(re.search(r'([\d.]+)', CartPage.bulk_discount_percentage).group(1)) if CartPage.bulk_discount_percentage != "Not found" else 0
            
            # Calculate expected pre-cart values
            pre_cart_original_price = product_price_num * entered_qty
            pre_cart_discount_amount = pre_cart_original_price * (pre_cart_bulk_percent / 100)
            pre_cart_final_price = pre_cart_original_price - pre_cart_discount_amount
            
            print("\n[INFO] ========== COMPARISON RESULTS ==========\n")
            
            # Validation 1: Quantity comparison
            if cart_quantity == CartPage.entered_quantity:
                print(f"[SUCCESS] ✅ Quantity matches: Cart ({cart_quantity}) = Entered ({CartPage.entered_quantity})")
            else:
                print(f"[FAIL] ❌ Quantity mismatch: Cart ({cart_quantity}) ≠ Entered ({CartPage.entered_quantity})")
            
            # Validation 2: Final price comparison
            if abs(cart_total_num - pre_cart_final_price) < 0.01:
                print(f"[SUCCESS] ✅ Total price matches: Cart (₹{cart_total_num}) = Pre-cart (₹{pre_cart_final_price})")
            else:
                print(f"[FAIL] ❌ Total price mismatch: Cart (₹{cart_total_num}) ≠ Pre-cart (₹{pre_cart_final_price})")
            
            # Validation 3: Discount amount comparison
            if abs(cart_discount_num - pre_cart_discount_amount) < 0.01:
                print(f"[SUCCESS] ✅ Discount amount matches: Cart (₹{cart_discount_num}) = Pre-cart (₹{pre_cart_discount_amount})")
            else:
                print(f"[FAIL] ❌ Discount amount mismatch: Cart (₹{cart_discount_num}) ≠ Pre-cart (₹{pre_cart_discount_amount})")
            
            # Validation 4: Bulk discount percentage comparison
            if abs(cart_bulk_percentage - pre_cart_bulk_percent) < 0.01:
                print(f"[SUCCESS] ✅ Bulk discount percentage matches: Cart ({cart_bulk_percentage}%) = Pre-cart ({pre_cart_bulk_percent}%)")
            else:
                print(f"[FAIL] ❌ Bulk discount percentage mismatch: Cart ({cart_bulk_percentage}%) ≠ Pre-cart ({pre_cart_bulk_percent}%)")
            
            print("\n[INFO] ========== CART VALIDATION COMPLETE ==========\n")
            return True
            
        except Exception as e:
            print(f"[ERROR] Could not validate cart item details: {e}")
            return False