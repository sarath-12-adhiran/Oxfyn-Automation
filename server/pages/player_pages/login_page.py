from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import PLAYER_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots
import time

class LoginPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver
        
    LOGIN_MODAL_BUTTON = (By.XPATH, "//button//span//span[text()='LOGIN']") 
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Login']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")


    def navigate_to_login(self):
        try:
            self.logger.info(f"Navigating to {PLAYER_BASE_URL}")
            self.driver.get(PLAYER_BASE_URL)
            self.logger.info("Attempting to trigger login modal")
            login_element = self.wait(self.LOGIN_MODAL_BUTTON)
            self.click(login_element)
            self.logger.info("login modal loaded successfully")
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to load login modal at {PLAYER_BASE_URL}: {str(e)}")
            raise

    def login(self, username, password):
        try:
            self.logger.info("Filling login form")
            self.enter_text(self.USERNAME_FIELD, username)
            self.enter_text(self.PASSWORD_FIELD, password)
            login_btn = self.wait(self.LOGIN_BUTTON)
            take_screenshots(self.driver, f"login_form")
            self.logger.info("Submitting registration form")
            self.click(login_btn)
        except TimeoutException as e:
            self.logger.error(f"Failed to interact with login form: {str(e)}")
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

    