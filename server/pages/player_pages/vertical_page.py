from selenium.webdriver.common.by import By
from conftest import driver, lobby
from pages.base_page import BasePage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from utils.helpers import take_screenshots
import re
import time
from config.config import PLAYER_BASE_URL

class VerticalPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver
    SWIPER_WRAPPER = (By.XPATH, "//div[@class='swiper-wrapper']")

    def navigate_to_player_site(self):
        try:
            self.logger.info(f"Navigating to {PLAYER_BASE_URL}")
            self.driver.get(PLAYER_BASE_URL)

        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"unable to navigate to player site: {str(e)}")
            raise

    def navigate_to_verticals(self, verticals):
        try:
            vertical_btn = self.wait((By.XPATH, f"//button[normalize-space()='{verticals}']"))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", vertical_btn)
            self.driver.execute_script("arguments[0].click();", vertical_btn)
            time.sleep(10)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"unable to redirect casino page: {str(e)}")
            raise   

    def find_lobby(self, lobby_name):
        try:

            swiper = self.wait(self.SWIPER_WRAPPER)

            lobby = swiper.find_element(By.XPATH, f"//div[@class='swiper-slide']//button[p[text()='{lobby_name}']]")
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", lobby)
            time.sleep(10)
            if lobby:
                return f"{lobby_name} Founded!"

            else:
                False
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"unable to get the lobby: {str(e)}")
            raise   

    def verify_exchange_load(self):
        try:
            iframe = self.find_element((By.XPATH, "/html/body/div[2]/div[2]/iframe"))
            self.driver.switch_to.frame(iframe)
            self.driver.execute_script("arguments[0].click();", iframe)

            self.logger.info("Exchange loaded successfully.")
            take_screenshots(self.driver, f"Exchange_Loaded_Successfully")
            self.driver.switch_to.default_content()
            return True
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Exchange failed to load: {str(e)}")
            raise
        
    def verify_live_casino_load(self):
        try:

            lobby = self.find_element((By.XPATH, "/html/body/div[3]/div/div"))

            games = self.find_element((By.XPATH, "/html/body/div[4]/div"))

            if lobby and games:
                take_screenshots(self.driver, f"Live_Casino_Loaded_Successfully")
                return True
            else:
                return False
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"unable to get the lobby: {str(e)}")
            raise

    def verify_sports_load(self):
        try:
            iframe = self.find_element((By.XPATH, "/html/body/div[2]/div[2]/iframe"))

            self.driver.switch_to.frame(iframe)
            self.driver.execute_script("arguments[0].click();", iframe)

            self.logger.info("Exchange loaded successfully.")
            take_screenshots(self.driver, f"Exchange_Loaded_Successfully")
            self.driver.switch_to.default_content()
            return True
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Exchange failed to load: {str(e)}")
            raise

    def verify_casino_load(self):
        try:
           
            lobby = self.find_element((By.XPATH, "/html/body/div[3]/div/div"))

            games = self.find_element((By.XPATH, "/html/body/div[4]/div"))

            if lobby and games:
                take_screenshots(self.driver, f"Casino_Loaded_Successfully")
                return True
            else:
                return False
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Exchange failed to load: {str(e)}")
            raise
