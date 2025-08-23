from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class AdminOrderManagementPage:
    # ================= LOCATORS =================
    ORDER_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Order Management']")
    ORDER_MANAGEMENT_TITLE = (By.XPATH, "(//th[normalize-space()='Order ID'])[1]")
    ORDER_ROWS = (By.XPATH, "//tbody/tr")
    PAGINATION_BUTTONS = (By.XPATH, "//div[contains(@class, 'flex-wrap')]//button")
    
    
    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Global variables to store table data
        self.order_data = []
        
        # Variables to store original values for editing
        self.original_order_id = ""
        self.original_order_status = ""

    # ================= METHODS =================

    def navigate_to_order_management(self):
        """Click on Order Management link"""
        try:
            order_link = self.wait.until(
                EC.element_to_be_clickable(self.ORDER_MANAGEMENT_LINK)
            )
            order_link.click()
            return True
        except Exception as e:
            print("Error navigating to Order management:", e)
            return False

    def verifying_orderManagement(self):
        """Verify if user is on Order management page"""
        print("🔍 Verifying Order Management page...")
        try:
            self.wait.until(
                EC.presence_of_element_located(self.ORDER_MANAGEMENT_TITLE)
            )
            print("✅ Order Management page verified successfully")
            return True
        except Exception as e:
            print("❌ Error verifying Order management page:", e)
            return False

    def count_order_items(self):
        """Counts the number of order items"""
        try:
            order_rows = self.wait.until(
                EC.presence_of_all_elements_located(self.ORDER_ROWS)
            )
            return len(order_rows)
        except Exception as e:
            print("Error counting order items:", e)
            return 0

    def count_all_order_items_with_pagination(self):
        """Counts all order items across all pages using pagination."""
        total_order_items = 0
        page_number = 1
        while True:
            print(f"Counting items on page {page_number}...")
            total_order_items += self.count_order_items()
            
            try:
                pagination_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PAGINATION_BUTTONS)
                )
                
                next_button = None
                for button in pagination_buttons:
                    if button.text == str(page_number + 1):
                        next_button = button
                        break
                
                if next_button:
                    print(f"Navigating to page {page_number + 1}...")
                    time.sleep(2) # wait for page to load
                    try:
                        next_button.click()
                    except Exception as e:
                        print(f"Could not click button normally, trying with javascript: {e}")
                        self.driver.execute_script("arguments[0].click();", next_button)

                    page_number += 1
                    # Wait for the next page to load, e.g., by waiting for the order rows to be present
                    self.wait.until(
                        EC.presence_of_all_elements_located(self.ORDER_ROWS)
                    )
                else:
                    print("No more pages to navigate.")
                    break
            except Exception as e:
                print(f"No more pagination buttons found or error clicking next page: {e}")
                break
                
        return total_order_items

    def print_summary(self):
        """Print summary of all table data collected"""
        print("\n" + "="*50)
        print("📊 SUMMARY OF ALL TABLE DATA")
        print("="*50)
        print(f"📦 Orders table has {len(self.order_data)} items")
        print("="*50)