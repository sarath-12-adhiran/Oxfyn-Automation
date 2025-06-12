import pytest
from pages.player_pages.login_page import LoginPage
from pages.player_pages.deposit_page import DepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots

def test_successful_login(driver, user_credentials, logger):
    login_page = LoginPage(driver, logger)
    try:
        logger.info("Starting test_successful_login")
        login_page.navigate_to_login()
        login_page.login(
            username=user_credentials['username'],
            password=user_credentials['password']

        )
        success_msg = login_page.get_success_message()
        error_msg = login_page.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg
        else:
            logger.info(f"Received error message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        take_screenshots(driver, "loggedin_failed")
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

