from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class AdminOrderManagementPage:
    # ================= LOCATORS =================
    ORDER_MANAGEMENT_LINK = (By.XPATH, "//span[normalize-space()='Order Management']")
    ORDER_MANAGEMENT_TITLE = (By.XPATH, "(//th[normalize-space()='Order ID'])[1]")
    ORDER_ROWS = (By.XPATH, "//tbody/tr")
    PAGINATION_BUTTONS = (By.XPATH, "//div[contains(@class, 'flex-wrap')]//button")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[@class='text-3xl font-bold text-blue-600']")
    PENDING_STATUS_SPANS = (By.XPATH, "//span[contains(@class, 'bg-yellow-100') and contains(@class, 'text-yellow-800') and text()='pending']")
    PENDING_ORDERS_COUNT = (By.XPATH, "//h3[text()='Pending Orders']/following-sibling::p[@class='text-3xl font-bold text-blue-600']")
    SHIPPED_ORDERS_COUNT = (By.XPATH, "//h3[text()='Shipped Orders']/following-sibling::p[@class='text-3xl font-bold text-blue-600']")
    CANCELLED_RETURNED_COUNT = (By.XPATH, "//h3[text()='Cancelled/Returned']/following-sibling::p[@class='text-3xl font-bold text-blue-600']")
    
    # Order details XPaths (relative to row)
    ORDER_ID_BUTTON = ".//td[1]//button"
    CUSTOMER_NAME = ".//td[2]//div[1]"
    CUSTOMER_EMAIL = ".//td[2]//div[2]"
    ORDER_TOTAL_AMOUNT = ".//td[4]"
    ORDER_DATE = ".//td[5]"
    
    # Status XPaths (relative to row)
    PENDING_STATUS = ".//span[contains(@class, 'bg-yellow-100') and contains(@class, 'text-yellow-800') and text()='pending']"
    SHIPPED_STATUS = ".//span[contains(@class, 'bg-blue-100') and contains(@class, 'text-blue-800') and text()='shipped']"
    CANCELLED_STATUS = ".//td[3]//span[text()='cancelled']"
    RETURNED_STATUS = ".//td[3]//span[text()='returned']"
    
    
    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Global variables to store table data
        self.order_data = []
        self.pending_orders = []
        
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

    def count_order_items(self):
        """Counts the number of order items"""
        try:
            order_rows = self.wait.until(
                EC.presence_of_all_elements_located(self.ORDER_ROWS)
            )
            return len(order_rows)
        except Exception as e:
            print("Error counting order items:", e)
            return 0

    def count_all_order_items_with_pagination(self):
        """Counts all order items across all pages using pagination."""
        total_order_items = 0
        page_number = 1
        while True:
            print(f"Counting items on page {page_number}...")
            total_order_items += self.count_order_items()
            
            try:
                pagination_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PAGINATION_BUTTONS)
                )
                
                next_button = None
                for button in pagination_buttons:
                    if button.text == str(page_number + 1):
                        next_button = button
                        break
                
                if next_button:
                    print(f"Navigating to page {page_number + 1}...")
                    time.sleep(2) # wait for page to load
                    try:
                        next_button.click()
                    except Exception as e:
                        print(f"Could not click button normally, trying with javascript: {e}")
                        self.driver.execute_script("arguments[0].click();", next_button)

                    page_number += 1
                    # Wait for the next page to load, e.g., by waiting for the order rows to be present
                    self.wait.until(
                        EC.presence_of_all_elements_located(self.ORDER_ROWS)
                    )
                else:
                    print("No more pages to navigate.")
                    break
            except Exception as e:
                print(f"No more pagination buttons found or error clicking next page: {e}")
                break
                
        return total_order_items

    def print_summary(self):
        """Print summary of all table data collected"""
        print("\n" + "="*50)
        print("📊 SUMMARY OF ALL TABLE DATA")
        print("="*50)
        print(f"📦 Orders table has {len(self.order_data)} items")
        print("="*50)

    def get_total_orders_from_header(self):
        """Gets the total order count from the header."""
        try:
            time.sleep(5) # Wait for the count to be loaded
            total_orders_element = self.wait.until(
                EC.presence_of_element_located(self.TOTAL_ORDERS_COUNT)
            )
            return int(total_orders_element.text)
        except Exception as e:
            print(f"Error getting total orders from header: {e}")
            return 0

    def compare_header_and_table_counts(self, header_count, table_count):
        """Compare header count with table count and print appropriate message"""
        if header_count == table_count:
            print(f"✅ Total orders match: Header shows {header_count} orders, Table shows {table_count} orders")
            return True
        else:
            print(f"❌ Total orders mismatch: Header shows {header_count} orders, Table shows {table_count} orders")
            return False

    def get_pending_orders_with_pagination(self):
        """Collect all pending orders across all pages with pagination"""
        pending_orders = []
        page_number = 1
        
        while True:
            print(f"📄 Checking pending orders on page {page_number}...")
            page_pending_count = 0
            
            # Get all rows on current page
            try:
                order_rows = self.wait.until(
                    EC.presence_of_all_elements_located(self.ORDER_ROWS)
                )
                print(f"   Found {len(order_rows)} total rows on page {page_number}")
                
                # Check each row for pending status
                for row in order_rows:
                    try:
                        # Check if this row has pending status
                        pending_span = row.find_element(By.XPATH, self.PENDING_STATUS)
                        
                        if pending_span:
                            # Extract order details
                            order_id = row.find_element(By.XPATH, self.ORDER_ID_BUTTON).text
                            customer_name = row.find_element(By.XPATH, self.CUSTOMER_NAME).text
                            customer_email = row.find_element(By.XPATH, self.CUSTOMER_EMAIL).text
                            total_amount = row.find_element(By.XPATH, self.ORDER_TOTAL_AMOUNT).text
                            order_date = row.find_element(By.XPATH, self.ORDER_DATE).text
                            
                            pending_orders.append({
                                'order_id': order_id,
                                'customer_name': customer_name,
                                'customer_email': customer_email,
                                'total_amount': total_amount,
                                'order_date': order_date,
                                'status': 'pending'
                            })
                            page_pending_count += 1
                    except Exception:
                        # Row doesn't have pending status, skip
                        continue
                        
                print(f"   🟡 Found {page_pending_count} pending orders on page {page_number}")
                        
            except Exception as e:
                print(f"Error getting rows on page {page_number}: {e}")
                break
            
            print(f"   Total pending orders so far: {len(pending_orders)}")
            
            # Try to navigate to next page
            try:
                pagination_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PAGINATION_BUTTONS)
                )
                
                next_button = None
                for button in pagination_buttons:
                    if button.text == str(page_number + 1):
                        next_button = button
                        break
                
                if next_button:
                    time.sleep(2)
                    try:
                        next_button.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    
                    page_number += 1
                    self.wait.until(
                        EC.presence_of_all_elements_located(self.ORDER_ROWS)
                    )
                else:
                    break
            except Exception:
                break
        
        # Print all pending orders
        self.print_pending_orders(pending_orders)
        return pending_orders
    
    def print_pending_orders(self, pending_orders):
        """Print all pending orders in a formatted way"""
        print("\n" + "="*80)
        print("🟡 PENDING ORDERS SUMMARY")
        print("="*80)
        print(f"Total Pending Orders: {len(pending_orders)}")
        print("="*80)
        
        if pending_orders:
            for i, order in enumerate(pending_orders, 1):
                print(f"{i:2d}. Order ID: {order['order_id']}")
                print(f"    Customer: {order['customer_name']} ({order['customer_email']})")
                print(f"    Amount: {order['total_amount']} | Date: {order['order_date']}")
                print("-" * 60)
        else:
            print("No pending orders found.")
        print("="*80)

    def get_pending_orders_count_from_dashboard(self):
        """Gets the pending orders count from the dashboard header"""
        try:
            time.sleep(2)
            pending_count_element = self.wait.until(
                EC.presence_of_element_located(self.PENDING_ORDERS_COUNT)
            )
            return int(pending_count_element.text)
        except Exception as e:
            print(f"Error getting pending orders count from dashboard: {e}")
            return 0

    def compare_dashboard_and_actual_pending_counts(self, dashboard_count, actual_count):
        """Compare dashboard pending count with actual pending orders found"""
        if dashboard_count == actual_count:
            print(f"✅ Pending orders match: Dashboard shows {dashboard_count} pending orders, Found {actual_count} pending orders")
            return True
        else:
            print(f"❌ Pending orders mismatch: Dashboard shows {dashboard_count} pending orders, Found {actual_count} pending orders")
            return False

    def get_shipped_orders_with_pagination(self):
        """Collect all shipped orders across all pages with pagination"""
        shipped_orders = []
        page_number = 1
        
        while True:
            print(f"🚚 Checking shipped orders on page {page_number}...")
            page_shipped_count = 0
            
            try:
                order_rows = self.wait.until(
                    EC.presence_of_all_elements_located(self.ORDER_ROWS)
                )
                
                for row in order_rows:
                    try:
                        # Check if this row has shipped status
                        shipped_span = row.find_element(By.XPATH, self.SHIPPED_STATUS)
                        
                        if shipped_span:
                            order_id = row.find_element(By.XPATH, self.ORDER_ID_BUTTON).text
                            customer_name = row.find_element(By.XPATH, self.CUSTOMER_NAME).text
                            customer_email = row.find_element(By.XPATH, self.CUSTOMER_EMAIL).text
                            total_amount = row.find_element(By.XPATH, self.ORDER_TOTAL_AMOUNT).text
                            order_date = row.find_element(By.XPATH, self.ORDER_DATE).text
                            
                            shipped_orders.append({
                                'order_id': order_id,
                                'customer_name': customer_name,
                                'customer_email': customer_email,
                                'total_amount': total_amount,
                                'order_date': order_date,
                                'status': 'shipped'
                            })
                            page_shipped_count += 1
                    except Exception:
                        continue
                        
                print(f"   🚚 Found {page_shipped_count} shipped orders on page {page_number}")
                        
            except Exception as e:
                print(f"Error getting rows on page {page_number}: {e}")
                break
            
            print(f"   Total shipped orders so far: {len(shipped_orders)}")
            
            # Navigate to next page
            try:
                pagination_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PAGINATION_BUTTONS)
                )
                
                next_button = None
                for button in pagination_buttons:
                    if button.text == str(page_number + 1):
                        next_button = button
                        break
                
                if next_button:
                    time.sleep(2)
                    try:
                        next_button.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    
                    page_number += 1
                    self.wait.until(
                        EC.presence_of_all_elements_located(self.ORDER_ROWS)
                    )
                else:
                    break
            except Exception:
                break
        
        print(f"\n🚚 Total Shipped Orders Found: {len(shipped_orders)}")
        return shipped_orders

    def get_cancelled_orders_with_pagination(self):
        """Collect all cancelled orders across all pages with pagination"""
        cancelled_orders = []
        page_number = 1
        
        while True:
            print(f"❌ Checking cancelled orders on page {page_number}...")
            page_cancelled_count = 0
            
            try:
                order_rows = self.wait.until(
                    EC.presence_of_all_elements_located(self.ORDER_ROWS)
                )
                
                for row in order_rows:
                    try:
                        # Check status column (3rd column) for cancelled status
                        cancelled_span = row.find_element(By.XPATH, self.CANCELLED_STATUS)
                        
                        if cancelled_span:
                            order_id = row.find_element(By.XPATH, self.ORDER_ID_BUTTON).text
                            customer_name = row.find_element(By.XPATH, self.CUSTOMER_NAME).text
                            customer_email = row.find_element(By.XPATH, self.CUSTOMER_EMAIL).text
                            total_amount = row.find_element(By.XPATH, self.ORDER_TOTAL_AMOUNT).text
                            order_date = row.find_element(By.XPATH, self.ORDER_DATE).text
                            
                            cancelled_orders.append({
                                'order_id': order_id,
                                'customer_name': customer_name,
                                'customer_email': customer_email,
                                'total_amount': total_amount,
                                'order_date': order_date,
                                'status': 'cancelled'
                            })
                            page_cancelled_count += 1
                    except Exception:
                        continue
                        
                print(f"   ❌ Found {page_cancelled_count} cancelled orders on page {page_number}")
                        
            except Exception as e:
                print(f"Error getting rows on page {page_number}: {e}")
                break
            
            print(f"   Total cancelled orders so far: {len(cancelled_orders)}")
            
            # Navigate to next page
            try:
                pagination_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PAGINATION_BUTTONS)
                )
                
                next_button = None
                for button in pagination_buttons:
                    if button.text == str(page_number + 1):
                        next_button = button
                        break
                
                if next_button:
                    time.sleep(2)
                    try:
                        next_button.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    
                    page_number += 1
                    self.wait.until(
                        EC.presence_of_all_elements_located(self.ORDER_ROWS)
                    )
                else:
                    break
            except Exception:
                break
        
        print(f"\n❌ Total Cancelled Orders Found: {len(cancelled_orders)}")
        return cancelled_orders

    def get_returned_orders_with_pagination(self):
        """Collect all returned orders across all pages with pagination"""
        returned_orders = []
        page_number = 1
        
        while True:
            print(f"↩️ Checking returned orders on page {page_number}...")
            page_returned_count = 0
            
            try:
                order_rows = self.wait.until(
                    EC.presence_of_all_elements_located(self.ORDER_ROWS)
                )
                
                for row in order_rows:
                    try:
                        # Check status column (3rd column) for returned status
                        returned_span = row.find_element(By.XPATH, self.RETURNED_STATUS)
                        
                        if returned_span:
                            order_id = row.find_element(By.XPATH, self.ORDER_ID_BUTTON).text
                            customer_name = row.find_element(By.XPATH, self.CUSTOMER_NAME).text
                            customer_email = row.find_element(By.XPATH, self.CUSTOMER_EMAIL).text
                            total_amount = row.find_element(By.XPATH, self.ORDER_TOTAL_AMOUNT).text
                            order_date = row.find_element(By.XPATH, self.ORDER_DATE).text
                            
                            returned_orders.append({
                                'order_id': order_id,
                                'customer_name': customer_name,
                                'customer_email': customer_email,
                                'total_amount': total_amount,
                                'order_date': order_date,
                                'status': 'returned'
                            })
                            page_returned_count += 1
                    except Exception:
                        continue
                        
                print(f"   ↩️ Found {page_returned_count} returned orders on page {page_number}")
                        
            except Exception as e:
                print(f"Error getting rows on page {page_number}: {e}")
                break
            
            print(f"   Total returned orders so far: {len(returned_orders)}")
            
            # Navigate to next page
            try:
                pagination_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PAGINATION_BUTTONS)
                )
                
                next_button = None
                for button in pagination_buttons:
                    if button.text == str(page_number + 1):
                        next_button = button
                        break
                
                if next_button:
                    time.sleep(2)
                    try:
                        next_button.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    
                    page_number += 1
                    self.wait.until(
                        EC.presence_of_all_elements_located(self.ORDER_ROWS)
                    )
                else:
                    break
            except Exception:
                break
        
        print(f"\n↩️ Total Returned Orders Found: {len(returned_orders)}")
        return returned_orders

    def get_cancelled_returned_count_from_dashboard(self):
        """Gets the cancelled/returned orders count from the dashboard header"""
        try:
            time.sleep(2)
            cancelled_returned_element = self.wait.until(
                EC.presence_of_element_located(self.CANCELLED_RETURNED_COUNT)
            )
            return int(cancelled_returned_element.text)
        except Exception as e:
            print(f"Error getting cancelled/returned orders count from dashboard: {e}")
            return 0

    def compare_dashboard_and_actual_cancelled_returned_counts(self, dashboard_count, cancelled_count, returned_count):
        """Compare dashboard cancelled/returned count with actual cancelled and returned orders found"""
        total_actual = cancelled_count + returned_count
        if dashboard_count == total_actual:
            print(f"✅ Cancelled/Returned orders match: Dashboard shows {dashboard_count}, Found {cancelled_count} cancelled + {returned_count} returned = {total_actual} total")
            return True
        else:
            print(f"❌ Cancelled/Returned orders mismatch: Dashboard shows {dashboard_count}, Found {cancelled_count} cancelled + {returned_count} returned = {total_actual} total")
            return False

    def get_shipped_orders_count_from_dashboard(self):
        """Gets the shipped orders count from the dashboard header"""
        try:
            time.sleep(2)
            shipped_count_element = self.wait.until(
                EC.presence_of_element_located(self.SHIPPED_ORDERS_COUNT)
            )
            return int(shipped_count_element.text)
        except Exception as e:
            print(f"Error getting shipped orders count from dashboard: {e}")
            return 0

    def compare_dashboard_and_actual_shipped_counts(self, dashboard_count, actual_count):
        """Compare dashboard shipped count with actual shipped orders found"""
        if dashboard_count == actual_count:
            print(f"✅ Shipped orders match: Dashboard shows {dashboard_count} shipped orders, Found {actual_count} shipped orders")
            return True
        else:
            print(f"❌ Shipped orders mismatch: Dashboard shows {dashboard_count} shipped orders, Found {actual_count} shipped orders")
            return False
