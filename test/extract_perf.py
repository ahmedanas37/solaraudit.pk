import asyncio
from playwright.async_api import async_playwright

CHROMIUM_EXE = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"
USER_DATA_DIR = r"C:\Users\Anas\AppData\Local\Chromium\User Data"

async def extract_perf_details():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROMIUM_EXE,
            headless=True,
            viewport={"width": 1440, "height": 1100},
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()

        # Performance Analytics
        perf_url = "https://search.google.com/search-console/performance/search-analytics?resource_id=https://solaraudit.online/"
        await page.goto(perf_url, wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # Extract Queries
        print("\n--- TOP SEARCH QUERIES ---")
        queries = await page.evaluate("""() => {
            const rows = Array.from(document.querySelectorAll('table tbody tr'));
            return rows.map(r => {
                const cells = Array.from(r.querySelectorAll('td')).map(c => c.innerText.trim());
                return cells;
            });
        }""")
        for q in queries[:10]:
            print(q)

        # Click PAGES tab
        print("\n--- TOP PAGES ---")
        pages_tab = page.locator("div[role='tab']:has-text('PAGES')")
        if await pages_tab.count() > 0:
            await pages_tab.first.click()
            await asyncio.sleep(2)
            page_rows = await page.evaluate("""() => {
                const rows = Array.from(document.querySelectorAll('table tbody tr'));
                return rows.map(r => {
                    const cells = Array.from(r.querySelectorAll('td')).map(c => c.innerText.trim());
                    return cells;
                });
            }""")
            for pr in page_rows[:10]:
                print(pr)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(extract_perf_details())
