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
    
    def clear_search(self):
        search_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search for products...']"))
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        return search_box.get_attribute("value") == ""

    def apply_brand_filter(self):
        """Scrolls to and clicks the brand filter button using ActionChains."""
        brand_filter_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[4]/div/div[1]/button[4]"))
        )

        # Move to the element using ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(brand_filter_button).click().perform()
    
    def count_products_by_brand(self, brand_name):
        """Count products with specific brand filter."""
        try:
            # Wait for brand elements to be present
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-blue-600') and contains(@class, 'bg-blue-50')]")
            ))
            
            # Find elements with more flexible matching
            brand_elements = self.driver.find_elements(
                By.XPATH, f"//div[contains(@class, 'text-blue-600') and contains(@class, 'bg-blue-50') and contains(text(), '{brand_name}')]"
            )
            return len(brand_elements)
        except:
            return 0
