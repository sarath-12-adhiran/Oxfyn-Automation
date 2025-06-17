from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import DEPOSIT_PAGE
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
import time
from utils.helpers import take_screenshots
from config.config import PLAYER_BASE_URL
import pyautogui


class BettingPage(BasePage):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
    
    CASINO_BUTTON = (By.XPATH, "//button[.//img[@alt='Casino']]")
    LOADER = (By.ID, "ScaleRootLoading")
    iframe = (By.XPATH, "//iframe")

    def navigate_to(self):
        self.driver.get(PLAYER_BASE_URL)

    def select_verticals(self, verticals):
        try:
            buttons = self.driver.find_elements(By.XPATH, "//button[.//img[@alt='Casino']]")

            for i, btn in enumerate(buttons):
                try:
                    if btn.is_displayed():
                        self.logger.info(f"Clicking Casino button #{i+1}")
                        btn.click()
                        break
                except Exception as e:
                    self.logger.warning(f"Casino button #{i+1} not clickable: {e}")

        except WebDriverException as e:
            self.logger.error(f"Error selecting verticals: {str(e)}")

    def select_lobby(self, lobby):
        
        try:
            self.click((By.XPATH, f"//button[.//p[text()='{lobby}']]"))
        except(WebDriverException) as e:
            self.logger.error(f"error selection lobby: {str(e)}")
    
    def select_game(self, game_name):
        try:
            self.wait((By.XPATH, f"//button[.//p[text()='{game_name}']]"), seconds=20)
            self.click((By.XPATH, f"//button[.//p[text()='{game_name}']]"))  


            #  # 2. Wait for the iframe to appear
            # iframe_locator = (By.XPATH, "//iframe[contains(@src, 'openGame')]")
            # iframe = self.find_element(iframe_locator,seconds=20)
            # if not iframe:
            #     self.logger.info("iframe not found")
            # # 3. Switch to the iframe
            # self.driver.switch_to.frame(iframe)


            time.sleep(50)
            self.logger.info("pyautogui started")

            # if not os.path.exists(r"C:\Users\sujit\OneDrive\Documents\GitHub\Oxfyn-Automation\server\pages\player_pages\round.png"):
            #     self.logger.error("image not found")
            # start_btn = pyautogui.locateOnScreen(r'C:\Users\sujit\OneDrive\Documents\GitHub\Oxfyn-Automation\server\pages\player_pages\round.png', confidence=0.6)
            # if start_btn:
            #     pyautogui.click(pyautogui.center(start_btn))
            #     self.logger.info("Button clicked!")
            # else:
            #     self.logger.error("Button not found on screen.")
            
            try:
                iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
                self.driver.switch_to.frame(iframe)
                self.logger.info("iframe deducted")
                self.wait((By.TAG_NAME, 'canvas'))
                canvas = self.driver.find_element(By.TAG_NAME, 'canvas')
                location = canvas.location
                size = canvas.size
                self.logger.info(f"{location['x']},{location['y'],size['width']},{size['height']}")
                # Calculate round button position (adjust 0.85 if button is higher/lower)
                target_x = location['x'] + (size['width'] // 2) + 50
                target_y = location['y'] + int(size['height'] * 0.98) + 90

                # Optional: move mouse before click
                time.sleep(1)
                pyautogui.moveTo(target_x, target_y, duration=0.5)
                pyautogui.click()
                time.sleep(20)
                
                self.driver.switch_to.default_content()
            except Exception as e:
                self.logger.error(f"some error occured {str(e)}")

        except(WebDriverException) as e:
            self.logger.error(f"error selecting game: {str(e)}")

        