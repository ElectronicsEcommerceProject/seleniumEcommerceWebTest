from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MyOrderPage:
    """Page object for the My Order page."""
    
    # Locators
    ORDER_ITEMS = (By.XPATH, "//div[contains(@class, 'w-full bg-white p-4 mb-4 rounded-lg shadow-md')]")
    LOAD_MORE_BUTTON = (By.XPATH, "//button[contains(normalize-space(), 'Load More Orders')]")
    ORDER_ITEMS_SHOWN_ON_PAGE = (By.XPATH, "//p[contains(@class, 'text-sm text-gray-600') and contains(text(), 'Showing')]")
    SEARCH_BOX = (By.XPATH, "//input[@placeholder='🔍 Search orders (auto-search after 1.5s)...']")
    
    # Filter section locators
    ORDER_STATUS_BUTTON = (By.XPATH, "//button[contains(text(), 'ORDER STATUS')]")
    FILTER_CHECKBOXES = (By.XPATH, "//input[@type='checkbox']")
    PENDING_FILTER = (By.XPATH, "//input[@type='checkbox' and @value='pending']")
    CONFIRMED_FILTER = (By.XPATH, "//input[@type='checkbox' and @value='confirmed']")
    SHIPPED_FILTER = (By.XPATH, "//input[@type='checkbox' and @value='shipped']")
    DELIVERED_FILTER = (By.XPATH, "//input[@type='checkbox' and @value='delivered']")
    CANCELLED_FILTER = (By.XPATH, "//input[@type='checkbox' and @value='cancelled']")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.initial_order_count = 0
        self.current_order_count = 0
        self.load_more_clicks = 0
    
    def check_no_orders_message(self):
        """Check if there's a 'no orders' message on the page."""
        try:
            page_source = self.driver.page_source.lower()
            no_orders_indicators = [
                "no orders found",
                "no orders yet", 
                "you haven't placed any orders",
                "no order history"
            ]
            
            for indicator in no_orders_indicators:
                if indicator in page_source:
                    print(f"[INFO] Found no orders message: '{indicator}'")
                    return True
            return False
        except Exception as e:
            print(f"[ERROR] Error checking no orders message: {e}")
            return False
    
    def wait_for_orders_to_load(self):
        """Wait for order items to load on the page."""
        print("[INFO] Waiting for orders to load...")
        try:
            # Wait for either orders to appear or no orders message
            self.wait.until(
                lambda driver: 
                len(driver.find_elements(*self.ORDER_ITEMS)) > 0 or
                self.check_no_orders_message()
            )
            time.sleep(1)  # Additional wait for complete loading
            return True
        except Exception as e:
            print(f"[INFO] Timeout waiting for orders to load: {e}")
            return False
    
    def count_visible_orders(self):
        """Count total visible orders on the page."""
        try:
            # Wait for orders to load first
            self.wait_for_orders_to_load()
            
            # Check if there's a no orders message
            if self.check_no_orders_message():
                print("[INFO] Page shows no orders available")
                return 0
            
            # Try to find orders with the current locator
            orders = self.driver.find_elements(*self.ORDER_ITEMS)
            order_count = len(orders)
            
            if order_count == 0:
                # Try alternative locators if current one doesn't work
                alt_locators = [
                    (By.XPATH, "//div[contains(@class, 'order-item')]"),
                    (By.XPATH, "//div[contains(text(), 'Order #')]/ancestor::div[1]"),
                    (By.XPATH, "//div[contains(@class, 'bg-white') and contains(@class, 'shadow')]"),
                ]
                
                for locator in alt_locators:
                    alt_orders = self.driver.find_elements(*locator)
                    if len(alt_orders) > 0:
                        print(f"[INFO] Found {len(alt_orders)} orders using alternative locator")
                        return len(alt_orders)
            
            print(f"Found {order_count} visible orders")
            return order_count
        except Exception as e:
            print(f"Error counting orders: {e}")
            return 0
    
    def check_load_more_button_present(self):
        """Check if Load More button is present and clickable."""
        try:
            load_more_button = self.driver.find_element(*self.LOAD_MORE_BUTTON)
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                button_text = load_more_button.text.strip()
                print(f"Load More button is present and clickable: '{button_text}'")
                return True
            else:
                print("Load More button is present but not clickable")
                return False
        except Exception as e:
            print("Load More button not found")
            return False
    
    def click_load_more_button(self):
        """Click the Load More button."""
        try:
            load_more_button = self.wait.until(EC.element_to_be_clickable(self.LOAD_MORE_BUTTON))
            
            # Scroll to the button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(0.5)
            
            # Click the button
            self.driver.execute_script("arguments[0].click();", load_more_button)
            self.load_more_clicks += 1
            print(f"Load More button clicked successfully (Click #{self.load_more_clicks})")
            return True
        except Exception as e:
            print(f"Error clicking Load More button: {e}")
            return False
    
    def wait_for_new_orders_to_load(self):
        """Wait for new orders to load after clicking Load More."""
        print("Waiting for new orders to load...")
        time.sleep(2)
        return True
    
    def get_total_orders_from_text(self):
        """Extract total order count from 'Showing x of y orders' text."""
        try:
            # Wait for the showing text element with shorter timeout
            print("[INFO] Waiting for showing text element...")
            showing_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(self.ORDER_ITEMS_SHOWN_ON_PAGE)
            )
            time.sleep(1)  # Additional wait for element to be fully loaded
            showing_text = showing_element.text.strip()
            print(f"[INFO] Found showing text: '{showing_text}'")
            
            # Extract numbers from "Showing 9 of 17 orders"
            import re
            match = re.search(r'Showing (\d+) of (\d+) orders', showing_text)
            if match:
                shown_count = int(match.group(1))
                total_count = int(match.group(2))
                print(f"[INFO] Showing {shown_count} of {total_count} total orders")
                return shown_count, total_count
            else:
                print(f"[ERROR] Could not parse showing text: {showing_text}")
                return 0, 0
        except:
            print(f"[INFO] Showing text element not available - page may be in filtered state")
            return 0, 0
    
    def validate_final_order_count(self):
        """Validate that final displayed orders match total available orders."""
        try:
            # Clear search first to ensure we're seeing all orders
            print("[INFO] Clearing search to validate final count...")
            self.clear_search()
            
            displayed_orders = self.count_visible_orders()
            shown_count, total_count = self.get_total_orders_from_text()
            
            if total_count > 0:
                if displayed_orders == total_count:
                    print(f"[SUCCESS] All {total_count} orders are now displayed")
                    return True
                else:
                    print(f"[INFO] Displaying {displayed_orders} orders, total available: {total_count}")
                    return False
            else:
                print("[INFO] No total count information available - using displayed count")
                return displayed_orders > 0
        except Exception as e:
            print(f"[ERROR] Error validating final order count: {e}")
            return False
    
    def validate_order_count_increase(self, previous_count):
        """Validate that order count has increased after Load More click."""
        new_count = self.count_visible_orders()
        if new_count > previous_count:
            print(f"Order count increased from {previous_count} to {new_count}")
            return True, new_count
        else:
            print(f"Order count did not increase (still {new_count})")
            return False, new_count
    
    def search_orders(self, search_term):
        """Search for orders using the search box."""
        try:
            search_box = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
            search_box.clear()
            search_box.send_keys(search_term)
            print(f"[ACTION] Entered search term: '{search_term}'")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[ERROR] Error searching orders: {e}")
            return False
    
    def test_exact_order_search(self, order_number="ORD-20250808-78EB"):
        """Test exact order number search."""
        print(f"[STEP] Testing exact order search with: {order_number}")
        if self.search_orders(order_number):
            result_count = self.count_visible_orders()
            if result_count >= 1:
                print(f"[SUCCESS] Exact search returned {result_count} result(s)")
                return True
            else:
                print(f"[INFO] Exact search returned no results")
                return False
        return False
    
    def test_partial_order_search(self, partial_term="ORD-20250808"):
        """Test partial order number search."""
        print(f"[STEP] Testing partial order search with: {partial_term}")
        if self.search_orders(partial_term):
            result_count = self.count_visible_orders()
            if result_count > 0:
                print(f"[SUCCESS] Partial search returned {result_count} results")
                return True
            else:
                print(f"[INFO] Partial search returned no results")
                return False
        return False
    
    def test_invalid_order_search(self, invalid_term="INVALID123XYZ"):
        """Test invalid/random text search."""
        print(f"[STEP] Testing invalid order search with: {invalid_term}")
        if self.search_orders(invalid_term):
            result_count = self.count_visible_orders()
            if result_count == 0:
                print(f"[SUCCESS] Invalid search correctly returned no results")
                return True
            else:
                print(f"[INFO] Invalid search unexpectedly returned {result_count} results")
                return False
        return False
    
    def clear_search(self):
        """Clear the search box to show all orders."""
        try:
            search_box = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
            search_box.clear()
            print("[ACTION] Cleared search box")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[ERROR] Error clearing search: {e}")
            return False
    
    def validate_all_orders_loaded(self):
        """Validate that all orders are loaded by comparing displayed count with total available."""
        try:
            # Get current displayed order count
            displayed_orders = self.count_visible_orders()
            
            # Get total available orders from showing text
            shown_count, total_count = self.get_total_orders_from_text()
            
            print(f"[INFO] Displayed orders: {displayed_orders}")
            print(f"[INFO] Total available orders: {total_count}")
            
            if total_count > 0:
                if displayed_orders == total_count:
                    print(f"[SUCCESS] All orders loaded! Total orders loaded ({displayed_orders}) matches total available ({total_count})")
                    return True
                else:
                    print(f"[INFO] Not all orders loaded - showing {displayed_orders} of {total_count} orders")
                    return False
            else:
                print(f"[INFO] Could not get total count information - using displayed count: {displayed_orders}")
                return displayed_orders > 0
        except Exception as e:
            print(f"[ERROR] Error validating all orders loaded: {e}")
            return False
    
    def tick_pending_filter_checkbox(self):
        """Tick only the first filter checkbox (Pending)."""
        try:
            print("[ACTION] Finding and ticking Pending filter checkbox...")
            
            # First, click the ORDER STATUS button to expand filters
            print("[STEP] Looking for ORDER STATUS button to expand filters...")
            try:
                order_status_button = self.wait.until(EC.presence_of_element_located(self.ORDER_STATUS_BUTTON))
                # Scroll to make button visible
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", order_status_button)
                time.sleep(1)
                # Use JavaScript click to avoid interception
                self.driver.execute_script("arguments[0].click();", order_status_button)
                print("[SUCCESS] Clicked ORDER STATUS button to expand filters")
                time.sleep(2)  # Wait for filters to expand
            except Exception as e:
                print(f"[ERROR] Could not find or click ORDER STATUS button: {e}")
                return False
            
            # Now find and tick only the first checkbox (Pending)
            print("[STEP] Looking for Pending filter checkbox...")
            checkboxes = self.driver.find_elements(*self.FILTER_CHECKBOXES)
            
            if not checkboxes:
                print("[INFO] No filter checkboxes found after expanding")
                return False
            
            print(f"[INFO] Found {len(checkboxes)} filter checkboxes")
            
            # Click only the first checkbox (Pending)
            try:
                first_checkbox = checkboxes[0]
                if first_checkbox.is_displayed() and not first_checkbox.is_selected():
                    # Scroll to checkbox and click
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", first_checkbox)
                    time.sleep(0.3)
                    first_checkbox.click()
                    print("[SUCCESS] Ticked Pending filter checkbox")
                    time.sleep(2)  # Wait for filter to apply
                    
                    # Count orders and load more if needed
                    self._count_and_load_filtered_orders()
                    
                    return True
                elif first_checkbox.is_selected():
                    print("[INFO] Pending checkbox already selected")
                    
                    # Count orders and load more if needed
                    self._count_and_load_filtered_orders()
                    
                    return True
                else:
                    print("[INFO] Pending checkbox not visible")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to tick Pending checkbox: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Error ticking Pending filter checkbox: {e}")
            return False
    
    def _count_and_load_filtered_orders(self):
        """Count filtered orders and load more if available."""
        try:
            # Get initial count
            initial_count = self.count_visible_orders()
            print(f"[INFO] Initial filtered orders count: {initial_count}")
            
            # Print the filtered order count from text
            shown_count, total_count = self.get_total_orders_from_text()
            if shown_count > 0 and total_count > 0:
                print(f"[INFO] Pending filter applied: Showing {shown_count} of {total_count} orders")
            
            current_count = initial_count
            
            # Load more orders if Load More button is available
            while self.check_load_more_button_present():
                print("[ACTION] Load More button found for filtered orders - clicking...")
                if self.click_load_more_button():
                    self.wait_for_new_orders_to_load()
                    new_count = self.count_visible_orders()
                    if new_count > current_count:
                        current_count = new_count
                        print(f"[INFO] Loaded more filtered orders. Current count: {current_count}")
                    else:
                        print("[INFO] No new filtered orders loaded")
                        break
                else:
                    print("[INFO] Failed to click Load More button")
                    break
            
            print(f"[SUCCESS] Total Pending orders loaded: {current_count}")
            
            # Compare total_count from text with actual loaded count
            if total_count > 0:
                if current_count == total_count:
                    print(f"[SUCCESS] Pending filter validation PASSED: Expected {total_count} orders, loaded {current_count} orders")
                else:
                    print(f"[FAIL] Pending filter validation FAILED: Expected {total_count} orders, but loaded {current_count} orders")
            else:
                print(f"[INFO] Could not validate filter - no total count available from text")
            
            return current_count
            
        except Exception as e:
            print(f"[ERROR] Error counting and loading filtered orders: {e}")
            return 0
