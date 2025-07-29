from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainDashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_on_dashboard(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Buttonphone')]"))
            )
            return True
        except:
            return False
