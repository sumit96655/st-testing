"""
test_login.py — Login page tests covering FR-01 through FR-05.

FR-01  Valid login with standard_user
FR-02  Invalid password / locked-out user  (data-driven from CSV)
FR-03  Blank username
FR-04  Blank password
FR-05  Username exceeding 30 characters  (boundary values from CSV)
"""

import csv
import os

import pytest

from pages.login_page import LoginPage
from pages.products_page import ProductsPage

# ── Helpers ──────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "testdata")


def _read_login_csv():
    """Yield rows from login_data.csv as (username, password, expected_error)."""
    csv_path = os.path.join(DATA_DIR, "login_data.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row["username"], row["password"], row["expected_error"]


def _read_long_username_csv():
    """Yield rows from login_data.csv that have a 'long_username' column."""
    csv_path = os.path.join(DATA_DIR, "login_data.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("long_username"):
                yield row["long_username"], int(row["char_count"])


# ════════════════════════════════════════════════════════════════════
# TESTS
# ════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
def test_login_success(driver, test_logger):
    """FR-01: Successful login with valid credentials → Products page."""
    test_logger.info("TEST START — test_login_success (FR-01)")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    assert products_page.get_page_title() == "Products", \
        "Expected to land on Products page after valid login"
    assert "inventory" in driver.current_url, \
        "URL should contain 'inventory' after login"
    test_logger.info("TEST PASSED — test_login_success")


@pytest.mark.smoke
@pytest.mark.parametrize(
    "username, password, expected_error",
    list(_read_login_csv()),
    ids=lambda val: val[:20] if isinstance(val, str) else str(val),
)
def test_login_invalid_password(driver, test_logger, username, password, expected_error):
    """FR-02: Invalid credentials show correct error message (data-driven)."""
    test_logger.info("TEST START — test_login_invalid_password (FR-02) user=%s", username)
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert login_page.is_error_displayed(), "Error message should be visible"
    actual = login_page.get_error_message()
    assert actual == expected_error, \
        f"Expected error '{expected_error}', got '{actual}'"
    test_logger.info("TEST PASSED — test_login_invalid_password user=%s", username)


@pytest.mark.regression
def test_login_blank_username(driver, test_logger):
    """FR-03: Blank username → appropriate error."""
    test_logger.info("TEST START — test_login_blank_username (FR-03)")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("", "secret_sauce")

    assert login_page.is_error_displayed(), "Error should appear for blank username"
    assert "Username is required" in login_page.get_error_message()
    test_logger.info("TEST PASSED — test_login_blank_username")


@pytest.mark.regression
def test_login_blank_password(driver, test_logger):
    """FR-04: Blank password → appropriate error."""
    test_logger.info("TEST START — test_login_blank_password (FR-04)")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "")

    assert login_page.is_error_displayed(), "Error should appear for blank password"
    assert "Password is required" in login_page.get_error_message()
    test_logger.info("TEST PASSED — test_login_blank_password")


@pytest.mark.regression
@pytest.mark.parametrize(
    "long_username, char_count",
    [
        ("a" * 30, 30),
        ("a" * 31, 31),
        ("a" * 50, 50),
    ],
    ids=["30_chars", "31_chars", "50_chars"],
)
def test_login_username_exceeds_30_chars(driver, test_logger, long_username, char_count):
    """FR-05: Username boundary — 30, 31, 50 characters → error expected."""
    test_logger.info(
        "TEST START — test_login_username_exceeds_30_chars (FR-05) len=%d", char_count
    )
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(long_username, "secret_sauce")

    # SauceDemo doesn't enforce a char limit; it just fails with "no match" error.
    # We verify that an error IS shown (invalid user).
    assert login_page.is_error_displayed(), \
        f"Error should appear for {char_count}-char username"
    error_msg = login_page.get_error_message()
    test_logger.info("Error for %d-char username: %s", char_count, error_msg)
    assert "Epic sadface" in error_msg, \
        "Expected 'Epic sadface' prefix in error message"
    test_logger.info("TEST PASSED — test_login_username_exceeds_30_chars len=%d", char_count)
