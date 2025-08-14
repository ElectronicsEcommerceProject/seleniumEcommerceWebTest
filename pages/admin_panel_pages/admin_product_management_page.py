from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminProductManagementPage:
    # ================= LOCATORS =================
    PRODUCT_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Product Management']")
    PRODUCT_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Product Management']")
    
    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= METHODS =================

    def navigate_to_product_management(self):
        """Click on Product Management link"""
        try:
            banner_link = self.wait.until(
                EC.element_to_be_clickable(self.PRODUCT_MANAGEMENT_LINK)
            )
            banner_link.click()
            return True
        except Exception as e:
            print("Error navigating to Product management:", e)
            return False

    def verifying_productManagement(self):
        """Verify if user is on Product management page"""
        print("🔍 Verifying Product Management page...")
        try:
            self.wait.until(
                EC.presence_of_element_located(self.PRODUCT_MANAGEMENT_TITLE)
            )
            print("✅ Product Management page verified successfully")
            return True
        except Exception as e:
            print("❌ Error verifying Product management page:", e)
            return False