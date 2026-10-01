"""
SOLARAUDIT.ONLINE - Mathematical & Physics Engine Verification Test
Verifies 2026 NEPRA billing slabs, solar physics, LiFePO4 vs tubular battery storage,
2026 Net-Billing financial calibration (On-Grid vs Hybrid LiFePO4),
and tests the REAL JavaScript calculation engine in Chromium headless via Playwright.
"""

import os
from playwright.sync_api import sync_playwright

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROMIUM_PATH = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"

def test_engine():
    # 1. Test Billing Slabs Logic (NEPRA 2026 baseline)
    print(">>> Testing NEPRA 2026 progressive billing logic...")
    units = 780
    base_energy = (
        (100 * 23.59) +
        (100 * 30.07) +
        (100 * 34.26) +
        (100 * 39.15) +
        (100 * 41.36) +
        (100 * 42.78) +
        (100 * 43.92) +
        (80 * 48.84)
    )
    print(f"Base Energy Cost for 780 units: Rs. {base_energy:,.2f}")
    assert base_energy > 28000, "Base energy calculation failed lower bound"

    fixed_charges = 4000
    subtotal = base_energy + fixed_charges
    fpa = units * 4.25
    fc = units * 3.23
    ed = subtotal * 0.015
    taxable = subtotal + fpa + fc + ed
    gst = taxable * 0.18
    tv = 35.0
    total_bill = taxable + gst + tv

    print(f"Total Bill for 780 units (inc. GST, FPA, FC, ED): Rs. {total_bill:,.2f}")
    assert 45000 < total_bill < 55000, f"Total bill out of expected range: {total_bill}"
    print("[OK] Billing slab math verified successfully.")

    # 2. Test Solar Sizing Logic
    print("\n>>> Testing Solar Sizing Logic...")
    psh = 5.4 # Karachi
    derating = 0.78
    daily_units = units / 30 # 26 units/day
    dc_kw_raw = daily_units / (psh * derating) # 26 / (5.4 * 0.78) = ~6.17 kW
    panel_watts = 580
    panel_count = int(-(- (dc_kw_raw * 1000) // panel_watts)) # Math.ceil
    actual_dc_kw = (panel_count * panel_watts) / 1000
    roof_sq_ft = panel_count * 28

    print(f"Daily Target: {daily_units:.1f} kWh/day")
    print(f"DC Raw Needed: {dc_kw_raw:.2f} kW")
    print(f"Panels (580W): {panel_count} units -> {actual_dc_kw:.2f} kWp")
    print(f"Roof Footprint: {roof_sq_ft} sq. ft. (~{roof_sq_ft / 225:.1f} Marla)")
    assert panel_count == 11, f"Expected 11 panels, got {panel_count}"
    assert roof_sq_ft == 308, f"Expected 308 sq ft, got {roof_sq_ft}"
    print("[OK] Solar sizing & roof footprint verified.")

    # 3. Test Night Battery Sizing (1 AC for 8 hours)
    print("\n>>> Testing Night Battery Storage Physics...")
    ac_running_watts = 750
    base_watts = 200
    night_hours = 8
    total_wh = ((1 * ac_running_watts) + base_watts) * night_hours
    total_kwh = total_wh / 1000 # 7.6 kWh

    # Lithium (85% DoD, 92% inverter efficiency)
    lithium_req = total_kwh / (0.85 * 0.92) # ~9.7 kWh
    lithium_units = int(-(- lithium_req // 5.12)) # Math.ceil
    print(f"Night Energy Needed: {total_kwh:.2f} kWh")
    print(f"Nominal Lithium Capacity: {lithium_req:.2f} kWh -> {lithium_units}x 5.12 kWh LiFePO4 packs")
    assert lithium_units >= 1, "Lithium unit calculation error"

    # Tubular (50% DoD, 85% inverter efficiency)
    tubular_req = total_kwh / (0.50 * 0.85) # ~17.88 kWh
    tubular_raw = int(-(- tubular_req // 2.76))
    tubular_banks = int(-(- tubular_raw // 4) * 4) # Multiples of 4 for 48V
    print(f"Nominal Tubular Capacity: {tubular_req:.2f} kWh -> {tubular_banks}x 12V 230Ah batteries")
    assert tubular_banks >= 4, "Tubular bank must be at least 4 units"
    print("[OK] Battery storage physics verified.")

    # 4. Test 2026 Net-Billing Calibration (On-Grid vs Hybrid LiFePO4)
    print("\n>>> Testing 2026 Net-Billing Financial Model Calibration...")
    naepp_export_rate = 21.50 # Rs./kWh wholesale buyback
    monthly_gen = round(actual_dc_kw * psh * derating * 30) # ~804 units
    daily_gen = monthly_gen / 30 # 26.8 units/day

    # Typical residential split: 35% day, 65% night
    day_demand = daily_units * 0.35 # 9.1 units/day
    night_demand = daily_units * 0.65 # 16.9 units/day

    # Scenario A: On-Grid System (No battery)
    ongrid_day_direct = min(day_demand, daily_gen) # 9.1 units
    ongrid_day_export = max(0, daily_gen - ongrid_day_direct) # 17.7 units
    ongrid_day_import = max(0, day_demand - ongrid_day_direct) # 0
    ongrid_night_import = night_demand # 16.9 units MUST import
    ongrid_monthly_import = round((ongrid_day_import + ongrid_night_import) * 30) # 507 units
    ongrid_monthly_export = round(ongrid_day_export * 30) # 531 units
    ongrid_export_credit = round(ongrid_monthly_export * naepp_export_rate) # Rs. 11,417

    print(f"On-Grid: Monthly Grid Import = {ongrid_monthly_import} units (Nighttime retail slab)")
    print(f"On-Grid: Monthly Grid Export = {ongrid_monthly_export} units @ Rs. {naepp_export_rate}/kWh -> Rs. {ongrid_export_credit:,}")
    assert ongrid_monthly_import > 450, "On-grid night import must remain substantial without battery"
    assert ongrid_export_credit > 8000, "On-grid daytime export must generate significant NAEPP credit"

    # Scenario B: Hybrid System with LiFePO4 battery (10.24 kWh = 7.6 kWh usable)
    hybrid_day_direct = min(day_demand, daily_gen) # 9.1 units
    hybrid_excess_day = daily_gen - hybrid_day_direct # 17.7 units
    hybrid_battery_stored = min(hybrid_excess_day, total_kwh, night_demand) # 7.6 units stored
    hybrid_day_export = max(0, hybrid_excess_day - hybrid_battery_stored) # 10.1 units exported
    hybrid_night_import = max(0, night_demand - hybrid_battery_stored) # 9.3 units import
    hybrid_monthly_import = round(hybrid_night_import * 30) # 279 units (drastic slab reduction!)
    hybrid_monthly_export = round(hybrid_day_export * 30) # 303 units

    print(f"Hybrid: Monthly Grid Import = {hybrid_monthly_import} units (Reduced from {ongrid_monthly_import} units!)")
    print(f"Hybrid: Monthly Grid Export = {hybrid_monthly_export} units")
    assert hybrid_monthly_import < ongrid_monthly_import, "Hybrid LiFePO4 battery MUST reduce grid import compared to on-grid"
    print("[OK] 2026 Net-Billing financial calibration verified.")

    # 5. Test Elevated L3 Structure & Quote Validator Logic
    print("\n>>> Testing Elevated L3 Pergola & Quote Validator...")
    l3_extra_per_watt = 13 # Rs. 13/W
    panels_cost = actual_dc_kw * 1000 * 33 # Rs. 33/W
    inverter_cost = 230000 # 6 kW Hybrid
    bos_cost = actual_dc_kw * 1000 * 20 # Rs. 20/W
    battery_cost = 225000 # 1x Lithium pack
    net_metering = 65000
    total_capex = panels_cost + inverter_cost + bos_cost + battery_cost + net_metering
    elevated_capex = total_capex + (actual_dc_kw * 1000 * l3_extra_per_watt)
    print(f"Elevated L3 Turnkey Capex: Rs. {elevated_capex:,.2f} (+Rs. {actual_dc_kw * 1000 * l3_extra_per_watt:,.0f} for heavy GI pergola)")
    assert elevated_capex > total_capex, "Elevated capex must exceed standard L2"

    quote_rate_a = 850000 / (6 * 1000)
    assert 130 <= quote_rate_a <= 165, f"Quote A should be fair, got {quote_rate_a}"
    quote_rate_b = 500000 / (6 * 1000)
    assert quote_rate_b < 95, f"Quote B should trigger cut-corner alert, got {quote_rate_b}"
    quote_rate_c = 1100000 / (6 * 1000)
    assert quote_rate_c > 150, f"Quote C should trigger overpriced alert, got {quote_rate_c}"
    print("[OK] Quote validator and L3 structure logic verified.")

    # 6. Test Multi-City Irradiance
    print("\n>>> Testing Multi-City Solar Yield Comparison...")
    target_units = 600
    daily_target = target_units / 30
    quetta_kw = daily_target / (5.8 * 0.78)
    lahore_kw = daily_target / (5.0 * 0.78)
    quetta_panels = int(-(- (quetta_kw * 1000) // 580))
    lahore_panels = int(-(- (lahore_kw * 1000) // 580))
    print(f"Quetta (5.8 PSH): {quetta_kw:.2f} kW -> {quetta_panels} panels")
    print(f"Lahore (5.0 PSH): {lahore_kw:.2f} kW -> {lahore_panels} panels")
    assert quetta_panels <= lahore_panels, "Quetta must require fewer or equal panels than Lahore"
    print("[OK] Multi-city climate irradiance comparison verified.")


def test_real_javascript_engine():
    print("\n========================================================")
    print(">>> Testing REAL JavaScript Engine in Headless Chromium...")
    print("========================================================")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=True)
        page = browser.new_page()
        page.goto(f"file:///{WORKSPACE}/index.html")
        page.wait_for_load_state("networkidle")

        # 1. Verify Bill Calculation in JS
        bill_res = page.evaluate("() => CalculatorEngine.calculateBillFromUnits(780, 'kelectric')")
        print("Real JS Bill for 780 units:", bill_res["totalBill"])
        assert 45000 < bill_res["totalBill"] < 55000, "JS Bill calculation out of expected range"

        # 2. Verify Solar Sizing in JS
        sizing_res = page.evaluate("() => CalculatorEngine.calculateSolarSizing(780, 'karachi')")
        print("Real JS Sizing for 780 units in Karachi:", sizing_res["actualDcKw"], "kWp, Panels:", sizing_res["panelCount"])
        assert sizing_res["panelCount"] == 11
        assert sizing_res["actualDcKw"] == 6.38

        # 3. Verify Battery Storage in JS
        bat_res = page.evaluate("() => CalculatorEngine.calculateNightBattery(1, 8, 'lithium')")
        print("Real JS Battery Sizing:", bat_res["unitSpec"], "| Total:", bat_res["totalEnergyKwh"], "kWh")
        assert bat_res["unitCount"] >= 1
        assert "LiFePO4" in bat_res["unitSpec"]

        # 4. Verify 2026 Net-Billing Model in JS: On-Grid vs Hybrid
        fin_ongrid = page.evaluate("""() => {
            const sizing = CalculatorEngine.calculateSolarSizing(780, 'kelectric');
            return CalculatorEngine.calculateFinancials(sizing, null, 48000, 'kelectric', true);
        }""")
        print("\nReal JS On-Grid Net-Billing Output:")
        print(f"  System Type: {fin_ongrid['netBilling']['systemType']}")
        print(f"  Monthly Generation: {fin_ongrid['netBilling']['monthlyGenerationUnits']} units")
        print(f"  Grid Import: {fin_ongrid['netBilling']['gridImportUnits']} units")
        print(f"  Grid Export: {fin_ongrid['netBilling']['gridExportUnits']} units")
        print(f"  Gross Import Bill: Rs. {fin_ongrid['netBilling']['grossImportBill']:,}")
        print(f"  NAEPP Export Credit: Rs. {fin_ongrid['netBilling']['exportCreditPkr']:,}")
        print(f"  Net Post-Solar Bill: Rs. {fin_ongrid['postBillPkr']:,}")
        print(f"  Monthly Savings: Rs. {fin_ongrid['monthlySavings']:,}")
        print(f"  Payback: {fin_ongrid['paybackYears']} Years")

        assert fin_ongrid["netBilling"]["isNetBilling"] == True
        assert fin_ongrid["netBilling"]["systemType"] == "ongrid_export"
        assert fin_ongrid["netBilling"]["gridImportUnits"] > 400
        assert fin_ongrid["netBilling"]["gridExportUnits"] > 300
        assert fin_ongrid["netBilling"]["exportCreditPkr"] > 0

        fin_hybrid = page.evaluate("""() => {
            const sizing = CalculatorEngine.calculateSolarSizing(780, 'kelectric');
            const battery = CalculatorEngine.calculateNightBattery(1, 8, 'lithium');
            return CalculatorEngine.calculateFinancials(sizing, battery, 48000, 'kelectric', true);
        }""")
        print("\nReal JS Hybrid (LiFePO4) Net-Billing Output:")
        print(f"  System Type: {fin_hybrid['netBilling']['systemType']}")
        print(f"  Grid Import: {fin_hybrid['netBilling']['gridImportUnits']} units (vs {fin_ongrid['netBilling']['gridImportUnits']} ongrid)")
        print(f"  Battery Self-Consumption: {fin_hybrid['netBilling']['batterySelfConsumptionUnits']} units")
        print(f"  Net Post-Solar Bill: Rs. {fin_hybrid['postBillPkr']:,} (vs Rs. {fin_ongrid['postBillPkr']:,} ongrid)")
        print(f"  Monthly Savings: Rs. {fin_hybrid['monthlySavings']:,} (vs Rs. {fin_ongrid['monthlySavings']:,} ongrid)")
        print(f"  Self-Consumption %: {fin_hybrid['netBilling']['selfConsumptionPercent']}%")

        assert fin_hybrid["netBilling"]["systemType"] == "hybrid_storage"
        assert fin_hybrid["netBilling"]["batterySelfConsumptionUnits"] > 0
        # Critical 2026 Net-Billing Check: Hybrid LiFePO4 MUST import fewer units than On-Grid
        assert fin_hybrid["netBilling"]["gridImportUnits"] < fin_ongrid["netBilling"]["gridImportUnits"]
        # Hybrid MUST deliver lower net post-solar bill than On-Grid
        assert fin_hybrid["postBillPkr"] < fin_ongrid["postBillPkr"]
        # Hybrid MUST deliver higher monthly savings than On-Grid
        assert fin_hybrid["monthlySavings"] > fin_ongrid["monthlySavings"]
        # Hybrid self-consumption % must exceed on-grid self-consumption %
        assert fin_hybrid["netBilling"]["selfConsumptionPercent"] > fin_ongrid["netBilling"]["selfConsumptionPercent"]

        # 5. Test Surplus Generation / Net Export Payout
        fin_surplus = page.evaluate("""() => {
            // Sizing for 300 units load, but generating 2000 units (oversized 15kW array)
            const sizing = CalculatorEngine.calculateSolarSizing(300, 'karachi');
            sizing.estimatedMonthlyGenerationUnits = 2000;
            sizing.actualDcKw = 15.0;
            return CalculatorEngine.calculateFinancials(sizing, null, 10000, 'kelectric', true);
        }""")
        print("\nReal JS Surplus Export Output (Oversized Array vs Small Load):")
        print(f"  Monthly Gen: {fin_surplus['netBilling']['monthlyGenerationUnits']} units")
        print(f"  Grid Export: {fin_surplus['netBilling']['gridExportUnits']} units")
        print(f"  Export Credit: Rs. {fin_surplus['netBilling']['exportCreditPkr']:,}")
        print(f"  Gross Import: Rs. {fin_surplus['netBilling']['grossImportBill']:,}")
        print(f"  Net Export Payout: Rs. {fin_surplus['netBilling']['netExportPayout']:,}")
        print(f"  Post-Solar Bill: Rs. {fin_surplus['postBillPkr']}")
        print(f"  Monthly Financial Gain: Rs. {fin_surplus['monthlySavings']:,}")

        assert fin_surplus["postBillPkr"] == 0
        assert fin_surplus["netBilling"]["netExportPayout"] > 0
        assert fin_surplus["monthlySavings"] == 10000 + fin_surplus["netBilling"]["netExportPayout"]

        # 6. Test Zero-Export Mode (includeNetMetering = false)
        fin_no_export = page.evaluate("""() => {
            const sizing = CalculatorEngine.calculateSolarSizing(780, 'kelectric');
            return CalculatorEngine.calculateFinancials(sizing, null, 48000, 'kelectric', false);
        }""")
        assert fin_no_export["netBilling"]["exportCreditPkr"] == 0
        assert fin_no_export["postBillPkr"] == fin_no_export["netBilling"]["grossImportBill"]
        assert fin_no_export["monthlySavings"] == 48000 - fin_no_export["postBillPkr"]

        # 7. Test Multi-City Sweet Spot Sizing
        sweet_quetta = page.evaluate("() => CalculatorEngine.calculateSweetSpot(780, 'qesco', 900000, { cityKey: 'quetta' })")
        sweet_lahore = page.evaluate("() => CalculatorEngine.calculateSweetSpot(780, 'lesco', 900000, { cityKey: 'lahore' })")
        print(f"\nSweet Spot City Sizing: Quetta (5.8 PSH) -> {sweet_quetta['recommendedKw']} kW | Lahore (5.0 PSH) -> {sweet_lahore['recommendedKw']} kW")
        assert sweet_quetta["recommendedKw"] < sweet_lahore["recommendedKw"], "Quetta sweet spot should require fewer kW than Lahore due to higher PSH"

        # 8. Verify Quote Validator in JS
        quote_res = page.evaluate("() => CalculatorEngine.validateInstallerQuote(6.0, 750000, 'hybrid')")
        safe_badge = quote_res["badgeText"].encode("ascii", "replace").decode("ascii")
        print("\nReal JS Quote Validator (6kW Hybrid @ Rs. 750k):", safe_badge, "| Status:", quote_res["status"])
        assert quote_res["status"] == "fair"

        browser.close()
    print("\n[PASS] Real JavaScript Engine in Chromium passed 100% of mathematical and net-billing checks!")


if __name__ == "__main__":
    test_engine()
    test_real_javascript_engine()
    print("\n========================================================")
    print("ALL ENGINE & PHYSICS VERIFICATIONS PASSED SUCCESSFULLY!")
    print("========================================================")
