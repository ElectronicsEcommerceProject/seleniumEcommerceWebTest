from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BuyNowPage:
    """Page object for the Buy Now page."""


    def __init__(self, driver):
            self.driver = driver
            self.wait = WebDriverWait(driver, 10)
    
    def click_on_product(self, product_xpath):
        """Click on a product based on provided xpath."""
        try:
            product_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, product_xpath))
            )
            
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
    
    def get_product_details(self, details_xpath):
        """Extract and print product details like price, SKU, etc."""
        try:
            details_container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, details_xpath))
            )
            
            # Find all key-value pairs
            detail_rows = details_container.find_elements(By.XPATH, ".//div[contains(@class, 'flex') and contains(@class, 'justify-between')]")
            
            print("\n📋 Product Details:")
            for row in detail_rows:
                try:
                    spans = row.find_elements(By.TAG_NAME, "span")
                    if len(spans) >= 2:
                        key = spans[0].text.strip()
                        value = spans[1].text.strip()
                        print(f"  {key} {value}")
                except:
                    continue
            
            return True
        except Exception as e:
            print(f"Error getting product details: {e}")
            return False
    
    def get_quantity_info(self, quantity_input_xpath):
        """Get quantity information from the number input field."""
        try:
            quantity_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, quantity_input_xpath))
            )
            
            min_quantity = quantity_input.get_attribute("min")
            current_value = quantity_input.get_attribute("value")
            
            print(f"\n🔢 Quantity Information:")
            print(f"  Min quantity to order: {min_quantity}")
            print(f"  Current quantity: {current_value}")
            
            return True
        except Exception as e:
            print(f"Error getting quantity info: {e}")
            return False
    
    def click_button(self, button_xpath):
        """Click on a button based on provided xpath."""
        try:
            button_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            
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
    
    def get_input(self, input_xpath, quantity_value):
        """Enter value into an input field based on provided xpath."""
        try:
            input_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, input_xpath))
            )
            
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