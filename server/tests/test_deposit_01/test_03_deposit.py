import pytest
from pages.player_pages.deposit_page import DepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException

def test_deposit(driver, logger, coupon_code, utr_number, file_screenshot):
    deposit_page = DepositPage(driver, logger)
    try:
        logger.info("Starting test_successful_deposit")
        deposit_page.trigger_deposit_btn()
        deposit_page.deposit_amount(coupon_code,utr_number['UTR'],file_screenshot)
        logger.info(f"closing deposit feature")
        success_msg = deposit_page.get_success_message()
        error_msg = deposit_page.get_error_message()
        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg
        else:
            logger.info(f"Received error message: {success_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")