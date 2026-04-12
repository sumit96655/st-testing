# SauceDemo Performance Test — Findings

## Test Configuration

| Parameter       | Value                       |
|-----------------|-----------------------------|
| Tool            | Apache JMeter 5.6.3         |
| Thread Count    | 20 concurrent users         |
| Ramp-Up Period  | 60 seconds                  |
| Test Duration   | 180 seconds (3 minutes)     |
| Target URL      | https://www.saucedemo.com   |

## NFR Compliance Summary

| NFR ID  | Requirement                                    | Threshold        | Measured Value | Status      |
|---------|------------------------------------------------|-------------------|----------------|-------------|
| NFR-01  | Page load time under normal load               | ≤ 3 seconds       | ___ ms         | ⬜ PENDING  |
| NFR-02  | System handles 20 concurrent users             | No errors > 1%    | ___% error     | ⬜ PENDING  |
| NFR-03  | Response time under peak load                  | ≤ 5 seconds (95th)| ___ ms         | ⬜ PENDING  |

> **Instructions**: Run the JMeter test, then fill in the "Measured Value" and "Status" columns with actual results.

## How to Run

### GUI Mode (for debugging)
```bash
jmeter -t performance/jmx/saucedemo_weekend_lab.jmx
```

### Non-GUI Mode (for actual test)
```bash
jmeter -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report/
```

### Generate HTML Report from Existing Results
```bash
jmeter -g performance/results/results.jtl -o performance/html_report/
```

## Sampler Breakdown

| Sampler                | Method | Path              | Expected Behavior              |
|------------------------|--------|--------------------|---------------------------------|
| 01 - GET Login Page    | GET    | `/`               | Returns 200, login HTML         |
| 02 - POST Login        | POST   | `/`               | Simulated login submission      |
| 03 - GET Products Page | GET    | `/inventory.html` | Returns 200, products HTML      |

## Notes

- SauceDemo is a **client-side rendered** JavaScript application. JMeter only measures HTTP response times for the raw HTML/JS files, not the full client-side rendering time.
- The POST login sampler simulates form submission but SauceDemo's authentication is handled entirely in JavaScript, so this measures server response time only.
- For true end-to-end performance testing of a JS-rendered app, a browser-based tool (e.g., Lighthouse, k6 browser) would be needed.

## Observations

_Fill in after running the test:_

1. **Average response time**: ___ ms
2. **95th percentile**: ___ ms
3. **99th percentile**: ___ ms
4. **Throughput**: ___ req/sec
5. **Error rate**: ____%
6. **Notable findings**: ___
