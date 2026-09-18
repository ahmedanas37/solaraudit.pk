import sys
from playwright.sync_api import sync_playwright

CHROMIUM_PATH = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"
HTML_URL = "file:///c:/Users/Anas/Documents/antigravity/excited-davinci/index.html"
SCREENSHOT_PATH = r"C:\Users\Anas\.gemini\antigravity\brain\bafcd24f-3ad9-405d-801f-292418080847\verified_ui.png"

def run_browser_verification():
    print(">>> Starting Playwright with Chromium:", CHROMIUM_PATH)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print(">>> Navigating to index.html...")
        page.goto(HTML_URL)
        page.wait_for_load_state("networkidle")

        # 1. Check initial irradiance pill
        psh_el = page.locator("#cityIrradiancePsh")
        print("Initial PSH:", psh_el.inner_text())
        assert "5.4" in psh_el.inner_text(), "Initial PSH should be 5.4 for Karachi"

        # 2. Test City Selection: Switch to Quetta
        print(">>> Switching city to Quetta...")
        page.select_option("#citySelect", "quetta")
        page.wait_for_timeout(300)
        print("Quetta PSH:", psh_el.inner_text())
        assert "5.8" in psh_el.inner_text(), "Quetta PSH should be 5.8"
        climate_el = page.locator("#cityIrradianceClimate")
        print("Quetta Climate:", climate_el.inner_text())
        assert "Highest solar potential" in climate_el.inner_text()

        # 3. Test Shortcut to Appliances
        print(">>> Testing shortcut: Estimate by appliances...")
        page.click("#shortcutToApplianceBtn")
        page.wait_for_timeout(300)
        assert page.is_visible("#applianceInputSection"), "Appliance section should be visible"
        assert not page.is_visible("#billInputSection"), "Bill section should be hidden"

        # 4. Test AC Hours & Increments
        print(">>> Testing appliance hours & increments...")
        hours_12_btn = page.locator("#hoursGroup_ac15 button[data-hours='12']")
        hours_12_btn.click()
        page.wait_for_timeout(200)

        # Check breakdown summary
        units_display = page.locator("#applianceTotalUnitsDisplay").inner_text()
        bill_display = page.locator("#applianceTotalBillDisplay").inner_text()
        dominant_display = page.locator("#applianceDominantText").inner_text()
        print(f"Appliance Breakdown: {units_display} | {bill_display} | Top: {dominant_display}")
        assert "Units" in units_display
        assert "Rs." in bill_display

        # 5. Test Shortcut Back to Bill
        print(">>> Testing shortcut: Back to Bill...")
        page.click("#shortcutBackToBillBtn")
        page.wait_for_timeout(300)
        assert page.is_visible("#billInputSection"), "Bill section should be visible"

        # 6. Take full-page screenshot
        print(f">>> Capturing screenshot to {SCREENSHOT_PATH}...")
        page.screenshot(path=SCREENSHOT_PATH, full_page=True)

        browser.close()

    assert len(console_errors) == 0, f"Console errors detected: {console_errors}"
    print("====================================================")
    print("ALL BROWSER INTERACTION VERIFICATIONS PASSED 100%!")
    print("====================================================")

if __name__ == "__main__":
    run_browser_verification()
