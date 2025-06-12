import pytest
from pages.backend_pages.backend_offline_deposit_page import BackendOfflineDepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from utils.helpers import take_screenshots

def test_successful_backend_offline_deposit(driver, user_credentials, logger, utr_number, brand_name):
    backend_offline_deposit = BackendOfflineDepositPage(driver, logger)
    try:
        logger.info("Starting test_successful_registration")
        backend_offline_deposit.trigger_offile_deposit_button()
        backend_offline_deposit.accept_income_deposit_request(
            username=user_credentials['username'],
            utr_number=utr_number['UTR'],
            brand_name=brand_name,
            payment_status="Rejected",
            comment="Ok"
        )
        success_msg = backend_offline_deposit.get_success_message()
        error_msg = backend_offline_deposit.get_error_message()

        if success_msg:
            take_screenshots(driver, "successfully_acceped_deposit")
            logger.info(f"Received success message: {success_msg}")
            assert success_msg

        else:
            take_screenshots(driver, "failed_acceped_deposit")
            logger.error(f"Received error message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        take_screenshots(driver, "falied_to_accept_deposit")
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")
