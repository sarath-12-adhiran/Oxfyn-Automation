from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import PLAYER_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots
import re
import time 

class BackendOfflineDepositPage(BasePage):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    OFFLINE_DEPOSIT_BUTTON = (By.XPATH, "//li[a/div/div//p[text()='Offline Deposit']]")
    OFFLINE_SEARCH = (By.XPATH, "//li[normalize-space()='Search']")
    BRAND = (By.ID, "brandIDs-autocomplete")
    USERNAME = (By.XPATH, "//label[text()='User Name']/following::input[1]")
    UTR_INPUT = (By.XPATH, "//label[text()='UTR/Tr ID']/following::input[@type='text'][1]")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")
    PAYMENT_DROP_DOWN = (By.XPATH, "//label[text()='Payment Status']/following-sibling::div//div[@role='combobox']")
    COMMENT = (By.XPATH, "//label[text()='Comment']/following::input[@type='text'][1]")
    APPROVE = (By.XPATH, "//input[@type='radio' and @value='3']/ancestor::label")
    # REJECT = (By.CSS_SELECTOR, 'input[name="approvereject"][value="6"]')
    # UPDATE_BUTTON = (By.XPATH, "//button[@type='submit' and .//span[contains(text(), 'update')]]")  
    UPDATE_BUTTON = (By.CSS_SELECTOR, ".css-176id20")

    DIALOG_BOX = (By.XPATH, "//div[@role='dialog']//button[normalize-space()='OK']")
    # DIALOG_MESSAGE = (By.XPATH, "//div[text()='Deposit transaction Updated Successfully']")
    PROFILE = (By.CSS_SELECTOR, '.css-196w96x')

    LOGOUT_BUTTON = (By.XPATH, "//ul[@role='menu']//li[p[normalize-space()='Logout']]")


    def trigger_offile_deposit_button(self):
        try:
            self.logger.info(f"Triggering to offile deposit button")
            self.click(self.OFFLINE_DEPOSIT_BUTTON)

            self.wait(self.OFFLINE_SEARCH)
            self.click(self.OFFLINE_SEARCH)
            self.logger.info("successfully triggred")
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to trigger offline deposit button {str(e)}")
            raise

    def accept_income_deposit_request(self, username, utr_number, brand_name, payment_status, comment):
        success_message = None
        try:
            time.sleep(10)
            # Locate the input field of the Autocomplete
            input_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "brandIDs-autocomplete"))
            )
            input_field.click()
            input_field.send_keys("BET DUNIYA")

            # Wait for the dropdown list to appear and locate the matching option
            option_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//li[contains(text(), 'BET DUNIYA')]")
                )
            )

            # Click the option to select it
            option_element.click()

            self.enter_text(self.UTR_INPUT, utr_number)

            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "userName"))
            )
            input_box.click()
            input_box.clear()
            input_box.send_keys(username)

            # self.logger.info(f"***********username {username}")
            # #assigning values
            # user_element = self.find_element(self.USERNAME)
            # user_element.send_keys(username)

            # self.logger.info(f"successfully entered username {username}")
          
            if payment_status:
                #trigger payment dropdown
                self.click(self.PAYMENT_DROP_DOWN)
                
                get_options = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{payment_status}']"))

                self.click(get_options)
            
            take_screenshots(self.driver, "offline_deposit_search_form")

            # trigger search button
            self.click(self.SEARCH_BUTTON)

            self.wait((By.XPATH, "//table[@aria-label='offline deposit table']"),seconds=20)

            i = 0
            while True:
                try:
                    # Re-locate the row in each iteration
                    current_row = self.find_element((By.XPATH, f"//table[@aria-label='offline deposit table']//tbody/tr[{i+1}]"))
                    username_element = current_row.find_element(By.XPATH, "./td[1]//a")
                    self.logger.info("looping started")

                    if username_element.text.strip() == username:
                        self.logger.info(f"Username found: {username_element.text}")
                        show_button = current_row.find_element(By.XPATH, ".//td[last()]//button[normalize-space()='Show']")
                        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", show_button)
                        self.driver.execute_script("arguments[0].click();", show_button)
                        # show_button.click()
                        self.logger.info("successfully triggered show button")
                        break
                    i += 1
                except Exception as e:
                    self.logger.error(f"Error processing row {i+1}: {str(e)}")
                    if "stale element reference" in str(e).lower():
                        self.logger.info("Stale element detected, retrying...")
                        continue
                    if "no such element" in str(e).lower():
                        self.logger.info("No more rows to process")
                        break
                    raise
            
            # self.wait(self.COMMENT)
            # #comment
            # self.enter_text(self.COMMENT, comment)
            # self.logger.info("successfully entered comment")

            self.wait(self.APPROVE, seconds=20)
            approve_element=self.find_element(self.APPROVE)
            if not approve_element:
                self.logger.info("approve radio button not found")

            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", approve_element)
            self.driver.execute_script("arguments[0].click();", approve_element)
            #approve or reject
            # self.click(self.APPROVE)
            self.logger.info("successfully check the approved")        
            
            self.wait(self.UPDATE_BUTTON, seconds=20)
            update_element=self.find_element(self.UPDATE_BUTTON)
            if not update_element:
                self.logger.info("update button not found")
            self.driver.execute_script("arguments[0].scrollIntoView();", update_element)
            self.driver.execute_script("arguments[0].click();", update_element)
            take_screenshots(self.driver, "offline_deposit_approve")

            return "Deposit transaction Updated Successfully"

        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"error to load offline deposit: {str(e)}")
            raise

    # def logout(self):
    #     try:
    #         self.wait(self.PROFILE)
    #         self.click(self.PROFILE)
    #         take_screenshots(self.driver, "backend_profile_page")
    #         self.click(self.LOGOUT_BUTTON)
    #     except (WebDriverException, TimeoutException) as e:
    #         self.logger.error(f"error to logout: {str(e)}")
    #         raise

    def navigate_player_dashboard(self):
        deposit_amount = None
        try:
            self.logger.info(f"Navigating to {PLAYER_BASE_URL}")
            self.driver.get(PLAYER_BASE_URL)
            
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"error to navigate player dashboard: {str(e)}")
            raise
        return deposit_amount

    def get_success_message(self):
        try:
            msg = self.get_text(self.SUCCESS_MESSAGE)
            take_screenshots(self.driver, f"{msg}")
            self.logger.info(f"Success message: {msg}")
            return msg
        except (WebDriverException,TimeoutException) as e:
            self.logger.error(f"unable to get success message: {str(e)}")
            raise

    def get_error_message(self):
        try:
            msg = self.get_text(self.ERROR_MESSAGE)
            take_screenshots(self.driver, f"{msg}")
            self.logger.info(f"Error message: {msg}")
            return msg
        except (WebDriverException,TimeoutException) as e:
            self.logger.error(f"unable to get error message: {str(e)}")
            raise

