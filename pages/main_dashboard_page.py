from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class MainDashboardPage:
    # Locators
    DASHBOARD_INDICATOR = (By.XPATH, "//button[contains(text(),'Buttonphone')]")
    SEARCH_BOX = (By.CSS_SELECTOR, "input[placeholder='Search for products...']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[class*='product'], [class*='item'], [class*='card']")
    BRAND_FILTER_BUTTON = (By.XPATH, "//button[contains(@class, 'px-4') and contains(@class, 'py-2') and contains(@class, 'rounded-full') and text()='Vivo']")
    VIVO_BRAND_ELEMENT = (By.XPATH, "//div[contains(@class, 'text-blue-600') and contains(@class, 'bg-blue-50') and contains(text(), 'Vivo')]")
    BRAND_WAIT_ELEMENT = (By.XPATH, "//div[contains(@class, 'text-blue-600') and contains(@class, 'bg-blue-50')]")
    IMAGES = (By.TAG_NAME, "img")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_on_dashboard(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.DASHBOARD_INDICATOR))
            return True
        except:
            return False
    
    def search_product(self, search_term):
        search_box = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)
        
    def get_search_results(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS))
            return True
        except:
            return False
    
    def clear_search(self):
        search_box = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
        search_box.click()
        search_box.clear()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        return search_box.get_attribute("value") == ""

    def apply_brand_filter(self):
        """Scrolls to and clicks the brand filter button using ActionChains."""
        brand_filter_button = self.wait.until(EC.element_to_be_clickable(self.BRAND_FILTER_BUTTON))
        actions = ActionChains(self.driver)
        actions.move_to_element(brand_filter_button).click().perform()
    
    def count_products_by_brand(self):
        """Count products with specific brand filter."""
        try:
            self.wait.until(EC.presence_of_element_located(self.BRAND_WAIT_ELEMENT))
            brand_elements = self.driver.find_elements(*self.VIVO_BRAND_ELEMENT)
            return len(brand_elements)
        except:
            return 0
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
    
    def find_images_with_url_pattern(self, url_pattern):
        """Find all images that contain the specified URL pattern."""
        try:
            self.wait.until(EC.presence_of_element_located(self.IMAGES))
            
            # Scroll down to load all images
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            import time
            time.sleep(2)
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Find all images with the specified URL pattern
            images = self.driver.find_elements(By.XPATH, f"//img[contains(@src, '{url_pattern}')]")
            print(f"Found {len(images)} images with pattern: {url_pattern}")            
            return len(images)
        except:
            return 0
    
    def click_button_by_text(self, button_text):
        """Click any button with specified text."""
        try:
            button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
            )
            
            # Scroll to the button and click
            actions = ActionChains(self.driver)
            actions.move_to_element(button).click().perform()
            return True
        except:
            return False

