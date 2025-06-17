import pytest
from pages.player_pages.betting_page import BettingPage
from selenium.common.exceptions import WebDriverException, TimeoutException
from pages.player_pages.login_page import LoginPage


def test_successful_login(driver, user_credentials, logger):
    login_page = LoginPage(driver, logger)
    try:
        logger.info("Starting test_successful_login")
        login_page.navigate_to_login()
        login_page.login(
            username="tester",
            password="Tester@123"

        )
        success_msg = login_page.get_success_message()
        error_msg = login_page.get_error_message()

        if success_msg:
            logger.info(f"Received success message: {success_msg}")
            assert success_msg
        else:
            logger.info(f"Received error message: {error_msg}")
            assert error_msg

    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")



def test_successfull_betting(driver, logger, verticals, lobby, game_name):

    betting_page = BettingPage(driver,logger)
    try:
        # betting_page.navigate_to()
        betting_page.select_verticals(verticals)
        betting_page.select_lobby(lobby)
        betting_page.select_game(game_name)
        assert "success"
    except (WebDriverException, TimeoutException) as e:
        logger.error(f"Test failed: {str(e)}")
        pytest.fail(f"Test failed due to: {str(e)}")