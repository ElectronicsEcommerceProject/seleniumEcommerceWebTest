from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminProductManagementPage:
    # ================= LOCATORS =================
    PRODUCT_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Product Management']")
    PRODUCT_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Product Management']")
    SEARCH_CATEGORY_INPUT = "//input[@placeholder='Search categories...']"
    CATEGORY_TABLE = "//body/div[@id='root']/div[@class='bg-gray-100 font-sans min-h-screen flex flex-col']/div[@class='flex flex-1']/main[@class='flex-1 pt-/div[@class='min-h-screen bg-gray-100 p-2 sm:p-4 md:p-6']/div[@class='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 md:gap-6']/div[1]"
    
    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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

    def read_category_table(self):
        """Read and print category table results"""
        try:
            # Target only the Categories table by finding the container with Categories heading
            category_container = self.driver.find_element(By.XPATH, "//h2[text()='Categories']/ancestor::div[contains(@class, 'bg-white rounded-xl')]")
            
            # Check for "No results found" message first
            no_results_msg = category_container.find_elements(By.XPATH, ".//*[contains(text(), 'No') and contains(text(), 'found')]")
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            # Check if table exists
            table_body = category_container.find_elements(By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(By.XPATH, ".//tr")
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Categories table:")
                for i, row in enumerate(table_rows[:5], 1):  # Show first 5 results
                    try:
                        # Check if each cell exists before reading
                        name_cell = row.find_elements(By.XPATH, ".//td[1]//div")
                        slug_cell = row.find_elements(By.XPATH, ".//td[2]//div")
                        role_cell = row.find_elements(By.XPATH, ".//td[3]//div")
                        
                        name = name_cell[0].text.strip() if name_cell else "N/A"
                        slug = slug_cell[0].text.strip() if slug_cell else "N/A"
                        role = role_cell[0].text.strip() if role_cell else "N/A"
                        
                        print(f"  {i}. Name: {name}, Slug: {slug}, Role: {role}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_box(self, search_xpath, search_value):
        """Perform search using provided xpath and value, then print results"""
        print(f"🔍 Searching for '{search_value}'...")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, search_xpath))
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            # Wait a moment for search results to load
            import time
            time.sleep(2)
            
            # Read table results
            self.read_category_table()
                
            return True
        except Exception as e:
            print(f"❌ Error performing search: {e}")
            return False

    def search_test_category(self):
        """Search for 'test category' in categories"""
        return self.search_box(self.SEARCH_CATEGORY_INPUT, "test category")