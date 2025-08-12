from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class LoginPage:
    """Page Object Model for Login Page"""

    # ================= LOCATORS =================
    LOGIN_BUTTON = (By.XPATH, "//button[@class='flex items-center space-x-1 bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-md transition-colors']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class,'w-full')]")
    LOGIN_SUCCESS_INDICATOR = (By.XPATH, "//div[@class='text-sm md:text-base font-medium bg-white/10 px-3 py-1 rounded-md inline-block w-fit']")
    ADMIN_BUTTON = (By.XPATH, "//button[contains(text(),'Admin')]")

    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= METHODS =================
    def open_sign_in_modal(self):
        """Hover and click on sign in button"""
        try:
            sign_in_button = self.wait.until(
                EC.visibility_of_element_located(self.LOGIN_BUTTON)
            )
            ActionChains(self.driver).move_to_element(sign_in_button).click().perform()
            return True
        except Exception as e:
            print("Error in open_sign_in_modal:", e)
            return False

    def login(self, email, password):
        """Fill login form and submit"""
        try:
            email_input = self.wait.until(
                EC.visibility_of_element_located(self.EMAIL_INPUT)
            )
            email_input.send_keys(email)

            password_input = self.wait.until(
                EC.presence_of_element_located(self.PASSWORD_INPUT)
            )
            password_input.send_keys(password)

            submit_btn = self.wait.until(
                EC.element_to_be_clickable(self.SUBMIT_BUTTON)
            )
            submit_btn.click()
            return True
        except Exception as e:
            print("Error in login:", e)
            return False

    def is_login_successful(self):
        """Check if login is successful"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.LOGIN_SUCCESS_INDICATOR)
            )
            return True
        except Exception as e:
            print("Login not successful:", e)
            return False

    def click_admin_button(self):
        """Click the Admin button"""
        try:
            admin_btn = self.wait.until(
                EC.element_to_be_clickable(self.ADMIN_BUTTON)
            )
            admin_btn.click()
            return True
        except Exception as e:
            print("Error in click_admin_button:", e)
            return False
