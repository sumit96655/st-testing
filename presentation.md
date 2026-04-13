# SauceDemo — Test Automation & Performance Testing Framework

## 📌 Project Overview

This repository contains a **complete test automation and performance testing framework** for the [SauceDemo](https://www.saucedemo.com) e-commerce web application. It combines:

1. **Functional Automation Testing** — Selenium 4 + PyTest using the Page Object Model (POM) design pattern
2. **Performance Testing** — Apache JMeter 5.6.3 load testing with measurable NFR thresholds

**Target Application:** https://www.saucedemo.com — A demo React SPA (Single-Page Application) with login, product catalog, shopping cart, and checkout functionality.

---

## 📁 Repository Structure

```
st-testing/
│
├── pages/                          # Page Object Model (POM) classes
│   ├── __init__.py
│   ├── base_page.py                # Base class — wait helpers, click, type, navigate
│   ├── login_page.py               # Login page locators and actions
│   ├── products_page.py            # Products/Inventory page locators and actions
│   ├── cart_page.py                # Shopping cart page locators and actions
│   ├── checkout_info_page.py       # Checkout: Your Information form
│   ├── checkout_overview_page.py   # Checkout: Overview (subtotal, tax, total)
│   └── checkout_complete_page.py   # Checkout: Complete confirmation
│
├── tests/                          # PyTest test cases
│   ├── __init__.py
│   ├── conftest.py                 # Fixtures (driver, login, logger) + hooks
│   ├── test_login.py               # FR-01 to FR-05: Login tests
│   ├── test_products.py            # FR-06 to FR-08: Products page tests
│   ├── test_cart.py                # FR-09 to FR-10: Cart + logout tests
│   └── test_checkout.py            # FR-11 to FR-16: Checkout flow tests
│
├── testdata/                       # External test data (data-driven testing)
│   ├── login_data.csv              # CSV: invalid login credentials
│   └── checkout_data.json          # JSON: postal code boundary values
│
├── performance/                    # JMeter performance testing
│   ├── jmx/
│   │   └── saucedemo_weekend_lab.jmx  # JMeter test plan
│   ├── results/
│   │   ├── results.jtl             # Raw JMeter results
│   │   └── aggregate.csv           # Aggregated statistics per sampler
│   ├── html_report/                # JMeter HTML dashboard (auto-generated)
│   │   └── index.html
│   ├── generate_aggregate.ps1      # Script to generate aggregate.csv from JTL
│   └── Findings.md                 # NFR compliance report (Pass/Fail)
│
├── reports/                        # Selenium test outputs
│   └── logs/
│       └── test_run.log            # Structured test execution log
│
├── requirements.txt                # Python dependencies
├── pytest.ini                      # PyTest configuration
├── .gitignore                      # Git ignore rules
└── README.md                       # Project README
```

---

## 🛠️ Setup & Installation

### Prerequisites

| Tool            | Version     | Purpose                           |
|-----------------|-------------|-----------------------------------|
| Python          | ≥ 3.10      | Automation framework runtime      |
| Google Chrome   | Latest      | Browser for Selenium tests        |
| Apache JMeter   | 5.6.3       | Performance / load testing        |
| Git             | Any         | Version control                   |

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd st-testing
```

### Step 2: Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies (`requirements.txt`):**

| Package            | Version  | Purpose                                |
|--------------------|----------|----------------------------------------|
| `selenium`         | ≥ 4.15.0 | Browser automation (Selenium 4)        |
| `pytest`           | ≥ 7.4.0  | Test runner and framework              |
| `pytest-html`      | ≥ 4.1.0  | HTML test report generation            |
| `webdriver-manager`| ≥ 4.0.0  | Automatic ChromeDriver management      |

### Step 4: Install JMeter (for Performance Testing)

1. Download Apache JMeter 5.6.3 from https://jmeter.apache.org/download_jmeter.cgi
2. Extract to a known location (e.g., `D:\jmeter\apache-jmeter-5.6.3`)
3. Ensure Java 8+ is installed (`java -version`)

---

## 🏗️ Architecture & Design Patterns

### Page Object Model (POM)

The framework follows the **Page Object Model** design pattern, which separates test logic from page interaction logic.

```
┌──────────────────────────────────────────────────┐
│                   Test Layer                      │
│  test_login.py | test_products.py | test_cart.py  │
│              test_checkout.py                     │
└──────────────┬───────────────────────────────────┘
               │ uses
┌──────────────▼───────────────────────────────────┐
│              Page Object Layer                    │
│  LoginPage | ProductsPage | CartPage              │
│  CheckoutInfoPage | CheckoutOverviewPage          │
│  CheckoutCompletePage                             │
└──────────────┬───────────────────────────────────┘
               │ inherits
┌──────────────▼───────────────────────────────────┐
│              Base Page                            │
│  wait_for_element() | wait_for_clickable()        │
│  click() | type_text() | get_text()               │
│  is_displayed() | navigate_to()                   │
└──────────────┬───────────────────────────────────┘
               │ drives
┌──────────────▼───────────────────────────────────┐
│         Selenium WebDriver (Chrome)               │
└──────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Explicit waits only** — `implicitly_wait(0)` is set; all waits use `WebDriverWait` with `expected_conditions`
2. **No `time.sleep()`** — Every wait is condition-based for reliability
3. **Function-scoped driver** — Each test gets a fresh browser instance for isolation
4. **Data-driven testing** — CSV for login data, JSON for checkout boundary values
5. **Automatic screenshot on failure** — Hook in `conftest.py` captures and attaches screenshots
6. **Structured logging** — All test actions logged to `reports/logs/test_run.log`

---

## 📄 Page Objects — Detailed Breakdown

### `pages/base_page.py` — Base Page Class

The foundation for all page objects. Provides reusable helper methods:

| Method               | Description                                               |
|----------------------|-----------------------------------------------------------|
| `wait_for_element()` | Waits until element is visible (explicit wait, 10s default)|
| `wait_for_clickable()` | Waits until element is clickable                        |
| `wait_for_elements()` | Waits until all matching elements are visible            |
| `click()`            | Waits for clickable, then clicks                          |
| `type_text()`        | Clears field, then types text                             |
| `get_text()`         | Returns visible text of an element                        |
| `is_displayed()`     | Returns `True`/`False` if element appears within timeout  |
| `navigate_to()`      | Navigates browser to a URL                                |

**Base URL:** `https://www.saucedemo.com`

---

### `pages/login_page.py` — Login Page

| Locator          | Strategy | Value            |
|------------------|----------|------------------|
| Username Input   | By.ID    | `user-name`      |
| Password Input   | By.ID    | `password`       |
| Login Button     | By.ID    | `login-button`   |
| Error Message    | By.CSS   | `.error-message-container h3` |

**Actions:** `open()`, `enter_username()`, `enter_password()`, `click_login()`, `login()` (convenience), `get_error_message()`, `is_error_displayed()`

---

### `pages/products_page.py` — Products Page

| Locator           | Strategy | Value                       |
|-------------------|----------|-----------------------------|
| Page Title        | By.CSS   | `.title`                    |
| Inventory Items   | By.CSS   | `.inventory_item`           |
| Item Names        | By.CSS   | `.inventory_item_name`      |
| Item Prices       | By.CSS   | `.inventory_item_price`     |
| Cart Badge        | By.CSS   | `.shopping_cart_badge`      |
| Cart Link         | By.CSS   | `.shopping_cart_link`       |
| Burger Menu       | By.ID    | `react-burger-menu-btn`     |
| Logout Link       | By.ID    | `logout_sidebar_link`       |

**Actions:** `get_product_count()`, `get_product_names()`, `get_product_prices()`, `add_to_cart_by_name()`, `remove_from_cart_by_name()`, `get_cart_badge_count()`, `go_to_cart()`, `logout()`

---

### `pages/cart_page.py` — Cart Page

| Locator                | Strategy | Value              |
|------------------------|----------|--------------------|
| Cart Items             | By.CSS   | `.cart_item`       |
| Item Names             | By.CSS   | `.inventory_item_name` |
| Item Prices            | By.CSS   | `.inventory_item_price` |
| Checkout Button        | By.ID    | `checkout`         |
| Continue Shopping Btn  | By.ID    | `continue-shopping`|

**Actions:** `get_cart_items()`, `get_item_names()`, `get_item_prices()`, `click_checkout()`, `click_continue_shopping()`

---

### `pages/checkout_info_page.py` — Checkout Information

| Locator           | Strategy | Value          |
|-------------------|----------|----------------|
| First Name Input  | By.ID    | `first-name`   |
| Last Name Input   | By.ID    | `last-name`    |
| Postal Code Input | By.ID    | `postal-code`  |
| Continue Button   | By.ID    | `continue`     |
| Cancel Button     | By.ID    | `cancel`       |
| Error Message     | By.CSS   | `.error-message-container h3` |

**Actions:** `fill_checkout_info()`, `enter_first_name()`, `enter_last_name()`, `enter_postal_code()`, `click_continue()`, `click_cancel()`, `get_error_message()`

---

### `pages/checkout_overview_page.py` — Checkout Overview

| Locator         | Strategy | Value                    |
|-----------------|----------|--------------------------|
| Subtotal        | By.CSS   | `.summary_subtotal_label`|
| Tax             | By.CSS   | `.summary_tax_label`     |
| Total           | By.CSS   | `.summary_total_label`   |
| Finish Button   | By.ID    | `finish`                 |
| Cancel Button   | By.ID    | `cancel`                 |

**Actions:** `get_subtotal()`, `get_tax()`, `get_total()`, `click_finish()`, `click_cancel()`

---

### `pages/checkout_complete_page.py` — Order Confirmation

| Locator          | Strategy | Value                                  |
|------------------|----------|----------------------------------------|
| Success Header   | By.CSS   | `.complete-header`                     |
| Back Home Button | By.CSS   | `button[data-test='back-to-products']` |

**Actions:** `get_success_message()`, `click_back_home()`

---

## 🧪 Test Cases — Functional Requirements

### Test Markers

Tests are organized with PyTest markers defined in `pytest.ini`:

| Marker        | Purpose                                |
|---------------|----------------------------------------|
| `@smoke`      | Critical path tests — mandatory FR coverage |
| `@regression` | Extended coverage — edge cases, boundary values |

---

### `tests/test_login.py` — Login Tests (FR-01 to FR-05)

| Test Function                         | FR ID  | Marker     | Description                                             | Data Source        |
|---------------------------------------|--------|------------|---------------------------------------------------------|--------------------|
| `test_login_success`                  | FR-01  | `smoke`    | Valid login with `standard_user` → Products page        | Hardcoded          |
| `test_login_invalid_password`         | FR-02  | `smoke`    | Invalid credentials show correct error (parametrized)   | `login_data.csv`   |
| `test_login_blank_username`           | FR-03  | `regression` | Blank username → "Username is required" error         | Hardcoded          |
| `test_login_blank_password`           | FR-04  | `regression` | Blank password → "Password is required" error         | Hardcoded          |
| `test_login_username_exceeds_30_chars`| FR-05  | `regression` | 30, 31, 50 char usernames → error (parametrized)     | Inline parameters  |

**Data-Driven:** `test_login_invalid_password` reads rows from `testdata/login_data.csv`:

```csv
username,password,expected_error
standard_user,wrong_password,Epic sadface: Username and password do not match any user in this service
locked_out_user,secret_sauce,"Epic sadface: Sorry, this user has been locked out."
```

---

### `tests/test_products.py` — Products Tests (FR-06 to FR-08)

| Test Function                    | FR ID  | Marker       | Description                                      |
|----------------------------------|--------|--------------|--------------------------------------------------|
| `test_products_visible_after_login` | FR-06 | `regression` | Products page shows ≥1 product after login       |
| `test_add_to_cart`               | FR-07  | `smoke`      | Adding "Sauce Labs Backpack" → cart badge = 1    |
| `test_remove_from_cart`          | FR-08  | `regression` | Removing item → cart badge = 0                   |

---

### `tests/test_cart.py` — Cart & Security Tests (FR-09 to FR-10)

| Test Function                          | FR ID  | Marker       | Description                                           |
|----------------------------------------|--------|--------------|-------------------------------------------------------|
| `test_cart_details_match`              | FR-09  | `regression` | Added items appear in cart with correct name & price   |
| `test_unauthorized_access_after_logout`| FR-10  | `regression` | After logout, navigating to inventory → error/redirect |

---

### `tests/test_checkout.py` — Checkout Tests (FR-11 to FR-16)

| Test Function                    | FR ID  | Marker       | Description                                            | Data Source          |
|----------------------------------|--------|--------------|--------------------------------------------------------|----------------------|
| `test_navigate_to_checkout`      | FR-11  | `regression` | Cart → Checkout navigates to info form                 | Hardcoded            |
| `test_checkout_blank_first_name` | FR-12  | `smoke`      | Blank first name → "First Name is required" error      | Hardcoded            |
| `test_checkout_blank_last_name`  | FR-13  | `regression` | Blank last name → "Last Name is required" error        | Hardcoded            |
| `test_postal_code_boundary`      | FR-14  | `smoke`      | Postal codes: 4, 5, 6 digits + non-numeric (parametrized) | `checkout_data.json` |
| `test_checkout_overview`         | FR-15  | `regression` | Overview page shows subtotal, tax, total               | Hardcoded            |
| `test_finish_order`              | FR-16  | `smoke`      | Finish → "Thank you for your order!" confirmation      | Hardcoded            |

**Data-Driven:** `test_postal_code_boundary` reads from `testdata/checkout_data.json`:

```json
{
  "postal_code_boundary": [
    {"code": "1234", "digits": 4, "valid": true},
    {"code": "12345", "digits": 5, "valid": true},
    {"code": "123456", "digits": 6, "valid": true},
    {"code": "abcde", "digits": 5, "valid": false, "type": "non-numeric"}
  ]
}
```

> **Note:** SauceDemo does NOT validate postal codes server-side — it accepts any non-empty string. The test documents this spec discrepancy.

---

### Total Test Count Summary

| Test File          | Total Tests | Smoke | Regression |
|--------------------|-------------|-------|------------|
| `test_login.py`    | 8*          | 3     | 5          |
| `test_products.py` | 3           | 1     | 2          |
| `test_cart.py`     | 2           | 0     | 2          |
| `test_checkout.py` | 10*         | 6     | 4          |
| **Total**          | **23**      | **10**| **13**     |

_*Includes parametrized test instances (e.g., 2 CSV rows × FR-02, 3 boundary values × FR-05, 4 JSON entries × FR-14)._

---

## ⚙️ Test Infrastructure — `tests/conftest.py`

### CLI Options

| Flag              | Default   | Description                         |
|-------------------|-----------|-------------------------------------|
| `--headless`      | `False`   | Run Chrome in headless mode         |
| `--browser_name`  | `chrome`  | Browser selection (chrome only)     |

### Fixtures

| Fixture       | Scope     | Description                                                   |
|---------------|-----------|---------------------------------------------------------------|
| `driver`      | function  | Creates a fresh Chrome WebDriver per test (auto-cleanup)      |
| `login`       | function  | Logs in with `standard_user` and returns a `ProductsPage`     |
| `test_logger` | session   | Structured logger → `reports/logs/test_run.log`               |

### Hooks

**`pytest_runtest_makereport`** — Automatically captures a screenshot on test failure and:
- Saves it to `reports/screenshots/<test_name>_<timestamp>.png`
- Attaches it to the `pytest-html` report (if generating one)

### Chrome Options

- `--start-maximized` — Full browser window
- `--disable-gpu` — Stability on CI/CD
- `--no-sandbox` — Container compatibility
- `--disable-dev-shm-usage` — Prevents memory issues
- Password manager / leak detection popups disabled
- `--headless=new` — When `--headless` flag is passed

---

## ▶️ How to Run — Selenium Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Only Smoke Tests

```bash
pytest -m smoke
```

### Run Only Regression Tests

```bash
pytest -m regression
```

### Run in Headless Mode

```bash
pytest --headless
```

### Run a Specific Test File

```bash
pytest tests/test_login.py
pytest tests/test_checkout.py
```

### Run a Specific Test Function

```bash
pytest tests/test_login.py::test_login_success
pytest tests/test_checkout.py::test_finish_order
```

### Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Combined Example (Headless + HTML Report + Smoke Only)

```bash
pytest -m smoke --headless --html=reports/report.html --self-contained-html -v
```

### Test Outputs

| Output                           | Location                            |
|----------------------------------|-------------------------------------|
| Console output                   | Terminal (stdout)                   |
| Test execution log               | `reports/logs/test_run.log`         |
| HTML report                      | `reports/report.html`               |
| Failure screenshots              | `reports/screenshots/`              |

---

## 🔥 Performance Testing — Apache JMeter

### Test Plan Overview

**File:** `performance/jmx/saucedemo_weekend_lab.jmx`

#### Load Profile

| Parameter        | Value                     |
|------------------|---------------------------|
| Concurrent Users | 20                        |
| Ramp-Up Time     | 60 seconds                |
| Test Duration    | 180 seconds (3 minutes)   |
| Think Time       | 0–500 ms (uniform random) |
| Loop Count       | Infinite (duration-based) |

#### Test Plan Components

```
SauceDemo Weekend Lab - Performance Test
├── Thread Group: SauceDemo Users (20 threads, 60s ramp, 180s duration)
│   ├── HTTP Cookie Manager
│   ├── HTTP Request Defaults (www.saucedemo.com, HTTPS)
│   ├── Think Time (0-500ms Uniform Random Timer)
│   │
│   ├── 01 - Login Page         → GET /                              [200 assertion]
│   ├── 02 - Products Page      → GET /static/js/main.bcf4bc5f.js   [200 assertion]
│   ├── 03 - Static Resources   → GET /static/css/main.8a7d64a1.css [200 assertion]
│   │
│   ├── Summary Report Listener
│   └── View Results Tree (disabled for CLI runs)
```

#### HTTP Samplers Explained

| Sampler                | Method | Path                              | What It Tests                              |
|------------------------|--------|------------------------------------|--------------------------------------------|
| **01 - Login Page**    | GET    | `/`                               | Login page HTML load time (NFR-01)         |
| **02 - Products Page** | GET    | `/static/js/main.bcf4bc5f.js`     | Products page JS bundle delivery (NFR-02)  |
| **03 - Static Resources** | GET | `/static/css/main.8a7d64a1.css`  | CSS stylesheet delivery                   |

> **Why JS bundle for Products?** SauceDemo v2 is a React SPA — the products page is rendered client-side by the JavaScript bundle. The traditional `/inventory.html` endpoint no longer exists (returns 404). The JS bundle contains all the products page rendering logic, making it the most relevant HTTP-level measurement.

---

### NFR (Non-Functional Requirements) Thresholds

| NFR ID | Requirement                                    | Threshold       |
|--------|------------------------------------------------|-----------------|
| NFR-01 | Login page response time P95 for 20 users      | P95 < 3.0 seconds |
| NFR-02 | Products page response time P95 for 20 users   | P95 < 4.0 seconds |
| NFR-03 | Overall error rate during test window           | < 2%            |

---

### How to Run — JMeter Tests

#### Non-GUI Mode (Recommended for actual testing)

```bash
# From the project root directory:
D:\jmeter\apache-jmeter-5.6.3\bin\jmeter.bat -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report/
```

**Flags explained:**

| Flag | Purpose                                    |
|------|--------------------------------------------|
| `-n` | Non-GUI (command-line) mode                |
| `-t` | Path to the `.jmx` test plan              |
| `-l` | Path to save raw results (`.jtl`)          |
| `-e` | Generate HTML report after test            |
| `-o` | Output directory for HTML dashboard        |

#### GUI Mode (For debugging & reviewing test plan)

```bash
D:\jmeter\apache-jmeter-5.6.3\bin\jmeter.bat -t performance/jmx/saucedemo_weekend_lab.jmx
```

#### Generate HTML Report from Existing Results

```bash
D:\jmeter\apache-jmeter-5.6.3\bin\jmeter.bat -g performance/results/results.jtl -o performance/html_report/
```

#### Generate Aggregate CSV

```bash
powershell -ExecutionPolicy Bypass -File performance/generate_aggregate.ps1
```

> **Important:** Before re-running, delete old results:
> ```bash
> Remove-Item -Recurse -Force performance/results/*, performance/html_report/*
> ```

---

### JMeter Test Outputs

| Deliverable        | File/Folder                          | Description                                |
|--------------------|--------------------------------------|--------------------------------------------|
| Raw results        | `performance/results/results.jtl`    | CSV with every sample (timestamp, elapsed, status, etc.) |
| Aggregate report   | `performance/results/aggregate.csv`  | Summary statistics per sampler (P90/P95/P99, error %, throughput) |
| HTML dashboard     | `performance/html_report/index.html` | Interactive JMeter dashboard with charts   |
| NFR findings       | `performance/Findings.md`           | NFR Pass/Fail mapping with measured values |

---

### Performance Test Results

#### Aggregate Report

| Sampler              | Samples | Avg (ms) | Median (ms) | P90 (ms) | P95 (ms) | P99 (ms) | Min (ms) | Max (ms) | Error % |
|----------------------|---------|----------|-------------|----------|----------|----------|----------|----------|---------|
| 01 - Login Page      | 3,009   | 46       | 37          | 62       | 84       | 150      | 18       | 1,330    | 0.00%   |
| 02 - Products Page   | 3,003   | 160      | 130         | 275      | 336      | 542      | 45       | 2,022    | 0.00%   |
| 03 - Static Resources| 2,996   | 49       | 42          | 67       | 86       | 160      | 19       | 1,167    | 0.00%   |
| **TOTAL**            | **9,008**| **85**  | **48**      | **179**  | **240**  | **406**  | **18**   | **2,022**| **0.00%** |

#### NFR Compliance

| NFR ID | Threshold       | Measured Value | Status      |
|--------|-----------------|----------------|-------------|
| NFR-01 | P95 < 3000 ms   | 84 ms          | ✅ **PASS** |
| NFR-02 | P95 < 4000 ms   | 336 ms         | ✅ **PASS** |
| NFR-03 | Error < 2%      | 0.00%          | ✅ **PASS** |

All three NFR thresholds are comfortably met. The login page (1.7 KB HTML) responds fastest (P95 = 84 ms), followed by CSS (P95 = 86 ms), and the JS bundle (667 KB) is slowest but still well within the 4-second threshold (P95 = 336 ms).

---

## 📊 Test Data Files

### `testdata/login_data.csv`

Used by `test_login_invalid_password` (FR-02) for data-driven negative login testing:

```csv
username,password,expected_error
standard_user,wrong_password,Epic sadface: Username and password do not match any user in this service
locked_out_user,secret_sauce,"Epic sadface: Sorry, this user has been locked out."
```

### `testdata/checkout_data.json`

Used by `test_postal_code_boundary` (FR-14) for boundary value analysis:

```json
{
  "postal_code_boundary": [
    {"code": "1234", "digits": 4, "valid": true},
    {"code": "12345", "digits": 5, "valid": true},
    {"code": "123456", "digits": 6, "valid": true},
    {"code": "abcde", "digits": 5, "valid": false, "type": "non-numeric"}
  ]
}
```

---

## 📝 Configuration Files

### `pytest.ini`

```ini
[pytest]
testpaths = tests
markers =
    smoke: Smoke tests — mandatory FR coverage
    regression: Regression tests — extended FR coverage
addopts = -v
```

### `requirements.txt`

```
selenium>=4.15.0
pytest>=7.4.0
pytest-html>=4.1.0
webdriver-manager>=4.0.0
```

### `.gitignore`

Excludes from version control:
- `__pycache__/`, `*.pyc` — Python bytecode
- `venv/` — Virtual environment
- `.pytest_cache/` — PyTest cache
- `reports/screenshots/`, `reports/logs/`, `reports/report.html` — Test outputs
- `performance/results/`, `performance/html_report/` — JMeter outputs

---

## 🔑 Key Testing Techniques Used

| Technique                  | Where Applied                          |
|----------------------------|----------------------------------------|
| **Page Object Model (POM)**| All page classes in `pages/`           |
| **Data-Driven Testing**    | CSV (login), JSON (postal codes)       |
| **Parametrized Tests**     | `@pytest.mark.parametrize` for FR-02, FR-05, FR-14 |
| **Boundary Value Analysis**| Username length (30/31/50), postal codes (4/5/6 digits) |
| **Negative Testing**       | Blank fields, invalid credentials, locked-out user |
| **Security Testing**       | Unauthorized access after logout (FR-10) |
| **Explicit Waits**         | All interactions via `WebDriverWait` (no `time.sleep`) |
| **Screenshot on Failure**  | `pytest_runtest_makereport` hook        |
| **Structured Logging**     | Session logger to file + console        |
| **Load/Performance Testing**| JMeter with 20 concurrent users        |

---

## 🎯 Test Case Design — Equivalence Partitioning & Boundary Value Analysis

Test cases in this framework are **systematically derived** from the functional requirements using two core black-box testing techniques:

1. **Equivalence Partitioning (EP)** — Divides input data into partitions (classes) where all values within a partition are expected to behave identically. One representative test case per partition provides sufficient coverage.
2. **Boundary Value Analysis (BVA)** — Tests values at the edges (boundaries) of equivalence partitions, where defects are most likely to occur.

---

### 1. Login — Username Field (FR-01 to FR-05)

**Requirement:** The system should authenticate users with valid credentials and reject invalid ones.

#### Equivalence Partitions

| Partition ID | Partition Description         | Input Example           | Expected Outcome         | Test Function                         |
|--------------|-------------------------------|-------------------------|--------------------------|---------------------------------------|
| EP-U1        | Valid registered username      | `standard_user`         | Login succeeds           | `test_login_success` (FR-01)          |
| EP-U2        | Valid but locked-out username  | `locked_out_user`       | Error: user locked out   | `test_login_invalid_password` (FR-02) |
| EP-U3        | Empty/blank username           | `""` (empty string)     | Error: username required | `test_login_blank_username` (FR-03)   |
| EP-U4        | Non-existent username          | `aaa...a` (30+ chars)   | Error: no match          | `test_login_username_exceeds_30_chars` (FR-05) |

#### Boundary Value Analysis — Username Length

The specification implies a username character limit of **30 characters**. We test at and around this boundary:

```
         ◄── Valid range (1–30 chars) ──►
─────────┬──────────────────────────────┬──────────────────►
         │                              │
     0 chars                       30 chars     31+ chars
     (empty)                       (boundary)   (exceeds)
      ▲                           ▲    ▲         ▲
      │                           │    │         │
    BVA-1                       BVA-2 BVA-3    BVA-4
   FR-03                        FR-05 FR-05    FR-05
```

| BVA ID | Value      | Length | Expected Behavior    | Test Function                    |
|--------|------------|--------|----------------------|----------------------------------|
| BVA-1  | `""`       | 0      | Error: required      | `test_login_blank_username`      |
| BVA-2  | `"a" × 30` | 30     | Error: no match      | `test_login_username_exceeds_30_chars[30_chars]` |
| BVA-3  | `"a" × 31` | 31     | Error: no match      | `test_login_username_exceeds_30_chars[31_chars]` |
| BVA-4  | `"a" × 50` | 50     | Error: no match      | `test_login_username_exceeds_30_chars[50_chars]` |

**Implementation:** These BVA values are parametrized directly in `test_login.py`:
```python
@pytest.mark.parametrize(
    "long_username, char_count",
    [("a" * 30, 30), ("a" * 31, 31), ("a" * 50, 50)],
    ids=["30_chars", "31_chars", "50_chars"],
)
def test_login_username_exceeds_30_chars(driver, test_logger, long_username, char_count):
```

---

### 2. Login — Password Field (FR-01, FR-02, FR-04)

**Requirement:** Valid password authenticates; invalid/blank password shows error.

#### Equivalence Partitions

| Partition ID | Partition Description     | Input Example      | Expected Outcome          | Test Function                   |
|--------------|---------------------------|--------------------|--------------------------|---------------------------------|
| EP-P1        | Correct password           | `secret_sauce`     | Login succeeds            | `test_login_success` (FR-01)    |
| EP-P2        | Incorrect password         | `wrong_password`   | Error: no match           | `test_login_invalid_password` (FR-02) |
| EP-P3        | Empty/blank password       | `""` (empty)       | Error: password required  | `test_login_blank_password` (FR-04) |

**Data-Driven:** EP-P2 test cases are loaded from `testdata/login_data.csv`, allowing easy addition of more invalid credential combinations without modifying code.

---

### 3. Login — Combined Input Analysis (FR-01 to FR-04)

When both username and password are considered together, we get a **2-dimensional** equivalence partition:

| Scenario           | Username           | Password        | Expected             | FR   | Test                          |
|--------------------|--------------------|-----------------|----------------------|------|-------------------------------|
| Both valid         | `standard_user`    | `secret_sauce`  | ✅ Login succeeds    | FR-01 | `test_login_success`         |
| Valid user, wrong pw | `standard_user`  | `wrong_password`| ❌ Error: no match   | FR-02 | `test_login_invalid_password`|
| Locked user, right pw | `locked_out_user` | `secret_sauce` | ❌ Error: locked out | FR-02 | `test_login_invalid_password`|
| Blank user         | `""`               | `secret_sauce`  | ❌ Error: required   | FR-03 | `test_login_blank_username`  |
| Blank password     | `standard_user`    | `""`            | ❌ Error: required   | FR-04 | `test_login_blank_password`  |

---

### 4. Cart Operations — Add/Remove (FR-07, FR-08)

**Requirement:** Users can add and remove products; the cart badge count should reflect the correct number.

#### Equivalence Partitions

| Partition ID | Partition Description       | Cart Badge Before | Action       | Cart Badge After | Test Function         |
|--------------|-----------------------------|-------------------|--------------|------------------|-----------------------|
| EP-C1        | Add to empty cart            | 0                 | Add 1 item   | 1                | `test_add_to_cart` (FR-07) |
| EP-C2        | Remove from cart (1 item)    | 1                 | Remove 1 item| 0                | `test_remove_from_cart` (FR-08) |
| EP-C3        | Add multiple items           | 0                 | Add 2 items  | 2                | `test_cart_details_match` (FR-09) |

#### Boundary Values — Cart Count

```
    ◄── Empty ──►◄── Has Items ──►
────────────────┬────────────────────►
                │
           0 items              n items
              ▲                   ▲
              │                   │
           BVA-C1              BVA-C2
           FR-08               FR-07, FR-09
     (remove → 0)          (add → 1, add → 2)
```

| BVA ID  | Condition            | Expected Badge | Test                    |
|---------|----------------------|----------------|-------------------------|
| BVA-C1  | Cart becomes empty   | 0 (no badge)   | `test_remove_from_cart`  |
| BVA-C2  | Cart has 1 item      | 1              | `test_add_to_cart`       |
| BVA-C3  | Cart has 2 items     | 2              | `test_cart_details_match`|

---

### 5. Checkout — Personal Information Fields (FR-12, FR-13)

**Requirement:** First name, last name, and postal code are all required. Blank fields show validation errors.

#### Equivalence Partitions — First Name

| Partition ID | Partition Description | Input      | Expected Outcome              | Test Function                    |
|--------------|-----------------------|------------|-------------------------------|----------------------------------|
| EP-FN1       | Non-empty first name  | `"Jane"`   | Proceeds to next step         | `test_finish_order` (FR-16)      |
| EP-FN2       | Empty first name      | `""`       | Error: First Name is required | `test_checkout_blank_first_name` (FR-12) |

#### Equivalence Partitions — Last Name

| Partition ID | Partition Description | Input      | Expected Outcome             | Test Function                   |
|--------------|-----------------------|------------|------------------------------|---------------------------------|
| EP-LN1       | Non-empty last name   | `"Smith"`  | Proceeds to next step        | `test_finish_order` (FR-16)     |
| EP-LN2       | Empty last name       | `""`       | Error: Last Name is required | `test_checkout_blank_last_name` (FR-13) |

---

### 6. Checkout — Postal Code Field (FR-14) ⭐ Key BVA Example

**Requirement:** Postal code should accept valid numeric codes (4–6 digits) and reject non-numeric input.

This is the **primary Boundary Value Analysis** test case in the framework, with data driven from `testdata/checkout_data.json`.

#### Equivalence Partitions

| Partition ID | Partition Description         | Input     | Expected (Spec) | Actual (App) | Test Function              |
|--------------|-------------------------------|-----------|-----------------|--------------|----------------------------|
| EP-PC1       | Valid numeric (within range)   | `"12345"` | ✅ Accept       | ✅ Accept    | `test_postal_code_boundary` |
| EP-PC2       | Non-numeric string             | `"abcde"` | ❌ Reject       | ✅ Accept*   | `test_postal_code_boundary` |
| EP-PC3       | Empty postal code              | `""`      | ❌ Reject       | ❌ Reject    | (covered by required-field validation) |

_*Spec discrepancy: SauceDemo accepts any non-empty string as a postal code._

#### Boundary Value Analysis — Postal Code Digit Count

Assuming a valid postal code is **5 digits** (standard US ZIP), we test at boundaries:

```
    ◄── Below ──►◄──── Valid Range ────►◄── Above ──►
────────────────┬───────────────────────┬────────────────►
                │                       │
           4 digits                6 digits
          (boundary-1)            (boundary+1)
              ▲          ▲            ▲
              │          │            │
           BVA-PC1    BVA-PC2     BVA-PC3
            "1234"    "12345"     "123456"
```

| BVA ID   | Input      | Digits | Type     | Expected (Spec) | Actual | Data Source          |
|----------|------------|--------|----------|-----------------|--------|----------------------|
| BVA-PC1  | `"1234"`   | 4      | Numeric  | Below boundary — may reject | Accepts | `checkout_data.json` |
| BVA-PC2  | `"12345"`  | 5      | Numeric  | On boundary — should accept | Accepts | `checkout_data.json` |
| BVA-PC3  | `"123456"` | 6      | Numeric  | Above boundary — may reject | Accepts | `checkout_data.json` |
| BVA-PC4  | `"abcde"`  | 5      | Non-numeric | Invalid class — should reject | Accepts* | `checkout_data.json` |

**Implementation:** Values are stored in `testdata/checkout_data.json` and loaded via parametrize:
```python
@pytest.mark.parametrize("postal_entry", _load_postal_code_data(),
    ids=lambda e: f"{e.get('digits','?')}digit_{'non_numeric' if e.get('type') == 'non-numeric' else 'numeric'}")
def test_postal_code_boundary(login, driver, test_logger, postal_entry):
```

> **Spec Discrepancy Found:** Through BVA testing, we discovered that SauceDemo does NOT validate postal code format. It accepts `"abcde"` (non-numeric) and any digit length. This is logged as a warning in the test output and documented in the test docstring.

---

### 7. Security — Session Management (FR-10)

**Requirement:** After logout, users should not be able to access protected pages.

#### Equivalence Partitions

| Partition ID | Partition Description          | Session State    | Action                       | Expected             | Test Function                         |
|--------------|--------------------------------|------------------|------------------------------|----------------------|---------------------------------------|
| EP-S1        | Authenticated user             | Logged in        | Access `/inventory.html`     | ✅ Access granted    | `test_products_visible_after_login`   |
| EP-S2        | Unauthenticated user (post-logout) | Logged out   | Access `/inventory.html`     | ❌ Error/redirect    | `test_unauthorized_access_after_logout` |

This is a two-partition scheme: **authorized** vs **unauthorized** access. No boundary exists — it's a binary state.

---

### Summary: EP & BVA Traceability Matrix

| Requirement | Input Domain          | EP Partitions | BVA Values | Test File            |
|-------------|-----------------------|---------------|------------|----------------------|
| FR-01       | Username + Password   | 2 (valid combo) | —        | `test_login.py`      |
| FR-02       | Invalid credentials   | 2 (wrong pw, locked user) | — | `test_login.py` |
| FR-03       | Blank username        | 1 (empty class) | 0 chars  | `test_login.py`      |
| FR-04       | Blank password        | 1 (empty class) | 0 chars  | `test_login.py`      |
| FR-05       | Username length       | 1 (exceeds limit) | 30, 31, 50 chars | `test_login.py` |
| FR-07       | Add to cart           | 1 (add action)  | 0→1 badge | `test_products.py`  |
| FR-08       | Remove from cart      | 1 (remove action) | 1→0 badge | `test_products.py` |
| FR-09       | Cart contents         | 1 (multi-item)  | 2 items   | `test_cart.py`       |
| FR-10       | Session state         | 2 (auth/unauth) | —         | `test_cart.py`       |
| FR-12       | First name            | 2 (empty/non-empty) | 0 chars | `test_checkout.py` |
| FR-13       | Last name             | 2 (empty/non-empty) | 0 chars | `test_checkout.py` |
| FR-14       | Postal code           | 3 (numeric/non-numeric/empty) | 4, 5, 6 digits | `test_checkout.py` |

**Total:** 19 equivalence partitions identified → mapped to 23 test cases (with parametrized expansion).

---

## 📋 Quick Reference — All FR/NFR Coverage

### Functional Requirements (Selenium)

| FR ID  | Description                            | Test File           | Status |
|--------|----------------------------------------|---------------------|--------|
| FR-01  | Valid login → Products page            | `test_login.py`     | ✅     |
| FR-02  | Invalid credentials → error message    | `test_login.py`     | ✅     |
| FR-03  | Blank username → error                 | `test_login.py`     | ✅     |
| FR-04  | Blank password → error                 | `test_login.py`     | ✅     |
| FR-05  | Username > 30 chars → error            | `test_login.py`     | ✅     |
| FR-06  | Products visible after login           | `test_products.py`  | ✅     |
| FR-07  | Add product to cart                    | `test_products.py`  | ✅     |
| FR-08  | Remove product from cart               | `test_products.py`  | ✅     |
| FR-09  | Cart shows correct item details        | `test_cart.py`      | ✅     |
| FR-10  | Unauthorized access after logout       | `test_cart.py`      | ✅     |
| FR-11  | Navigate to checkout from cart         | `test_checkout.py`  | ✅     |
| FR-12  | Blank first name → error              | `test_checkout.py`  | ✅     |
| FR-13  | Blank last name → error               | `test_checkout.py`  | ✅     |
| FR-14  | Postal code boundary values            | `test_checkout.py`  | ✅     |
| FR-15  | Checkout overview price summary        | `test_checkout.py`  | ✅     |
| FR-16  | Finish order → success confirmation    | `test_checkout.py`  | ✅     |

### Non-Functional Requirements (JMeter)

| NFR ID | Description                        | Threshold       | Result      |
|--------|------------------------------------|-----------------|-------------|
| NFR-01 | Login page P95 response time       | < 3.0 seconds   | ✅ PASS (84 ms)    |
| NFR-02 | Products page P95 response time    | < 4.0 seconds   | ✅ PASS (336 ms)   |
| NFR-03 | Overall error rate                 | < 2%            | ✅ PASS (0.00%)    |
