from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminBannerManagementPage:
    """Page Object Model for Admin Banner Management Page"""

    # ================= LOCATORS =================
    BANNER_MANAGEMENT_TITLE = (By.XPATH, "//h1[normalize-space()='Banner Management']")
    DEACTIVATE_BUTTON = (By.XPATH, "(//button[@class='px-3 py-1 rounded text-xs font-medium bg-red-100 text-red-800 hover:bg-red-200'][normalize-space()='Deactivate'])[1]")
    ACTIVATE_BUTTON = (By.XPATH, "(//button[normalize-space()='Activate'])[1]")
    STATUS_SPAN = (By.XPATH, "(//span[@class='px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800'])[1]")
    EDIT_BUTTON = (By.XPATH, "(//*[name()='path'])[23]")
    
    # Form elements
    TEXT_INPUTS = (By.XPATH, "//input[@type='text']")
    NUMBER_INPUTS = (By.XPATH, "//input[@type='number']")
    DROPDOWNS = (By.XPATH, "//select")
    ACTIVE_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")

    # ================= INIT =================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= METHODS =================
    def verifying_bannerManagement(self):
        """Verify if user is on banner management page"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.BANNER_MANAGEMENT_TITLE)
            )
            return True
        except Exception as e:
            print("Error verifying banner management page:", e)
            return False

    def clicking_button(self):
        """Click activate or deactivate button and print status text, then revert back"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            # First click
            button = None
            try:
                button = self.wait.until(
                    EC.presence_of_element_located(self.DEACTIVATE_BUTTON)
                )
            except:
                button = self.wait.until(
                    EC.presence_of_element_located(self.ACTIVATE_BUTTON)
                )
            
            print(f"Button text before clicking: {button.text}")
            ActionChains(self.driver).move_to_element(button).click().perform()
            
            status_span = self.wait.until(
                EC.presence_of_element_located(self.STATUS_SPAN)
            )
            print(f"Status text after clicking: {status_span.text}")
            
            # Second click to revert back
            try:
                button = self.wait.until(
                    EC.presence_of_element_located(self.DEACTIVATE_BUTTON)
                )
            except:
                button = self.wait.until(
                    EC.presence_of_element_located(self.ACTIVATE_BUTTON)
                )
            
            print(f"Button text before reverting: {button.text}")
            ActionChains(self.driver).move_to_element(button).click().perform()
            
            status_span = self.wait.until(
                EC.presence_of_element_located(self.STATUS_SPAN)
            )
            print(f"Status text after reverting: {status_span.text}")
            return True
        except Exception as e:
            print("Error clicking button:", e)
            return False

    def clicking_edit_button(self):
        """Click edit button"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            edit_btn = self.wait.until(
                EC.presence_of_element_located(self.EDIT_BUTTON)
            )
            ActionChains(self.driver).move_to_element(edit_btn).click().perform()
            return True
        except Exception as e:
            print("Error clicking edit button:", e)
            return False

    def editing_banner(self):
        """Edit banner form with test data"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.support.ui import Select
            import os
            
            # Fill text inputs
            text_inputs = self.driver.find_elements(*self.TEXT_INPUTS)
            for input_field in text_inputs:
                if input_field.is_displayed() and input_field.is_enabled():
                    input_field.clear()
                    input_field.send_keys("This is testing banner from selenium")
            
            # Fill number inputs
            number_inputs = self.driver.find_elements(*self.NUMBER_INPUTS)
            for input_field in number_inputs:
                if input_field.is_displayed() and input_field.is_enabled():
                    input_field.clear()
                    input_field.send_keys("123")
            
            # Handle dropdowns
            dropdowns = self.driver.find_elements(*self.DROPDOWNS)
            for dropdown in dropdowns:
                if dropdown.is_displayed() and dropdown.is_enabled():
                    select = Select(dropdown)
                    if len(select.options) > 1:
                        select.select_by_index(1)
            
            # Uncheck active checkbox if checked
            checkboxes = self.driver.find_elements(*self.ACTIVE_CHECKBOX)
            for checkbox in checkboxes:
                if checkbox.is_displayed() and checkbox.is_enabled() and checkbox.is_selected():
                    ActionChains(self.driver).move_to_element(checkbox).click().perform()
            
            # Upload file
            file_inputs = self.driver.find_elements(*self.FILE_INPUT)
            for file_input in file_inputs:
                if file_input.is_displayed():
                    # Create a simple test image file
                    from PIL import Image
                    test_file_path = os.path.join(os.getcwd(), "test_image.jpg")
                    img = Image.new('RGB', (100, 100), color='red')
                    img.save(test_file_path)
                    file_input.send_keys(test_file_path)
                    
                    # Handle any alert that might appear
                    try:
                        self.wait.until(EC.alert_is_present())
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except:
                        pass
            
            # Click save button
            save_buttons = self.driver.find_elements(*self.SAVE_BUTTON)
            for save_btn in save_buttons:
                if save_btn.is_displayed() and save_btn.is_enabled():
                    ActionChains(self.driver).move_to_element(save_btn).click().perform()
                    break
            
            return True
        except Exception as e:
            print("Error editing banner:", e)
            # Handle any remaining alerts
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
            return False