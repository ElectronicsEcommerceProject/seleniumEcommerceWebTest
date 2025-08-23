from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class AdminOrderManagementPage:
    # ================= LOCATORS =================
    ORDER_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Order Management']")
    ORDER_MANAGEMENT_TITLE = (By.XPATH, "(//th[normalize-space()='Order ID'])[1]")
    
    
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


        """Print summary of all table data collected"""
        print("\n" + "="*50)
        print("📊 SUMMARY OF ALL TABLE DATA")
        print("="*50)
        print(f"📦 Orders table has {len(self.order_data)} items")
        print("="*50)