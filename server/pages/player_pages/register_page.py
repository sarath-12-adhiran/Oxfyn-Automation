from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots
import time

class RegisterPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver

    # Modal trigger button
    REGISTER_MODAL_BUTTON = (By.CSS_SELECTOR, ".css-1vvn66i") 

    # Form field locators
    USERNAME_FIELD = (By.NAME, "userName")
    PASSWORD_FIELD = (By.NAME, "password")
    CONFIRM_PASSWORD_FIELD = (By.NAME, "confirmPassword")
    # PROMO_CODE_FIELD = (By.NAME, "promoCode")
    COUNTRY_CODE_DROPDOWN = (By.ID, "mui-component-select-countryCode")
    MOBILE_NUMBER_FIELD = (By.NAME, "mobile")
    AGE_CHECKBOX = (By.XPATH, '//input[@name="is18Plus"]/parent::span')
    TERMS_CHECKBOX = (By.XPATH, '//input[@name="agree"]/parent::span')
    REGISTER_BUTTON = (By.CSS_SELECTOR, ".css-d2r5ds")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")

    PROFILE_BTN = (By.CSS_SELECTOR, ".css-21z1y4")

    LOGOUT_BTN = (By.CSS_SELECTOR, ".css-9m9epz")

    def navigate_to_register(self):
        try:
            self.logger.info(f"Navigating to {BASE_URL}")
            self.driver.get(BASE_URL)
            self.logger.info("Attempting to trigger registration modal")
            self.click(self.REGISTER_MODAL_BUTTON)
            self.logger.info("Registration modal loaded successfully")
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to load registration modal at {BASE_URL}: {str(e)}")
            raise

    def register(self, username, password, confirm_password, country_code, mobile_number, age_confirm=True, terms_agree=True):
        try:
            self.logger.info("Filling registration form")
            self.enter_text(self.USERNAME_FIELD, username)
            time.sleep(2)
            self.enter_text(self.PASSWORD_FIELD, password)
            time.sleep(2)
            self.enter_text(self.CONFIRM_PASSWORD_FIELD, confirm_password)
            # self.enter_text(self.PROMO_CODE_FIELD, promo_code)
            time.sleep(2)
            # Click dropdown to open options
            self.logger.debug("Clicking country code dropdown")
            self.click(self.COUNTRY_CODE_DROPDOWN)
            # Select option by value
            dropdown_option = (By.XPATH, f"//li[@value='{country_code}']")
            self.click(dropdown_option)
            time.sleep(2)
            self.enter_text(self.MOBILE_NUMBER_FIELD, mobile_number)
            time.sleep(2)
            if age_confirm:
                self.click(self.AGE_CHECKBOX)
            time.sleep(2)
            if terms_agree:
                self.click(self.TERMS_CHECKBOX)
            time.sleep(2)
            # Check if Register button is enabled
            self.logger.info(f"Register button enabled: {self.find_element(self.REGISTER_BUTTON).is_enabled()}")
            # Wait for Register button to be clickable
            self.logger.info("Submitting registration form")
            take_screenshots(self.driver, "register_form")
            self.click(self.REGISTER_BUTTON)

        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to interact with registration form: {str(e)}")
            raise

    def logout(self):
        try:
            #trigger profiel button
            time.sleep(2)
            self.click(self.PROFILE_BTN)
            take_screenshots(self.driver, "profile_page")
            time.sleep(2)
            self.click(self.LOGOUT_BTN)
        except TimeoutException as e:
            self.logger.error(f"Failed to logout: {str(e)}")
            raise

    def get_success_message(self):
        try:
            msg = self.get_text(self.SUCCESS_MESSAGE)
            if msg:
                take_screenshots(self.driver, f"{msg}")
            self.logger.info(f"Success message: {msg}")
            return msg
        except:
            self.logger.warning("Success message not found")
            return "Unable to get the message"

    def get_error_message(self):
        try:
            msg = self.get_text(self.ERROR_MESSAGE)
            if msg:
                take_screenshots(self.driver, f"{msg}")
            self.logger.info(f"Error message: {msg}")
            return msg
        except:
            self.logger.warning("Error message not found")
            return "Unable to get the message"

    