"""
conftest.py — Shared PyTest fixtures and hooks for the SauceDemo test suite.

Provides:
  • driver        – function-scoped Chrome WebDriver (headless via --headless flag)
  • login         – logs in with standard_user and returns ProductsPage
  • test_logger   – session-scoped structured logger → reports/logs/test_run.log
  • screenshot-on-failure hook (pytest_runtest_makereport)
  • --headless / --browser_name CLI options
"""

import os
import logging
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.products_page import ProductsPage


# ════════════════════════════════════════════════════════════════════
# CLI OPTIONS
# ════════════════════════════════════════════════════════════════════
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Browser to use (currently only 'chrome' supported)",
    )


# ════════════════════════════════════════════════════════════════════
# FIXTURES
# ════════════════════════════════════════════════════════════════════

# Module-level logger (not a fixture — avoids teardown ordering issues)
_log_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "logs")
os.makedirs(_log_dir, exist_ok=True)
_log_file = os.path.join(_log_dir, "test_run.log")

_logger = logging.getLogger("saucedemo_tests")
_logger.setLevel(logging.DEBUG)

# Avoid adding duplicate handlers on re-import
if not _logger.handlers:
    _fh = logging.FileHandler(_log_file, mode="w", encoding="utf-8")
    _fh.setLevel(logging.DEBUG)
    _fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    _fh.setFormatter(_fmt)
    _logger.addHandler(_fh)

    _ch = logging.StreamHandler()
    _ch.setLevel(logging.INFO)
    _ch.setFormatter(_fmt)
    _logger.addHandler(_ch)


@pytest.fixture(scope="session")
def test_logger():
    """Session-scoped logger that writes to reports/logs/test_run.log."""
    _logger.info("Test session started")
    yield _logger
    _logger.info("Test session ended")


@pytest.fixture(scope="function")
def driver(request, test_logger):
    """Create a fresh Chrome WebDriver for each test function."""
    headless = request.config.getoption("--headless")
    browser_name = request.config.getoption("--browser_name")

    test_logger.info(
        "Setting up %s driver (headless=%s) for %s",
        browser_name,
        headless,
        request.node.name,
    )

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Suppress Chrome Password Manager / data-breach popups
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-notifications")

        _driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    _driver.implicitly_wait(0)  # We use explicit waits only
    _driver.maximize_window()

    yield _driver

    test_logger.info("Tearing down driver for %s", request.node.name)
    _driver.quit()


@pytest.fixture(scope="function")
def login(driver, test_logger):
    """Log in with standard_user and return a ProductsPage instance."""
    test_logger.info("Logging in with standard_user")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    products_page = ProductsPage(driver)
    # Wait for products page to fully load
    products_page.get_page_title()
    test_logger.info("Login successful — on Products page")
    return products_page


# ════════════════════════════════════════════════════════════════════
# HOOKS
# ════════════════════════════════════════════════════════════════════
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot on test failure and attach it to the HTML report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        _driver = item.funcargs.get("driver")
        if _driver is not None:
            screenshot_dir = os.path.join(
                os.path.dirname(__file__), "..", "reports", "screenshots"
            )
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            filepath = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")

            _driver.save_screenshot(filepath)
            _logger.error("Screenshot saved: %s", filepath)

            # Attach to pytest-html report if available
            try:
                from pytest_html import extras
                extra = getattr(report, "extras", [])
                extra.append(extras.image(filepath))
                report.extras = extra
            except (ImportError, Exception):
                pass  # pytest-html not installed or not generating report
