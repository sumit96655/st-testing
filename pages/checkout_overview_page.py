"""CheckoutOverviewPage — Page Object for Checkout: Overview step."""

import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutOverviewPage(BasePage):
    """Encapsulates locators and actions for the Checkout Overview page."""

    # ── Locators ─────────────────────────────────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    SUBTOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    # ── Actions ──────────────────────────────────────────────────────
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_subtotal(self) -> str:
        """Return the subtotal text, e.g. 'Item total: $29.99'."""
        return self.get_text(self.SUBTOTAL_LABEL)

    def get_tax(self) -> str:
        """Return the tax text, e.g. 'Tax: $2.40'."""
        return self.get_text(self.TAX_LABEL)

    def get_total(self) -> str:
        """Return the total text, e.g. 'Total: $32.39'."""
        return self.get_text(self.TOTAL_LABEL)

    def click_finish(self) -> None:
        logger.info("Clicking Finish on checkout overview")
        self.click(self.FINISH_BUTTON)

    def click_cancel(self) -> None:
        logger.info("Clicking Cancel on checkout overview")
        self.click(self.CANCEL_BUTTON)
