from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class MainDashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_on_dashboard(self, dashboard_xpath):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, dashboard_xpath))
            )
            return True
        except:
            return False
    
    def search_product(self, search_term, search_box_selector):
        search_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, search_box_selector))
        )
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)
        
    def get_search_results(self, results_selector):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, results_selector))
            )
            return True
        except:
            return False
    
    def clear_search(self, search_box_selector):
        search_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, search_box_selector))
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        return search_box.get_attribute("value") == ""

    def apply_brand_filter(self, filter_xpath):
        """Scrolls to and clicks the brand filter button using ActionChains."""
        brand_filter_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, filter_xpath))
        )

        # Move to the element using ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(brand_filter_button).click().perform()
    
    def count_products_by_brand(self, brand_xpath, wait_xpath=None):
        """Count products with specific brand filter."""
        try:
            # Wait for brand elements to be present
            if wait_xpath:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, wait_xpath))
                )
            
            # Find elements using provided xpath
            brand_elements = self.driver.find_elements(By.XPATH, brand_xpath)
            return len(brand_elements)
        except:
            return 0
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
    
    def find_images_with_url_pattern(self, url_pattern):
        """Find all images that contain the specified URL pattern."""
        try:
            # Wait for images to load
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            
            # Find all images with the specified URL pattern
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

