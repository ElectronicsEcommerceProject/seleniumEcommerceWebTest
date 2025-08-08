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