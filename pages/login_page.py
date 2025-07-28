from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open_sign_in_modal(self):
        sign_in_button = self.driver.find_element(By.XPATH, "//span[text()='Sign In']")
        sign_in_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )

    def login(self, email, password):
        self.driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(email)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("dashboard")
        )
