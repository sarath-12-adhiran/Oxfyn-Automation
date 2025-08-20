from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from utils.helpers import take_screenshots
import re
import time

class VerticalPage(BasePage):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver
    SWIPER_WRAPPER = (By.XPATH, "//div[@class='swiper-wrapper']")
    def navigate_to_verticals(self, verticals):
        try:
            vertical_btn = self.wait((By.XPATH, f"//button[normalize-space()='{verticals}']"))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", vertical_btn)
            self.driver.execute_script("arguments[0].click();", vertical_btn)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"unable to redirect casino page: {str(e)}")
            raise   

    def find_lobby(self, lobby_name):
        try:

            swiper = self.wait(self.SWIPER_WRAPPER)

            lobby = swiper.find_element(By.XPATH, f"//div[@class='swiper-slide']//button[p[text()='{lobby_name}']]")
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", lobby)

            if lobby:
                return f"{lobby_name} Founded!"

            else:
                False
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"unable to get the lobby: {str(e)}")
            raise   
    