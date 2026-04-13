# Test Framework — Explained

## What Is This Framework?

This is a **Selenium 4 + PyTest** test automation framework built to test the [SauceDemo](https://www.saucedemo.com) web application. It follows industry-standard practices used in real-world QA engineering teams.

The framework automates **16 functional requirements** (FR-01 to FR-16) covering login, products, cart, and checkout flows, and validates **3 non-functional requirements** (NFR-01 to NFR-03) using Apache JMeter for performance testing.

---

## 🧭 Testing Strategy

The framework implements a **multi-layered testing strategy** that combines different testing types to achieve comprehensive coverage. Each type targets a different aspect of application quality.

### Testing Types Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    TESTING STRATEGY                           │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│  SMOKE       │  REGRESSION  │  FUNCTIONAL  │  PERFORMANCE    │
│  (Critical)  │  (Extended)  │  (Full)      │  (Non-Func)     │
│  10 tests    │  13 tests    │  23 tests    │  JMeter         │
│  ~2 min      │  ~4 min      │  ~6 min      │  3 min          │
├──────────────┴──────────────┴──────────────┴─────────────────┤
│  DATA-DRIVEN │ BOUNDARY VALUE │ NEGATIVE   │ SECURITY        │
│  CSV + JSON  │ EP + BVA       │ Blank/Bad  │ Session Mgmt    │
└──────────────────────────────────────────────────────────────┘
```

---

### 1. Smoke Testing

**What:** A quick, high-priority subset of tests that verify the most critical user flows work. If smoke tests fail, the build is broken — no point running the full suite.

**When to run:** After every build, deployment, or code change. First line of defense.

**Where it's used in our framework:**

```bash
pytest -m smoke    # Run only smoke tests (~2 minutes)
```

| Test | FR ID | What It Verifies |
|------|-------|-----------------|
| `test_login_success` | FR-01 | User can log in |
| `test_login_invalid_password` | FR-02 | Invalid login shows error |
| `test_add_to_cart` | FR-07 | User can add items to cart |
| `test_checkout_blank_first_name` | FR-12 | Form validation works |
| `test_postal_code_boundary` | FR-14 | Checkout accepts postal codes |
| `test_finish_order` | FR-16 | Full checkout flow completes |

**Key idea:** If a user can't log in, add to cart, and checkout — the app is fundamentally broken.

---

### 2. Regression Testing

**What:** An extended test suite that covers edge cases, boundary values, and secondary flows. Ensures that new code changes haven't broken existing functionality.

**When to run:** Before releases, after major changes, during nightly CI/CD runs.

**Where it's used in our framework:**

```bash
pytest -m regression    # Run regression tests (~4 minutes)
```

| Test | FR ID | What It Verifies |
|------|-------|-----------------|
| `test_login_blank_username` | FR-03 | Edge case: empty username |
| `test_login_blank_password` | FR-04 | Edge case: empty password |
| `test_login_username_exceeds_30_chars` | FR-05 | Boundary: username length |
| `test_products_visible_after_login` | FR-06 | Products page loads correctly |
| `test_remove_from_cart` | FR-08 | Remove item flow |
| `test_cart_details_match` | FR-09 | Cart data integrity |
| `test_unauthorized_access_after_logout` | FR-10 | Security: session management |
| `test_navigate_to_checkout` | FR-11 | Navigation flow |
| `test_checkout_blank_last_name` | FR-13 | Edge case: blank last name |
| `test_checkout_overview` | FR-15 | Price calculation display |

**Key idea:** These tests catch subtle bugs that smoke tests miss — boundary values, empty inputs, state transitions.

---

### 3. Functional Testing

**What:** The full suite (smoke + regression) that verifies every functional requirement. Covers all 16 FRs end-to-end.

**When to run:** Full regression before release.

```bash
pytest    # Run all 23 tests (~6 minutes)
```

The complete suite covers the entire user journey:
```
Login → Products → Add to Cart → Cart → Checkout Info → Overview → Complete
FR-01    FR-06      FR-07        FR-09   FR-11/12/13     FR-15     FR-16
  to       to                     to       FR-14
FR-05    FR-08                   FR-10
```

---

### 4. Negative Testing

**What:** Tests that verify the application handles **invalid, unexpected, or missing input** correctly. The app should show appropriate error messages — not crash.

**Where it's used:**

| Test | Input | Expected Error |
|------|-------|---------------|
| `test_login_invalid_password` | Wrong password | "Username and password do not match" |
| `test_login_blank_username` | Empty username | "Username is required" |
| `test_login_blank_password` | Empty password | "Password is required" |
| `test_login_username_exceeds_30_chars` | 30/31/50 char usernames | "Epic sadface" error |
| `test_checkout_blank_first_name` | Empty first name | "First Name is required" |
| `test_checkout_blank_last_name` | Empty last name | "Last Name is required" |

**Key idea:** A good application fails gracefully. Negative tests ensure error handling works.

---

### 5. Data-Driven Testing

**What:** Test logic is written once but runs multiple times with different data from external files (CSV, JSON). Separates test data from test code.

**Where it's used:**

| Data File | Format | Test | Purpose |
|-----------|--------|------|---------|
| `testdata/login_data.csv` | CSV | `test_login_invalid_password` (FR-02) | Multiple invalid credential combos |
| `testdata/checkout_data.json` | JSON | `test_postal_code_boundary` (FR-14) | Postal code boundary values |

**How it works with `@pytest.mark.parametrize`:**
```python
# One test function → runs 2 times (once per CSV row)
@pytest.mark.parametrize("username, password, expected_error", list(_read_login_csv()))
def test_login_invalid_password(driver, username, password, expected_error):
```

**Key idea:** To add a new test case, just add a row to the CSV/JSON — no code changes needed.

---

### 6. Boundary Value Analysis (BVA) Testing

**What:** Tests inputs at the **edges** of valid ranges where bugs are most likely to hide. Based on the principle that errors cluster at boundaries.

**Where it's used:**

| Input | Boundary | Values Tested | Test |
|-------|----------|--------------|------|
| Username length | 30 chars (spec limit) | 0, 30, 31, 50 chars | `test_login_blank_username`, `test_login_username_exceeds_30_chars` |
| Postal code digits | 5 digits (US ZIP) | 4, 5, 6 digits + non-numeric | `test_postal_code_boundary` |
| Cart item count | 0 items (empty) | 0→1, 1→0, 0→2 items | `test_add_to_cart`, `test_remove_from_cart`, `test_cart_details_match` |

**Key idea:** If the system handles 30-character and 31-character usernames correctly, it almost certainly handles 25 or 35 correctly too.

---

### 7. Security Testing

**What:** Verifies that the application properly enforces access control — unauthorized users cannot access protected resources.

**Where it's used:**

| Test | What It Checks |
|------|---------------|
| `test_unauthorized_access_after_logout` (FR-10) | After logout, navigating directly to `/inventory.html` is blocked |

**How it works:**
1. Log in with valid credentials → Products page loads ✅
2. Logout via burger menu → Back to login page
3. Manually navigate to `https://www.saucedemo.com/inventory.html`
4. **Assert:** App shows error message and denies access ✅

**Key idea:** Tests the authentication session lifecycle — logged out users must not access protected pages.

---

### 8. Load / Performance Testing (JMeter)

**What:** Simulates multiple concurrent users to verify the application meets response time and error rate thresholds under load.

**Tool:** Apache JMeter 5.6.3 (separate from Selenium — runs at HTTP protocol level)

**Where it's used:**

```bash
D:\jmeter\apache-jmeter-5.6.3\bin\jmeter.bat -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report/
```

| NFR | What It Tests | Load | Threshold | Result |
|-----|--------------|------|-----------|--------|
| NFR-01 | Login page response time | 20 users, 3 min | P95 < 3.0s | ✅ 84 ms |
| NFR-02 | Products page response time | 20 users, 3 min | P95 < 4.0s | ✅ 336 ms |
| NFR-03 | Overall error rate | 20 users, 3 min | < 2% | ✅ 0.00% |

**Key idea:** Functional tests prove the app works for 1 user. Load tests prove it works for 20 simultaneous users.

---

### Strategy Summary: When to Run What

| Scenario | What to Run | Command | Time |
|----------|------------|---------|------|
| Quick sanity check | Smoke tests | `pytest -m smoke` | ~2 min |
| Before merging PR | Full suite | `pytest` | ~6 min |
| Before release | Full + Performance | `pytest` + JMeter | ~9 min |
| Investigating a bug | Specific test | `pytest tests/test_login.py::test_name` | ~30s |
| Nightly CI/CD | Full + HTML report | `pytest --html=reports/report.html` | ~6 min |

---

## Why Page Object Model (POM)?

The biggest problem in test automation is **maintenance**. When the UI changes (a button ID changes, a CSS class is renamed), you don't want to update 50 test files — you want to update **one place**.

That's what POM solves.

### Without POM (Bad Practice)

```python
# Every test file repeats the same locators and logic
def test_login():
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

def test_login_blank():
    driver.find_element(By.ID, "user-name").send_keys("")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
```

**Problem:** If `user-name` changes to `username`, you must update every test file.

### With POM (Our Approach)

```python
# pages/login_page.py — locators defined ONCE
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")  # Change here only
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

# tests/test_login.py — clean, readable tests
def test_login_success(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
```

**Benefit:** If `user-name` changes to `username`, you update **one line** in `login_page.py` and all tests still work.

---

## How the Framework Layers Work

```
┌─────────────────────────────────────────────┐
│              TEST LAYER (tests/)            │
│  • What to test (assertions, data, logic)   │
│  • Does NOT know how the UI works           │
│  • Example: "login should show Products"    │
├─────────────────────────────────────────────┤
│           PAGE OBJECT LAYER (pages/)        │
│  • How to interact with the UI              │
│  • Knows locators and actions               │
│  • Example: "type into #user-name field"    │
├─────────────────────────────────────────────┤
│              BASE PAGE (base_page.py)       │
│  • Reusable wait/click/type helpers         │
│  • Handles synchronization (explicit waits) │
│  • Every page object inherits from this     │
├─────────────────────────────────────────────┤
│           SELENIUM WEBDRIVER                │
│  • Controls the actual browser              │
│  • Sends commands to Chrome                 │
└─────────────────────────────────────────────┘
```

### Layer Rules

1. **Tests never touch Selenium directly** — they call page object methods
2. **Page objects never make assertions** — they return data for tests to verify
3. **Base page handles waiting** — no page or test uses `time.sleep()`

---

## Why Explicit Waits? (No `time.sleep`)

Web pages load asynchronously — elements appear at different times. There are three ways to handle this:

### ❌ `time.sleep(3)` — Hardcoded Wait

```python
driver.find_element(By.ID, "login-button").click()
time.sleep(3)  # Wait 3 seconds and hope the page loaded
```

**Problem:** If the page loads in 0.5s, you waste 2.5s per test. If it takes 4s (slow network), the test fails.

### ❌ `implicitly_wait(10)` — Implicit Wait

```python
driver.implicitly_wait(10)  # Wait up to 10s for ANY element
```

**Problem:** Applies globally to ALL element lookups. Can mask real failures and makes debugging difficult.

### ✅ `WebDriverWait` — Explicit Wait (Our Approach)

```python
# base_page.py
def wait_for_element(self, locator, timeout=10):
    return WebDriverWait(self.driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
```

**How it works:** Polls every 0.5 seconds until the **specific condition** is met (element visible, element clickable, etc.) or the timeout expires. Fast when the page loads quickly, patient when it's slow.

Our `base_page.py` provides these wait helpers:

| Method | Waits Until... |
|--------|---------------|
| `wait_for_element()` | Element is **visible** on the page |
| `wait_for_clickable()` | Element is **visible AND enabled** (can be clicked) |
| `wait_for_elements()` | **All** matching elements are visible |

Every `click()`, `type_text()`, and `get_text()` method in the framework uses these helpers internally, so tests never need to worry about timing.

---

## How `conftest.py` Works

PyTest's `conftest.py` is a special file that provides **shared fixtures** — reusable setup/teardown code that tests can request by name.

### The `driver` Fixture

```python
@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    _driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    yield _driver        # Test runs here
    _driver.quit()       # Cleanup after test
```

**Key points:**
- `scope="function"` → Each test gets a **fresh** browser (no state leakage between tests)
- `ChromeDriverManager().install()` → Automatically downloads the correct ChromeDriver version
- `yield` → The driver is created before the test, and `quit()` runs after, even if the test fails

### The `login` Fixture

```python
@pytest.fixture(scope="function")
def login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    return ProductsPage(driver)
```

Tests that need a logged-in state just add `login` as a parameter:

```python
def test_add_to_cart(login, driver):
    products_page = login  # Already logged in!
    products_page.add_to_cart_by_name("Sauce Labs Backpack")
```

### Screenshot on Failure Hook

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        driver.save_screenshot(f"reports/screenshots/{item.name}.png")
```

**What this does:** If any test fails, PyTest automatically captures a browser screenshot and saves it. This is invaluable for debugging — you can see exactly what the browser looked like when the assertion failed.

---

## How Data-Driven Testing Works

Instead of hardcoding test inputs in the test file, we store them in external files. This allows:
- Adding new test cases **without modifying code**
- Keeping test logic separate from test data
- Easy maintenance by non-developers

### CSV for Login Tests

**File:** `testdata/login_data.csv`
```csv
username,password,expected_error
standard_user,wrong_password,Epic sadface: Username and password do not match...
locked_out_user,secret_sauce,"Epic sadface: Sorry, this user has been locked out."
```

**How it's loaded:**
```python
def _read_login_csv():
    with open("testdata/login_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row["username"], row["password"], row["expected_error"]

@pytest.mark.parametrize("username, password, expected_error", list(_read_login_csv()))
def test_login_invalid_password(driver, username, password, expected_error):
    # This test runs ONCE for each row in the CSV
```

**Result:** Adding a new row to the CSV automatically creates a new test case — no code changes needed.

### JSON for Checkout Tests

**File:** `testdata/checkout_data.json`
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

**How it's loaded:**
```python
def _load_postal_code_data():
    with open("testdata/checkout_data.json") as f:
        return json.load(f)["postal_code_boundary"]

@pytest.mark.parametrize("postal_entry", _load_postal_code_data())
def test_postal_code_boundary(login, driver, postal_entry):
    code = postal_entry["code"]
    is_valid = postal_entry["valid"]
    # Test runs once per JSON entry
```

---

## How PyTest Markers Work

Markers let you **tag** tests and run subsets:

```python
@pytest.mark.smoke       # Critical path — must always pass
def test_login_success(): ...

@pytest.mark.regression  # Extended coverage — edge cases
def test_login_blank_username(): ...
```

**Running by marker:**
```bash
pytest -m smoke        # Only run smoke tests (fast verification)
pytest -m regression   # Only run regression tests (thorough check)
pytest                 # Run everything
```

**Defined in `pytest.ini`:**
```ini
[pytest]
markers =
    smoke: Smoke tests — mandatory FR coverage
    regression: Regression tests — extended FR coverage
```

---

## How the Logging System Works

The framework has a structured logging system that writes to both console and file:

```python
# In conftest.py
_logger = logging.getLogger("saucedemo_tests")
_logger.setLevel(logging.DEBUG)

# File handler → reports/logs/test_run.log
_fh = logging.FileHandler("reports/logs/test_run.log")

# Console handler → terminal output
_ch = logging.StreamHandler()
```

**In tests:**
```python
def test_login_success(driver, test_logger):
    test_logger.info("TEST START — test_login_success (FR-01)")
    # ... test logic ...
    test_logger.info("TEST PASSED — test_login_success")
```

**In page objects:**
```python
def login(self, username, password):
    logger.info("Logging in as '%s'", username)
    # ... interaction logic ...
```

**Sample log output (`reports/logs/test_run.log`):**
```
2026-04-13 11:20:01 - saucedemo_tests - INFO - Test session started
2026-04-13 11:20:01 - saucedemo_tests - INFO - Setting up chrome driver for test_login_success
2026-04-13 11:20:03 - pages.login_page - INFO - Opened login page
2026-04-13 11:20:03 - pages.login_page - INFO - Logging in as 'standard_user'
2026-04-13 11:20:04 - saucedemo_tests - INFO - TEST PASSED — test_login_success
```

This gives you a complete trace of every action — invaluable when debugging failing tests.

---

## How JMeter Performance Testing Works

While Selenium tests verify **functional correctness** (does the app behave correctly?), JMeter tests verify **performance** (does the app respond fast enough under load?).

### What JMeter Does

JMeter simulates **20 users** simultaneously hitting the SauceDemo server for **3 minutes**:

```
Time 0s    → User 1 starts
Time 3s    → User 2 starts
Time 6s    → User 3 starts
...          (1 new user every 3 seconds)
Time 57s   → User 20 starts
Time 60s   → All 20 users active, running concurrently
...
Time 180s  → Test ends
```

Each user repeats this loop:
1. **GET `/`** → Download the login page HTML
2. **GET `/static/js/main.bcf4bc5f.js`** → Download the JS bundle (products page)
3. **GET `/static/css/main.8a7d64a1.css`** → Download the CSS stylesheet
4. **Wait 0–500ms** → Random think time (simulates real user pauses)
5. **Repeat from step 1**

### What JMeter Measures

For each request, JMeter records:
- **Response time** (elapsed milliseconds)
- **Response code** (200 OK, 404 Not Found, etc.)
- **Success/failure** status
- **Bytes received**

From these raw samples (~9,000 per run), we calculate:
- **P95** = the response time that 95% of requests were faster than
- **Error rate** = percentage of non-200 responses

### Why Not Selenium for Performance?

| Aspect | Selenium | JMeter |
|--------|----------|--------|
| Protocol | Drives a **real browser** | Sends **HTTP requests** |
| Resource usage | 1 browser per user (heavy) | Lightweight threads |
| 20 users | Would need 20 Chrome instances | Runs in one JVM |
| Measures | Full page render time | HTTP response time |
| Best for | Functional testing | Load/stress testing |

---

## Framework File Summary

| File | Purpose | Key Concept |
|------|---------|-------------|
| `pages/base_page.py` | Reusable wait/click/type helpers | **Inheritance** — all pages extend this |
| `pages/login_page.py` | Login page locators + actions | **Encapsulation** — locators in one place |
| `pages/products_page.py` | Products page locators + actions | **POM** — separates UI from tests |
| `pages/cart_page.py` | Cart page locators + actions | **POM** |
| `pages/checkout_*.py` | Checkout flow (3 pages) | **POM** |
| `tests/conftest.py` | Fixtures + hooks | **Dependency injection** via PyTest |
| `tests/test_login.py` | Login tests (FR-01–05) | **Data-driven** via CSV |
| `tests/test_products.py` | Product tests (FR-06–08) | **Parametrized** assertions |
| `tests/test_cart.py` | Cart tests (FR-09–10) | **Security testing** (logout) |
| `tests/test_checkout.py` | Checkout tests (FR-11–16) | **BVA** via JSON data |
| `testdata/login_data.csv` | Invalid login credentials | **External test data** |
| `testdata/checkout_data.json` | Postal code boundaries | **External test data** |
| `pytest.ini` | PyTest configuration | **Test markers** (smoke/regression) |
| `requirements.txt` | Python dependencies | **Reproducible environment** |
| `performance/jmx/*.jmx` | JMeter test plan | **Load testing** |
| `performance/Findings.md` | NFR pass/fail report | **Performance compliance** |
