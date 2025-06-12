import pytest
from pages.player_pages.login_page import LoginPage
from pages.player_pages.deposit_page import DepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import take_screenshots

def test_successful_login(driver, user_credentials, logger):
    register_page = LoginPage(driver, logger)
    try:
        logger.info("Starting test_successful_login")
        register_page.navigate_to_login()
        register_page.register(
            username=user_credentials['username'],
            password=user_credentials['password']

        )
        success_msg = register_page.get_success_message()
        error_msg = register_page.get_error_message()

        if success_msg:
            take_screenshots(driver, "successfully_loggedin")
            logger.info(f"Received success message: {success_msg}")
            assert success_msg
        else:
            take_screenshots(driver, "failed_login")
            logger.info(f"Received error message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        take_screenshots(driver, "loggedin_failed")
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

