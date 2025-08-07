from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MainZonePage:
    # Locators
    CATEGORY_BUTTON = (By.XPATH, "//button[contains(@class, 'text-xs') and contains(@class, 'md:text-sm') and contains(@class, 'font-medium') and contains(text(), 'Charger')]")
    ZONE_INDICATOR = (By.XPATH, "//span[normalize-space()='Price -- High to Low']")
    BRAND_CHECKBOXES = (By.XPATH, "//div[contains(@class, 'max-h-40') and contains(@class, 'overflow-y-auto') and contains(@class, 'custom-scrollbar')]//label[input[@type='checkbox']]")
    BRAND_LABELS = (By.XPATH, "//div[contains(@class, 'max-h-40') and contains(@class, 'overflow-y-auto') and contains(@class, 'custom-scrollbar')]//label")
    BRAND_SEARCH_BOX = (By.XPATH, "//input[@placeholder='Search brands...']")
    PRODUCT_SEARCH_BOX = (By.XPATH, "//input[@placeholder='🔍 Search products (auto-search after 1.5s or press Enter)...']")
    CHECKBOX_INPUT = (By.XPATH, ".//input[@type='checkbox']")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def clicked_on_category(self):
        try:
            category_button = self.wait.until(EC.element_to_be_clickable(self.CATEGORY_BUTTON))
            category_button.click()
            return True
        except:
            return False

    def is_on_zone_page(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.ZONE_INDICATOR))
            return True
        except:
            return False
    
    def check_brand_checkboxes(self):
        """Check which brand checkboxes are checked and unchecked."""
        try:
            labels = self.driver.find_elements(*self.BRAND_CHECKBOXES)
            checked_brands = []
            unchecked_brands = []
            for label in labels:
                checkbox = label.find_element(*self.CHECKBOX_INPUT)
                brand_name = label.text.strip()
                if checkbox.is_selected():
                    checked_brands.append(brand_name)
                    print(f"✅ {brand_name} is checked")
                else:
                    unchecked_brands.append(brand_name)
                    print(f"❌ {brand_name} is not checked")
            print(f"\n📊 Total brands: {len(labels)}")
            print(f"✅ Checked brands: {len(checked_brands)}")
            print(f"❌ Unchecked brands: {len(unchecked_brands)}")
            return {
                'checked': checked_brands,
                'unchecked': unchecked_brands,
                'total': len(labels)
            }
        except Exception as e:
            print(f"Error checking brand checkboxes: {e}")
            return None
    
    def found_brand_names(self):
        """Find and display brand names from search results."""
        try:
            labels = self.driver.find_elements(*self.BRAND_LABELS)
            
            brand_names = []
            
            for label in labels:
                brand_name = label.text.strip()
                if brand_name:  # Only add non-empty brand names
                    brand_names.append(brand_name)
                    print(f"📱 Found brand: {brand_name}")
            
            if len(brand_names) == 0:
                print("📊 Found 0 brands according to search result")
            else:
                print(f"📊 Found {len(brand_names)} brands according to search result")
            
            return brand_names
        except Exception as e:
            print(f"Error finding brand names: {e}")
            return []

    def search_brand_name(self, brand_name, search_type="brand"):
        try:
            if search_type == "brand":
                search_box = self.wait.until(EC.presence_of_element_located(self.BRAND_SEARCH_BOX))
            else:
                search_box = self.wait.until(EC.presence_of_element_located(self.PRODUCT_SEARCH_BOX))
            search_box.clear()
            search_box.send_keys(brand_name)
            return True
        except Exception as e:
            print(f"Error searching for brand: {e}")
            return False
    
    def count_products_on_page(self, url_pattern):
        """Count number of products on page based on image URL pattern."""
        try:
            # Scroll to load all products
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Find all images with the specified URL pattern
            product_images = self.driver.find_elements(By.XPATH, f"//img[contains(@src, '{url_pattern}')]")
            
            print(f"📊 Number of products on web page by search applied: {len(product_images)}")
            
            return len(product_images)
        except Exception as e:
            print(f"Error counting products: {e}")
            return 0
