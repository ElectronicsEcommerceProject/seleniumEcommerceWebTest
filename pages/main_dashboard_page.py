from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



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
    
    def search_product(self, search_term):
        search_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search for products...']"))
        )
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)
        
    def get_search_results(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='product'], [class*='item'], [class*='card']"))
            )
            return True
        except:
            return False

    def apply_brand_filter(self):
        """Scrolls to and clicks the brand filter button using ActionChains."""
        brand_filter_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[4]/div/div[1]/button[4]"))
        )

        # Move to the element using ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(brand_filter_button).click().perform()
