import pytest
from pages.back_office.backend_login_page import BackendLoginPage
from selenium.common.exceptions import WebDriverException, TimeoutException

def test_successful_backend_login(driver, admin_credentials, logger):
    backend_login = BackendLoginPage(driver, logger)
    try:
        logger.info("Starting test_successful_login_backend")
        backend_login.navigate_to_backend_login()
        backend_login.backend_login(
            username=admin_credentials['username'],
            password=admin_credentials['password'],
            captcha=True
        )
        success_msg = backend_login.get_success_message()
        error_msg = backend_login.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg
        else:
            logger.info(f"Received error message: {error_msg}")
            assert error_msg
    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")
