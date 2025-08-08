from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BuyNowPage:
    """Page object for the Buy Now page."""
    
    # Locators
    PRODUCT_LINK = (By.XPATH, "//h3[contains(text(), 'Redbon fast charger')]")
    PRODUCT_DETAILS = (By.XPATH, "//div[contains(@class, 'mt-3') and contains(@class, 'p-3') and contains(@class, 'bg-gray-50')]")
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number' and contains(@class, 'w-16')]")
    SET_CUSTOM_QUANTITY_BUTTON = (By.XPATH, "//button[contains(text(), 'Set Custom Quantity')]")
    CUSTOM_QUANTITY_INPUT = (By.XPATH, "//input[@type='number' and @placeholder='Enter quantity']")
    SET_BUTTON = (By.XPATH, "//button[contains(text(), 'Set')]")
    PRICE_CONTAINER = (By.XPATH, "//span[@class='text-xl font-bold text-green-600']")
    DISCOUNTED_PRICE = (By.XPATH, ".//span[contains(@class, 'text-green-600') and contains(@class, 'font-bold')]")
    ORIGINAL_PRICE = (By.XPATH, ".//span[contains(@class, 'line-through')]")
    SAVINGS_TEXT = (By.XPATH, ".//span[contains(text(), 'Save')]")
    DETAIL_ROWS = (By.XPATH, ".//div[contains(@class, 'flex') and contains(@class, 'justify-between')]")
    SPAN_TAGS = (By.TAG_NAME, "span")
    WRITE_REVIEW_BUTTON = (By.XPATH, "//button[normalize-space()='Write a Review']")
    REVIEW_TITLE_INPUT = (By.XPATH, "//input[@placeholder='Summarize your experience']")
    REVIEW_TEXT_AREA = (By.XPATH, "//textarea[@placeholder='Share your experience with this product']")
    VARIANT_SELECT = (By.XPATH, "//select[contains(@class, 'w-full p-2 border')]")
    SUBMIT_REVIEW_BUTTON = (By.XPATH, "//button[contains(text(), 'Submit Review')]")
    BUY_NOW_BUTTON = (By.XPATH, "//button[contains(@class, 'bg-green-600') and .//div[text()='BUY NOW']]")
    ADDRESS_INFO = (By.XPATH, "//*[contains(text(), 'addresses') or contains(text(), 'address')]")
    ADDRESS_AREA = (By.XPATH, "//div[contains(@class, 'p-4 border rounded-lg cursor-pointer') and contains(@class, 'transition-colors')]")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_on_product(self):
        """Click on a product."""
        try:
            product_element = self.wait.until(EC.presence_of_element_located(self.PRODUCT_LINK))
            
            # Scroll to the element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", product_element)
            time.sleep(2)
            
            # Try JavaScript click first
            self.driver.execute_script("arguments[0].click();", product_element)
            print("Product clicked using JavaScript")
            
            return True
        except Exception as e:
            print(f"Error clicking on product: {e}")
            # Try clicking on parent element as fallback
            try:
                parent_element = product_element.find_element(By.XPATH, "./ancestor::*[contains(@class, 'group') or contains(@class, 'card') or contains(@class, 'product')][1]")
                self.driver.execute_script("arguments[0].click();", parent_element)
                print("Clicked on parent element instead")
                return True
            except:
                return False
    
    def get_product_details(self):
        """Extract and print product details like price, SKU, etc."""
        try:
            details_container = self.wait.until(EC.presence_of_element_located(self.PRODUCT_DETAILS))
            
            # Find all key-value pairs
            detail_rows = details_container.find_elements(*self.DETAIL_ROWS)
            
            product_details = {}
            print("\n📋 Product Details:")
            for row in detail_rows:
                try:
                    spans = row.find_elements(*self.SPAN_TAGS)
                    if len(spans) >= 2:
                        key = spans[0].text.strip()
                        value = spans[1].text.strip()
                        print(f"  {key} {value}")
                        
                        # Store specific details
                        if "Price:" in key:
                            product_details['price'] = value
                        elif "Quantity Discount:" in key:
                            product_details['quantity_discount'] = value
                        elif "Bulk Discount:" in key:
                            product_details['bulk_discount'] = value
                except:
                    continue
            
            return product_details
        except Exception as e:
            print(f"Error getting product details: {e}")
            return None
    
    def get_quantity_info(self):
        """Get quantity information from the number input field."""
        try:
            quantity_input = self.wait.until(EC.presence_of_element_located(self.QUANTITY_INPUT))
            
            min_quantity = quantity_input.get_attribute("min")
            current_value = quantity_input.get_attribute("value")
            
            print(f"\n🔢 Quantity Information:")
            print(f"  Min quantity to order: {min_quantity}")
            print(f"  Current quantity: {current_value}")
            
            return int(min_quantity) if min_quantity else None
        except Exception as e:
            print(f"Error getting quantity info: {e}")
            return None
    
    def click_button(self, button_type="set_custom_quantity"):
        """Click on a button based on button type."""
        try:
            if button_type == "set_custom_quantity":
                button_element = self.wait.until(EC.element_to_be_clickable(self.SET_CUSTOM_QUANTITY_BUTTON))
            elif button_type == "set":
                button_element = self.wait.until(EC.element_to_be_clickable(self.SET_BUTTON))
            else:
                raise ValueError(f"Unknown button type: {button_type}")
            
            # Scroll to the button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
            time.sleep(1)
            
            # Click the button
            self.driver.execute_script("arguments[0].click();", button_element)
            print(f"Button clicked successfully")
            
            return True
        except Exception as e:
            print(f"Error clicking button: {e}")
            return False
    
    def get_input(self, quantity_value):
        """Enter value into the custom quantity input field."""
        try:
            input_element = self.wait.until(EC.element_to_be_clickable(self.CUSTOM_QUANTITY_INPUT))
            
            # Scroll to the input
            self.driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
            time.sleep(1)
            
            # Clear and enter value
            input_element.clear()
            input_element.send_keys(str(quantity_value))
            print(f"Entered value '{quantity_value}' into input field")
            
            return True
        except Exception as e:
            print(f"Error entering value into input: {e}")
            return False
    
    def get_web_price_info(self):
        """Extract price and savings information from web elements."""
        try:
            # Get the discounted price directly
            discounted_price_element = self.wait.until(EC.presence_of_element_located(self.PRICE_CONTAINER))
            web_discounted_price = discounted_price_element.text.strip()
            
            # Find parent container to get other price elements
            parent_container = discounted_price_element.find_element(By.XPATH, "./parent::*")
            
            # Extract original price (line-through)
            original_price_element = parent_container.find_element(*self.ORIGINAL_PRICE)
            web_original_price = original_price_element.text.strip()
            
            # Extract savings amount
            savings_element = parent_container.find_element(*self.SAVINGS_TEXT)
            web_savings = savings_element.text.strip().replace('Save ', '')
            
            return {
                'discounted_price': web_discounted_price,
                'original_price': web_original_price,
                'savings': web_savings
            }
        except Exception as e:
            print(f"Error getting web price info: {e}")
            return None
    
    def get_current_quantity(self):
        """Get the current quantity value from the input field."""
        try:
            quantity_input = self.driver.find_element(*self.QUANTITY_INPUT)
            current_qty = quantity_input.get_attribute("value")
            return int(current_qty) if current_qty else None
        except Exception as e:
            print(f"Error getting current quantity: {e}")
            return None
    
    def click_write_review_button(self):
        """Click on the write review button."""
        try:
            review_button = self.wait.until(EC.element_to_be_clickable(self.WRITE_REVIEW_BUTTON))
            
            # Scroll to the button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_button)
            time.sleep(1)
            
            # Click the button
            self.driver.execute_script("arguments[0].click();", review_button)
            print("Write review button clicked successfully")
            
            return True
        except Exception as e:
            print(f"Error clicking write review button: {e}")
            return False
    
    def fill_review_form(self):
        """Fill the review form with test data."""
        try:
            # Wait for form to appear
            time.sleep(2)
            
            # Fill review title
            title_input = self.wait.until(EC.element_to_be_clickable(self.REVIEW_TITLE_INPUT))
            title_input.clear()
            title_input.send_keys("This is a test review title by selenium")
            print("Review title filled successfully")
            
            # Fill review text
            review_textarea = self.wait.until(EC.element_to_be_clickable(self.REVIEW_TEXT_AREA))
            review_textarea.clear()
            review_textarea.send_keys("This is a test review text by selenium")
            print("Review text filled successfully")
            
            # Select variant (select the first available option)
            try:
                variant_select = self.wait.until(EC.element_to_be_clickable(self.VARIANT_SELECT))
                # Click to open dropdown
                variant_select.click()
                time.sleep(1)
                # Select the first option (index 1, since 0 is "Select a variant")
                options = variant_select.find_elements(By.TAG_NAME, "option")
                if len(options) > 1:
                    options[1].click()
                    print("Product variant selected successfully")
            except Exception as e:
                print(f"Could not select variant: {e}")
            
            print("Review form filled successfully")
            return True
            
        except Exception as e:
            print(f"Error filling review form: {e}")
            return False
    
    def submit_review_and_verify(self):
        """Click submit review button and verify success alert."""
        try:
            # Click submit review button
            submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_REVIEW_BUTTON))
            submit_button.click()
            print("Submit review button clicked successfully")
            
            # Wait for alert and verify message
            time.sleep(2)
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert message: {alert_text}")
                
                if alert_text == "Thank you! Your review has been submitted successfully.":
                    alert.accept()
                    print("Review submitted successfully!")
                    return True
                else:
                    alert.accept()
                    print(f"Unexpected alert message: {alert_text}")
                    return False
                    
            except Exception as e:
                print(f"No alert found or error handling alert: {e}")
                return False
                
        except Exception as e:
            print(f"Error submitting review: {e}")
            return False
    
    def get_buy_now_button_prices(self):
        """Extract saved amount and total price from BUY NOW button."""
        try:
            buy_now_button = self.wait.until(EC.presence_of_element_located(self.BUY_NOW_BUTTON))
            
            # Find the price container within the button
            price_container = buy_now_button.find_element(By.XPATH, ".//div[@class='text-xs opacity-90']")
            
            # Extract original price (line-through)
            original_price_element = price_container.find_element(By.XPATH, ".//span[@class='line-through']")
            original_price = original_price_element.text.strip()
            
            # Extract discounted price
            discounted_price_element = price_container.find_element(By.XPATH, ".//span[@class='ml-1']")
            discounted_price = discounted_price_element.text.strip()
            
            # Calculate saved amount
            original_value = float(original_price.replace('₹', '').replace(',', ''))
            discounted_value = float(discounted_price.replace('₹', '').replace(',', ''))
            saved_amount = original_value - discounted_value
            
            print(f"\n[INFO] BUY NOW Button Prices:")
            print(f"  - Original Price: {original_price}")
            print(f"  - Discounted Price: {discounted_price}")
            print(f"  - Saved Amount: ₹{saved_amount:.2f}")
            
            return {
                'original_price': original_price,
                'discounted_price': discounted_price,
                'saved_amount': f"₹{saved_amount:.2f}"
            }
            
        except Exception as e:
            print(f"Error getting BUY NOW button prices: {e}")
            return None
    
    def click_buy_now_button(self):
        """Click BUY NOW button and handle alert."""
        try:
            buy_now_button = self.wait.until(EC.element_to_be_clickable(self.BUY_NOW_BUTTON))
            
            # Scroll to the button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", buy_now_button)
            time.sleep(1)
            
            # Click the button
            self.driver.execute_script("arguments[0].click();", buy_now_button)
            print("BUY NOW button clicked successfully")
            
            # Wait for alert and handle it
            time.sleep(2)
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert message: {alert_text}")
                alert.accept()
                print("Alert accepted successfully")
                
                # Wait for page to load and get address information
                time.sleep(3)
                try:
                    address_info = self.wait.until(EC.presence_of_element_located(self.ADDRESS_INFO))
                    address_text = address_info.text.strip()
                    print(f"Address information: {address_text}")
                except Exception as e:
                    # Try to find any element with address-related text
                    try:
                        all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Found') or contains(text(), 'address')]")
                        if all_elements:
                            for element in all_elements:
                                if element.text.strip():
                                    print(f"Found address-related text: {element.text.strip()}")
                        else:
                            print("No address information found on page")
                    except Exception as e2:
                        print(f"No address information found: {e}")
                
                return True
            except Exception as e:
                print(f"No alert found or error handling alert: {e}")
                return False
                
        except Exception as e:
            print(f"Error clicking BUY NOW button: {e}")
            return False
    
    def click_address_and_place_order(self):
        """Click on address area and handle order placement alert."""
        try:
            address_area = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_AREA))
            
            # Scroll to the address area
            self.driver.execute_script("arguments[0].scrollIntoView(true);", address_area)
            time.sleep(1)
            
            # Click the address area
            self.driver.execute_script("arguments[0].click();", address_area)
            print("Address area clicked successfully")
            
            # Wait for order placement alert
            time.sleep(2)
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"Order placement alert: {alert_text}")
                alert.accept()
                print("Order placement alert accepted successfully")
                return True
            except Exception as e:
                print(f"No order placement alert found: {e}")
                return False
                
        except Exception as e:
            print(f"Error clicking address area: {e}")
            return False