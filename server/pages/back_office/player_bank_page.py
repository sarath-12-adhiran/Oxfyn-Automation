from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from config.config import BACKEND_BASE_URL
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots
import pandas as pd
import openpyxl
import os
import re
import time

class PlayerBankPage(BasePage):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    player_bank_btn = (By.XPATH, "//li[a/div/div//p[text()='Player Bank Details']]")

    bank_create_btn = (By.XPATH, "//button[normalize-space()='Create Bank']")
    username_input = (By.XPATH, "//input[@name='userName']")
    bank_name = (By.XPATH, "//input[@name='bankName']")
    ifsc_code = (By.XPATH, "//input[@name='ifscCode']")
    account_number = (By.XPATH, "//input[@name='accountNumber']")
    name = (By.XPATH, "//input[@name='name']")
    account_dropdown = (By.XPATH, "//div[@role='combobox' and @id='mui-component-select-accountType']")
    branch = (By.XPATH, "//input[@name='branch']")

    submit_btn = (By.XPATH, "//button[normalize-space()='Create']")
    

    offline_withdrawal = (By.XPATH, "//li[a/div/div//p[text()='Offline Withdrawal']]")
    approve_btn = (By.XPATH, "//li[a/div/div//p[text()='Approve']]")

    # def navigate_to_backoffice(self):
    #     self.driver.get(BACKEND_BASE_URL)

    def trigger_bank_menu(self):
        self.logger.info("trigger Player Bank button")
        bank_btn = self.wait(self.player_bank_btn)
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", bank_btn)
        self.click(bank_btn)
        self.click(self.bank_create_btn)

    def create_player_bank(self, username, bank_name, ifsc_code, account_number, name,  account_type, branch):

        try:
            self.logger.info("Creating player bank account")

            time.sleep(5)
            self.find_element(self.username_input).send_keys(username)

            PLAYER_OPTION = self.find_element((By.XPATH, f"//li[text()='{username}']"))
            PLAYER_OPTION.click()

            self.enter_text(self.bank_name, bank_name)

            self.enter_text(self.ifsc_code, ifsc_code)

            self.enter_text(self.account_number, account_number)

            self.enter_text(self.name, name)

            self.click(self.account_dropdown)

            ADJUSTMENT_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{account_type}']"))
            ADJUSTMENT_TYPE.click()


            self.enter_text(self.branch, branch)

            self.click(self.submit_btn)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Error occurred while creating player bank account: {e}")


    def create_and_auto_approve_offile_withdrawal(self, brand_name, username, withdraw_amount):
        try:
            self.logger.info("Creating and auto approving offline withdrawal")
            self.click(self.offline_withdrawal)
            self.enter_text(self.username_input, username)
            self.enter_text(self.withdrawal_amount, withdraw_amount)
            self.click(self.approve_btn)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Error occurred while creating and auto approving offline withdrawal: {e}")