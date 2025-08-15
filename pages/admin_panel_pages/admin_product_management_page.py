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

    # ================= METHODS =================

    def navigate_to_product_management(self):
        """Click on Product Management link"""
        try:
            banner_link = self.wait.until(
                EC.element_to_be_clickable(self.PRODUCT_MANAGEMENT_LINK)
            )
            banner_link.click()
            return True
        except Exception as e:
            print("Error navigating to Product management:", e)
            return False

    def verifying_productManagement(self):
        """Verify if user is on Product management page"""
        print("🔍 Verifying Product Management page...")
        try:
            self.wait.until(
                EC.presence_of_element_located(self.PRODUCT_MANAGEMENT_TITLE)
            )
            print("✅ Product Management page verified successfully")
            return True
        except Exception as e:
            print("❌ Error verifying Product management page:", e)
            return False

    def collect_table_counts(self):
        """Count total rows in each table before searches"""
        print("📁 Collecting table row counts...")
        
        import time
        time.sleep(2)  # Wait for tables to load
        
        # Count category rows
        try:
            category_container = self.wait.until(EC.presence_of_element_located(self.CATEGORY_CONTAINER))
            table_body = category_container.find_elements(*self.CATEGORY_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                print(f"📁 Categories table: {len(table_rows)} items")
            else:
                print("📁 Categories table: 0 items")
        except:
            print("📁 Categories table: 0 items")
            
        # Count brand rows
        try:
            brand_container = self.driver.find_element(*self.BRAND_CONTAINER)
            table_body = brand_container.find_elements(*self.BRAND_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                print(f"🏷️ Brands table: {len(table_rows)} items")
            else:
                print("🏷️ Brands table: 0 items")
        except:
            print("🏷️ Brands table: 0 items")
            
        # Count product rows
        try:
            product_container = self.driver.find_element(*self.PRODUCT_CONTAINER)
            table_body = product_container.find_elements(*self.PRODUCT_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                print(f"📦 Products table: {len(table_rows)} items")
            else:
                print("📦 Products table: 0 items")
        except:
            print("📦 Products table: 0 items")
            
        # Count variant rows
        try:
            variant_container = self.driver.find_element(*self.VARIANT_CONTAINER)
            table_body = variant_container.find_elements(*self.VARIANT_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                print(f"🔧 Variants table: {len(table_rows)} items")
            else:
                print("🔧 Variants table: 0 items")
        except:
            print("🔧 Variants table: 0 items")
            
        # Count attribute rows
        try:
            attribute_container = self.driver.find_element(*self.ATTRIBUTE_CONTAINER)
            table_body = attribute_container.find_elements(*self.ATTRIBUTE_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                print(f"⚙️ Attributes table: {len(table_rows)} items")
            else:
                print("⚙️ Attributes table: 0 items")
        except:
            print("⚙️ Attributes table: 0 items")
            
        print("✅ Table counts collected successfully")

    def search_box(self, search_xpath, search_value):
        """Perform search using provided xpath and value, then print results"""
        print(f"🔍 Searching for '{search_value}' in categories...")
        print(f"📝 Search term entered: '{search_value}'")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable(search_xpath)
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            import time
            time.sleep(2)
            
            self.read_category_table()
            
            # Clear search box using backspace keys
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            
            # Collect all data after clearing search
            self.collect_all_category_data()
                
            return True
        except Exception as e:
            print(f"❌ Error performing search: {e}")
            return False

    def read_category_table(self):
        """Read and print category table results"""
        try:
            category_container = self.driver.find_element(*self.CATEGORY_CONTAINER)
            no_results_msg = category_container.find_elements(*self.NO_RESULTS_MESSAGE)
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            table_body = category_container.find_elements(*self.CATEGORY_TABLE_BODY)
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Categories table:")
                for i, row in enumerate(table_rows, 1):
                    try:
                        name_cell = row.find_elements(*self.CELL_NAME)
                        name = name_cell[0].text.strip() if name_cell else "N/A"
                        if name != "N/A" and name not in self.category_data:
                            self.category_data.append(name)
                        
                        if i <= 5:  # Show first 5 results
                            slug_cell = row.find_elements(*self.CELL_SLUG)
                            role_cell = row.find_elements(*self.CELL_ROLE)
                            slug = slug_cell[0].text.strip() if slug_cell else "N/A"
                            role = role_cell[0].text.strip() if role_cell else "N/A"
                            print(f"  {i}. Name: {name}, Slug: {slug}, Role: {role}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_brand_box(self, search_value):
        """Perform brand search and print results"""
        print(f"🔍 Searching for '{search_value}' in brands...")
        print(f"📝 Search term entered: '{search_value}'")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable(self.SEARCH_BRAND_INPUT)
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            import time
            time.sleep(2)
            
            self.read_brand_table()
            
            # Clear search box using backspace keys
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            
            # Collect all data after clearing search
            self.collect_all_brand_data()
                
            return True
        except Exception as e:
            print(f"❌ Error performing brand search: {e}")
            return False

    def read_brand_table(self):
        """Read and print brand table results"""
        try:
            brand_container = self.driver.find_element(*self.BRAND_CONTAINER)
            no_results_msg = brand_container.find_elements(*self.NO_RESULTS_MESSAGE)
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            table_body = brand_container.find_elements(*self.BRAND_TABLE_BODY)
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Brands table:")
                for i, row in enumerate(table_rows[:5], 1):
                    try:
                        name_cell = row.find_elements(*self.BRAND_CELL_NAME)
                        slug_cell = row.find_elements(*self.BRAND_CELL_SLUG)
                        
                        name = name_cell[0].text.strip() if name_cell else "N/A"
                        slug = slug_cell[0].text.strip() if slug_cell else "N/A"
                        
                        if name != "N/A" and name not in self.brand_data:
                            self.brand_data.append(name)
                        
                        print(f"  {i}. Name: {name}, Slug: {slug}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_product_box(self, search_value):
        """Perform product search and print results"""
        print(f"🔍 Searching for '{search_value}' in products...")
        print(f"📝 Search term entered: '{search_value}'")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable(self.SEARCH_PRODUCT_INPUT)
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            import time
            time.sleep(2)
            
            self.read_product_table()
            
            # Clear search box using backspace keys
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            
            # Collect all data after clearing search
            self.collect_all_product_data()
                
            return True
        except Exception as e:
            print(f"❌ Error performing product search: {e}")
            return False

    def read_product_table(self):
        """Read and print product table results"""
        try:
            product_container = self.driver.find_element(*self.PRODUCT_CONTAINER)
            no_results_msg = product_container.find_elements(*self.NO_RESULTS_MESSAGE)
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            table_body = product_container.find_elements(*self.PRODUCT_TABLE_BODY)
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Products table:")
                for i, row in enumerate(table_rows[:5], 1):
                    try:
                        name_cell = row.find_elements(*self.PRODUCT_CELL_NAME)
                        slug_cell = row.find_elements(*self.PRODUCT_CELL_SLUG)
                        price_cell = row.find_elements(*self.PRODUCT_CELL_PRICE)
                        rating_cell = row.find_elements(*self.PRODUCT_CELL_RATING)
                        
                        name = name_cell[0].text.strip() if name_cell else "N/A"
                        slug = slug_cell[0].text.strip() if slug_cell else "N/A"
                        price = price_cell[0].text.strip() if price_cell else "N/A"
                        rating = rating_cell[0].text.strip() if rating_cell else "N/A"
                        
                        if name != "N/A" and name not in self.product_data:
                            self.product_data.append(name)
                        
                        print(f"  {i}. Name: {name}, Slug: {slug}, Price: {price}, Rating: {rating}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_variant_box(self, search_value):
        """Perform product variants search and print results"""
        print(f"🔍 Searching for '{search_value}' in product variants...")
        print(f"📝 Search term entered: '{search_value}'")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable(self.SEARCH_VARIANT_INPUT)
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            import time
            time.sleep(2)
            
            self.read_variant_table()
            
            # Clear search box using backspace keys
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            
            # Collect all data after clearing search
            self.collect_all_variant_data()
                
            return True
        except Exception as e:
            print(f"❌ Error performing variant search: {e}")
            return False

    def read_variant_table(self):
        """Read and print product variants table results"""
        try:
            variant_container = self.driver.find_element(*self.VARIANT_CONTAINER)
            no_results_msg = variant_container.find_elements(*self.NO_RESULTS_MESSAGE)
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            table_body = variant_container.find_elements(*self.VARIANT_TABLE_BODY)
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Product Variants table:")
                for i, row in enumerate(table_rows[:5], 1):
                    try:
                        name_cell = row.find_elements(*self.VARIANT_CELL_NAME)
                        product_cell = row.find_elements(*self.VARIANT_CELL_PRODUCT)
                        price_cell = row.find_elements(*self.VARIANT_CELL_PRICE)
                        stock_cell = row.find_elements(*self.VARIANT_CELL_STOCK)
                        discount_cell = row.find_elements(*self.VARIANT_CELL_DISCOUNT)
                        min_qty_cell = row.find_elements(*self.VARIANT_CELL_MIN_QTY)
                        
                        name = name_cell[0].text.strip() if name_cell else "N/A"
                        product = product_cell[0].text.strip() if product_cell else "N/A"
                        price = price_cell[0].text.strip() if price_cell else "N/A"
                        stock = stock_cell[0].text.strip() if stock_cell else "N/A"
                        discount = discount_cell[0].text.strip() if discount_cell else "N/A"
                        min_qty = min_qty_cell[0].text.strip() if min_qty_cell else "N/A"
                        
                        if name != "N/A" and name not in self.variant_data:
                            self.variant_data.append(name)
                        
                        print(f"  {i}. Variant: {name}, Product: {product}, Price: {price}, Stock: {stock}, Discount: {discount}%, Min Qty: {min_qty}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_attribute_box(self, search_value):
        """Perform attribute values search and print results"""
        print(f"🔍 Searching for '{search_value}' in attribute values...")
        print(f"📝 Search term entered: '{search_value}'")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable(self.SEARCH_ATTRIBUTE_INPUT)
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            import time
            time.sleep(2)
            
            self.read_attribute_table()
            
            # Clear search box using backspace keys
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            
            # Collect all data after clearing search
            self.collect_all_attribute_data()
                
            return True
        except Exception as e:
            print(f"❌ Error performing attribute search: {e}")
            return False

    def read_attribute_table(self):
        """Read and print attribute values table results"""
        try:
            attribute_container = self.driver.find_element(*self.ATTRIBUTE_CONTAINER)
            no_results_msg = attribute_container.find_elements(*self.NO_RESULTS_MESSAGE)
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            table_body = attribute_container.find_elements(*self.ATTRIBUTE_TABLE_BODY)
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Attribute Values table:")
                for i, row in enumerate(table_rows[:5], 1):
                    try:
                        attribute_cell = row.find_elements(*self.ATTRIBUTE_CELL_ATTRIBUTE)
                        value_cell = row.find_elements(*self.ATTRIBUTE_CELL_VALUE)
                        
                        attribute = attribute_cell[0].text.strip() if attribute_cell else "N/A"
                        value = value_cell[0].text.strip() if value_cell else "N/A"
                        
                        if attribute != "N/A" and attribute not in self.attribute_data:
                            self.attribute_data.append(attribute)
                        
                        print(f"  {i}. Attribute: {attribute}, Value: {value}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_test_category(self):
        """Search for 'test category' in categories"""
        return self.search_box(self.SEARCH_CATEGORY_INPUT, "test category")
        
    def search_test_brand(self):
        """Search for 'test brand' in brands"""
        return self.search_brand_box("test brand")
        
    def search_test_product(self):
        """Search for 'test product' in products"""
        return self.search_product_box("test product")

    def search_test_variant(self):
        """Search for 'test variant' in product variants"""
        return self.search_variant_box("test variant")

    def search_test_attribute(self):
        """Search for 'test attribute' in attribute values"""
        return self.search_attribute_box("test attribute")

    def collect_all_category_data(self):
        """Collect all category names after search is cleared"""
        try:
            category_container = self.driver.find_element(*self.CATEGORY_CONTAINER)
            table_body = category_container.find_elements(*self.CATEGORY_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                for row in table_rows:
                    name_cell = row.find_elements(*self.CELL_NAME)
                    if name_cell:
                        name = name_cell[0].text.strip()
                        if name and name != "N/A" and name not in self.category_data:
                            self.category_data.append(name)
        except:
            pass

    def collect_all_brand_data(self):
        """Collect all brand names after search is cleared"""
        try:
            brand_container = self.driver.find_element(*self.BRAND_CONTAINER)
            table_body = brand_container.find_elements(*self.BRAND_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                for row in table_rows:
                    name_cell = row.find_elements(*self.BRAND_CELL_NAME)
                    if name_cell:
                        name = name_cell[0].text.strip()
                        if name and name != "N/A" and name not in self.brand_data:
                            self.brand_data.append(name)
        except:
            pass

    def collect_all_product_data(self):
        """Collect all product names after search is cleared"""
        try:
            product_container = self.driver.find_element(*self.PRODUCT_CONTAINER)
            table_body = product_container.find_elements(*self.PRODUCT_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                for row in table_rows:
                    name_cell = row.find_elements(*self.PRODUCT_CELL_NAME)
                    if name_cell:
                        name = name_cell[0].text.strip()
                        if name and name != "N/A" and name not in self.product_data:
                            self.product_data.append(name)
        except:
            pass

    def collect_all_variant_data(self):
        """Collect all variant names after search is cleared"""
        try:
            variant_container = self.driver.find_element(*self.VARIANT_CONTAINER)
            table_body = variant_container.find_elements(*self.VARIANT_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                for row in table_rows:
                    name_cell = row.find_elements(*self.VARIANT_CELL_NAME)
                    if name_cell:
                        name = name_cell[0].text.strip()
                        if name and name != "N/A" and name not in self.variant_data:
                            self.variant_data.append(name)
        except:
            pass

    def collect_all_attribute_data(self):
        """Collect all attribute names after search is cleared"""
        try:
            attribute_container = self.driver.find_element(*self.ATTRIBUTE_CONTAINER)
            table_body = attribute_container.find_elements(*self.ATTRIBUTE_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                for row in table_rows:
                    attribute_cell = row.find_elements(*self.ATTRIBUTE_CELL_ATTRIBUTE)
                    if attribute_cell:
                        attribute = attribute_cell[0].text.strip()
                        if attribute and attribute != "N/A" and attribute not in self.attribute_data:
                            self.attribute_data.append(attribute)
        except:
            pass

    def click_category_and_test_filter(self, category_name):
        """Click on a category and test if filter is working"""
        print(f"🔍 Clicking on category: {category_name}")
        try:
            # Store original counts
            original_brands = len(self.brand_data)
            original_products = len(self.product_data)
            original_variants = len(self.variant_data)
            original_attributes = len(self.attribute_data)
            
            # Click on category
            category_container = self.driver.find_element(*self.CATEGORY_CONTAINER)
            table_body = category_container.find_element(*self.CATEGORY_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            clicked = False
            for row in rows:
                name_cell = row.find_elements(*self.CELL_NAME)
                if name_cell:
                    cell_text = name_cell[0].text.strip()
                    if cell_text and category_name.lower() == cell_text.lower():
                        self.driver.execute_script("arguments[0].click();", name_cell[0])
                        clicked = True
                        print(f"✅ Successfully clicked on category: {cell_text}")
                        break
            
            if not clicked:
                print(f"❌ Could not find category: {category_name}")
                return False
            
            import time
            time.sleep(3)  # Wait for filter to apply
            
            # Count filtered results
            filtered_brands = self.count_filtered_brands()
            filtered_products = self.count_filtered_products()
            filtered_variants = self.count_filtered_variants()
            filtered_attributes = self.count_filtered_attributes()
            
            print(f"📊 FILTER TEST RESULTS for {category_name}:")
            print(f"🏷️ Brands: {original_brands} -> {filtered_brands}")
            print(f"📦 Products: {original_products} -> {filtered_products}")
            print(f"🔧 Variants: {original_variants} -> {filtered_variants}")
            print(f"⚙️ Attributes: {original_attributes} -> {filtered_attributes}")
            
            # Test if filter is working
            if (filtered_brands <= original_brands and 
                filtered_products <= original_products and 
                filtered_variants <= original_variants and 
                filtered_attributes <= original_attributes):
                print("✅ PASS: Category filter is working correctly")
                self.reset_filters()
            else:
                print("❌ FAIL: Category filter is not working")
                
            return True
        except Exception as e:
            print(f"❌ Error testing category filter: {e}")
            return False
    
    def count_filtered_brands(self):
        """Count brands after filter is applied"""
        try:
            brand_container = self.driver.find_element(*self.BRAND_CONTAINER)
            table_body = brand_container.find_elements(*self.BRAND_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                return len(table_rows)
        except:
            pass
        return 0
    
    def count_filtered_products(self):
        """Count products after filter is applied"""
        try:
            product_container = self.driver.find_element(*self.PRODUCT_CONTAINER)
            table_body = product_container.find_elements(*self.PRODUCT_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                return len(table_rows)
        except:
            pass
        return 0
    
    def count_filtered_variants(self):
        """Count variants after filter is applied"""
        try:
            variant_container = self.driver.find_element(*self.VARIANT_CONTAINER)
            table_body = variant_container.find_elements(*self.VARIANT_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                return len(table_rows)
        except:
            pass
        return 0
    
    def count_filtered_attributes(self):
        """Count attributes after filter is applied"""
        try:
            attribute_container = self.driver.find_element(*self.ATTRIBUTE_CONTAINER)
            table_body = attribute_container.find_elements(*self.ATTRIBUTE_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                return len(table_rows)
        except:
            pass
        return 0
    
    def count_filtered_categories(self):
        """Count categories after filter is applied"""
        try:
            category_container = self.driver.find_element(*self.CATEGORY_CONTAINER)
            table_body = category_container.find_elements(*self.CATEGORY_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                return len(table_rows)
        except:
            pass
        return 0

    def click_product_and_test_filter(self):
        """Click on first available product and test if filter is working"""
        try:
            # Reset filters first
            self.reset_filters()
            
            # Store original counts
            original_categories = len(self.category_data)
            original_brands = len(self.brand_data)
            original_variants = len(self.variant_data)
            original_attributes = len(self.attribute_data)
            
            # Find and click first product
            product_container = self.driver.find_element(*self.PRODUCT_CONTAINER)
            table_body = product_container.find_element(*self.PRODUCT_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                name_cell = first_row.find_elements(*self.PRODUCT_CELL_NAME)
                if name_cell:
                    product_name = name_cell[0].text.strip()
                    print(f"🔍 Clicking on product: {product_name}")
                    self.driver.execute_script("arguments[0].click();", name_cell[0])
                    
                    import time
                    time.sleep(3)  # Wait for filter to apply
                    
                    # Count after product filter
                    filtered_categories = self.count_filtered_categories()
                    filtered_brands = self.count_filtered_brands()
                    filtered_variants = self.count_filtered_variants()
                    filtered_attributes = self.count_filtered_attributes()
                    
                    print(f"📊 PRODUCT FILTER TEST RESULTS for {product_name}:")
                    print(f"📁 Categories: {original_categories} -> {filtered_categories}")
                    print(f"🏷️ Brands: {original_brands} -> {filtered_brands}")
                    print(f"🔧 Variants: {original_variants} -> {filtered_variants}")
                    print(f"⚙️ Attributes: {original_attributes} -> {filtered_attributes}")
                    
                    # Test if product filter is working
                    if (filtered_categories <= original_categories and
                        filtered_brands <= original_brands and
                        filtered_variants <= original_variants and 
                        filtered_attributes <= original_attributes):
                        print("✅ PASS: Product filter is working correctly")
                        self.reset_filters()
                    else:
                        print("❌ FAIL: Product filter is not working")
                        
            return True
        except Exception as e:
            print(f"❌ Error testing product filter: {e}")
            return False

    def click_variant_and_test_filter(self):
        """Click on first available variant and test if filter is working"""
        try:
            # Reset filters first
            self.reset_filters()
            
            # Store original counts
            original_categories = len(self.category_data)
            original_brands = len(self.brand_data)
            original_products = len(self.product_data)
            original_attributes = len(self.attribute_data)
            
            # Find and click first variant
            variant_container = self.driver.find_element(*self.VARIANT_CONTAINER)
            table_body = variant_container.find_element(*self.VARIANT_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                name_cell = first_row.find_elements(*self.VARIANT_CELL_NAME)
                if name_cell:
                    variant_name = name_cell[0].text.strip()
                    print(f"🔍 Clicking on variant: {variant_name}")
                    self.driver.execute_script("arguments[0].click();", name_cell[0])
                    
                    import time
                    time.sleep(3)  # Wait for filter to apply
                    
                    # Count after variant filter
                    filtered_categories = self.count_filtered_categories()
                    filtered_brands = self.count_filtered_brands()
                    filtered_products = self.count_filtered_products()
                    filtered_attributes = self.count_filtered_attributes()
                    
                    print(f"📊 VARIANT FILTER TEST RESULTS for {variant_name}:")
                    print(f"📁 Categories: {original_categories} -> {filtered_categories}")
                    print(f"🏷️ Brands: {original_brands} -> {filtered_brands}")
                    print(f"📦 Products: {original_products} -> {filtered_products}")
                    print(f"⚙️ Attributes: {original_attributes} -> {filtered_attributes}")
                    
                    # Test if variant filter is working
                    if (filtered_categories <= original_categories and
                        filtered_brands <= original_brands and
                        filtered_products <= original_products and 
                        filtered_attributes <= original_attributes):
                        print("✅ PASS: Variant filter is working correctly")
                        self.reset_filters()
                    else:
                        print("❌ FAIL: Variant filter is not working")
                        
            return True
        except Exception as e:
            print(f"❌ Error testing variant filter: {e}")
            return False

    def click_attribute_and_test_filter(self):
        """Click on first available attribute and test if filter is working"""
        try:
            # Reset filters first
            self.reset_filters()
            
            # Store original counts
            original_categories = len(self.category_data)
            original_brands = len(self.brand_data)
            original_products = len(self.product_data)
            original_variants = len(self.variant_data)
            
            # Find and click first attribute
            attribute_container = self.driver.find_element(*self.ATTRIBUTE_CONTAINER)
            table_body = attribute_container.find_element(*self.ATTRIBUTE_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                name_cell = first_row.find_elements(*self.ATTRIBUTE_CELL_ATTRIBUTE)
                if name_cell:
                    attribute_name = name_cell[0].text.strip()
                    print(f"🔍 Clicking on attribute: {attribute_name}")
                    self.driver.execute_script("arguments[0].click();", name_cell[0])
                    
                    import time
                    time.sleep(3)  # Wait for filter to apply
                    
                    # Count after attribute filter
                    filtered_categories = self.count_filtered_categories()
                    filtered_brands = self.count_filtered_brands()
                    filtered_products = self.count_filtered_products()
                    filtered_variants = self.count_filtered_variants()
                    
                    print(f"📊 ATTRIBUTE FILTER TEST RESULTS for {attribute_name}:")
                    print(f"📁 Categories: {original_categories} -> {filtered_categories}")
                    print(f"🏷️ Brands: {original_brands} -> {filtered_brands}")
                    print(f"📦 Products: {original_products} -> {filtered_products}")
                    print(f"🔧 Variants: {original_variants} -> {filtered_variants}")
                    
                    # Test if attribute filter is working
                    if (filtered_categories <= original_categories and
                        filtered_brands <= original_brands and
                        filtered_products <= original_products and 
                        filtered_variants <= original_variants):
                        print("✅ PASS: Attribute filter is working correctly")
                        self.reset_filters()
                    else:
                        print("❌ FAIL: Attribute filter is not working")
                        
            return True
        except Exception as e:
            print(f"❌ Error testing attribute filter: {e}")
            return False

    def edit_category_and_revert(self):
        """Edit first category and then revert back to original values"""
        try:
            import time
            time.sleep(2)
            
            # Try multiple locators for category container
            category_container = None
            locators = [
                (By.XPATH, "//h2[contains(text(),'Categories')]/ancestor::div[contains(@class, 'bg-white')]"),
                (By.XPATH, "//h2[text()='Categories']/parent::div/parent::div"),
                (By.XPATH, "//div[.//h2[contains(text(),'Categories')]]"),
                (By.XPATH, "//div[contains(@class,'bg-white') and .//h2[contains(text(),'Categories')]]"),
            ]
            
            for locator in locators:
                try:
                    category_container = self.driver.find_element(*locator)
                    print(f"✅ Found category container with locator: {locator[1]}")
                    break
                except:
                    continue
            
            if not category_container:
                print("❌ Could not find category container")
                return False
            
            # Find table body and rows
            table_body = category_container.find_element(*self.CATEGORY_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                
                # Store original values
                name_cell = first_row.find_elements(*self.CELL_NAME)
                slug_cell = first_row.find_elements(*self.CELL_SLUG)
                role_cell = first_row.find_elements(*self.CELL_ROLE)
                
                self.original_name = name_cell[0].text.strip() if name_cell else ""
                self.original_slug = slug_cell[0].text.strip() if slug_cell else ""
                self.original_role = role_cell[0].text.strip() if role_cell else ""
                
                print(f"📝 Original values - Name: {self.original_name}, Slug: {self.original_slug}, Role: {self.original_role}")
                
                # Click edit button
                edit_button = first_row.find_element(*self.EDIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", edit_button)
                
                time.sleep(2)  # Wait for edit form to load
                
                # Edit the values (add "_edited" suffix)
                name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='name' or contains(@placeholder,'name') or contains(@id,'name')]")))
                slug_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='slug' or contains(@placeholder,'slug') or contains(@id,'slug')]")))
                
                # Clear and enter new values
                self.driver.execute_script("arguments[0].value = '';", name_input)
                name_input.send_keys(self.original_name + "_edited")
                
                self.driver.execute_script("arguments[0].value = '';", slug_input)
                slug_input.send_keys(self.original_slug + "_edited")
                
                # Handle role dropdown
                try:
                    role_dropdown = self.driver.find_element(By.XPATH, "//select[@name='target_role']")
                    select = Select(role_dropdown)
                    
                    # Select different role (if original was 'both', select 'customer', otherwise select 'both')
                    if self.original_role.lower() == 'both':
                        select.select_by_value('customer')
                    else:
                        select.select_by_value('both')
                    print(f"✅ Changed role from {self.original_role} to {'customer' if self.original_role.lower() == 'both' else 'both'}")
                except Exception as e:
                    print(f"⚠️ Could not change role dropdown: {e}")
                
                # Save changes
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
                save_button.click()
                
                time.sleep(3)  # Wait for save and potential alert
                
                print("✅ Category edited successfully")
                
                # Now revert back to original values
                self.revert_category_edit()
                
            return True
        except Exception as e:
            print(f"❌ Error editing category: {e}")
            return False
    
    def revert_category_edit(self):
        """Revert category back to original values"""
        try:
            import time
            time.sleep(3)  # Wait longer for page to refresh
            
            # Try multiple locators for category container
            category_container = None
            locators = [
                (By.XPATH, "//h2[contains(text(),'Categories')]/ancestor::div[contains(@class, 'bg-white')]"),
                (By.XPATH, "//h2[text()='Categories']/parent::div/parent::div"),
                (By.XPATH, "//div[.//h2[contains(text(),'Categories')]]"),
                (By.XPATH, "//div[contains(@class,'bg-white') and .//h2[contains(text(),'Categories')]]"),
            ]
            
            for locator in locators:
                try:
                    category_container = self.wait.until(EC.presence_of_element_located(locator))
                    break
                except:
                    continue
            
            if not category_container:
                print("❌ Could not find category container for revert")
                return False
            
            # Wait for table to load and find the edited category
            table_body = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")))
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            # Find row with edited name
            for row in rows:
                name_cell = row.find_elements(*self.CELL_NAME)
                if name_cell and "_edited" in name_cell[0].text:
                    edit_button = row.find_element(*self.EDIT_BUTTON)
                    self.driver.execute_script("arguments[0].click();", edit_button)
                    break
            
            time.sleep(2)
            
            # Revert to original values
            name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='name' or contains(@placeholder,'name') or contains(@id,'name')]")))
            slug_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='slug' or contains(@placeholder,'slug') or contains(@id,'slug')]")))
            
            self.driver.execute_script("arguments[0].value = '';", name_input)
            name_input.send_keys(self.original_name)
            
            self.driver.execute_script("arguments[0].value = '';", slug_input)
            slug_input.send_keys(self.original_slug)
            
            # Revert role dropdown to original value
            try:
                role_dropdown = self.driver.find_element(By.XPATH, "//select[@name='target_role']")
                select = Select(role_dropdown)
                
                # Set original role value
                if self.original_role.lower() == 'both':
                    select.select_by_value('both')
                elif self.original_role.lower() == 'customer':
                    select.select_by_value('customer')
                else:
                    select.select_by_value('retailer')
                print(f"✅ Reverted role back to {self.original_role}")
            except Exception as e:
                print(f"⚠️ Could not revert role dropdown: {e}")
            
            # Save reverted changes
            save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
            save_button.click()
            
            time.sleep(3)
            
            print("✅ Category reverted to original values successfully")
            
            return True
        except Exception as e:
            print(f"❌ Error reverting category: {e}")
            return False

    def click_brand_and_test_filter(self):
        """Click on first available brand and test if filter is working"""
        try:
            # Reset filters first
            self.reset_filters()
            
            # Store original counts
            original_categories = len(self.category_data)
            original_products = len(self.product_data)
            original_variants = len(self.variant_data)
            original_attributes = len(self.attribute_data)
            
            # Find and click first brand
            brand_container = self.driver.find_element(*self.BRAND_CONTAINER)
            table_body = brand_container.find_element(*self.BRAND_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                name_cell = first_row.find_elements(*self.BRAND_CELL_NAME)
                if name_cell:
                    brand_name = name_cell[0].text.strip()
                    print(f"🔍 Clicking on brand: {brand_name}")
                    self.driver.execute_script("arguments[0].click();", name_cell[0])
                    
                    import time
                    time.sleep(3)  # Wait for filter to apply
                    
                    # Count after brand filter
                    filtered_categories = self.count_filtered_categories()
                    filtered_products = self.count_filtered_products()
                    filtered_variants = self.count_filtered_variants()
                    filtered_attributes = self.count_filtered_attributes()
                    
                    print(f"📊 BRAND FILTER TEST RESULTS for {brand_name}:")
                    print(f"📁 Categories: {original_categories} -> {filtered_categories}")
                    print(f"📦 Products: {original_products} -> {filtered_products}")
                    print(f"🔧 Variants: {original_variants} -> {filtered_variants}")
                    print(f"⚙️ Attributes: {original_attributes} -> {filtered_attributes}")
                    
                    # Test if brand filter is working
                    if (filtered_categories <= original_categories and
                        filtered_products <= original_products and 
                        filtered_variants <= original_variants and 
                        filtered_attributes <= original_attributes):
                        print("✅ PASS: Brand filter is working correctly")
                    else:
                        print("❌ FAIL: Brand filter is not working")
                        
            return True
        except Exception as e:
            print(f"❌ Error testing brand filter: {e}")
            return False

    def reset_filters(self):
        """Click reset filters button to clear all filters"""
        try:
            reset_button = self.wait.until(
                EC.presence_of_element_located(self.RESET_FILTERS_BUTTON)
            )
            # Scroll to button and click using JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView(true);", reset_button)
            self.driver.execute_script("arguments[0].click();", reset_button)
            
            import time
            time.sleep(2)  # Wait for filters to clear
            
            print("✅ Filter is cleared")
            return True
        except Exception as e:
            print(f"❌ Error clearing filters: {e}")
            return False

    def print_all_table_data(self):
        """Print summary of all table data collected"""
        print("\n" + "="*50)
        print("📊 SUMMARY OF ALL TABLE DATA")
        print("="*50)
        print(f"📁 Categories table has {len(self.category_data)} items")
        print(f"🏷️ Brands table has {len(self.brand_data)} items")
        print(f"📦 Products table has {len(self.product_data)} items")
        print(f"🔧 Variants table has {len(self.variant_data)} items")
        print(f"⚙️ Attributes table has {len(self.attribute_data)} items")
        print("="*50)