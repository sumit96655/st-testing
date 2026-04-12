"""
BasePage — Common wrapper for all page objects.
Provides explicit-wait helpers so that no page class ever uses time.sleep().
"""

import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

BASE_URL = "https://www.saucedemo.com"


class BasePage:
    """Base class for every Page Object in the framework."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.base_url = BASE_URL

    # ── Wait helpers ─────────────────────────────────────────────────
    def wait_for_element(self, locator: tuple, timeout: int = 10) -> WebElement:
        """Wait until the element is visible and return it."""
        logger.debug("Waiting for element %s (timeout=%ss)", locator, timeout)
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error("Element %s not visible after %ss", locator, timeout)
            raise

    def wait_for_clickable(self, locator: tuple, timeout: int = 10) -> WebElement:
        """Wait until the element is clickable and return it."""
        logger.debug("Waiting for clickable %s (timeout=%ss)", locator, timeout)
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error("Element %s not clickable after %ss", locator, timeout)
            raise

    def wait_for_elements(self, locator: tuple, timeout: int = 10) -> list[WebElement]:
        """Wait until at least one element matching the locator is visible."""
        logger.debug("Waiting for elements %s (timeout=%ss)", locator, timeout)
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            logger.error("Elements %s not visible after %ss", locator, timeout)
            raise

    # ── Interaction helpers ──────────────────────────────────────────
    def click(self, locator: tuple) -> None:
        """Wait for an element to be clickable, then click it."""
        logger.info("Clicking element %s", locator)
        self.wait_for_clickable(locator).click()

    def type_text(self, locator: tuple, text: str) -> None:
        """Clear the field, then type text into it."""
        logger.info("Typing into %s", locator)
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        text = self.wait_for_element(locator).text
        logger.debug("Text of %s → '%s'", locator, text)
        return text

    def is_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """Return True if the element becomes visible within *timeout* seconds."""
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

    # ── Navigation helpers ───────────────────────────────────────────
    def get_current_url(self) -> str:
        return self.driver.current_url

    def navigate_to(self, url: str) -> None:
        logger.info("Navigating to %s", url)
        self.driver.get(url)
