from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminBannerManagementPage:
    """Page Object Model for Admin Banner Management Page"""

    # ================= LOCATORS =================
    BANNER_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Banner Management']")
    DEACTIVATE_BUTTON = (By.XPATH, "(//button[@class='px-3 py-1 rounded text-xs font-medium bg-red-100 text-red-800 hover:bg-red-200'][normalize-space()='Deactivate'])[1]")
    ACTIVATE_BUTTON = (By.XPATH, "(//button[normalize-space()='Activate'])[1]")
    STATUS_SPAN = (By.XPATH, "(//span[@class='px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800'])[1]")
    EDIT_BUTTON = (By.XPATH, "(//*[name()='path'])[23]")

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

    def clicking_button(self):
        """Click activate or deactivate button and print status text, then revert back"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            # First click
            button = None
            try:
                button = self.wait.until(
                    EC.presence_of_element_located(self.DEACTIVATE_BUTTON)
                )
            except:
                button = self.wait.until(
                    EC.presence_of_element_located(self.ACTIVATE_BUTTON)
                )
            
            print(f"Button text before clicking: {button.text}")
            ActionChains(self.driver).move_to_element(button).click().perform()
            
            status_span = self.wait.until(
                EC.presence_of_element_located(self.STATUS_SPAN)
            )
            print(f"Status text after clicking: {status_span.text}")
            
            # Second click to revert back
            try:
                button = self.wait.until(
                    EC.presence_of_element_located(self.DEACTIVATE_BUTTON)
                )
            except:
                button = self.wait.until(
                    EC.presence_of_element_located(self.ACTIVATE_BUTTON)
                )
            
            print(f"Button text before reverting: {button.text}")
            ActionChains(self.driver).move_to_element(button).click().perform()
            
            status_span = self.wait.until(
                EC.presence_of_element_located(self.STATUS_SPAN)
            )
            print(f"Status text after reverting: {status_span.text}")
            return True
        except Exception as e:
            print("Error clicking button:", e)
            return False

    def clicking_edit_button(self):
        """Click edit button"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            edit_btn = self.wait.until(
                EC.presence_of_element_located(self.EDIT_BUTTON)
            )
            ActionChains(self.driver).move_to_element(edit_btn).click().perform()
            return True
        except Exception as e:
            print("Error clicking edit button:", e)
            return False