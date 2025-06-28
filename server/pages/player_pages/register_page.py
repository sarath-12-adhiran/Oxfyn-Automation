from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import PLAYER_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots
import time

class RegisterPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver

    REGISTER_MODAL_BUTTON = (By.XPATH, "//button//span[text()='SIGN UP']") 
    USERNAME_FIELD = (By.XPATH, "//div//input[@placeholder='Enter your username']")
    PASSWORD_FIELD = (By.XPATH, "//div//input[@placeholder='Enter your password']")
    CONFIRM_PASSWORD_FIELD = (By.XPATH, "//div//input[@placeholder='Enter your confirm password']")
    # PROMO_CODE_FIELD = (By.NAME, "promoCode")
    COUNTRY_CODE_DROPDOWN = (By.ID, "mui-component-select-countryId")
    MOBILE_NUMBER_FIELD = (By.XPATH, "//div//input[@placeholder='Enter Mobile Number']")
    AGE_CHECKBOX = (By.XPATH, '//input[@name="is18Plus"]/parent::span')
    TERMS_CHECKBOX = (By.XPATH, '//input[@name="isTermsAndConditions"]/parent::span')
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Sign Up Now']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")
    PROFILE_BTN = (By.XPATH, "//p[text()='Profile']/following-sibling::button")
    LOGOUT_BTN = (By.XPATH, "//li[contains(., 'LOGOUT')]")

    def navigate_to_register(self):
        try:
            self.logger.info(f"Navigating to {PLAYER_BASE_URL}")
            self.driver.get(PLAYER_BASE_URL)
            self.logger.info("Attempting to trigger registration modal")
            register_model = self.wait(self.REGISTER_MODAL_BUTTON)
            self.click(register_model)
            self.logger.info("Registration modal loaded successfully")
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to load registration modal at {PLAYER_BASE_URL}: {str(e)}")
            raise

    def register(self, username, password, confirm_password, country_code, mobile_number, age_confirm=True, terms_agree=True):
        try:
            self.logger.info("Filling registration form")
            self.enter_text(self.USERNAME_FIELD, username)
            
            self.enter_text(self.PASSWORD_FIELD, password)

            self.enter_text(self.CONFIRM_PASSWORD_FIELD, confirm_password)
            # self.enter_text(self.PROMO_CODE_FIELD, promo_code)

            self.click(self.COUNTRY_CODE_DROPDOWN)

            dropdown_option = (By.XPATH, f"//li[text()='{country_code}']")
            self.click(dropdown_option)

            self.enter_text(self.MOBILE_NUMBER_FIELD, mobile_number)

            if age_confirm:
                self.click(self.AGE_CHECKBOX)

            if terms_agree:
                self.click(self.TERMS_CHECKBOX)
           
            self.logger.info("Submitting registration form")
            take_screenshots(self.driver, "register_form")

            self.click(self.REGISTER_BUTTON)

        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to interact with registration form: {str(e)}")
            raise

    def logout(self):
        try:
            profile_btn = self.wait(self.PROFILE_BTN)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", profile_btn)
            self.driver.execute_script("arguments[0].click();", profile_btn)
            # self.click(profile_btn)
            self.click(self.LOGOUT_BTN)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to logout: {str(e)}")
            raise

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