from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class AdminOrderManagementPage:
    # ================= LOCATORS =================
    ORDER_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Order Management']")
    ORDER_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Order Management']")
    RESET_FILTERS_BUTTON = (By.XPATH, "//button[contains(@class, 'bg-gray-200') and contains(text(), 'Reset Filters')]")
    EDIT_BUTTON = (By.XPATH, "//button[@aria-label='Edit orders']")
    SEARCH_ORDER_INPUT = (By.XPATH, "//input[@placeholder='Search orders...']")
    ORDER_CONTAINER = (By.XPATH, "//h2[text()='Orders']/ancestor::div[contains(@class, 'bg-white rounded-xl')]")
    ORDER_TABLE_BODY = (By.XPATH, ".//tbody[@class='divide-y divide-gray-100']")
    TABLE_ROWS = (By.XPATH, ".//tr")
    NO_RESULTS_MESSAGE = (By.XPATH, ".//*[contains(text(), 'No') and contains(text(), 'found')]")
    ORDER_CELL_ID = (By.XPATH, ".//td[1]//div")
    ORDER_CELL_CUSTOMER = (By.XPATH, ".//td[2]//div")
    ORDER_CELL_STATUS = (By.XPATH, ".//td[3]//div")
    ORDER_CELL_TOTAL = (By.XPATH, ".//td[4]//div")
    ORDER_CELL_DATE = (By.XPATH, ".//td[5]//div")
    
    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Global variables to store table data
        self.order_data = []
        
        # Variables to store original values for editing
        self.original_order_id = ""
        self.original_order_status = ""

    # ================= METHODS =================

    def navigate_to_order_management(self):
        """Click on Order Management link"""
        try:
            order_link = self.wait.until(
                EC.element_to_be_clickable(self.ORDER_MANAGEMENT_LINK)
            )
            order_link.click()
            return True
        except Exception as e:
            print("Error navigating to Order management:", e)
            return False

    def verifying_orderManagement(self):
        """Verify if user is on Order management page"""
        print("🔍 Verifying Order Management page...")
        try:
            self.wait.until(
                EC.presence_of_element_located(self.ORDER_MANAGEMENT_TITLE)
            )
            print("✅ Order Management page verified successfully")
            return True
        except Exception as e:
            print("❌ Error verifying Order management page:", e)
            return False

    def collect_table_counts(self):
        """Count total rows in orders table"""
        print("📁 Collecting order table row counts...")
        
        import time
        time.sleep(2)  # Wait for tables to load
        
        # Count order rows
        try:
            order_container = self.wait.until(EC.presence_of_element_located(self.ORDER_CONTAINER))
            table_body = order_container.find_elements(*self.ORDER_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                print(f"📦 Orders table: {len(table_rows)} items")
            else:
                print("📦 Orders table: 0 items")
        except:
            print("📦 Orders table: 0 items")
            
        print("✅ Table counts collected successfully")

    def search_order_box(self, search_value):
        """Perform order search and print results"""
        print(f"🔍 Searching for '{search_value}' in orders...")
        print(f"📝 Search term entered: '{search_value}'")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable(self.SEARCH_ORDER_INPUT)
            )
            search_input.clear()
            search_input.send_keys(search_value)
            
            import time
            time.sleep(2)
            
            self.read_order_table()
            
            # Clear search box using backspace keys
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            
            # Collect all data after clearing search
            self.collect_all_order_data()
                
            return True
        except Exception as e:
            print(f"❌ Error performing order search: {e}")
            return False

    def read_order_table(self):
        """Read and print order table results"""
        try:
            order_container = self.driver.find_element(*self.ORDER_CONTAINER)
            no_results_msg = order_container.find_elements(*self.NO_RESULTS_MESSAGE)
            if no_results_msg:
                print("❌ No results found - search term not matched")
                return
            
            table_body = order_container.find_elements(*self.ORDER_TABLE_BODY)
            if not table_body:
                print("❌ No results found - table is empty")
                return
                
            table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
            
            if table_rows:
                print(f"✅ Found {len(table_rows)} result(s) in Orders table:")
                for i, row in enumerate(table_rows[:5], 1):
                    try:
                        id_cell = row.find_elements(*self.ORDER_CELL_ID)
                        customer_cell = row.find_elements(*self.ORDER_CELL_CUSTOMER)
                        status_cell = row.find_elements(*self.ORDER_CELL_STATUS)
                        total_cell = row.find_elements(*self.ORDER_CELL_TOTAL)
                        date_cell = row.find_elements(*self.ORDER_CELL_DATE)
                        
                        order_id = id_cell[0].text.strip() if id_cell else "N/A"
                        customer = customer_cell[0].text.strip() if customer_cell else "N/A"
                        status = status_cell[0].text.strip() if status_cell else "N/A"
                        total = total_cell[0].text.strip() if total_cell else "N/A"
                        date = date_cell[0].text.strip() if date_cell else "N/A"
                        
                        if order_id != "N/A" and order_id not in self.order_data:
                            self.order_data.append(order_id)
                        
                        print(f"  {i}. ID: {order_id}, Customer: {customer}, Status: {status}, Total: {total}, Date: {date}")
                    except Exception as e:
                        print(f"  {i}. [Unable to read row data]")
            else:
                print("❌ No results found - search returned empty")
        except Exception as e:
            print(f"❌ No results found - search term not matched")

    def search_test_order(self):
        """Search for 'test order' in orders"""
        return self.search_order_box("test order")

    def collect_all_order_data(self):
        """Collect all order IDs after search is cleared"""
        try:
            order_container = self.driver.find_element(*self.ORDER_CONTAINER)
            table_body = order_container.find_elements(*self.ORDER_TABLE_BODY)
            if table_body:
                table_rows = table_body[0].find_elements(*self.TABLE_ROWS)
                for row in table_rows:
                    id_cell = row.find_elements(*self.ORDER_CELL_ID)
                    if id_cell:
                        order_id = id_cell[0].text.strip()
                        if order_id and order_id != "N/A" and order_id not in self.order_data:
                            self.order_data.append(order_id)
        except:
            pass

    def edit_order_and_revert(self):
        """Edit first order status and then revert back to original values"""
        try:
            import time
            time.sleep(2)
            
            # Find order container
            order_container = self.wait.until(EC.presence_of_element_located(self.ORDER_CONTAINER))
            table_body = order_container.find_element(*self.ORDER_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            if rows:
                first_row = rows[0]
                
                # Store original values
                id_cell = first_row.find_elements(*self.ORDER_CELL_ID)
                status_cell = first_row.find_elements(*self.ORDER_CELL_STATUS)
                
                self.original_order_id = id_cell[0].text.strip() if id_cell else ""
                self.original_order_status = status_cell[0].text.strip() if status_cell else ""
                
                print(f"📝 Original order values - ID: {self.original_order_id}, Status: {self.original_order_status}")
                
                # Click edit button
                edit_button = first_row.find_element(*self.EDIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", edit_button)
                
                time.sleep(2)  # Wait for edit form to load
                
                # Edit the status (change to different status)
                status_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='status' or contains(@id,'status')]")))
                select = Select(status_dropdown)
                
                # Change status to different value
                if self.original_order_status.lower() == 'pending':
                    select.select_by_value('processing')
                else:
                    select.select_by_value('pending')
                
                # Save changes
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
                save_button.click()
                
                time.sleep(3)  # Wait for save
                
                # Handle alert if present
                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                except:
                    pass
                
                print("✅ Order edited successfully")
                
                # Now revert back to original values
                self.revert_order_edit()
                
            return True
        except Exception as e:
            print(f"❌ Error editing order: {e}")
            return False
    
    def revert_order_edit(self):
        """Revert order back to original values"""
        try:
            import time
            time.sleep(3)  # Wait for page refresh
            
            # Find order container
            order_container = self.wait.until(EC.presence_of_element_located(self.ORDER_CONTAINER))
            table_body = order_container.find_element(*self.ORDER_TABLE_BODY)
            rows = table_body.find_elements(*self.TABLE_ROWS)
            
            # Click edit button on first row (same order we edited)
            if rows:
                first_row = rows[0]
                edit_button = first_row.find_element(*self.EDIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", edit_button)
            
            time.sleep(2)
            
            # Revert to original status
            status_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='status' or contains(@id,'status')]")))
            select = Select(status_dropdown)
            
            # Set original status value
            if self.original_order_status.lower() == 'pending':
                select.select_by_value('pending')
            elif self.original_order_status.lower() == 'processing':
                select.select_by_value('processing')
            elif self.original_order_status.lower() == 'completed':
                select.select_by_value('completed')
            else:
                select.select_by_value('cancelled')
            
            # Save reverted changes
            save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
            save_button.click()
            
            time.sleep(3)
            
            # Handle alert if present
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
            
            print("✅ Order reverted to original values successfully")
            
            return True
        except Exception as e:
            print(f"❌ Error reverting order: {e}")
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
        print(f"📦 Orders table has {len(self.order_data)} items")
        print("="*50)