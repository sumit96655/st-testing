"""
test_products.py — Products page tests covering FR-06, FR-07, FR-08.

FR-06  Products visible after login
FR-07  Add product to cart
FR-08  Remove product from cart
"""

import pytest

from pages.products_page import ProductsPage


@pytest.mark.regression
def test_products_visible_after_login(login, driver, test_logger):
    """FR-06: After login, the Products page shows at least 1 product."""
    test_logger.info("TEST START — test_products_visible_after_login (FR-06)")
    products_page = login  # already logged in via fixture

    title = products_page.get_page_title()
    assert title == "Products", f"Expected 'Products', got '{title}'"

    count = products_page.get_product_count()
    test_logger.info("Product count: %d", count)
    assert count > 0, "At least one product should be visible"

    names = products_page.get_product_names()
    test_logger.info("Products: %s", names)
    assert len(names) == count, "Name count should match product count"
    test_logger.info("TEST PASSED — test_products_visible_after_login")


@pytest.mark.smoke
def test_add_to_cart(login, driver, test_logger):
    """FR-07: Adding a product increments the cart badge."""
    test_logger.info("TEST START — test_add_to_cart (FR-07)")
    products_page = login

    product_name = "Sauce Labs Backpack"
    products_page.add_to_cart_by_name(product_name)

    badge = products_page.get_cart_badge_count()
    test_logger.info("Cart badge after add: %d", badge)
    assert badge == 1, f"Cart badge should be 1 after adding one item, got {badge}"
    test_logger.info("TEST PASSED — test_add_to_cart")


@pytest.mark.regression
def test_remove_from_cart(login, driver, test_logger):
    """FR-08: Removing a product decrements the cart badge."""
    test_logger.info("TEST START — test_remove_from_cart (FR-08)")
    products_page = login

    product_name = "Sauce Labs Backpack"
    products_page.add_to_cart_by_name(product_name)
    assert products_page.get_cart_badge_count() == 1, "Badge should be 1 after add"

    products_page.remove_from_cart_by_name(product_name)
    badge = products_page.get_cart_badge_count()
    test_logger.info("Cart badge after remove: %d", badge)
    assert badge == 0, f"Cart badge should be 0 after removing item, got {badge}"
    test_logger.info("TEST PASSED — test_remove_from_cart")
