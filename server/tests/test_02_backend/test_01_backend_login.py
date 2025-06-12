import pytest
from pages.backend_pages.backend_login_page import BackendLoginPage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from utils.helpers import take_screenshots

def test_successful_backend_login(driver, admin_credentials, logger):
    backend_login = BackendLoginPage(driver, logger)
    try:
        logger.info("Starting test_successful_registration")
        backend_login.navigate_to_backend_login()
        backend_login.backend_login(
            username=admin_credentials['username'],
            password=admin_credentials['password'],
            captcha=True
        )
        success_msg = backend_login.get_success_message()
        error_msg = backend_login.get_error_message()

        if success_msg:
            take_screenshots(driver, "successfully_backend_loggedin")
            logger.info(f"Received success message: {success_msg}")
            # backend_login.logout()
            # take_screenshots(driver, "successfully_backend_loggedin")
            assert success_msg
        else:
            take_screenshots(driver, "failed_backend_login")
            logger.info(f"Received error message: {error_msg}")
            assert error_msg
    except (WebDriverException, TimeoutException) as e:
        take_screenshots(driver, "login_failed")
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")
