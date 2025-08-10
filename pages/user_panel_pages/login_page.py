from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_sign_in_modal(self):
        sign_in_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='text-sm font-medium' and text()='Sign In']"))
        )
        hover = ActionChains(self.driver).move_to_element(sign_in_button)
        hover.perform()
        
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']"))
        )
        login_button.click()

    def login(self, email, password):
        email_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.send_keys(email)
        
        password_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)
        
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[type='submit'].w-full.bg-gradient-to-r.from-blue-600.to-blue-700"))
        )
        login_button.click()
        
    def is_login_successful(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Buttonphone')]"))
            )
            return True
        except:
            return False
