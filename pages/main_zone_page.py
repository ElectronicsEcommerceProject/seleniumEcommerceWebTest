from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainZonePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def clicked_on_category(self, category_xpath):
        try:
            category_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, category_xpath))
            )
            category_button.click()
            return True
        except:
            return False

    def is_on_zone_page(self, zone_xpath):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, zone_xpath))
            )
            return True
        except:
            return False