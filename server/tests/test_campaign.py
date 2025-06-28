import pytest
from pages.back_office.campaign_page import CampaignPage
from pages.player_pages.deposit_page import DepositPage
from pages.player_pages.register_page import RegisterPage
from pages.back_office.backend_login_page import BackendLoginPage
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
from datetime import date, timedelta


class TestCampaign:

    def test_backoffice_login(self, driver, admin_credentials, logger):
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
            #     logger.error(f"test failed dude to unexpected response error message: {error_msg}")

            # assert "Login successful" in success_msg

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

    def test_create_campaign(self, driver, brand_name, logger, campaign_code):
        campaign = CampaignPage(driver, logger)
        try:
            campaign.navigate_to_campaign()
            campaign.create_campaign(
                brand_name=brand_name, 
                campaign_type = "Deposit",
                vertical_name = "Casino", 
                bonus_type = "Deposit", 
                max_redeem = "300", 
                deposit_type = "First Deposit", 
                campaign_name = campaign_code, 
                bonus = "Amount", 
                expiry_count = "5", 
                active_status = "Active", 
                min_deposit = "200", 
                campaign_code = campaign_code, 
                turnover = "1", 
                max_bonus = "100", 
                date_range = None,
                bonus_amount = "100",
                start_date = date.today(),
                end_date = date.today() + timedelta(days=1)
            )
            
        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

    def test_registration(self, driver, user_credentials, logger):
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

        
    def test_verify_campaign(self, driver, logger, campaign_code):
        campaign = DepositPage(driver, logger)
        try:
            campaign.trigger_deposit_btn()
            response = campaign.verify_campaign(
            campaign_name = campaign_code
            )
            assert "Campaign Founded" in response

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")
