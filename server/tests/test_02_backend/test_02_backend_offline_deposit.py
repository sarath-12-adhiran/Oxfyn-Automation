import pytest
from pages.back_office.backend_offline_deposit_page import BackendOfflineDepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from pages.player_pages.login_page import LoginPage

def test_successful_backend_offline_deposit(driver, user_credentials, logger, utr_number, brand_name):
    backend_offline_deposit = BackendOfflineDepositPage(driver, logger)
    try:
        logger.info("Starting test_successful_registration")
        backend_offline_deposit.trigger_offile_deposit_button()
        backend_offline_deposit.accept_income_deposit_request(
            username=user_credentials['username'],
            utr_number=utr_number['UTR'],
            brand_name=brand_name,
            payment_status="Pending",
            comment="Ok"
        )
        success_msg = backend_offline_deposit.get_success_message()
        error_msg = backend_offline_deposit.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg

        else:
            logger.error(f"Received error message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

def test_successfull_backend_logout(driver, logger):
    backend = BackendOfflineDepositPage(driver, logger)

    try:
        backend.logout()
        backend.navigate_player_dashboard()

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

