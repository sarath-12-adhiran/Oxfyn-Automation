from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
from utils.helpers import take_screenshots
from datetime import datetime, timezone, date
import calendar

class CampaignPage(BasePage):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    CAMPAIGN = (By.XPATH, "/html/body/div[1]/nav/div/div/div/div/ul/li[16]/a")
    CREATE_BUTTON = (By.XPATH, "//button[text()='Create']")
    BRAND_DROPDOWN = (By.XPATH, "//div[@id='reportingHirearchyUserId']")
    CAMPAIGN_TYPE_DROPDOWN = (By.ID, "mui-component-select-campaignType")
    VERTICAL_DROPDOWN = (By.ID, "gameVertical")
    BONUS_DROPDOWN = (By.ID, "bonusType")
    MAX_REDEEM_AMOUNT = (By.NAME, "maxWithDrawlCap")
    DEPOSIT_DROPDOWN = (By.ID, "mui-component-select-depositType")
    CAMPAIGN_NAME = (By.NAME, "name")
    BONUS = (By.ID, "mui-component-select-processType")
    EXPIRE_COUNT = (By.NAME, "expiryDayCount")
    ACTIVE_STATUS = (By.ID, "mui-component-select-activeStatus")
    MIN_DEPOSIT = (By.NAME, "minimumDepositLimit")
    CAMPAIGN_CODE = (By.NAME, "code")
    TURNOVER = (By.NAME, "turnoverMultipliers")
    MAX_BONUS_AMOUNT = (By.NAME, "maxBonusAmount")
    DATE_RANGE_BUTTON = (By.XPATH, "//button[normalize-space()='Select date range']")
    PROMOTE = (By.XPATH, "//label[.//span[text()='Promote']]")
    BONUS_AMOUNT = (By.XPATH, "//input[@name='bonusAmount']")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='create']")


    PREVIOUS_BTN = (By.XPATH, "//button[.//svg[contains(@class, 'lucide-chevron-left')]]")
    FORWARD_BTN = (By.XPATH, "//button[.//svg[contains(@class, 'lucide-chevron-right')]]")
    APPLY_BTN = (By.XPATH, "//button[normalize-space()='Apply']")
    TODAY = (By.XPATH, "//div//button[normalize-space()='Today']")

    def navigate_to_campaign(self):
        try:
            camp_btn = self.wait(self.CAMPAIGN)
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", camp_btn)
            self.driver.execute_script("arguments[0].click();", camp_btn)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Error navigating to campaign: {str(e)}")
            raise

    def create_campaign(self, brand_name, campaign_type, vertical_name, bonus_type, max_redeem, deposit_type, campaign_name, bonus, expiry_count, active_status, min_deposit, campaign_code, turnover, max_bonus, date_range, bonus_amount, start_date, end_date):
        try:
            self.click(self.CREATE_BUTTON)

            brand_element  = self.wait(self.BRAND_DROPDOWN)
            if not brand_element:
                self.logger.error("brand element not found ***********************************")
            self.click(brand_element)


            BRAND_NAME = self.wait((By.XPATH, f"//ul[@role='listbox']//li[text()='{brand_name}']"))
            self.click(BRAND_NAME)

            self.click(self.CAMPAIGN_TYPE_DROPDOWN)

            CAMPAIGN_NAME = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{campaign_type}']"))
            CAMPAIGN_NAME.click()

            self.click(self.VERTICAL_DROPDOWN)

            VERTICAL_NAME = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{vertical_name}']"))
            VERTICAL_NAME.click()

            self.click(self.BONUS_DROPDOWN)

            BONUS_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{bonus_type}']"))
            BONUS_TYPE.click()

            self.enter_text(self.MAX_REDEEM_AMOUNT, max_redeem)

            self.click(self.DEPOSIT_DROPDOWN)

            DEPOSIT_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{deposit_type}']"))
            DEPOSIT_TYPE.click()

            self.enter_text(self.CAMPAIGN_NAME, campaign_name)

            self.click(self.BONUS)

            BONUS_METHOD = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{bonus}']"))
            BONUS_METHOD.click()

            self.enter_text(self.BONUS_AMOUNT, bonus_amount)

            self.enter_text(self.EXPIRE_COUNT, expiry_count)
            
            self.click(self.ACTIVE_STATUS)

            ACTIVE_TYPE = self.find_element((By.XPATH, f"//ul[@role='listbox']//li[text()='{active_status}']"))
            ACTIVE_TYPE.click()

            self.enter_text(self.MIN_DEPOSIT, min_deposit)
            
            self.enter_text(self.CAMPAIGN_CODE, campaign_code)

            self.enter_text(self.TURNOVER, turnover)

            self.click(self.DATE_RANGE_BUTTON)

            # self.enter_text(self.MAX_BONUS_AMOUNT, max_bonus)
            
            month = date.today().month
            year = date.today().year

            month_name = calendar.month_name[month]


            if start_date.month > month:
                self.click(self.FORWARD_BTN)

            if start_date.day:
                find_start_date_element = self.find_element((By.XPATH, f"//div//p[text()='{start_date.day}']"))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", find_start_date_element)
                self.driver.execute_script("arguments[0].click();", find_start_date_element)

            if end_date.day:
                find_end_date_element = self.find_element((By.XPATH, f"//div//p[text()='{end_date.day}']"))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", find_end_date_element)
                self.driver.execute_script("arguments[0].click();", find_end_date_element)
            
            self.click(self.APPLY_BTN)

            # CURRENT_MONTH = self.find_element((By.XPATH, f"//p[text()='{month_name} {year}']"))
            
            # self.click(self.TODAY)

            self.click(self.PROMOTE)

            self.click(self.SUBMIT_BUTTON)

        except (WebDriverException, TimeoutException) as e:
            self.logger.error("")
            raise