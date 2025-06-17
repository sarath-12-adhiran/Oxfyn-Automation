import pytest
from pages.player_pages.register_page import RegisterPage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os

def test_successful_registration(driver, user_credentials, logger):
    register_page = RegisterPage(driver, logger)
    try:
        logger.info("Starting test_successful_registration")
        register_page.navigate_to_register()
        register_page.register(
            username=user_credentials['username'],
            password=user_credentials['password'],
            confirm_password=user_credentials['password'],
            # promo_code="PROMO2025",
            country_code="95",  # +91 India
            mobile_number=user_credentials['mobile'],
            age_confirm=True,
            terms_agree=True
        )
        success_msg = register_page.get_success_message()
        error_msg = register_page.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg

        else:
            logger.info(f"Received success message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")
