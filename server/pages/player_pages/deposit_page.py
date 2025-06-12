from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import DEPOSIT_PAGE
from selenium.common.exceptions import WebDriverException, TimeoutException
import os


class DepositPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver
    
    DEPOSIT_BUTTON = (By.CSS_SELECTOR, ".css-rdb04b")
    AMOUNT_BUTTONS = (By.CSS_SELECTOR, ".css-1eikg3m")
    UTR_NUMBER = (By.XPATH, "//p[text()='Enter UTR Number']/following::input[1]")
    INPUT_FILE = (By.ID, 'file-upload')
    SUBMIT_BTN = (By.CSS_SELECTOR, '.css-criioj')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")
    SWIPER_SLIDES = (By.CLASS_NAME, "swiper-slide")

    def trigger_deposit_btn(self):
        #Trigger Desposit button
        self.logger.info("triggering deposit button.")
        self.click(self.DEPOSIT_BUTTON)
        self.logger.info("successfully triggered deposit button.")

    def deposit_amount(self, coupon_code, utr_number, file_path):
        try:
            self.logger.info(f"checking Coupons {coupon_code} is available")

            swiper_sliders = (By.XPATH, f"//div[contains(@class, 'swiper-slide')]//p[contains(text(), '{coupon_code}')]")
            slide = self.find_element(swiper_sliders)

            # Find the parent swiper-slide of the coupon code
            parent_slide = slide.find_element(By.XPATH, "./ancestor::div[contains(@class, 'swiper-slide')]")

            # Locate the "Apply Code" button within the same slide
            apply_button = parent_slide.find_element(By.XPATH, ".//button[contains(text(), 'Apply Code')]")

            self.click(apply_button)
            self.logger.info(f"Successfully clicked the 'Apply Code' button for coupon code {coupon_code}")
            
            # Try primary locator
            self.enter_text(self.UTR_NUMBER, utr_number)
            self.logger.info(f"Successfully entered UTR number {utr_number}")
            
            
            if not os.path.exists(file_path):
                self.logger.error(f"Image file not found at {file_path}")
                return  # Stop test early if file doesn't exist

            # Wait for the input field to be present in DOM
            wait = WebDriverWait(self.driver, 10)
            file_input = wait.until(EC.presence_of_element_located(self.INPUT_FILE))


            # Unhide the file input
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)

            # Send file path to input
            file_input.send_keys(file_path)
            self.logger.info(f"Successfully uploaded image from {file_path}")

            # Submit the form
            self.click(self.SUBMIT_BTN)

            #enter utr number
        except TimeoutException as e:
            self.logger.error(f"Failed to intract with deposit form: {str(e)}")
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

    

    