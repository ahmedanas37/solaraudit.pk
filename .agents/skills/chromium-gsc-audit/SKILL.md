---
name: chromium-gsc-audit
description: >-
  Use this skill when auditing or extracting performance metrics, top search queries,
  page indexing status, or sitemap health from Google Search Console using the user's
  authenticated Chromium browser profile.
---

# Chromium Google Search Console Audit

This runbook describes how to safely inspect Google Search Console using the user's existing logged-in Chromium browser profile without needing stored passwords or API credentials.

## Prerequisites & Critical Constraints

1. **Mandatory Chromium Executable**: Always use `C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe`.
2. **Prohibited Google Chrome**: Never execute or connect to `C:\Program Files\Google\Chrome\Application\chrome.exe`.
3. **No Screen Recording**: Video recording is disabled. Only capture still PNG screenshots for visual verification.
4. **Persistent User Data**: Profile directory is located at `C:\Users\Anas\AppData\Local\Chromium\User Data`.

## Procedure

### Step 1: Verify Process Lock
Before launching persistent context, ensure no active Chromium process holds an exclusive lock on the user data folder:
```powershell
Get-Process | Where-Object { $_.Path -like "*Chromium*" }
```

### Step 2: Automation with Python Playwright
Launch Playwright using persistent context with `headless=True`:

```python
import asyncio
from playwright.async_api import async_playwright

CHROMIUM_EXE = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"
USER_DATA_DIR = r"C:\Users\Anas\AppData\Local\Chromium\User Data"

async def inspect_gsc():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROMIUM_EXE,
            headless=True,
            viewport={"width": 1400, "height": 1200},
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # Performance Analytics
        perf_url = "https://search.google.com/search-console/performance/search-analytics?resource_id=https://solaraudit.online/"
        await page.goto(perf_url, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        await page.evaluate("window.scrollTo(0, 800)")
        await page.screenshot(path="gsc_performance.png")
        
        # Page Indexing Report
        index_url = "https://search.google.com/search-console/index?resource_id=https://solaraudit.online/"
        await page.goto(index_url, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        await page.screenshot(path="gsc_indexing.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_gsc())
```

### Step 3: Viewport & Layout Handling
* Use viewport height of at least `1200px` or scroll `window.scrollTo(0, 800)` to bring GSC data tables into view.
* Navigation should use `wait_until="domcontentloaded"` rather than `networkidle` to avoid timeouts from streaming telemetry.
