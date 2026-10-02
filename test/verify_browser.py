import sys
from playwright.sync_api import sync_playwright

CHROMIUM_PATH = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"
HTML_URL = "file:///c:/Users/Anas/Documents/antigravity/excited-davinci/index.html"
SCREENSHOT_DESKTOP = r"C:\Users\Anas\.gemini\antigravity\brain\bafcd24f-3ad9-405d-801f-292418080847\verified_ui_desktop.png"
SCREENSHOT_MOBILE = r"C:\Users\Anas\.gemini\antigravity\brain\bafcd24f-3ad9-405d-801f-292418080847\verified_ui_mobile.png"

def run_browser_verification():
    print(">>> Starting Playwright with Chromium:", CHROMIUM_PATH)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=True)

        # ─────────────────────────────────────────────────────────
        # Part A: Desktop Viewport (1280 x 900)
        # ─────────────────────────────────────────────────────────
        print("\n--- Testing Desktop Viewport (1280x900) ---")
        page_desk = browser.new_page(viewport={"width": 1280, "height": 900})
        console_errors = []
        page_desk.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("Navigating to index.html...")
        page_desk.goto(HTML_URL)
        page_desk.wait_for_load_state("networkidle")

        # 1. Check initial irradiance pill
        psh_el = page_desk.locator("#cityIrradiancePsh")
        print("Initial PSH:", psh_el.inner_text())
        assert "5.4" in psh_el.inner_text(), "Initial PSH should be 5.4 for Karachi"

        # 2. Test City Selection: Switch to Quetta
        print("Switching city to Quetta...")
        page_desk.select_option("#citySelect", "quetta")
        page_desk.wait_for_timeout(200)
        assert "5.8" in psh_el.inner_text(), "Quetta PSH should be 5.8"

        # 3. Test Shortcut to Appliances
        print("Testing shortcut: Estimate by appliances...")
        page_desk.click("#shortcutToApplianceBtn")
        page_desk.wait_for_timeout(200)
        assert page_desk.is_visible("#applianceInputSection"), "Appliance section should be visible"
        assert not page_desk.is_visible("#billInputSection"), "Bill section should be hidden"

        # 4. Check Appliance Button Touch Targets (min 44px)
        dec_btn = page_desk.locator("#dec_ac15")
        box = dec_btn.bounding_box()
        print(f"Appliance Button Touch Target: {box['width']}px x {box['height']}px")
        assert box['width'] >= 44 and box['height'] >= 44, f"Touch target too small: {box}"

        # 5. Test AC Hours & Increments and verify touch target persists after click
        hours_12_btn = page_desk.locator("#hoursGroup_ac15 button[data-hours='12']")
        hours_12_btn.click()
        page_desk.wait_for_timeout(150)
        box_hours = hours_12_btn.bounding_box()
        print(f"Hours Button Touch Target after click: {box_hours['width']}px x {box_hours['height']}px")
        assert box_hours['width'] >= 44 and box_hours['height'] >= 44, f"Hours button touch target collapsed: {box_hours}"

        # 6. Test Structure Type Toggle (Standard L2 vs Elevated L3 Pergola)
        print("Testing Structure Type Toggle...")
        elevated_btn = page_desk.locator("#structElevatedBtn")
        elevated_btn.click()
        page_desk.wait_for_timeout(150)
        box_elevated = elevated_btn.bounding_box()
        assert box_elevated['height'] >= 44, f"Elevated button height < 44px: {box_elevated}"

        standard_btn = page_desk.locator("#structStandardBtn")
        standard_btn.click()
        page_desk.wait_for_timeout(150)

        # 7. Test Meter Phase Toggle (3-Phase vs Single-Phase)
        print("Testing Meter Phase Toggle...")
        single_phase_btn = page_desk.locator("#meterSinglePhaseBtn")
        single_phase_btn.click()
        page_desk.wait_for_timeout(150)
        assert page_desk.is_visible("#singlePhaseNotice"), "Single phase notice should appear"
        three_phase_btn = page_desk.locator("#meterThreePhaseBtn")
        three_phase_btn.click()
        page_desk.wait_for_timeout(150)
        assert not page_desk.is_visible("#singlePhaseNotice"), "Single phase notice should be hidden"

        # 8. Test Night AC Toggle Switch & Chemistry
        print("Testing Night AC Toggle & Battery Chemistry...")
        tubular_btn = page_desk.locator("#batteryTypeTubular")
        tubular_btn.click()
        page_desk.wait_for_timeout(150)
        box_tubular = tubular_btn.bounding_box()
        assert box_tubular['height'] >= 44, f"Tubular button height < 44px: {box_tubular}"
        
        lithium_btn = page_desk.locator("#batteryTypeLithium")
        lithium_btn.click()
        page_desk.wait_for_timeout(150)

        # Toggle Night AC switch off (On-grid mode)
        page_desk.click("label:has(#nightAcToggle)")
        page_desk.wait_for_timeout(200)
        assert "On-Grid" in page_desk.locator("#outBatterySpec").inner_text()
        assert "On-Grid" in page_desk.locator("#nbNote").inner_text()

        # Toggle Night AC switch back on (Hybrid mode)
        page_desk.click("label:has(#nightAcToggle)")
        page_desk.wait_for_timeout(200)
        assert "LiFePO4" in page_desk.locator("#outBatterySpec").inner_text()
        assert "Hybrid" in page_desk.locator("#nbNote").inner_text()

        # Verify Net-Billing UI Breakdown Elements
        assert page_desk.is_visible("#nbSelfConsumption"), "Net-Billing self-consumption element missing"
        assert page_desk.is_visible("#nbExportCredit"), "Net-Billing export credit element missing"
        assert page_desk.is_visible("#nbPostBill"), "Net-Billing post-solar bill element missing"
        print("2026 Net-Billing Readout:", page_desk.locator("#nbSelfConsumption").inner_text(), "|", page_desk.locator("#nbExportCredit").inner_text())

        # 9. Test Shortcut Back to Bill
        page_desk.click("#shortcutBackToBillBtn")
        page_desk.wait_for_timeout(200)
        assert page_desk.is_visible("#billInputSection"), "Bill section should be visible"

        # 10. Test Quick Bill Preset Chip
        print("Testing quick bill preset chips...")
        preset_85k_btn = page_desk.locator("button[data-preset-val='85000']")
        preset_85k_btn.click()
        page_desk.wait_for_timeout(200)
        assert "85,000" in page_desk.locator("#heroPreBill").inner_text()
        assert page_desk.locator("#billInputNumber").input_value() == "85000"

        # 11. Test Direct Editable Number Input
        print("Testing direct editable bill input...")
        page_desk.fill("#billInputNumber", "60000")
        page_desk.wait_for_timeout(200)
        assert "60,000" in page_desk.locator("#heroPreBill").inner_text()
        assert "60,000" in page_desk.locator("#billValueDisplay").inner_text()

        # 12. Verify Hero Solar Verdict Elements
        assert page_desk.is_visible("#heroPreBill"), "Hero Pre-Bill missing"
        assert page_desk.is_visible("#heroPostBill"), "Hero Post-Bill missing"
        assert page_desk.is_visible("#heroSavingsBar"), "Hero Savings Bar missing"
        print("Hero Solar Verdict:", page_desk.locator("#heroPreBill").inner_text(), "->", page_desk.locator("#heroPostBill").inner_text(), "| Saved:", page_desk.locator("#heroNetPocket").inner_text())

        # 7. Test Quote Validator Interaction
        print("Testing Contractor Quote Validator...")
        page_desk.fill("#quoteKwInput", "6")
        page_desk.fill("#quotePriceInput", "750000")
        page_desk.select_option("#quoteSystemType", "hybrid")
        page_desk.wait_for_timeout(200)
        assert page_desk.is_visible("#quoteValidatorResult"), "Validator result should appear"
        val_badge = page_desk.locator("#quoteResultBadge").inner_text()
        print("Quote Validator Status:", val_badge.encode('ascii', 'replace').decode('ascii'))
        assert "Fair Market Pricing" in val_badge

        # 8. Check that Sticky Mobile Bar is hidden on Desktop
        sticky_mobile = page_desk.locator("#stickyMobileSummary")
        assert not sticky_mobile.is_visible(), "Sticky mobile summary bar should be hidden on desktop (lg:hidden)"

        # 9. Test dynamic lazy-loading PDF trigger
        print("Testing dynamic jsPDF lazy loading on button click...")
        has_jspdf_before = page_desk.evaluate("() => typeof window.jspdf !== 'undefined'")
        assert not has_jspdf_before, "jsPDF should NOT be loaded initially in head!"
        
        # Click PDF button (with mock alert so it doesn't block)
        page_desk.evaluate("() => { window.alert = () => {}; }")
        page_desk.click("#downloadPdfBtn")
        page_desk.wait_for_timeout(1000) # give dynamic script a moment to load
        has_jspdf_after = page_desk.evaluate("() => typeof window.jspdf !== 'undefined'")
        print("jsPDF loaded dynamically on click:", has_jspdf_after)
        assert has_jspdf_after, "jsPDF must be dynamically loaded when user clicks Download PDF!"

        # Scroll to top and screenshot Desktop
        page_desk.evaluate("() => window.scrollTo(0, 0)")
        page_desk.wait_for_timeout(200)
        page_desk.screenshot(path=r"C:\Users\Anas\.gemini\antigravity\brain\bafcd24f-3ad9-405d-801f-292418080847\desktop_viewport.png")
        page_desk.screenshot(path=SCREENSHOT_DESKTOP, full_page=True)
        page_desk.close()

        # ─────────────────────────────────────────────────────────
        # Part B: Mobile Viewport (390 x 844 - iPhone / Mobile)
        # ─────────────────────────────────────────────────────────
        print("\n--- Testing Mobile Viewport (390x844) ---")
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page_mob.goto(HTML_URL)
        page_mob.wait_for_load_state("networkidle")

        # 1. Sticky Mobile Summary Bar MUST be visible
        sticky_bar = page_mob.locator("#stickyMobileSummary")
        assert sticky_bar.is_visible(), "Sticky mobile summary bar MUST be visible on mobile viewport (<1024px)!"

        initial_mob_kw = page_mob.locator("#mobileStickyKw").inner_text()
        initial_mob_savings = page_mob.locator("#mobileStickySavings").inner_text()
        print(f"Mobile Sticky Summary Live Readout: {initial_mob_kw} | {initial_mob_savings}")
        assert "kW" in initial_mob_kw
        assert "Rs." in initial_mob_savings

        # 2. Test Slider interaction updating mobile summary live
        print("Dragging bill slider on mobile...")
        page_mob.evaluate("""() => {
            const slider = document.getElementById("billSlider");
            slider.value = 120000;
            slider.dispatchEvent(new Event("input"));
            slider.dispatchEvent(new Event("change"));
        }""")
        page_mob.wait_for_timeout(200)

        updated_mob_kw = page_mob.locator("#mobileStickyKw").inner_text()
        updated_mob_savings = page_mob.locator("#mobileStickySavings").inner_text()
        print(f"Updated Mobile Live Readout: {updated_mob_kw} | {updated_mob_savings}")
        assert updated_mob_kw != initial_mob_kw, "Mobile sticky bar did not update upon slider change!"

        # 3. Test View Specs button click
        print("Testing 'View Specs' mobile button click...")
        page_mob.click("#mobileViewBreakdownBtn")
        page_mob.wait_for_timeout(300)

        # Screenshot Mobile
        page_mob.screenshot(path=SCREENSHOT_MOBILE)
        page_mob.close()

        browser.close()

    assert len(console_errors) == 0, f"Console errors detected: {console_errors}"
    print("\n====================================================")
    print("ALL DESKTOP & MOBILE BROWSER VERIFICATIONS PASSED 100%!")
    print("====================================================")

if __name__ == "__main__":
    run_browser_verification()
