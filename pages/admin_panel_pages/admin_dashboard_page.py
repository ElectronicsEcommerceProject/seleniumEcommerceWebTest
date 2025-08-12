from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminDashboardPage:
    """Page Object Model for Admin Dashboard Page"""

    # ================= LOCATORS =================
    TOTAL_USERS_HEADER = (By.XPATH, "//h2[normalize-space()='Total Users']")

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