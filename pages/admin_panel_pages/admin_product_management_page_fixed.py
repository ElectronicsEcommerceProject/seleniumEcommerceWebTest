from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class AdminProductManagementPage:
    # ================= LOCATORS =================
    PRODUCT_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Product Management']")
    PRODUCT_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Product Management']")
    RESET_FILTERS_BUTTON = (By.XPATH, "//button[contains(@class, 'bg-gray-200') and contains(text(), 'Reset Filters')]")
    EDIT_BUTTON = (By.XPATH, "//button[@aria-label='Edit categories']")
    BRAND_EDIT_BUTTON = (By.XPATH, "//button[@aria-label='Edit brands']")
    PRODUCT_EDIT_BUTTON = (By.XPATH, "//button[@aria-label='Edit products']")
    SEARCH_CATEGORY_INPUT = (By.XPATH, "//input[@placeholder='Search categories...']")
    CATEGORY_TABLE = (By.XPATH, "//body/div[@id='root']/div[@class='bg-gray-100 font-sans min-h-screen flex flex-col']/div[@class='flex flex-1']/main[@class='flex-1 pt-/div[@class='min-h-screen bg-gray-100 p-2 sm:p-4 md:p-6']/div[@class='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 md:gap-6']/div[1]")
    CATEGORY_CONTAINER = (By.XPATH, "//h2[contains(text(),'Categories')]/ancestor::div[contains(@class, 'bg-white')]")
    CATEGORY_TABLE_BODY = (By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
    TABLE_ROWS = (By.XPATH, ".//tr")
    NO_RESULTS_MESSAGE = (By.XPATH, ".//*[contains(text(), 'No') and contains(text(), 'found')]")
    CELL_NAME = (By.XPATH, ".//td[1]//div")
    CELL_SLUG = (By.XPATH, ".//td[2]//div")
    CELL_ROLE = (By.XPATH, ".//td[3]//div")
    
    # Brand table locators
    SEARCH_BRAND_INPUT = (By.XPATH, "//input[@placeholder='Search brands...']")
    BRAND_CONTAINER = (By.XPATH, "//h2[text()='Brands']/ancestor::div[contains(@class, 'bg-white rounded-xl')]")
    BRAND_TABLE_BODY = (By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
    BRAND_CELL_NAME = (By.XPATH, ".//td[1]//div")
    BRAND_CELL_SLUG = (By.XPATH, ".//td[2]//div")
    
    # Product table locators
    SEARCH_PRODUCT_INPUT = (By.XPATH, "//input[@placeholder='Search products...']")
    PRODUCT_CONTAINER = (By.XPATH, "//h2[text()='Products']/ancestor::div[contains(@class, 'bg-white rounded-xl')]")
    PRODUCT_TABLE_BODY = (By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
    PRODUCT_CELL_NAME = (By.XPATH, ".//td[1]//div")
    PRODUCT_CELL_SLUG = (By.XPATH, ".//td[2]//div")
    PRODUCT_CELL_PRICE = (By.XPATH, ".//td[3]//div")
    PRODUCT_CELL_RATING = (By.XPATH, ".//td[4]//div")
    
    # Product variants table locators
    SEARCH_VARIANT_INPUT = (By.XPATH, "//input[@placeholder='Search variants...']")
    VARIANT_CONTAINER = (By.XPATH, "//h2[text()='Product Variants']/ancestor::div[contains(@class, 'bg-white rounded-xl')]")
    VARIANT_TABLE_BODY = (By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
    VARIANT_CELL_NAME = (By.XPATH, ".//td[1]//div")
    VARIANT_CELL_PRODUCT = (By.XPATH, ".//td[2]//div")
    VARIANT_CELL_PRICE = (By.XPATH, ".//td[3]//div")
    VARIANT_CELL_STOCK = (By.XPATH, ".//td[4]//div")
    VARIANT_CELL_DISCOUNT = (By.XPATH, ".//td[5]//div")
    VARIANT_CELL_MIN_QTY = (By.XPATH, ".//td[6]//div")
    
    # Attribute values table locators
    SEARCH_ATTRIBUTE_INPUT = (By.XPATH, "//input[@placeholder='Search attribute values...']")
    ATTRIBUTE_CONTAINER = (By.XPATH, "//h2[text()='Attribute Values']/ancestor::div[contains(@class, 'bg-white rounded-xl')]")
    ATTRIBUTE_TABLE_BODY = (By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
    ATTRIBUTE_CELL_ATTRIBUTE = (By.XPATH, ".//td[1]//div")
    ATTRIBUTE_CELL_VALUE = (By.XPATH, ".//td[2]//div")
    
    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Global variables to store table data
        self.category_data = []
        self.brand_data = []
        self.product_data = []
        self.variant_data = []
        self.attribute_data = []
        
        # Variables to store original values for editing
        self.original_name = ""
        self.original_slug = ""
        self.original_role = ""
        
        # Variables for brand editing
        self.original_brand_name = ""
        self.original_brand_slug = ""
        
        # Variables for product editing
        self.original_product_name = ""
        self.original_product_slug = ""

    def edit_product_and_revert(self):
        """Edit first product and then revert back to original values"""
        try:
            import time
            time.sleep(2)
            
            # Find product container
            product_container = self.wait.until(EC.presence_of_element_located(self.PRODUCT_CONTAINER))
            table_body = product_container.find_element(*self.PRODUCT_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                
                # Store original values
                name_cell = first_row.find_elements(*self.PRODUCT_CELL_NAME)
                slug_cell = first_row.find_elements(*self.PRODUCT_CELL_SLUG)
                
                self.original_product_name = name_cell[0].text.strip() if name_cell else ""
                self.original_product_slug = slug_cell[0].text.strip() if slug_cell else ""
                
                print(f"📝 Original product values - Name: {self.original_product_name}, Slug: {self.original_product_slug}")
                
                # Click edit button
                edit_button = first_row.find_element(*self.PRODUCT_EDIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", edit_button)
                
                time.sleep(2)  # Wait for edit form to load
                
                # Edit the values (add "_edited" suffix)
                name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='name' or contains(@placeholder,'name') or contains(@id,'name')]")))
                slug_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='slug' or contains(@placeholder,'slug') or contains(@id,'slug')]")))
                
                # Clear and enter new values
                self.driver.execute_script("arguments[0].value = '';", name_input)
                name_input.send_keys(self.original_product_name + "_edited")
                
                self.driver.execute_script("arguments[0].value = '';", slug_input)
                slug_input.send_keys(self.original_product_slug + "_edited")
                
                # Save changes
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
                save_button.click()
                
                # Handle alert immediately after save
                time.sleep(1)
                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    time.sleep(2)
                except:
                    time.sleep(3)
                
                print("✅ Product edited successfully")
                
                # Now revert back to original values
                self.revert_product_edit()
                
            return True
        except Exception as e:
            print(f"❌ Error editing product: {e}")
            return False
    
    def revert_product_edit(self):
        """Revert product back to original values"""
        try:
            import time
            time.sleep(3)  # Wait for page refresh
            
            # Find product container
            product_container = self.wait.until(EC.presence_of_element_located(self.PRODUCT_CONTAINER))
            table_body = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")))
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            # Find row with the modified name (original + "_edited")
            target_name = self.original_product_name + "_edited"
            for row in rows:
                name_cell = row.find_elements(*self.PRODUCT_CELL_NAME)
                if name_cell and name_cell[0].text.strip() == target_name:
                    edit_button = row.find_element(*self.PRODUCT_EDIT_BUTTON)
                    self.driver.execute_script("arguments[0].click();", edit_button)
                    break
            
            time.sleep(2)
            
            # Revert to original values
            name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='name' or contains(@placeholder,'name') or contains(@id,'name')]")))
            slug_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='slug' or contains(@placeholder,'slug') or contains(@id,'slug')]")))
            
            self.driver.execute_script("arguments[0].value = '';", name_input)
            name_input.send_keys(self.original_product_name)
            
            self.driver.execute_script("arguments[0].value = '';", slug_input)
            slug_input.send_keys(self.original_product_slug)
            
            # Save reverted changes
            save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
            save_button.click()
            
            # Handle alert immediately after save
            time.sleep(1)
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(2)
            except:
                time.sleep(3)
            
            print("✅ Product reverted to original values successfully")
            
            return True
        except Exception as e:
            # Handle any remaining alerts before reporting error
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
            print(f"❌ Error reverting product: {e}")
            return False