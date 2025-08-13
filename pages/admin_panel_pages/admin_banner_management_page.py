from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminBannerManagementPage:
    """Page Object Model for Admin Banner Management Page"""

    # ================= LOCATORS =================
    BANNER_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Banner Management']")

    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= METHODS =================
    def verifying_bannerManagement(self):
        """Verify if user is on banner management page"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.BANNER_MANAGEMENT_TITLE)
            )
            return True
        except Exception as e:
            print("Error verifying banner management page:", e)
            return False