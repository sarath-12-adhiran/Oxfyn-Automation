import pytest
from pages.player_pages.deposit_page import DepositPage
from selenium.common.exceptions import WebDriverException, TimeoutException
from pages.back_office.backend_login_page import BackendLoginPage
from pages.player_pages.login_page import LoginPage
from pages.player_pages.deposit_page import DepositPage
from pages.back_office.backend_offline_deposit_page import BackendOfflineDepositPage
from pages.player_pages.register_page import RegisterPage


class TestDeposit:

    def test_register(self, driver, logger, user_credentials):
        register_page = RegisterPage(driver, logger)
        try:
            logger.info("Starting test_successful_registration")
            register_page.navigate_to_register()
            register_page.register(
                username=user_credentials['username'],
                password=user_credentials['password'],
                confirm_password=user_credentials['password'],
                # promo_code="PROMO2025",
                country_code="India",  # +91 India
                mobile_number=user_credentials['mobile'],
                age_confirm=True,
                terms_agree=True
            )
            success_msg = register_page.get_success_message()

            if not "Registered Successfully" in success_msg:
                error_msg = register_page.get_error_message()
                logger.error(f"unable to register some error occured: {error_msg}")

            assert "Registered Successfully" in success_msg

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

    def test_logout(self, driver, logger):
        register_page = RegisterPage(driver, logger)
        try:
            logger.info("Starting test_successful_logout")
            
            register_page.logout()

            success_msg = register_page.get_success_message()

            if not "Logout successful" in success_msg:
                error_msg = register_page.get_error_message()
                logger.error(f"unabel to logout some error occured: {error_msg}")

            assert "Logout successful" in success_msg

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

    def test_login(self, driver, user_credentials, logger):
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

    def test_deposit(self, driver, logger, coupon_code, utr_number, file_screenshot):
        deposit_page = DepositPage(driver, logger)
        try:
            logger.info("Starting test_successful_deposit")
            deposit_page.trigger_deposit_btn()
            deposit_page.deposit_amount(coupon_code,utr_number['UTR'],file_screenshot)
            logger.info(f"closing deposit feature")

            success_msg = deposit_page.get_success_message()
            
            if not "Deposit successful" in success_msg:
                error_msg = deposit_page.get_error_message()
                logger.error(f"unable to deposit some error occured: {error_msg}")

            assert "Deposit successful" in success_msg

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")
        
    
    def test_backoffice_login(self, driver, logger, admin_credentials):
        backend_login = BackendLoginPage(driver, logger)
        try:
            logger.info("Starting test_successful_login_backend")
            backend_login.navigate_to_backend_login()
            backend_login.backend_login(
                username=admin_credentials['username'],
                password=admin_credentials['password'],
                captcha=True
            )
            # success_msg = backend_login.get_success_message()

            # if not "Login successful" in success_msg:
            #     error_msg = backend_login.get_error_message()
            #     logger.error("unable to login some error occured: {error_msg}")

            # assert "Login successful" in success_msg

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

    def test_backoffice_offline_deposit(self, driver, logger, user_credentials, utr_number, brand_name):
        backend_offline_deposit = BackendOfflineDepositPage(driver, logger)
        try:
            logger.info("Starting test_successful_registration")
            backend_offline_deposit.trigger_offile_deposit_button()
            response = backend_offline_deposit.accept_income_deposit_request(
                username=user_credentials['username'],
                utr_number=utr_number['UTR'],
                brand_name=brand_name,
                payment_status="Pending",
                comment="Ok"
            )

            if not "Deposit transaction Updated Successfully" in response:
                error_msg = backend_offline_deposit.get_error_message()
                logger.error(f"unable to update offline deposit some error occured {error_msg}")

            assert "Deposit transaction Updated Successfully" in response

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")
    
    
    def test_backoffice_logout(self, driver, logger,):
        backend = BackendOfflineDepositPage(driver, logger)

        try:
            backend.logout()
            backend.navigate_player_dashboard()
        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

    def test_verifying_deposit(self, driver, logger,):
        player_page =  DepositPage(driver, logger)

        try:
            response = player_page.verify_deposit()

            if not "600.00" in response:
                logger.error("the deposit amount was not found or invalid")
        
            assert "600.00" in response

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")