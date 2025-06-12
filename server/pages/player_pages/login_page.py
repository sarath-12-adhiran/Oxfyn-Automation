from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException

class LoginPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver
        
    # Modal trigger button
    LOGIN_MODAL_BUTTON = (By.CSS_SELECTOR, ".css-1kh64c0") 

    # Form field locators
    USERNAME_FIELD = (By.NAME, "userName")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".css-survuw")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")


    def navigate_to_login(self):
        try:
            self.logger.info(f"Navigating to {BASE_URL}")
            self.driver.get(BASE_URL)
            self.logger.info("Attempting to trigger login modal")
            self.click(self.LOGIN_MODAL_BUTTON)
            self.logger.info("login modal loaded successfully")
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to load login modal at {BASE_URL}: {str(e)}")
            raise

    def register(self, username, password):
        try:
            self.logger.info("Filling login form")
            self.enter_text(self.USERNAME_FIELD, username)
            self.enter_text(self.PASSWORD_FIELD, password)

            
            # Check if login button is enabled
            self.logger.info(f"login button enabled: {self.find_element(self.LOGIN_BUTTON).is_enabled()}")
            # Wait for Register button to be clickable
            self.logger.info("Waiting for login button to be enabled")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON)
            )
            
            self.logger.info("Submitting registration form")
            self.click(self.LOGIN_BUTTON)
        except TimeoutException as e:
            self.logger.error(f"Failed to interact with login form: {str(e)}")
            raise

    def get_success_message(self):
        try:
            msg = self.get_text(self.SUCCESS_MESSAGE)
            self.logger.info(f"Success message: {msg}")
            return msg
        except:
            self.logger.warning("Success message not found")
            return "Unable to get the message"

    def get_error_message(self):
        try:
            msg = self.get_text(self.ERROR_MESSAGE)
            self.logger.info(f"Error message: {msg}")
            return msg
        except:
            self.logger.warning("Error message not found")
            return "Unable to get the message"

    