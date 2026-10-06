import asyncio
import os
from playwright.async_api import async_playwright

CHROMIUM_EXE = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"
USER_DATA_DIR = r"C:\Users\Anas\AppData\Local\Chromium\User Data"
OUTPUT_DIR = r"C:\Users\Anas\.gemini\antigravity\brain\bafcd24f-3ad9-405d-801f-292418080847"

async def audit_gsc():
    print(">>> Launching Chromium persistent context...")
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROMIUM_EXE,
            headless=True,
            viewport={"width": 1440, "height": 1100},
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()

        # 1. Performance Report
        print(">>> Navigating to GSC Performance Analytics...")
        perf_url = "https://search.google.com/search-console/performance/search-analytics?resource_id=https://solaraudit.online/"
        await page.goto(perf_url, wait_until="domcontentloaded")
        await asyncio.sleep(5)
        perf_shot = os.path.join(OUTPUT_DIR, "gsc_live_performance.png")
        await page.screenshot(path=perf_shot)
        print(f"Captured performance screenshot: {perf_shot}")

        # Scroll to see queries / pages table if present
        await page.evaluate("window.scrollTo(0, 700)")
        await asyncio.sleep(1)
        perf_table_shot = os.path.join(OUTPUT_DIR, "gsc_live_performance_table.png")
        await page.screenshot(path=perf_table_shot)
        print(f"Captured performance table screenshot: {perf_table_shot}")

        # 2. Page Indexing Report
        print(">>> Navigating to GSC Page Indexing Report...")
        index_url = "https://search.google.com/search-console/index?resource_id=https://solaraudit.online/"
        await page.goto(index_url, wait_until="domcontentloaded")
        await asyncio.sleep(5)
        index_shot = os.path.join(OUTPUT_DIR, "gsc_live_indexing.png")
        await page.screenshot(path=index_shot)
        print(f"Captured indexing screenshot: {index_shot}")

        await page.evaluate("window.scrollTo(0, 600)")
        await asyncio.sleep(1)
        index_reasons_shot = os.path.join(OUTPUT_DIR, "gsc_live_indexing_reasons.png")
        await page.screenshot(path=index_reasons_shot)
        print(f"Captured indexing reasons screenshot: {index_reasons_shot}")

        # 3. Sitemaps Report
        print(">>> Navigating to GSC Sitemaps Report...")
        sitemap_url = "https://search.google.com/search-console/sitemaps?resource_id=https://solaraudit.online/"
        await page.goto(sitemap_url, wait_until="domcontentloaded")
        await asyncio.sleep(4)
        sitemap_shot = os.path.join(OUTPUT_DIR, "gsc_live_sitemaps.png")
        await page.screenshot(path=sitemap_shot)
        print(f"Captured sitemaps screenshot: {sitemap_shot}")

        await browser.close()
    print(">>> GSC Audit completed successfully!")

if __name__ == "__main__":
    asyncio.run(audit_gsc())
