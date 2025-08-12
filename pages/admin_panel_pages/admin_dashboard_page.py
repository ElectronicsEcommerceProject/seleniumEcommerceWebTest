from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminDashboardPage:
    """Page Object Model for Admin Dashboard Page"""

    # ================= LOCATORS =================
    TOTAL_USERS_HEADER = (By.XPATH, "//h2[normalize-space()='Total Users']")
    ADD_PRODUCT_BUTTON = (By.XPATH, "//button[normalize-space()='Add Product']")
    CREATE_COUPON_BUTTON = (By.XPATH, "//button[normalize-space()='Create Coupon']")

    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= METHODS =================
    def verifying_adminDashboard(self):
        """Verify if user is on admin dashboard page"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.TOTAL_USERS_HEADER)
            )
            return True
        except Exception as e:
            print("Error verifying admin dashboard:", e)
            return False

    def checking_button_working(self):
        """Check if buttons work and print redirect URLs"""
        current_url = self.driver.current_url
        
        # Test Add Product button
        try:
            add_product_btn = self.wait.until(
                EC.element_to_be_clickable(self.ADD_PRODUCT_BUTTON)
            )
            add_product_btn.click()
            self.wait.until(lambda driver: driver.current_url != current_url)
            print(f"Add Product redirected to: {self.driver.current_url}")
            self.driver.back()
            self.wait.until(lambda driver: driver.current_url == current_url)
        except Exception as e:
            print(f"Add Product button error: {e}")
        
        # Test Create Coupon button
        try:
            create_coupon_btn = self.wait.until(
                EC.element_to_be_clickable(self.CREATE_COUPON_BUTTON)
            )
            create_coupon_btn.click()
            self.wait.until(lambda driver: driver.current_url != current_url)
            print(f"Create Coupon redirected to: {self.driver.current_url}")
            self.driver.back()
            self.wait.until(lambda driver: driver.current_url == current_url)
        except Exception as e:
            print(f"Create Coupon button error: {e}")
            
        return True