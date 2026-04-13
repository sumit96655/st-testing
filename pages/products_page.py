"""ProductsPage — Page Object for https://www.saucedemo.com/inventory.html"""

import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """Encapsulates locators and actions for the Products / Inventory page."""

    # ── Locators ─────────────────────────────────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_ITEM = (By.CSS_SELECTOR, ".inventory_item")
    INVENTORY_ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    INVENTORY_ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    # deliberately adding error - commenting the next line
    # BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # ── Actions ──────────────────────────────────────────────────────
    def get_page_title(self) -> str:
        """Return the page heading text (e.g. 'Products')."""
        return self.get_text(self.PAGE_TITLE)

    def get_all_products(self):
        """Return a list of all inventory item WebElements."""
        return self.wait_for_elements(self.INVENTORY_ITEM)

    def get_product_count(self) -> int:
        """Return the number of products displayed."""
        return len(self.get_all_products())

    def get_product_names(self) -> list[str]:
        """Return a list of all visible product names."""
        elements = self.wait_for_elements(self.INVENTORY_ITEM_NAME)
        return [el.text for el in elements]

    def get_product_prices(self) -> list[str]:
        """Return a list of all visible product prices (e.g. '$29.99')."""
        elements = self.wait_for_elements(self.INVENTORY_ITEM_PRICE)
        return [el.text for el in elements]

    def add_to_cart_by_name(self, product_name: str) -> None:
        """Click the 'Add to cart' button for a product identified by its name."""
        # SauceDemo button IDs follow the pattern: add-to-cart-<lowercase-name-with-hyphens>
        button_id = "add-to-cart-" + product_name.lower().replace(" ", "-")
        locator = (By.ID, button_id)
        logger.info("Adding '%s' to cart (button id: %s)", product_name, button_id)
        self.click(locator)

    def remove_from_cart_by_name(self, product_name: str) -> None:
        """Click the 'Remove' button for a product identified by its name."""
        button_id = "remove-" + product_name.lower().replace(" ", "-")
        locator = (By.ID, button_id)
        logger.info("Removing '%s' from cart (button id: %s)", product_name, button_id)
        self.click(locator)

    def get_cart_badge_count(self) -> int:
        """Return the number displayed on the cart badge, or 0 if no badge."""
        if self.is_displayed(self.CART_BADGE, timeout=2):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        """Click the shopping cart icon."""
        self.click(self.CART_LINK)

    def logout(self) -> None:
        """Open the burger menu and click Logout."""
        logger.info("Logging out via burger menu")
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
