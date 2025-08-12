from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class AdminDashboardPage:
    """Page Object Model for Admin Dashboard Page"""

    # ================= LOCATORS =================
    TOTAL_USERS_HEADER = (By.XPATH, "//h2[normalize-space()='Total Users']")
    ADD_PRODUCT_BUTTON = (By.XPATH, "//button[normalize-space()='Add Product']")
    CREATE_COUPON_BUTTON = (By.XPATH, "//button[normalize-space()='Create Coupon']")
    COUPON_MODAL = (By.XPATH, "//div[@class='bg-white rounded-lg p-4 sm:p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto animate-slide-in relative']")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[@class='absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl font-bold']")
    COUPON_MODAL_TITLE = (By.XPATH, "//h3[text()='CREATE COUPON']")

    FIRST_ORDER_LINK = (By.XPATH, "(//div[@col-id='id']/button)[1]")
    ORDER_DETAILS_MODAL_TITLE = (By.XPATH, "//h2[contains(text(), 'Order Details')]")
    MODAL_CLOSE_BUTTON_ORDER_DETAILS = (By.XPATH, "//div[@class='flex justify-between items-center mb-4']/button")
    ORDER_ROWS = (By.XPATH, "//div[@role='row' and contains(@class, 'ag-row')]")
    ORDER_STATUS_SPAN = (By.XPATH, ".//div[@col-id='status']/span")
    ORDER_LINK_BUTTON = (By.XPATH, ".//div[@col-id='id']/button")

    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= METHODS =================
    def verifying_adminDashboard(self):
        """Verify if user is on admin dashboard page"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.TOTAL_USERS_HEADER)
            )
            return True
        except Exception as e:
            print("Error verifying admin dashboard:", e)
            return False

    def checking_button_working(self):
        """Check if buttons work and print redirect URLs"""
        current_url = self.driver.current_url
        
        # Test Add Product button
        try:
            add_product_btn = self.wait.until(
                EC.element_to_be_clickable(self.ADD_PRODUCT_BUTTON)
            )
            add_product_btn.click()
            self.wait.until(lambda driver: driver.current_url != current_url)
            print(f"Add Product redirected to: {self.driver.current_url}")
            self.driver.back()
            self.wait.until(lambda driver: driver.current_url == current_url)
        except Exception as e:
            print(f"Add Product button error: {e}")
        
        # Test Create Coupon button (opens modal)
        try:
            create_coupon_btn = self.wait.until(
                EC.element_to_be_clickable(self.CREATE_COUPON_BUTTON)
            )
            create_coupon_btn.click()
            # Check if modal opened instead of URL change
            try:
                self.wait.until(EC.presence_of_element_located(self.COUPON_MODAL))
                print("Create Coupon opened modal successfully")
                # Close modal using the X button
                close_btn = self.wait.until(EC.element_to_be_clickable(self.MODAL_CLOSE_BUTTON))
                close_btn.click()
            except:
                print("Create Coupon: No modal detected, URL remains same")
        except Exception as e:
            print(f"Create Coupon button error: {e}")
            
        return True

    def check_first_order_link_navigation(self):
        """Clicks the first order link in the customer orders table and verifies navigation."""
        current_url = self.driver.current_url
        try:
            first_order_link = self.wait.until(
                EC.element_to_be_clickable(self.FIRST_ORDER_LINK)
            )
            print("🖱️ Clicking on the first customer order link...")
            ActionChains(self.driver).move_to_element(first_order_link).click().perform()
            
            # Wait for the modal to appear
            self.wait.until(EC.presence_of_element_located(self.ORDER_DETAILS_MODAL_TITLE))
            print("✅ Order details modal opened successfully.")
            
            # Close the modal
            close_btn = self.wait.until(EC.element_to_be_clickable(self.MODAL_CLOSE_BUTTON_ORDER_DETAILS))
            close_btn.click()
            self.wait.until(EC.invisibility_of_element_located(self.ORDER_DETAILS_MODAL_TITLE))
            print("✅ Order details modal closed.")
            return True
        except Exception as e:
            print(f"Error during first order link navigation check: {e}")
            return False

    def click_pending_order(self):
        """Finds and clicks on the first pending order in the customer orders table."""
        try:
            order_rows = self.wait.until(EC.presence_of_all_elements_located(self.ORDER_ROWS))
            print(f"Found {len(order_rows)} order rows.")

            for row in order_rows:
                status_element = row.find_element(*self.ORDER_STATUS_SPAN)
                status_text = status_element.text.strip().lower()

                if status_text == "pending":
                    order_link = row.find_element(*self.ORDER_LINK_BUTTON)
                    print(f"Found pending order: {order_link.text}. Clicking it...")
                    ActionChains(self.driver).move_to_element(order_link).click().perform()

                    # Verify modal and close it
                    self.wait.until(EC.presence_of_element_located(self.ORDER_DETAILS_MODAL_TITLE))
                    print("✅ Order details modal opened successfully for pending order.")
                    close_btn = self.wait.until(EC.element_to_be_clickable(self.MODAL_CLOSE_BUTTON_ORDER_DETAILS))
                  
                    close_btn.click()
                    self.wait.until(EC.invisibility_of_element_located(self.ORDER_DETAILS_MODAL_TITLE))
                    print("✅ Order details modal closed for pending order.")
                    return True
            print("No pending orders found.")
            return False
        except Exception as e:
            print(f"Error while trying to click pending order: {e}")
            return False