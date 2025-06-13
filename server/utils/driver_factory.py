from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config.config import IMPLICIT_WAIT

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--ignore-certificate-errors")  # Bypass SSL errors
    options.add_argument("--disable-web-security")      # Disable web security for testing
    options.add_argument("--allow-running-insecure-content")  # Allow insecure content
    # options.add_argument("--headless")  # Uncomment for headless mode if needed
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.maximize_window()
    return driver

def teardown_driver(driver):
    if driver:
        driver.quit()