from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import BACKEND_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
from utils.helpers import take_screenshots

class BackendLoginPage(BasePage):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    USERNAME = (By.CSS_SELECTOR, '.css-sydhbg')
    PASSWORD = (By.CSS_SELECTOR, '.css-1yxkpls')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.css-1nc1bkw')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")


    def navigate_to_backend_login(self):
        try:
            self.logger.info(f"Navigating to {BACKEND_BASE_URL}")
            self.driver.get(BACKEND_BASE_URL)
            self.logger.info("successfully navigated to backend")
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to load backend {BACKEND_BASE_URL}: {str(e)}")
            raise

    def backend_login(self, username, password, captcha):
        
        try:
            #assigning values

            self.enter_text(self.USERNAME, username)
            self.enter_text(self.PASSWORD, password)
            # Wait for login button to be clickable
            time.sleep(10) 
            take_screenshots(self.driver, "backend_login_page")
            self.click(self.LOGIN_BUTTON)
        except TimeoutException as e:
            self.logger.error(f"error to login: {str(e)}")
            raise

    
    def get_success_message(self):
        try:
            msg = self.get_text(self.SUCCESS_MESSAGE)
            take_screenshots(self.driver, f"{msg}")
            self.logger.info(f"Success message: {msg}")
            return msg
        except:
            self.logger.warning("Success message not found")
            return "Unable to get the message"
        
    def get_error_message(self):
        try:
            msg = self.get_text(self.ERROR_MESSAGE)
            take_screenshots(self.driver, f"{msg}")
            self.logger.info(f"Error message: {msg}")
            return msg
        except:
            self.logger.warning("Error message not found")
            return "Unable to get the message"

    
