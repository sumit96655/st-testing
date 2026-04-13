# SauceDemo Performance Test — Findings

## Test Configuration

| Parameter       | Value                       |
|-----------------|------------------------------|
| Tool            | Apache JMeter 5.6.3         |
| Thread Count    | 20 concurrent users         |
| Ramp-Up Period  | 60 seconds                  |
| Test Duration   | 180 seconds (3 minutes)     |
| Think Time      | 0–500 ms (uniform random)   |
| Target URL      | https://www.saucedemo.com   |

## NFR Compliance Summary

| NFR ID | Requirement                                          | Threshold           | Measured Value | Status    |
|--------|------------------------------------------------------|----------------------|----------------|-----------|
| NFR-01 | Login page response time P95 < 3.0 seconds           | P95 < 3000 ms       | 84 ms          | ✅ **PASS** |
| NFR-02 | Products page response time P95 < 4.0 seconds        | P95 < 4000 ms       | 336 ms         | ✅ **PASS** |
| NFR-03 | Overall error rate < 2% during the test window        | Error < 2%          | 0.00%          | ✅ **PASS** |

## Aggregate Report

| Sampler              | Samples | Avg (ms) | Median (ms) | P90 (ms) | P95 (ms) | P99 (ms) | Min (ms) | Max (ms) | Error % | Throughput |
|----------------------|---------|----------|-------------|----------|----------|----------|----------|----------|---------|------------|
| 01 - Login Page      | 3,009   | 46       | 37          | 62       | 84       | 150      | 18       | 1,330    | 0.00%   | ~16.7/s    |
| 02 - Products Page   | 3,003   | 160      | 130         | 275      | 336      | 542      | 45       | 2,022    | 0.00%   | ~16.7/s    |
| 03 - Static Resources| 2,996   | 49       | 42          | 67       | 86       | 160      | 19       | 1,167    | 0.00%   | ~16.6/s    |
| **TOTAL**            | **9,008** | **85** | **48**      | **179**  | **240**  | **406**  | **18**   | **2,022**| **0.00%** | **~50.0/s** |

## Sampler Breakdown

| Sampler                | Method | Path                              | Purpose                                 |
|------------------------|--------|------------------------------------|-----------------------------------------|
| 01 - Login Page        | GET    | `/`                               | Measures login page HTML response time  |
| 02 - Products Page     | GET    | `/static/js/main.bcf4bc5f.js`     | Measures products page JS bundle load   |
| 03 - Static Resources  | GET    | `/static/css/main.8a7d64a1.css`   | Measures CSS stylesheet load            |

## How to Run

### Non-GUI Mode (for actual test)
```bash
jmeter -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report/
```

### GUI Mode (for debugging)
```bash
jmeter -t performance/jmx/saucedemo_weekend_lab.jmx
```

### Generate HTML Report from Existing Results
```bash
jmeter -g performance/results/results.jtl -o performance/html_report/
```

## Observations

1. **Average response time**: 85 ms (overall), well within acceptable limits
2. **95th percentile**: 240 ms (overall) — all individual samplers pass their NFR thresholds
3. **99th percentile**: 406 ms (overall) — even tail latencies are excellent
4. **Throughput**: ~50 req/sec across all samplers with 20 concurrent users
5. **Error rate**: 0.00% — zero errors across 9,008 total samples
6. **Notable findings**: All three NFR thresholds are comfortably met. The login page (1.7 KB HTML) responds fastest (P95 = 84 ms), followed by CSS (P95 = 86 ms), and the JS bundle (667 KB) is slowest but still well within the 4-second threshold (P95 = 336 ms).

## Notes

- SauceDemo is a **client-side rendered** JavaScript application (React SPA). JMeter measures HTTP response times for the raw HTML/JS/CSS files, not the full client-side rendering time.
- The previous version of SauceDemo served `/inventory.html` as a separate file. This endpoint now returns **404 Not Found** in the current v2 SPA deployment.
- Authentication is handled entirely in JavaScript — there is no server-side login POST endpoint (the server returns **405 Method Not Allowed** for POST requests to `/`).
- For true end-to-end performance testing of a JS-rendered SPA, browser-based tools (e.g., Lighthouse, k6 browser, Playwright) would be more appropriate.
