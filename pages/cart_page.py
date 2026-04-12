"""CartPage — Page Object for https://www.saucedemo.com/cart.html"""

import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Encapsulates locators and actions for the Shopping Cart page."""

    # ── Locators ─────────────────────────────────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    # ── Actions ──────────────────────────────────────────────────────
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_cart_items(self):
        """Return all cart item WebElements."""
        return self.wait_for_elements(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        """Return a list of product names in the cart."""
        elements = self.wait_for_elements(self.ITEM_NAME)
        return [el.text for el in elements]

    def get_item_prices(self) -> list[str]:
        """Return a list of product prices in the cart."""
        elements = self.wait_for_elements(self.ITEM_PRICE)
        return [el.text for el in elements]

    def click_checkout(self) -> None:
        """Click the Checkout button."""
        logger.info("Clicking Checkout")
        self.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self) -> None:
        """Click Continue Shopping to go back to products."""
        logger.info("Clicking Continue Shopping")
        self.click(self.CONTINUE_SHOPPING_BUTTON)
