import pytest
from pages.player_pages.login_page import LoginPage
from pages.player_pages.deposit_page import DepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException

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

        if not "Login successful" in success_msg:
            error_msg = login_page.get_error_message()
            logger.error(f"unable to login some error occured: {error_msg}")

        assert "Login successful" in success_msg

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

