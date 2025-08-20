from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from utils.helpers import take_screenshots
import re
import time

class DepositPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver
    
    DEPOSIT_BUTTON = (By.XPATH, "//button[normalize-space()='₹ Deposit']")
    UTR_NUMBER = (By.XPATH, "//label[text()='Enter UTR Number']/following-sibling::div//input")
    INPUT_FILE = (By.ID, "file-upload")
    SUBMIT_BTN = (By.XPATH, "//button//span[text()='Submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")
    REFRESH_BUTTON = (By.CSS_SELECTOR, ".css-dum73y")
    
    DEPOSIT_AMOUNT = (By.XPATH, "//p[text()='Balance']/following-sibling::p")
    
    def trigger_deposit_btn(self):
        #Trigger Desposit button
        self.logger.info("triggering deposit button.")
        deposit_btn = self.wait(self.DEPOSIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", deposit_btn)
        self.driver.execute_script("arguments[0].click();", deposit_btn)
        # self.click(deposit_btn)
        self.logger.info("successfully triggered deposit button.")


    def verify_campaign(self, campaign_name):
        try:
        
            swiper_sliders = (By.XPATH, f"//div[contains(@class, 'swiper-slide')]//p[contains(text(), '{campaign_name}')]")
            slide = self.wait(swiper_sliders)
            self.logger.info(f"campaign founded ******************{slide}")
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", slide)
            time.sleep(5)
            return "Campaign Founded" if slide else False
        
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to intract with deposit form: {str(e)}")
            raise   
    

    def deposit_amount(self, coupon_code, utr_number, file_path):
        try:
            swiper_sliders = (By.XPATH, f"//div[contains(@class, 'swiper-slide')]//p[contains(text(), '{coupon_code}')]")
            slide = self.wait(swiper_sliders)
            self.logger.info(f"****************8888ddsf {slide}")
            if not slide:
                self.logger.error("slider element not found*************")

            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", slide)
            # Get the swiper-slide container
            parent_slide = slide.find_element(By.XPATH, "./ancestor::div[contains(@class, 'swiper-slide')]")


            # Find the "Apply Code" button inside it
            apply_button = parent_slide.find_element(By.XPATH, ".//button[.//p[text()='Apply Code']]")

            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", apply_button)
            self.driver.execute_script("arguments[0].click();", apply_button)
            # self.click(apply_button)
            
            # Try primary locator
            self.enter_text(self.UTR_NUMBER, utr_number)
            self.logger.info(f"Successfully entered UTR number {utr_number}")
            
            
            if not os.path.exists(file_path):
                self.logger.error(f"Image file not found at {file_path}")
                return  # Stop test early if file doesn't exist

            file_input = self.wait(self.INPUT_FILE)

            # Make sure it's not 'display: none' or hidden
            self.driver.execute_script("""
                arguments[0].style.display = 'block';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.opacity = 1;
            """, file_input)

            # Upload the file
            file_input.send_keys(file_path)

            self.logger.info(f"Successfully uploaded image from {file_path}")

            take_screenshots(self.driver, "deposit_page")
            # Submit the form
            self.click(self.SUBMIT_BTN)

            #enter utr number
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to intract with deposit form: {str(e)}")
            raise   
    
    def verify_deposit(self):
        deposit_amount = None
        try:
            refresh_element = self.wait(self.REFRESH_BUTTON)
            self.driver.execute_script("arguments[0].click();", refresh_element)
            
            time.sleep(5)
            deposit_amount = self.wait(self.DEPOSIT_AMOUNT)
            
            amount = self.driver.execute_script("return arguments[0].innerText;", deposit_amount)

            deposit_amount = re.sub(r'[^\d.]', '', amount)
            take_screenshots(self.driver, "deposited")

        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to intract with deposit form: {str(e)}")
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
    