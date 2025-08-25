from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from config.config import PLAYER_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots
import pandas as pd
import openpyxl
import os
import re
import time

class WalletAdjustmentPage(BasePage):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    WALLET_ADJUSTMENT = (By.XPATH, "//li[a/div/div//p[text()='Wallet Adjustment']]")
    MASS_UPLOAD = (By.XPATH, "//button[@aria-label='Mass Adjustment']")
    UPLOAD_INPUT = (By.CSS_SELECTOR, 'input[type="file"]')
    UPLOAD_BUTTON = (By.XPATH, "//button[normalize-space()='Upload']")
    PROFILE_BTN = (By.XPATH, "//p[text()='Profile']/following-sibling::button")
    WALLET_BTN = (By.XPATH, '//a[@href="/wallet"]')
    MONEY = (By.XPATH, ".//div[starts-with(@class, 'MuiBox-root')]")

    BRAND = (By.CSS_SELECTOR, "div[aria-labelledby='brand-select-label']")
    PLAYER_NAME = (By.XPATH, "//label[text()='Player Name']/following::input[1]")
    AMOUNT = (By.XPATH, "//label[text()='Amount']/following::input[1]")
    ADJUSTMENT_DROPDOWN = (By.XPATH,"//div[@role='combobox' and @id='adjustmenttype']")
    WALLET_DROPDOWN = (By.XPATH, "//div[@role='combobox' and @id='walletType']")
    POCKET_DROPDOWN = (By.XPATH, "//div[@role='combobox' and @id='pockettype']")

    ADJUST_BUTTON = (By.XPATH, "//button[normalize-space()='Adjust']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".Toastify__toast--error")

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
                self.logger.info("excel file not found")

            df = pd.read_excel(filepath, engine="openpyxl")
            df['playerUserName'] = pd.NA
            df['amount'] = pd.NA
            df['playerUserName'] = username
            df['amount'] = amount

            df.to_excel(filepath, index=False)

            self.wait(self.UPLOAD_INPUT)
            file_input = self.find_element(self.UPLOAD_INPUT)

            file_input.send_keys(filepath)

            upload_button = self.wait(self.UPLOAD_BUTTON)
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
            profile_btn = self.wait(self.PROFILE_BTN)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", profile_btn)
            self.driver.execute_script("arguments[0].click();", profile_btn)

            self.wait(self.WALLET_BTN)
            self.click(self.WALLET_BTN)

            # Find the container element first
            container = self.driver.find_element(By.CSS_SELECTOR, ".css-1hiomp7")
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", container)

            boxes = container.find_elements(By.XPATH, ".//div[contains(@class, 'MuiPaper-root')]")
            self.logger.info("boxes founded")

            for i, block in enumerate(boxes):
                para = block.find_elements(By.TAG_NAME, "span")
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

    def wallet_adjustment_for_win(self, brand_name, player_name, amount, adjustment_type, wallet_type, pocket_type):
        try:
            time.sleep(2)
            self.click(self.BRAND)
        
            BRAND_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{brand_name}']"))
            BRAND_TYPE.click()
            
            self.enter_text(self.PLAYER_NAME, player_name)
            time.sleep(15)
            PLAYER_OPTION = self.find_element((By.XPATH, f"//li[text()='{player_name}']"))
            PLAYER_OPTION.click()

            self.enter_text(self.AMOUNT, amount)

            self.click(self.ADJUSTMENT_DROPDOWN)

            ADJUSTMENT_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{adjustment_type}']"))
            ADJUSTMENT_TYPE.click()

            self.click(self.WALLET_DROPDOWN)
            WALLET_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{wallet_type}']"))
            WALLET_TYPE.click()

            self.click(self.POCKET_DROPDOWN)
            POCKET_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{pocket_type}']"))
            POCKET_TYPE.click()

            self.wait(self.ADJUST_BUTTON)
            self.click(self.ADJUST_BUTTON)
    
        except (WebDriverException,TimeoutException) as e:
            self.logger.error(f"some error occured: {str(e)}")
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
            self.logger.error(f"unable to get error: {str(e)}")
            raise
