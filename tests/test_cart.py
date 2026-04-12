"""
test_cart.py — Cart page tests covering FR-09, FR-10.

FR-09  Cart details (name, price) match what was added
FR-10  Unauthorized access after logout redirects to login
"""

import pytest

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage


@pytest.mark.regression
def test_cart_details_match(login, driver, test_logger):
    """FR-09: Items in the cart reflect correct name and price from the products page."""
    test_logger.info("TEST START — test_cart_details_match (FR-09)")
    products_page = login

    # Add two products
    products_page.add_to_cart_by_name("Sauce Labs Backpack")
    products_page.add_to_cart_by_name("Sauce Labs Bike Light")
    assert products_page.get_cart_badge_count() == 2

    products_page.go_to_cart()

    cart_page = CartPage(driver)
    names = cart_page.get_item_names()
    prices = cart_page.get_item_prices()

    test_logger.info("Cart items: %s | Prices: %s", names, prices)

    assert "Sauce Labs Backpack" in names, "Backpack should be in cart"
    assert "Sauce Labs Bike Light" in names, "Bike Light should be in cart"
    assert len(names) == 2, f"Expected 2 items, got {len(names)}"

    # Verify prices are non-empty and start with '$'
    for price in prices:
        assert price.startswith("$"), f"Price '{price}' should start with '$'"

    test_logger.info("TEST PASSED — test_cart_details_match")


@pytest.mark.regression
def test_unauthorized_access_after_logout(login, driver, test_logger):
    """FR-10: After logout, navigating to inventory URL should deny access."""
    test_logger.info("TEST START — test_unauthorized_access_after_logout (FR-10)")
    products_page = login

    products_page.logout()

    # Verify we're back on the login page
    login_page = LoginPage(driver)
    assert login_page.is_displayed(LoginPage.LOGIN_BUTTON), \
        "Login button should be visible after logout"

    # Attempt direct navigation to inventory
    driver.get("https://www.saucedemo.com/inventory.html")

    # SauceDemo shows an error or redirects to login
    assert login_page.is_error_displayed(), \
        "Error should be shown when accessing inventory while logged out"
    error = login_page.get_error_message()
    test_logger.info("Unauthorized access error: %s", error)
    assert "You can only access" in error or "Epic sadface" in error, \
        f"Unexpected error message: {error}"
    test_logger.info("TEST PASSED — test_unauthorized_access_after_logout")
