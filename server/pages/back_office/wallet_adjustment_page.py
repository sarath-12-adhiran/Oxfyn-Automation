from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import PLAYER_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
from utils.helpers import take_screenshots
import pandas as pd
import openpyxl
import os
import re

class WalletAdjustmentPage(BasePage):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    WALLET_ADJUSTMENT = (By.XPATH, "//li[a/div/div//p[text()='Wallet Adjustment']]")
    MASS_UPLOAD = (By.XPATH, "//button[@aria-label='Mass Adjustment']")
    UPLOAD_INPUT = (By.CSS_SELECTOR, 'input[type="file"]')
    UPLOAD_BUTTON = (By.XPATH, "//button[normalize-space()='Upload']")
    PROFILE_BTN = (By.CSS_SELECTOR, ".css-21z1y4")
    WALLET_BTN = (By.XPATH, '//a[@href="/wallet"]')
    MONEY = (By.XPATH, ".//div[starts-with(@class, 'MuiBox-root')]")

    def click_wallet_adjustment_button(self):
        try:
            if not self.find_element(self.WALLET_ADJUSTMENT):
                self.logger.info("wallet button not found")
            self.click(self.WALLET_ADJUSTMENT)
        except (WebDriverException) as e:
            self.logger.error(f"some error occured: {str(e)}")
    
    def add_wallet_adjustemnt(self, filepath, username, amount):
        try:
            #click upload button
            self.click(self.MASS_UPLOAD)

            if not os.path.exists(filepath):
                print("excel file not found")
            time.sleep(2)
            df = pd.read_excel(filepath, engine="openpyxl")
            df['playerUserName'] = pd.NA
            df['amount'] = pd.NA
            df['playerUserName'] = username
            df['amount'] = amount

            df.to_excel(r"C:\Users\sujit\OneDrive\Documents\GitHub\Oxfyn-Automation\server\static\sample_file.xlsx", index=False)
            time.sleep(2)

            self.wait(self.UPLOAD_INPUT)
            file_input = self.find_element(self.UPLOAD_INPUT)
            time.sleep(2)
            file_input.send_keys(filepath)
            time.sleep(2)
            self.wait(self.UPLOAD_BUTTON, seconds=30)
            self.click(self.UPLOAD_BUTTON)

        except (WebDriverException,TimeoutException) as e:
            self.logger.error(f"some error occured: {str(e)}")

    def redirect_to_player_page(self):
        try:
            self.driver.get(PLAYER_BASE_URL)
        except (WebDriverException,TimeoutException) as e:
            self.logger.error(f"some error occured: {str(e)}")    
            
    def validate_player_wallet(self):
        amount = []

        try:
            self.click(self.PROFILE_BTN)
            self.wait(self.WALLET_BTN,seconds=30)
            self.click(self.WALLET_BTN)

            time.sleep(5)
            # Find the container element first
            container = self.driver.find_element(By.CSS_SELECTOR, ".css-f9ihvp")
            self.driver.execute_script("arguments[0].scrollIntoView();", container)
            # Find all sub-boxes with class starting with 'css-1niqfd2' or 'css-1ks1ssp'
            time.sleep(5)
            boxes = container.find_elements(By.XPATH, ".//div[starts-with(@class, 'MuiBox-root')]")
            self.logger.info("boxes founded")
            time.sleep(5)

            for i, block in enumerate(boxes):
                para = block.find_elements(By.TAG_NAME, "p")
                self.logger.info(f"[{i}] paragraph count: {len(para)}")

                if len(para) < 2:
                    self.logger.warning(f"[{i}] Less than 2 paragraphs found, skipping block")
                    continue

                try:
                    label = para[0].text.strip()
                    value_text = para[1].text.strip()

                    # Remove currency symbol and commas (e.g., ₹1,000.00 -> 1000.00)
                    value = re.sub(r'[^\d.]', '', value_text)

                    self.logger.info(f"[{i}] Extracted -> label: {label}, raw value: {value_text}, cleaned value: {value}")
                    amount.append({"label": label, "value": value})
                    take_screenshots(self.driver, f"wallet")
                except Exception as e:
                    self.logger.error(f"[{i}] Error extracting label/value: {e}")
                    take_screenshots(self.driver, f"wallet")

        except (WebDriverException,TimeoutException) as e:
            self.logger.error(f"some error occured: {str(e)}")
        return amount if amount else []

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

    
