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

        if not "Login successful" in success_msg:
            error_msg = backend_login.get_error_message()
            logger.error(f"test failed dude to unexpected response error message: {error_msg}")

        assert "Login successful" in success_msg

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

def test_add_bulk_wallet_adjusment(driver, logger, user_credentials):
    wallet_adjustment = WalletAdjustmentPage(driver, logger)
    try:
        file_path = r"C:\Users\sujit\OneDrive\Documents\GitHub\Oxfyn-Automation\server\static\sample_file.xlsx"

        wallet_adjustment.click_wallet_adjustment_button()
        wallet_adjustment.add_wallet_adjustemnt(file_path,username=user_credentials['username'],amount=500)


        success_msg = wallet_adjustment.get_success_message()
        
        if not "File Upload Successfully" in success_msg:
            error_msg = wallet_adjustment.get_error_message()
            logger.error(f"test failed dude to unexpected response error message: {error_msg}")
            
        assert "File Upload Successfully" in success_msg
        
    except (WebDriverException, TimeoutException) as e:
        logger.info(f"test failed dude to: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

def test_verifying_bulk_added_amount(driver, logger):
    player_wallet = WalletAdjustmentPage(driver, logger)
    try:
        
        player_wallet.redirect_to_player_page()
        res = player_wallet.validate_player_wallet()
        
        deposit_amount = all(data['value'] == "500.00" for data in res)
        
        if not deposit_amount:
            logger.error(f"Deposit amount not found or invalid")

        assert deposit_amount 
    except (WebDriverException, TimeoutException) as e:
        logger.info(f"test failed dude to: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

def test_add_single_wallet_adjustment(driver, logger, user_credentials):
    wallet_adjustment = WalletAdjustmentPage(driver, logger)
    backend_login = BackendLoginPage(driver, logger)

    try:
        backend_login.navigate_to_backend_login()
        wallet_adjustment.click_wallet_adjustment_button()
        wallet_adjustment.wallet_adjustment_for_win(
            brand_name = "BET DUNIYA",
            player_name = user_credentials['username'], 
            amount = 500,
            adjustment_type = "Add",
            wallet_type = "Casino", 
            pocket_type = "Win"
        )
        assert wallet_adjustment
    except (WebDriverException, TimeoutException) as e:
        logger.info(f"test failed dude to: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")

def test_verifying_single_wallet_amount(driver, logger):
    player_wallet = WalletAdjustmentPage(driver, logger)
    try:
        
        player_wallet.redirect_to_player_page()
        res = player_wallet.validate_player_wallet()
        
        deposit_amount = any(data['label'] == "Casino Money" and data['value'] == "1000.00" for data in res)
        
        if not deposit_amount:
            logger.error(f"Deposit amount for win not found or invalid")

        assert deposit_amount 

    except (WebDriverException, TimeoutException) as e:
        logger.info(f"test failed dude to: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")
