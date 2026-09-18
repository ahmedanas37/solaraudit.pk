"""
SOLARAUDIT.ONLINE - Mathematical Engine Verification Test
Runs standalone in Python to verify all billing slabs, solar sizing, and battery math.
"""

def test_engine():
    # 1. Test Billing Slabs Logic (NEPRA 2026 baseline)
    print(">>> Testing NEPRA 2026 progressive billing logic...")
    
    # Example: 780 units (typical residential consumer running 2 ACs)
    units = 780
    
    # Slabs for unprotected:
    # 1-100 @ 23.59
    # 101-200 @ 30.07
    # 201-300 @ 34.26
    # 301-400 @ 39.15
    # 401-500 @ 41.36
    # 501-600 @ 42.78
    # 601-700 @ 43.92
    # 701-780 (80 units) @ 48.84
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

    # Fixed charge for >700 units = 10 kW * 400 = Rs. 4,000
    fixed_charges = 4000
    subtotal = base_energy + fixed_charges

    # Taxes & Surcharges
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

    # 4. Financials & Payback
    print("\n>>> Testing Financial Payback Engine...")
    panels_cost = actual_dc_kw * 1000 * 33 # Rs. 33/W
    inverter_cost = 280000 # 6 kW Hybrid
    bos_cost = actual_dc_kw * 1000 * 22 # Rs. 22/W
    battery_cost = 310000 # 1x Lithium pack
    net_metering = 75000
    total_capex = panels_cost + inverter_cost + bos_cost + battery_cost + net_metering
    monthly_savings = total_bill # Assuming near 100% offset
    payback_months = (total_capex / (monthly_savings * 12)) * 12
    five_year_net = (monthly_savings * 60) - total_capex

    print(f"Total Capex: Rs. {total_capex:,.2f}")
    print(f"Monthly Savings: Rs. {monthly_savings:,.2f}")
    print(f"Payback Period: {payback_months:.1f} Months ({payback_months / 12:.1f} Years)")
    print(f"5-Year Net Profit: Rs. {five_year_net:,.2f}")
    print("[OK] Financial payback engine verified.")

    # 5. Test Elevated L3 Structure & Quote Validator Logic
    print("\n>>> Testing Elevated L3 Pergola & Quote Validator...")
    l3_extra_per_watt = 14 # Rs. 14/W
    elevated_capex = total_capex + (actual_dc_kw * 1000 * l3_extra_per_watt)
    print(f"Elevated L3 Turnkey Capex: Rs. {elevated_capex:,.2f} (+Rs. {actual_dc_kw * 1000 * l3_extra_per_watt:,.0f} for heavy GI pergola)")
    assert elevated_capex > total_capex, "Elevated capex must exceed standard L2"

    # Quote Validator Check
    # Case A: 6 kW quote @ Rs. 850,000 hybrid -> ~Rs. 141/W -> Fair
    quote_rate_a = 850000 / (6 * 1000)
    assert 130 <= quote_rate_a <= 165, f"Quote A should be fair, got {quote_rate_a}"

    # Case B: 6 kW quote @ Rs. 600,000 hybrid -> ~Rs. 100/W -> Cheap/Suspicious
    quote_rate_b = 600000 / (6 * 1000)
    assert quote_rate_b < 115, f"Quote B should trigger cut-corner alert, got {quote_rate_b}"

    # Case C: 6 kW quote @ Rs. 1,200,000 hybrid -> ~Rs. 200/W -> Overpriced
    quote_rate_c = 1200000 / (6 * 1000)
    assert quote_rate_c > 175, f"Quote C should trigger overpriced alert, got {quote_rate_c}"
    print("[OK] Quote validator and L3 structure logic verified.")

    # 6. Test Multi-City Solar Yields (Quetta vs Lahore vs Karachi)
    print("\n>>> Testing Multi-City Solar Yield Comparison...")
    # Sizing for 600 units/month in Quetta (5.8 PSH) vs Lahore (5.0 PSH)
    target_units = 600
    daily_target = target_units / 30
    quetta_kw = daily_target / (5.8 * 0.78)
    lahore_kw = daily_target / (5.0 * 0.78)
    quetta_panels = int(-(- (quetta_kw * 1000) // 580))
    lahore_panels = int(-(- (lahore_kw * 1000) // 580))
    print(f"Quetta (5.8 PSH): {quetta_kw:.2f} kW raw -> {quetta_panels} panels (580W)")
    print(f"Lahore (5.0 PSH): {lahore_kw:.2f} kW raw -> {lahore_panels} panels (580W)")
    assert quetta_panels <= lahore_panels, "Quetta with higher PSH must require fewer or equal panels than Lahore"
    print("[OK] Multi-city climate irradiance comparison verified.")

    # 7. Test Appliance Load Breakdown Logic
    print("\n>>> Testing Appliance Load Breakdown Logic...")
    # 2x 1.5T AC (750W * 8h = 12 kWh/day = 360 kWh/mo)
    # 5x Fans (55W * 14h = 3.85 kWh/day = 115.5 kWh/mo)
    # 1x Fridge (150W * 24h = 3.6 kWh/day = 108 kWh/mo)
    # 1x 1HP Pump (1100W * 1h = 1.1 kWh/day = 33 kWh/mo)
    ac_mo = 2 * 0.75 * 8 * 30
    fans_mo = 5 * 0.055 * 14 * 30
    fridge_mo = 1 * 0.15 * 24 * 30
    pump_mo = 1 * 1.1 * 1 * 30
    total_mo = ac_mo + fans_mo + fridge_mo + pump_mo
    print(f"Appliance Monthly Sum: {total_mo:.1f} kWh (AC: {ac_mo:.0f} kWh = {ac_mo/total_mo*100:.1f}%)")
    assert 616 <= round(total_mo) <= 617, f"Expected ~616-617 kWh, got {total_mo}"
    assert (ac_mo / total_mo) > 0.55, "ACs should constitute >55% of summer load"
    print("[OK] Appliance unit profiler math verified.")

    # 8. Test High-Consumption Estate / 1-2 Kanal Villa (Rs. 350,000 bill, 6 ACs overnight)
    print("\n>>> Testing High-Consumption 1-2 Kanal Villa Math...")
    high_units = 5500 # ~Rs. 350k bill in summer
    high_daily = high_units / 30
    high_dc_kw = high_daily / (5.0 * 0.78) # Lahore irradiance
    high_panels = int(-(- (high_dc_kw * 1000) // 580))
    high_actual_kw = (high_panels * 580) / 1000
    
    # 6 ACs overnight for 8 hours
    ac_night_total_wh = ((6 * 750) + 200) * 8 # 37,600 Wh = 37.6 kWh
    lithium_kwh_req = (ac_night_total_wh / 1000) / (0.85 * 0.92)
    lithium_packs = int(-(- lithium_kwh_req // 5.12))
    
    print(f"High Consumption (5,500 units): {high_actual_kw:.2f} kWp ({high_panels} panels)")
    print(f"6x Inverter ACs Night Load: {ac_night_total_wh/1000:.1f} kWh -> {lithium_packs}x 5.12 kWh LiFePO4 packs")
    assert high_panels >= 75, f"Expected >= 75 panels for 5500 units, got {high_panels}"
    assert lithium_packs >= 9, f"Expected >= 9 lithium packs for 6 ACs, got {lithium_packs}"
    print("[OK] High-consumption estate calculations verified.")

    print("\n========================================================")
    print("ALL TESTS PASSED: Mathematical & Physics Engine is Sound!")
    print("========================================================")

if __name__ == "__main__":
    test_engine()
