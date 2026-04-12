"""LoginPage — Page Object for https://www.saucedemo.com/"""

import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Encapsulates locators and actions for the SauceDemo login page."""

    # ── Locators ─────────────────────────────────────────────────────
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container h3")

    # ── Actions ──────────────────────────────────────────────────────
    def open(self):
        """Navigate to the login page."""
        self.navigate_to(self.base_url)
        logger.info("Opened login page")
        return self

    def enter_username(self, username: str):
        """Type a username into the username field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """Type a password into the password field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click the Login button."""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """Convenience: fill both fields and click Login."""
        logger.info("Logging in as '%s'", username)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self) -> str:
        """Return the text of the error banner."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True if an error message is visible."""
        return self.is_displayed(self.ERROR_MESSAGE)
