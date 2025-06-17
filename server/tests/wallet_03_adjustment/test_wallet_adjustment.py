import pytest
from pages.back_office.backend_login_page import BackendLoginPage
from pages.back_office.wallet_adjustment_page import WalletAdjustmentPage
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

def test_wallet_adjustment(driver, logger, user_credentials):
    wallet_adjustment = WalletAdjustmentPage(driver, logger)
    try:
        file_path = r"C:\Users\sujit\OneDrive\Documents\GitHub\Oxfyn-Automation\server\static\sample_file.xlsx"

        wallet_adjustment.click_wallet_adjustment_button()
        wallet_adjustment.add_wallet_adjustemnt(file_path,username=user_credentials['username'],amount=500)


        success_msg = wallet_adjustment.get_success_message()
        error_msg = wallet_adjustment.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg

        else:
            logger.info(f"Received success message: {error_msg}")
            assert error_msg
    except (WebDriverException, TimeoutException) as e:
        logger.info(f"test failed dude to: {str(e)}")

def test_check_player_wallet(driver, logger):
    player_wallet = WalletAdjustmentPage(driver, logger)
    try:
        
        player_wallet.redirect_to_player_page()
        res = player_wallet.validate_player_wallet()
        
        found = all(data['value'] == "500.00" for data in res)
        
        assert found 
    except (WebDriverException, TimeoutException) as e:
        logger.info(f"test failed dude to: {str(e)}")