from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, seconds=30):
        return WebDriverWait(self.driver, seconds).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator, seconds=30):
        element = WebDriverWait(self.driver, seconds).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def select_dropdown_by_value(self, locator, value):
        element = self.find_element(locator)
        Select(element).select_by_value(value)
  