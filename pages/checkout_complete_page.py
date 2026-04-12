"""CheckoutCompletePage — Page Object for Checkout: Complete! step."""

import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutCompletePage(BasePage):
    """Encapsulates locators and actions for the order-complete confirmation."""

    # ── Locators ─────────────────────────────────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    SUCCESS_HEADER = (By.CSS_SELECTOR, ".complete-header")
    BACK_HOME_BUTTON = (By.CSS_SELECTOR, "button[data-test='back-to-products']")

    # ── Actions ──────────────────────────────────────────────────────
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_success_message(self) -> str:
        """Return the confirmation header text (e.g. 'Thank you for your order!')."""
        return self.get_text(self.SUCCESS_HEADER)

    def click_back_home(self) -> None:
        logger.info("Clicking Back Home")
        self.click(self.BACK_HOME_BUTTON)
