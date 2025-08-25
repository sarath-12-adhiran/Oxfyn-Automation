from utils.driver_factory import setup_driver, teardown_driver
import pytest
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from logging import Formatter
from utils.helpers import generate_username, generate_mobile_number, generate_utr, generate_campaign_code, generate_lobby_name, generate_account_number
from selenium.common.exceptions import WebDriverException

@pytest.fixture(scope="session")
def driver():
    try:
        driver = setup_driver()
        yield driver
    except WebDriverException as e:
        logging.error("WebDriver error during test setup or execution", exc_info=True)
        raise e 
    finally:
        teardown_driver(driver)

@pytest.fixture
def logger():
    folder_path="logs"

    #create log folder
    if not os.path.exists(folder_path):
        os.mkdir(folder_path.split('/')[0])

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    current_date = datetime.now().strftime("%d-%m-%Y")
    file_path = os.path.join(folder_path, f"{current_date}.log")

    # Create a logger object
    _logger = logging.getLogger('TestLog')  # Use a specific name instead of file path
    _logger.setLevel(logging.DEBUG)

    # Set up file handler with rotating files
    file_handler = RotatingFileHandler(file_path, maxBytes=10 ** 6, backupCount=5)  # 1MB per log file
    file_handler.setLevel(logging.DEBUG)

    # Set up the formatter to include the date and time
    formatter = Formatter('| TestLog | - %(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    if not _logger.handlers:
        _logger.addHandler(file_handler)
    # Set up console handler (StreamHandler)
    console_handler = logging.StreamHandler()  # Create a console handler
    console_handler.setLevel(logging.DEBUG)  # Set its level
    console_handler.setFormatter(formatter)  # Use the same formatter as the file handler
    # Add the console handler to the logger
    _logger.addHandler(console_handler)

    return _logger

@pytest.fixture(scope="session")
def user_credentials():
    username = generate_username()
    mobile = generate_mobile_number()
    password = "Password123!"  
    return {"username": username, "mobile": mobile, "password": password}


@pytest.fixture(scope="session")
def utr_number():
    return {"UTR": generate_utr()}

@pytest.fixture(scope="session")
def coupon_code():
    code = "FDPBNEXPIRY"
    return code


@pytest.fixture(scope="session")
def admin_credentials():
    username = "Superadmin"
    password = "Password@123"  
    return {"username": username,"password": password}


@pytest.fixture(scope="session")
def brand_name():
    names = "BET DUNIYA"
    return names

@pytest.fixture(scope="session")
def verticals():
    name = "casino"
    return name

@pytest.fixture(scope="session")
def lobby():
    name = "Casino"
    return name

@pytest.fixture(scope="session")
def game_name():
    name = "Wolf Gold"
    return name

@pytest.fixture(scope="session")
def campaign_code():
    code = generate_campaign_code()
    return code

@pytest.fixture(scope="session")
def lobby_name():
    name = generate_lobby_name()
    return name

@pytest.fixture(scope="session")
def account_number():
    return generate_account_number()