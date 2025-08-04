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