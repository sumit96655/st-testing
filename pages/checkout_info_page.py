"""CheckoutInfoPage — Page Object for Checkout: Your Information step."""

import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutInfoPage(BasePage):
    """Encapsulates locators and actions for the Checkout Information form."""

    # ── Locators ─────────────────────────────────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container h3")

    # ── Actions ──────────────────────────────────────────────────────
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def enter_first_name(self, first_name: str):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str):
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str):
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """Convenience: fill all three fields."""
        logger.info("Filling checkout info: %s %s, %s", first_name, last_name, postal_code)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self):
        logger.info("Clicking Continue on checkout info")
        self.click(self.CONTINUE_BUTTON)
        return self

    def click_cancel(self):
        logger.info("Clicking Cancel on checkout info")
        self.click(self.CANCEL_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self.ERROR_MESSAGE)
