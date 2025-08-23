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
                        pending_span = row.find_element(By.XPATH, ".//span[contains(@class, 'bg-yellow-100') and contains(@class, 'text-yellow-800') and text()='pending']")
                        
                        if pending_span:
                            # Extract order details
                            order_id = row.find_element(By.XPATH, ".//td[1]//button").text
                            customer_name = row.find_element(By.XPATH, ".//td[2]//div[1]").text
                            customer_email = row.find_element(By.XPATH, ".//td[2]//div[2]").text
                            total_amount = row.find_element(By.XPATH, ".//td[4]").text
                            order_date = row.find_element(By.XPATH, ".//td[5]").text
                            
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
