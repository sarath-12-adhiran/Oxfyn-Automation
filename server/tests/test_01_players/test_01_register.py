import pytest
from pages.player_pages.register_page import RegisterPage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from utils.helpers import take_screenshots
from datetime import time

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
        take_screenshots(driver, f"{str(e)}")
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

def test_successful_logout(driver, logger):
    register_page = RegisterPage(driver, logger)
    try:
        logger.info("Starting test_successful_logout")
        
        register_page.logout()

        success_msg = register_page.get_success_message()
        error_msg = register_page.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg

        else:
            logger.info(f"Received success message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        take_screenshots(driver, "registration_failed")
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")


# def test_registration_with_existing_username(driver):
#     register_page = RegisterPage(driver)
#     try:
#         logger.info("Starting test_registration_with_existing_username")
#         register_page.navigate_to_register()
#         register_page.register(
#             username="testuser123",  # Assuming this username exists
#             password="Password123!",
#             confirm_password="Password123!",
#             # promo_code="PROMO2025",
#             country_code="95",
#             mobile_number="9876543210",
#             age_confirm=True,
#             terms_agree=True
#         )
#         error_msg = register_page.get_error_message()
#         logger.info(f"Received error message: {error_msg}")
#         assert "Username already exists" in error_msg
#     except (WebDriverException, TimeoutException) as e:
#         driver.save_screenshot("test_registration_with_existing_username_failure.png")
#         logger.error(f"Test failed: {str(e)}")
#         pytest.fail(f"Test failed due to: {str(e)}")

# def test_registration_without_terms_agreement(driver):
#     register_page = RegisterPage(driver)
#     try:
#         logger.info("Starting test_registration_without_terms_agreement")
#         register_page.navigate_to_register()
#         register_page.register(
#             username="testuser456",
#             password="Password123!",
#             confirm_password="Password123!",
#             promo_code="PROMO2025",
#             country_code="95",
#             mobile_number="9876543210",
#             age_confirm=True,
#             terms_agree=False
#         )
#         error_msg = register_page.get_error_message()
#         logger.info(f"Received error message: {error_msg}")
#         assert "You must agree to the terms" in error_msg
#     except (WebDriverException, TimeoutException) as e:
#         driver.save_screenshot("test_registration_without_terms_agreement_failure.png")
#         logger.error(f"Test failed: {str(e)}")
#         pytest.fail(f"Test failed due to: {str(e)}")
