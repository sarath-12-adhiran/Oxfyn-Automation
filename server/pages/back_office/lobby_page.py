from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
from utils.helpers import take_screenshots
from datetime import datetime, timezone, date
from config.config import PLAYER_BASE_URL

class LobbyPage(BasePage):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    LOBBY_BUTTON = (By.XPATH,"//li[a/div/div//p[text()='Lobby Management']]")
    LOBBY_CREATE = (By.XPATH, "//li[normalize-space()='Create']")

    BRAND_DROPDOWN = (By.ID, "brand-select")
    LOBBY_NAME = (By.NAME, "lobbyName")
    VERTICAL_DROPDOWN = (By.ID, "gameVertical")
    CATEGORY_ORDER = (By.XPATH, "//input[@type='number' and @name='promote']")
    STATUS_DROPDOWN = (By.ID, "activeStatus")

    AGGREGATOR_DROPDOW  = (By.ID, "aggregator")
    GAME_PROVIDER = (By.ID, "game-provider-autocomplete")

    GAME_SEARCH = (By.XPATH, "//button[normalize-space()='Search']")
    UNASSIGNED_GAMES = (By.XPATH, "//div//h6[contains(text(), 'Unassigned Games - ')]")
    FIRST_FIVE_ITEMS = (By.XPATH, "//div//li[@role='menuitem']//div[position()=1]")
    ASSIGN_BUTTON = (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/form/div[3]/div[2]/div[2]/div/button[1]")
    SAVE_BTN = (By.XPATH, "//button[text()='Save']")

    


    def navigate_to_lobby_management(self):
        try:
            lobby_manage_btn = self.wait(self.LOBBY_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", lobby_manage_btn)
            self.click(self.LOBBY_BUTTON)
            self.click(self.LOBBY_CREATE)
        except (WebDriverException, TimeoutException) as e:
            self.logger.error(f"Failed to lobby management: {str(e)}")
            raise   
    
    def create_new_lobby(self, lobby_name, brand_name, vertical, category_order, status, aggregator, game_provider):
        
        try:
            self.click(self.BRAND_DROPDOWN)
            brand = self.wait((By.XPATH, f"//ul//li[text()='{brand_name}']"))    
            self.click(brand)

            self.enter_text(self.LOBBY_NAME, lobby_name)

            self.click(self.VERTICAL_DROPDOWN)
            vertical = self.wait((By.XPATH, f"//ul//li[text()='{vertical}']"))
            self.click(vertical)

            self.enter_text(self.CATEGORY_ORDER, category_order)

            self.click(self.STATUS_DROPDOWN)
            status = self.wait((By.XPATH, f"//ul//li[text()='{status}']"))
            self.click(status)

            self.click(self.AGGREGATOR_DROPDOW)
            aggregator = self.wait((By.XPATH, f"//ul//li[text()='{aggregator}']"))
            self.click(aggregator)

            self.enter_text(self.GAME_PROVIDER, game_provider)
            provider = self.wait((By.XPATH, f"//div[normalize-space()='{game_provider}']"))
            self.click(provider)

            self.click(self.GAME_SEARCH)

            self.wait(self.FIRST_FIVE_ITEMS, seconds=60)
            time.sleep(2)
            five_games = self.driver.find_elements(*self.FIRST_FIVE_ITEMS)[:5]
            self.logger.info(f"element founded five {five_games}")
            for item in five_games:
                self.logger.info(f"game founded {item}")
                self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", item)
                self.driver.execute_script("arguments[0].click();", item)

            self.click(self.ASSIGN_BUTTON)

            self.click(self.SAVE_BTN)
            time.sleep(2)
        except (WebDriverException, TimeoutException) as e:
                self.logger.error(f"Failed to create lobby management: {str(e)}")
                raise   
        
