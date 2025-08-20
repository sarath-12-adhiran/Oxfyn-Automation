import pytest
from pages.back_office.lobby_page import LobbyPage
from pages.back_office.backend_login_page import BackendLoginPage
from pages.player_pages.register_page import RegisterPage
from pages.player_pages.vertical_page import VerticalPage
from selenium.common.exceptions import WebDriverException, TimeoutException

class TestLobby:

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

    def test_create_lobby(self, driver, logger, brand_name, lobby_name):
        loggy_management = LobbyPage(driver, logger)
        try:
            loggy_management.navigate_to_lobby_management()
            res = loggy_management.create_new_lobby(
                lobby_name=lobby_name,
                brand_name=brand_name,
                vertical="Casino",
                category_order='1',
                status="Active",
                aggregator="RJ VK Casino",
                game_provider="Pragmatic Play"
            )

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")

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
    
    def test_verify_created_lobby(self, driver, logger, lobby_name):
        game_page = VerticalPage(driver, logger)
        try:
            game_page.navigate_to_verticals(verticals="Casino")
            res = game_page.find_lobby(
                lobby_name=lobby_name
            )

            if f"{lobby_name} Founded!" not in res:
                logger.error('Lobby Not Created or Founded')

        except (WebDriverException, TimeoutException) as e:
            logger.error(f"Test failed: {str(e)}")
            pytest.fail(f"Test failed due to: {str(e)}")