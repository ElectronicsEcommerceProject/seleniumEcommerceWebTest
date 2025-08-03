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
    
    def check_brand_checkboxes(self, labels_xpath):
        """Check which brand checkboxes are checked and unchecked. Accepts XPath for labels as argument."""
        try:
            labels = self.driver.find_elements(By.XPATH, labels_xpath)
            checked_brands = []
            unchecked_brands = []
            for label in labels:
                checkbox = label.find_element(By.XPATH, ".//input[@type='checkbox']")
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

    def search_brand_name(self, brand_name, search_box_xpath):
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, search_box_xpath))
            )
            search_box.clear()
            search_box.send_keys(brand_name)
            return True
        except Exception as e:
            print(f"Error searching for brand: {e}")
            return False
