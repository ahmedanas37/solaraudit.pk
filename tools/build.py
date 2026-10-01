"""
SOLARAUDIT.ONLINE - Master Template Compiler & Static Build Automation
Generates and synchronizes all 14 satellite landing pages + index.html,
compiles standalone minified CSS (removing Tailwind runtime CDN),
lazy-loads jsPDF, and verifies SEO integrity.
"""

import os
import re
import json
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROMIUM_PATH = r"C:\Users\Anas\AppData\Local\Chromium\Application\chrome.exe"
ASSET_VERSION = "2026.2"

# ─────────────────────────────────────────────────────────────
# 1. PAGE DEFINITIONS (Metadata, Presets, Schemas & Editorial)
# ─────────────────────────────────────────────────────────────

PAGES = [
    {
        "filename": "index.html",
        "url_path": "/",
        "title": "SOLARAUDIT.ONLINE - 2026 Pakistan Solar Sizing & Electricity Bill Calculator",
        "description": "Independent solar system sizing, 580W panel count, roof space, and night AC battery storage calculator based on active 2026 NEPRA & K-Electric tariff rates. Free instant PDF audit sheet.",
        "h1": "Solar System &amp; Electricity Bill Calculator",
        "lead": "Estimate your required solar capacity, panel count, roof space, and battery storage based on active NEPRA progressive tariffs.",
        "body_attrs": "",
        "city_selected": "karachi",
        "faq": [
            ("How many units does 1 kW solar produce per day in Pakistan?", "Across major Pakistani urban centers (Karachi, Lahore, Islamabad, Multan), 1 kW of installed solar capacity yields approximately 3.8 to 4.2 usable kilowatt-hours (units) per day after applying a realistic 0.78 system derating factor for high summer temperatures and airborne dust deposition."),
            ("Can I install solar net-metering on a single-phase electricity meter in Pakistan?", "No. NEPRA distributed generation regulations strictly require a 3-phase bidirectional green meter for net-metering. Single-phase consumers must apply to their local DISCO (such as K-Electric, LESCO, IESCO, or MEPCO) for a Phase Conversion and Sanctioned Load Extension before their net-metering application can be processed."),
            ("What is a fair price per watt for residential solar systems in Pakistan in 2026?", "Based on current wholesale hardware benchmarks, turnkey on-grid residential solar installations typically range between Rs. 75 and Rs. 95 per watt. Turnkey hybrid installations (including 48V LiFePO4 battery storage) range between Rs. 105 and Rs. 135 per watt. Quotes exceeding Rs. 150/W indicate excessive contractor markup, while quotes under Rs. 95/W for hybrid systems indicate compromised hardware quality."),
            ("How does the 2026 NEPRA Net-Billing policy affect solar payback periods?", "Under NEPRA's Net-Billing regime, exported units are credited at the National Average Energy Purchase Price (NAEPP), while imported units are billed at progressive retail slab tariffs. Because approximately 70% to 75% of residential solar generation is consumed directly during daylight hours (avoiding high peak retail tariffs), typical payback periods remain robust at 2.0 to 2.5 years."),
            ("Which battery is recommended for running an inverter AC overnight on solar?", "A 48V Lithium Iron Phosphate (LiFePO4) battery bank (minimum 100Ah to 200Ah usable capacity) is strongly recommended. Deep-cycle lead-acid tubular batteries only offer 50% usable depth of discharge and quickly degrade under inductive AC compressor loads within 12 to 18 months, whereas LiFePO4 cells deliver 4,000+ charge cycles at 85% depth of discharge.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">
            Independent Solar Engineering Audit for Pakistani Homes &amp; Commercial Plazas
          </h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            With electricity tariffs in Pakistan crossing Rs. 60 per unit in upper progressive slabs, solar energy has transitioned from an elective amenity to a vital financial safeguard. SOLARAUDIT.ONLINE was engineered to provide transparent, un-gated mathematical audits free from contractor sales bias.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">
            Regional Grid Utility Calculations &amp; Dedicated DISCO Audits
          </h3>
          <p class="text-xs sm:text-sm text-slate-600 leading-relaxed mb-3">
            Every distribution company in Pakistan operates under distinct solar insolation profiles and local load constraints. Audit your exact utility tariff:
          </p>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="p-2.5 rounded-lg bg-white border border-slate-200 hover:border-slate-400 font-semibold text-slate-800 hover:text-emerald-700 flex items-center justify-between shadow-2xs"><span>Lahore (LESCO)</span><span>&rarr;</span></a>
            <a href="/ke-bill-calculator.html" class="p-2.5 rounded-lg bg-white border border-slate-200 hover:border-slate-400 font-semibold text-slate-800 hover:text-emerald-700 flex items-center justify-between shadow-2xs"><span>Karachi (K-Electric)</span><span>&rarr;</span></a>
            <a href="/iesco-solar-calculator.html" class="p-2.5 rounded-lg bg-white border border-slate-200 hover:border-slate-400 font-semibold text-slate-800 hover:text-emerald-700 flex items-center justify-between shadow-2xs"><span>Islamabad (IESCO)</span><span>&rarr;</span></a>
            <a href="/mepco-solar-calculator.html" class="p-2.5 rounded-lg bg-white border border-slate-200 hover:border-slate-400 font-semibold text-slate-800 hover:text-emerald-700 flex items-center justify-between shadow-2xs"><span>Multan (MEPCO)</span><span>&rarr;</span></a>
            <a href="/gepco-solar-calculator.html" class="p-2.5 rounded-lg bg-white border border-slate-200 hover:border-slate-400 font-semibold text-slate-800 hover:text-emerald-700 flex items-center justify-between shadow-2xs"><span>Gujranwala (GEPCO)</span><span>&rarr;</span></a>
            <a href="/fesco-solar-calculator.html" class="p-2.5 rounded-lg bg-white border border-slate-200 hover:border-slate-400 font-semibold text-slate-800 hover:text-emerald-700 flex items-center justify-between shadow-2xs"><span>Faisalabad (FESCO)</span><span>&rarr;</span></a>
          </div>
        </div>
        """
    },
    {
        "filename": "3kw-solar-system-pakistan.html",
        "url_path": "/3kw-solar-system-pakistan.html",
        "title": "3kW Solar System Price in Pakistan (2026 Sizing & Payback) — SOLARAUDIT.ONLINE",
        "description": "Calculate 3kW solar system cost in Pakistan, 580W panel count (5-6 panels), monthly generation (350-420 units), and net-billing payback for 5-7 Marla homes.",
        "h1": "3kW Solar System in Pakistan: Sizing, Cost &amp; Units Generated (2026)",
        "lead": "Complete engineering specification, 580W panel count, and turnkey cost breakdown for entry-level 3kW residential solar setups in Pakistan.",
        "body_attrs": 'data-preset-bill="25000" data-preset-mode="bill" data-preset-city="lahore"',
        "city_selected": "lahore",
        "faq": [
            ("How many units does a 3kW solar system generate per month in Pakistan?", "A 3kW system (configured with 5 to 6 Tier-1 580W panels) generates approximately 360 to 440 kilowatt-hours (units) per month across Punjab and Sindh, depending on summer dust and seasonal cloud cover."),
            ("Can a 3kW solar system run a 1.5-ton inverter AC?", "Yes. During bright sunlight hours (10:30 AM to 4:00 PM), a 3kW solar system generates enough power to run 1x 1.5-ton inverter AC in eco mode alongside basic household loads like a refrigerator, lights, and fans."),
            ("What is the turnkey cost of a 3kW solar system in Pakistan in 2026?", "In 2026, an on-grid 3kW system costs between Rs. 3.4 Lakhs to Rs. 4.2 Lakhs. A hybrid setup with a backup battery bank typically costs Rs. 4.8 Lakhs to Rs. 5.8 Lakhs.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">3kW Solar System Price in Pakistan (2026 Turnkey Breakdown)</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            A 3kW (or 3.2kW to 3.5kW DC) solar installation is Pakistan's premier entry-level residential system, perfectly sized for 3-Marla to 7-Marla houses with electricity bills ranging from Rs. 20,000 to Rs. 35,000 per month.
          </p>
          <ul class="list-disc list-inside space-y-1 text-slate-700 text-xs sm:text-sm pl-2 pt-2">
            <li><strong>On-Grid Turnkey Cost:</strong> Approximately <strong>Rs. 3.4 Lakhs to Rs. 4.2 Lakhs</strong> (includes 5-6x 580W panels, 3kW inverter, AC/DC protections, and standard L2 mounting structure).</li>
            <li><strong>Hybrid Turnkey Cost (with Battery):</strong> Approximately <strong>Rs. 4.8 Lakhs to Rs. 5.8 Lakhs</strong> (includes 3.2kW hybrid inverter and 24V or 48V battery bank for loadshedding).</li>
          </ul>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Regional Grid Tariffs &amp; DISCO Payback</h3>
          <p class="text-xs sm:text-sm text-slate-600 leading-relaxed mb-3">
            Compare 3kW system yields across your local regional utility provider:
          </p>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO Lahore</a>
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO Islamabad</a>
            <a href="/mepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">MEPCO Multan</a>
            <a href="/fesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">FESCO Faisalabad</a>
            <a href="/gepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">GEPCO Gujranwala</a>
          </div>
        </div>
        """
    },
    {
        "filename": "5kw-solar-system-pakistan.html",
        "url_path": "/5kw-solar-system-pakistan.html",
        "title": "5kW Solar System Price in Pakistan (2026 Specs & Panel Count) — SOLARAUDIT.ONLINE",
        "description": "Engineering guide & cost calculator for 5kW solar systems in Pakistan. 9x 580W panels, 600-750 units/mo yield, inverter selection, and 2-year net-billing payback.",
        "h1": "5kW Solar System in Pakistan: Sizing, 580W Panel Count &amp; Price",
        "lead": "The sweet-spot residential solar system for 10-Marla Pakistani homes running 2 Inverter ACs and eliminating high progressive slab tariffs.",
        "body_attrs": 'data-preset-bill="42000" data-preset-mode="bill" data-preset-city="lahore"',
        "city_selected": "lahore",
        "faq": [
            ("How many 580W panels are needed for a 5kW solar system?", "A standard 5kW setup requires 9x 580W Tier-1 panels, giving an actual DC capacity of 5.22 kWp, which pairs perfectly with 5kW and 6kW hybrid inverters."),
            ("How much does a 5kW solar system cost in Pakistan in 2026?", "Turnkey pricing for a 5kW on-grid system ranges between Rs. 4.8 Lakhs to Rs. 5.6 Lakhs. A hybrid installation with 48V 100Ah LiFePO4 battery storage ranges from Rs. 7.2 Lakhs to Rs. 8.4 Lakhs."),
            ("What is the monthly electricity bill saving on a 5kW solar system?", "A 5kW array generates 600 to 750 units monthly, saving approximately Rs. 35,000 to Rs. 48,000 per month by completely shaving off the top progressive tariff slabs (>300 and >700 units).")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">5kW Solar System: The Residential Sweet Spot in Pakistan</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            The 5kW (5.22 kWp DC) system is the most popular residential solar configuration in Pakistan. It is tailored for 10-Marla and compact 1-Kanal homes where monthly summer consumption hits 600 to 800 units due to two inverter air conditioners.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Explore Regional DISCO Net-Billing Sizing</h3>
          <p class="text-xs sm:text-sm text-slate-600 leading-relaxed mb-3">
            Explore how 5kW yields perform under regional DISCO net-billing rules:
          </p>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO Lahore</a>
            <a href="/ke-bill-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">K-Electric Karachi</a>
            <a href="/mepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">MEPCO Multan</a>
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO Islamabad</a>
            <a href="/gepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">GEPCO Gujranwala</a>
          </div>
        </div>
        """
    },
    {
        "filename": "10kw-solar-system-pakistan.html",
        "url_path": "/10kw-solar-system-pakistan.html",
        "title": "10kW Solar System Price in Pakistan (2026 Net-Metering Payback) — SOLARAUDIT.ONLINE",
        "description": "Complete 10kW solar system guide in Pakistan. Sizing for 1 Kanal homes running 3-4 ACs, 18x 580W panels, 3-phase net-billing, and LiFePO4 battery integration.",
        "h1": "10kW Solar System in Pakistan: Commercial &amp; 1-Kanal Home Payback",
        "lead": "Engineering specifications, 3-phase inverter requirements, and turnkey financial return for 1-Kanal homes and light commercial offices.",
        "body_attrs": 'data-preset-bill="85000" data-preset-mode="bill" data-preset-city="lahore"',
        "city_selected": "lahore",
        "faq": [
            ("How many units does a 10kW solar system produce per month?", "In Pakistan, a 10kW array (18x 580W panels = 10.44 kWp) produces between 1,250 and 1,550 units per month, delivering over 15,000 units annually."),
            ("What is the cost of a 10kW solar system in Pakistan in 2026?", "A turnkey 10kW on-grid 3-phase system costs Rs. 8.5 Lakhs to Rs. 9.8 Lakhs. A hybrid setup with a 10kWh LiFePO4 battery bank costs between Rs. 13.5 Lakhs and Rs. 15.5 Lakhs."),
            ("Does a 10kW solar system require a 3-phase meter?", "Yes. All solar inverters rated 8kW and above are 3-phase in Pakistan. You must have an approved 3-phase connection from your DISCO (LESCO, K-Electric, IESCO, etc.) to install a 10kW system.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">10kW Solar Architecture: Standard for 1-Kanal Residences</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            For 1-Kanal homes running 3 to 4 inverter air conditioners, continuous refrigeration, water motors, and home electronics, a 10kW solar array represents the benchmark capacity. Under 2026 NEPRA progressive tariffs, a 10kW installation protects consumers against peak slab charges of Rs. 48-60/kWh.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Check Regional 10kW DISCO Net-Billing Policies</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore 1-Kanal)</a>
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO (Islamabad Sectors)</a>
            <a href="/ke-bill-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">K-Electric (DHA/Clifton)</a>
            <a href="/mepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">MEPCO (Multan/Cantt)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "15kw-20kw-solar-system-pakistan.html",
        "url_path": "/15kw-20kw-solar-system-pakistan.html",
        "title": "15kW & 20kW Solar System Pakistan (2026 Commercial & Villa Audit) — SOLARAUDIT.ONLINE",
        "description": "Commercial & luxury villa solar sizing for 15kW to 20kW installations in Pakistan. High-voltage 3-phase inverters, 2,000-3,000+ units/mo yield, and ROI analysis.",
        "h1": "15kW &ndash; 20kW Solar System Pakistan: Plazas, Estates &amp; Net-Billing",
        "lead": "Commercial plazas, schools, private hospitals, and 2-Kanal luxury estates with monthly electricity bills between Rs. 150,000 and Rs. 350,000.",
        "body_attrs": 'data-preset-bill="175000" data-preset-mode="bill" data-preset-city="lahore"',
        "city_selected": "lahore",
        "faq": [
            ("How many panels are needed for a 15kW to 20kW solar system?", "A 15kW system requires 26x 580W panels (15.08 kWp), while a 20kW system uses 35x 580W panels (20.3 kWp)."),
            ("What is the monthly generation of a 20kW solar installation?", "A 20kW array produces between 2,500 and 3,100 kilowatt-hours (units) per month in Pakistan, resulting in monthly savings exceeding Rs. 120,000 to Rs. 160,000."),
            ("What roof space is required for a 20kW system?", "A 20kW system with 35 panels requires approximately 980 to 1,100 square feet (approx. 4.5 to 5 Marlas) of shadow-free rooftop space.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">High-Capacity Solar Architecture for Commercial &amp; Estate Load</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            Systems of 15kW to 20kW utilize high-voltage 3-phase commercial inverters (Sungrow, Huawei, Solis, Deye). They are designed for large joint families running 5 to 8 air conditioners simultaneously or commercial properties seeking to reduce operational overhead under NEPRA commercial tariffs.
          </p>
        </div>
        """
    },
    {
        "filename": "solar-panels-for-ac-pakistan.html",
        "url_path": "/solar-panels-for-ac-pakistan.html",
        "title": "Solar Panels for AC in Pakistan (1.5-Ton & 1-Ton Inverter AC Sizing) — SOLARAUDIT.ONLINE",
        "description": "How many solar panels do you need to run a 1.5-ton or 1-ton inverter AC in Pakistan? Day running vs overnight LiFePO4 battery sizing, wattages, and costs.",
        "h1": "Solar Panels for Inverter AC in Pakistan: Day &amp; Night Sizing Guide",
        "lead": "Exact wattage consumption, daytime panel requirements, and overnight Lithium battery storage physics for 1-Ton, 1.5-Ton, and 2-Ton Inverter ACs.",
        "body_attrs": 'data-preset-mode="appliances" data-preset-night-ac="true" data-preset-night-ac-count="2"',
        "city_selected": "karachi",
        "faq": [
            ("How many 580W solar panels to run one 1.5-ton inverter AC during the day?", "A 1.5-ton inverter AC draws around 750W to 900W running continuously at 26°C. Factoring in startup surge and summer heat derating, a minimum of 3x 580W panels (1.74 kWp) is required per AC for daytime operation."),
            ("Can I run an inverter AC on solar without batteries?", "Yes! With an on-grid or grid-tied hybrid inverter, you can run your inverter AC directly from solar panels during daylight hours, importing power from the grid only when clouds pass."),
            ("What battery is needed to run a 1.5-ton AC all night?", "To run one 1.5-ton AC for 8 hours overnight (consuming approx. 6.5 to 7.5 kWh), you need a 48V 150Ah or 200Ah Lithium LiFePO4 battery bank (7.68 kWh to 10.24 kWh nominal capacity).")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">The Physics of Running Inverter ACs on Solar in Pakistan</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            In Pakistani summers, air conditioning represents over 60% of total household electricity consumption. Modern DC inverter air conditioners employ variable-speed rotary compressors that reduce power consumption from 1,600W at startup down to 550W–750W once the room stabilizes at 26°C.
          </p>
        </div>
        """
    },
    {
        "filename": "solar-batteries-pakistan.html",
        "url_path": "/solar-batteries-pakistan.html",
        "title": "Solar Battery Price in Pakistan (2026 LiFePO4 vs Tubular) — SOLARAUDIT.ONLINE",
        "description": "LiFePO4 Lithium vs tubular battery comparison for solar systems in Pakistan. 48V battery sizing for overnight inverter AC loads, cycle lifespan, and prices.",
        "h1": "Solar Batteries in Pakistan: Lithium LiFePO4 vs. Tubular ROI Comparison",
        "lead": "Engineering analysis comparing 48V Lithium Iron Phosphate (LiFePO4) storage against deep-cycle lead-acid tubular batteries for night loadshedding and AC operation.",
        "body_attrs": 'data-preset-mode="bill" data-preset-night-ac="true"',
        "city_selected": "karachi",
        "faq": [
            ("Can a solar battery run an inverter AC all night in Pakistan?", "Yes, but only with a properly sized 48V Lithium (LiFePO4) battery bank of at least 100Ah to 150Ah capacity (5.1kWh to 7.6kWh). Lead-acid tubular batteries cannot withstand continuous night AC loads and fail within 12 to 18 months."),
            ("How much does a LiFePO4 lithium solar battery cost in Pakistan in 2026?", "In 2026, a standard 48V 100Ah (5.12 kWh) server-rack or wall-mount LiFePO4 battery with integrated BMS costs approximately Rs. 2.1 Lakhs to Rs. 2.4 Lakhs in wholesale markets (Hall Road/Saddar)."),
            ("How long do lithium solar batteries last in Pakistan?", "Quality Tier-1 LiFePO4 batteries (Narada, Pylontech, Dyness, Shoto) are rated for 4,000 to 6,000 cycles at 80% depth of discharge, which equates to 10 to 15 years of daily cycling.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Solar Battery Chemistry: Why Tubular Fails Under AC Loads</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            The single most critical financial decision when purchasing a hybrid solar system in Pakistan is battery chemistry selection. Contractors frequently push deep-cycle lead-acid tubular batteries due to lower upfront shelf prices, but fail to disclose that tubular batteries suffer from severe Peukert capacity loss and plate sulfation when subjected to continuous inductive compressor loads.
          </p>
        </div>
        """
    },
    {
        "filename": "solar-quote-validator.html",
        "url_path": "/solar-quote-validator.html",
        "title": "Solar Quotation Validator Pakistan (Audit Contractor Pricing) — SOLARAUDIT.ONLINE",
        "description": "Check if your solar installer is overcharging or cutting corners. Benchmark your turnkey solar quote against 2026 wholesale Tier-1 hardware prices in Pakistan.",
        "h1": "Contractor Solar Quotation Validator: Audit Turnkey Rates &amp; BOM",
        "lead": "The Pakistani solar market's independent 'BS-Detector': Benchmark your contractor's quote per watt against active wholesale hardware rates in Hall Road and Saddar.",
        "body_attrs": 'data-focus-section="validator"',
        "city_selected": "lahore",
        "faq": [
            ("What is the fair turnkey price per watt for solar in Pakistan in 2026?", "On-grid residential installations range from Rs. 75 to Rs. 95 per watt. Hybrid systems with LiFePO4 batteries range from Rs. 105 to Rs. 135 per watt. Quotes over Rs. 150/W indicate excessive contractor markup."),
            ("What are the warning signs of a cut-corner solar installation?", "Warning signs include prices below Rs. 65/W for ongrid or below Rs. 95/W for hybrid, use of copper-clad aluminum (CCA) wiring instead of 99.9% pure copper, uncertified non-AEDB engineers, or B-grade panel barcodes."),
            ("Why is elevated L3 structure more expensive than standard L2?", "Elevated L3 structure (walkable pergola) uses heavy 12-gauge hot-dip galvanized steel columns raised 8 to 10 feet above the roof, adding approximately Rs. 12 to Rs. 14 per watt to turnkey capex.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Contractor Quote Verification: How to Spot Overcharging &amp; Hardware Cuts</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            Contractor margins in Pakistan can swing wildly between 10% and 60% for the exact same hardware bill of materials. By auditing total price per watt against current Tier-1 import benchmarks, consumers can negotiate with institutional-grade authority.
          </p>
        </div>
        """
    },
    {
        "filename": "ke-bill-calculator.html",
        "url_path": "/ke-bill-calculator.html",
        "title": "K-Electric Solar Bill Calculator & Net-Billing Payback Karachi (2026) — SOLARAUDIT.ONLINE",
        "description": "Audit your K-Electric Karachi electricity bill and calculate required solar capacity, 580W panel count, and net-billing payback under active 2026 KE tariffs.",
        "h1": "K-Electric Solar Bill Calculator &amp; Net-Billing Payback (Karachi 2026)",
        "lead": "Calibrated for K-Electric Karachi consumers navigating high Fuel Price Adjustments (FPA), Financing Surcharges, and 5.4 Peak Sun Hours.",
        "body_attrs": 'data-preset-city="karachi" data-preset-disco="kelectric" data-preset-bill="48000"',
        "city_selected": "karachi",
        "faq": [
            ("How does K-Electric calculate solar net-billing in Karachi?", "K-Electric credits exported daylight solar units at the NEPRA-mandated NAEPP wholesale rate, while grid imports at night are billed under progressive residential slabs. Daytime self-consumption directly avoids high retail slabs."),
            ("What is Karachi's average solar peak sun hours (PSH)?", "Karachi enjoys an excellent solar insolation rating of approximately 5.4 Peak Sun Hours per day year-round, despite coastal humidity and marine haze."),
            ("What is the cost of a 3-phase net meter with K-Electric?", "The K-Electric net-metering process costs approximately Rs. 65,000 to Rs. 85,000, covering testing, load clearance NOC, and bidirectional green meter installation.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Karachi Solar Economics under K-Electric 2026 Tariff Regimes</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            Karachi consumers face some of the highest effective electricity rates in Pakistan due to volatile monthly Fuel Charges Adjustments (FCA) and quarterly tariff determinations. Sizing a solar array in Karachi delivers rapid 1.8 to 2.2-year payback periods because direct self-consumption avoids both base tariffs and FPA surcharges.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Compare Sizing with Other DISCO Regions</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore)</a>
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO (Islamabad)</a>
            <a href="/mepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">MEPCO (Multan)</a>
            <a href="/gepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">GEPCO (Gujranwala)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "lesco-solar-calculator.html",
        "url_path": "/lesco-solar-calculator.html",
        "title": "LESCO Solar Calculator & Net-Billing Payback Lahore (2026) — SOLARAUDIT.ONLINE",
        "description": "Calculate LESCO residential solar system size, net billing savings, and 580W panel count for Lahore & Punjab. Free PDF engineering sheet.",
        "h1": "LESCO Solar Calculator &amp; Lahore Net-Billing Payback Guide",
        "lead": "Customized for Lahore Electric Supply Company (LESCO) consumers, accounting for summer peak heat and winter smog solar derating.",
        "body_attrs": 'data-preset-city="lahore" data-preset-disco="lesco" data-preset-bill="52000"',
        "city_selected": "lahore",
        "faq": [
            ("How does winter smog in Lahore affect solar generation?", "Winter smog in Lahore can reduce solar generation by up to 45% between November and January. Our calculator factors in a 0.78 derating factor and recommends proper tilt angle (28°-30°) for winter clearance."),
            ("What are the steps for LESCO net-metering approval?", "The process involves submitting an AEDB-certified engineer dossier, obtaining a DISCO NOC, paying the bidirectional meter demand notice, and completing the electrical inspection."),
            ("Is solar profitable in Lahore under LESCO net-billing?", "Yes. Because residential tariffs in LESCO reach up to Rs. 48/unit in peak summer slabs, self-consuming solar energy saves substantial money, delivering a payback of 2.0 to 2.4 years.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">LESCO Solar Engineering &amp; Smog Resilience in Lahore</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            Lahore features intense solar irradiance during summer (5.0 PSH), which perfectly matches peak air conditioning demand. Sizing a system under LESCO requires careful attention to rooftop pergola elevation to clear terrace parapets and smog dust cleaning protocols.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Explore Neighboring Punjab Utility Calculators</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/gepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">GEPCO (Gujranwala / Sialkot)</a>
            <a href="/fesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">FESCO (Faisalabad)</a>
            <a href="/mepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">MEPCO (South Punjab)</a>
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO (Islamabad / RWP)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "iesco-solar-calculator.html",
        "url_path": "/iesco-solar-calculator.html",
        "title": "IESCO Solar Calculator & Payback Islamabad / Rawalpindi (2026) — SOLARAUDIT.ONLINE",
        "description": "IESCO solar calculator for Islamabad & Rawalpindi. Calculate solar system size, panel count, roof space, and payback under active IESCO 2026 tariffs.",
        "h1": "IESCO Solar Calculator: Islamabad &amp; Rawalpindi Net-Billing Audit",
        "lead": "Engineered for Islamabad and Rawalpindi consumers under Islamabad Electric Supply Company (IESCO), featuring clean air clearance and 5.1 PSH.",
        "body_attrs": 'data-preset-city="islamabad" data-preset-disco="iesco" data-preset-bill="50000"',
        "city_selected": "islamabad",
        "faq": [
            ("How long does IESCO net-metering take in Islamabad?", "IESCO net-metering typically takes between 4 to 8 weeks from the date of application submission by an AEDB-accredited installer to bidirectional meter commissioning."),
            ("What is the solar irradiance in Islamabad & Rawalpindi?", "Islamabad enjoys clean atmospheric clearance with an average of 5.1 Peak Sun Hours (PSH) per day, resulting in exceptional yearly kilowatt-hour generation."),
            ("Does CDA allow elevated solar structures in Islamabad?", "Yes, the Capital Development Authority (CDA) permits rooftop solar mounting structures provided they adhere to height restrictions and do not violate building setback bylaws.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Solar Potential in Islamabad &amp; Rawalpindi (IESCO)</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            Consumers in Islamabad sectors (F, G, E, Bahria Town, DHA) and Rawalpindi benefit from lower airborne particulate matter compared to central Punjab, ensuring higher solar yield per installed kilowatt.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Regional Grid Utilities</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore)</a>
            <a href="/gepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">GEPCO (Gujranwala)</a>
            <a href="/pesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">PESCO (Peshawar)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "mepco-solar-calculator.html",
        "url_path": "/mepco-solar-calculator.html",
        "title": "MEPCO Solar Calculator & Net-Billing Sizing Multan (2026) — SOLARAUDIT.ONLINE",
        "description": "MEPCO solar sizing & bill audit tool for Multan, Bahawalpur, and South Punjab. High summer solar insolation calculations and 2026 progressive slab savings.",
        "h1": "MEPCO Solar Calculator: Multan &amp; South Punjab Solar Sizing",
        "lead": "Calibrated for Multan Electric Power Company (MEPCO) consumers with high solar insolation (5.3 PSH) and intense ambient summer heat.",
        "body_attrs": 'data-preset-city="multan" data-preset-disco="mepco" data-preset-bill="45000"',
        "city_selected": "multan",
        "faq": [
            ("How does extreme heat in Multan affect solar panels?", "High ambient temperatures (45°C+) cause solar panel voltage to decrease by approx 0.30% per °C above 25°C. Using modern N-Type TOPCon panels with lower temperature coefficients (-0.29%/°C) minimizes heat loss in South Punjab."),
            ("What is MEPCO's net-metering procedure in Multan?", "MEPCO processes net-metering through its sub-divisional offices with demand notices issued for 3-phase electronic bidirectional meters."),
            ("What is the solar payback period in MEPCO region?", "Due to 5.3 Peak Sun Hours and high cooling loads, typical payback in Multan and Bahawalpur is among the fastest in Pakistan at 1.9 to 2.2 years.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">High Solar Insolation &amp; Temperature Management in South Punjab</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            South Punjab receives exceptional solar radiation, making solar systems highly productive. However, proper rear ventilation and elevated mounting are essential to dissipate extreme summer heat build-up under the panels.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Explore Regional DISCOs</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore)</a>
            <a href="/fesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">FESCO (Faisalabad)</a>
            <a href="/ke-bill-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">K-Electric (Karachi)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "gepco-solar-calculator.html",
        "url_path": "/gepco-solar-calculator.html",
        "title": "GEPCO Solar Calculator & Sizing Gujranwala / Sialkot (2026) — SOLARAUDIT.ONLINE",
        "description": "Calculate solar sizing and payback under GEPCO tariffs for Gujranwala, Sialkot, and Gujrat. Tier-1 panel counts, rooftop space, and turnkey costs.",
        "h1": "GEPCO Solar Calculator: Gujranwala &amp; Sialkot Net-Billing Payback",
        "lead": "Customized for Gujranwala Electric Power Company (GEPCO) consumers across Gujranwala, Sialkot, and Gujrat export industrial hubs.",
        "body_attrs": 'data-preset-city="gujranwala" data-preset-disco="gepco" data-preset-bill="48000"',
        "city_selected": "gujranwala",
        "faq": [
            ("What is the typical solar system size in Gujranwala and Sialkot?", "Most 10-Marla to 1-Kanal homes and small export factories install 5kW to 15kW systems to offset daytime running loads and severe peak progressive tariffs."),
            ("How does GEPCO handle net-metering applications?", "GEPCO requires AEDB-certified contractor documentation and issues 3-phase bidirectional green meters across Gujranwala, Sialkot, and Gujrat circles."),
            ("What are the savings on a 10kW system under GEPCO?", "A 10kW array produces 1,250 to 1,450 units per month, delivering monthly bill reductions of Rs. 65,000 to Rs. 80,000 under active 2026 tariffs.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Solar Energy for Gujranwala, Sialkot &amp; Gujrat Industrial Hubs</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            The Golden Triangle region (Gujranwala, Sialkot, Gujrat) contains Pakistan's densest concentration of light manufacturing and export businesses. Investing in rooftop solar eliminates peak commercial tariffs and protects against recurring grid outages.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Explore Regional DISCOs</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore)</a>
            <a href="/fesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">FESCO (Faisalabad)</a>
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO (Islamabad)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "fesco-solar-calculator.html",
        "url_path": "/fesco-solar-calculator.html",
        "title": "FESCO Solar Calculator & Net-Billing Faisalabad (2026) — SOLARAUDIT.ONLINE",
        "description": "FESCO solar sizing calculator for Faisalabad, Sargodha, and Jhang. Calculate panel count, battery requirements, and payback under 2026 progressive tariffs.",
        "h1": "FESCO Solar Calculator: Faisalabad Industrial &amp; Home Sizing",
        "lead": "Engineered for Faisalabad Electric Supply Company (FESCO) consumers in Faisalabad, Sargodha, and Jhang textile and residential centers.",
        "body_attrs": 'data-preset-city="faisalabad" data-preset-disco="fesco" data-preset-bill="48000"',
        "city_selected": "faisalabad",
        "faq": [
            ("What is the solar insolation in Faisalabad under FESCO?", "Faisalabad receives an average of 5.1 Peak Sun Hours (PSH) per day, making it an ideal candidate for high-yield rooftop solar generation."),
            ("How does industrial textile load affect solar sizing in Faisalabad?", "For commercial power looms and packaging units, day-time self-consumption often reaches 80-90%, maximizing ROI under NEPRA net-billing by directly replacing peak grid tariffs."),
            ("What is the average payback period for a 10kW system in FESCO?", "Payback periods for 10kW residential and commercial setups in Faisalabad range between 2.0 and 2.3 years.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Solar Energy in the Textile Capital: Faisalabad Sizing Strategy</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            As Pakistan's textile capital, Faisalabad experiences heavy daytime electrical loads. Rooftop solar provides immediate tariff mitigation, allowing businesses and residents to lock in electricity costs at under Rs. 10/unit over 25 years.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Explore Regional DISCOs</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore)</a>
            <a href="/gepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">GEPCO (Gujranwala)</a>
            <a href="/mepco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">MEPCO (Multan)</a>
          </div>
        </div>
        """
    },
    {
        "filename": "pesco-solar-calculator.html",
        "url_path": "/pesco-solar-calculator.html",
        "title": "PESCO Solar Calculator & Net-Billing Peshawar / KP (2026) — SOLARAUDIT.ONLINE",
        "description": "PESCO solar calculator for Peshawar, Mardan, and Khyber Pakhtunkhwa. Calculate solar panel requirements, battery backup, and net-billing payback under 2026 tariffs.",
        "h1": "PESCO Solar Calculator: Peshawar &amp; KP Net-Billing Payback",
        "lead": "Customized for Peshawar Electric Supply Company (PESCO) consumers across Peshawar, Mardan, and Khyber Pakhtunkhwa.",
        "body_attrs": 'data-preset-city="peshawar" data-preset-disco="pesco" data-preset-bill="42000"',
        "city_selected": "peshawar",
        "faq": [
            ("What is the solar insolation in Peshawar under PESCO?", "Peshawar averages approximately 4.9 Peak Sun Hours (PSH) per day, with clear skies from March through October providing dependable power generation."),
            ("Why is hybrid battery backup recommended in PESCO region?", "Due to frequent feeder loadshedding in suburban Peshawar and KP circles, hybrid systems with LiFePO4 batteries ensure 24/7 uninterrupted power for ACs, fans, and refrigeration."),
            ("What are the net-metering requirements under PESCO?", "PESCO processes net-metering applications for 3-phase consumers through its regional revenue offices, requiring AEDB engineer approval.")
        ],
        "editorial": """
        <div>
          <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-2">Solar Energy Adoption across Peshawar &amp; Khyber Pakhtunkhwa</h2>
          <p class="text-sm text-slate-700 leading-relaxed">
            In Khyber Pakhtunkhwa, hybrid solar systems provide two indispensable benefits: slashing high NEPRA progressive electricity bills and providing complete independence from unpredictable grid outages.
          </p>
        </div>
        <div>
          <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-2">Explore Regional DISCOs</h3>
          <div class="flex flex-wrap gap-2 text-xs">
            <a href="/iesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">IESCO (Islamabad / RWP)</a>
            <a href="/lesco-solar-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">LESCO (Lahore)</a>
            <a href="/ke-bill-calculator.html" class="px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">K-Electric (Karachi)</a>
          </div>
        </div>
        """
    }
]

# ─────────────────────────────────────────────────────────────
# 2. MASTER HTML TEMPLATE GENERATOR
# ─────────────────────────────────────────────────────────────

def render_master_page(page_def):
    url_canonical = f"https://solaraudit.online{page_def['url_path']}"
    
    # Generate JSON-LD Schema
    faq_entities = []
    for q, a in page_def["faq"]:
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
        
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "@id": f"{url_canonical}#webapp",
                "name": page_def["title"],
                "url": url_canonical,
                "applicationCategory": "UtilityApplication",
                "operatingSystem": "Web",
                "browserRequirements": "Requires JavaScript. Requires HTML5.",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "PKR"
                },
                "description": page_def["description"]
            },
            {
                "@type": "FAQPage",
                "@id": f"{url_canonical}#faq",
                "mainEntity": faq_entities
            },
            {
                "@type": "HowTo",
                "@id": "https://solaraudit.online/#howto",
                "name": "How to Verify Your Contractor Solar Quotation in Pakistan",
                "description": "Step-by-step guide to verifying whether a contractor's solar proposal contains fair market pricing or overcharges.",
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": 1,
                        "name": "Extract Quoted Capacity and Total Price",
                        "text": "Identify the total system DC capacity in kilowatts (kW) and the turnkey price quoted in Pakistani Rupees."
                    },
                    {
                        "@type": "HowToStep",
                        "position": 2,
                        "name": "Calculate Price Per Watt",
                        "text": "Divide total quoted price in PKR by total wattage (e.g., Rs. 950,000 divided by 6,000 Watts equals Rs. 158 per Watt)."
                    },
                    {
                        "@type": "HowToStep",
                        "position": 3,
                        "name": "Compare Against Wholesale Benchmarks",
                        "text": "Check against standard benchmarks: On-grid should range between Rs. 75-95/W, while Hybrid with battery should range between Rs. 105-135/W."
                    }
                ]
            }
        ]
    }
    schema_json = json.dumps(schema_graph, indent=2)

    # City Options
    cities = [
        ("karachi", "Karachi (K-Electric)"),
        ("lahore", "Lahore (LESCO)"),
        ("islamabad", "Islamabad / RWP (IESCO)"),
        ("multan", "Multan / South Punjab (MEPCO)"),
        ("faisalabad", "Faisalabad (FESCO)"),
        ("gujranwala", "Gujranwala / Sialkot (GEPCO)"),
        ("peshawar", "Peshawar (PESCO)"),
        ("quetta", "Quetta / Balochistan (QESCO)"),
        ("sukkur", "Sukkur / Upper Sindh (SEPCO)"),
        ("hyderabad", "Hyderabad / Lower Sindh (HESCO)")
    ]
    city_options_html = ""
    for c_val, c_name in cities:
        selected_attr = " selected" if c_val == page_def["city_selected"] else ""
        city_options_html += f'          <option value="{c_val}"{selected_attr}>{c_name}</option>\n'

    # Render FAQ Accordion
    faq_html = ""
    for q, a in page_def["faq"]:
        faq_html += f"""
          <details class="group border border-slate-200 rounded-lg p-3.5 bg-white">
            <summary class="flex justify-between items-center font-medium text-slate-900 text-xs sm:text-sm cursor-pointer select-none">
              <span>{q}</span>
              <span class="transition group-open:rotate-180 text-slate-500 text-xs" aria-hidden="true">&#9660;</span>
            </summary>
            <p class="text-xs text-slate-700 mt-2.5 leading-relaxed">
              {a}
            </p>
          </details>"""

    html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon.png">
  <link rel="apple-touch-icon" href="favicon.png">
  <title>{page_def['title']}</title>
  <meta name="description" content="{page_def['description']}">
  <meta name="keywords" content="solar calculator pakistan, k electric bill calculator 2026, nepra tariff slabs, solar payback period pakistan, lithium battery for ac, 5kw solar system price in pakistan">
  <link rel="canonical" href="{url_canonical}">

  <!-- Open Graph & WhatsApp Social Card -->
  <meta property="og:title" content="{page_def['title']}">
  <meta property="og:description" content="{page_def['description']}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url_canonical}">
  <meta property="og:image" content="https://solaraudit.online/og-image.png">
  <meta property="og:image:secure_url" content="https://solaraudit.online/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="SOLARAUDIT.ONLINE — Pakistan Solar Sizing &amp; Bill Audit Engine">
  <meta property="og:locale" content="en_PK">
  <meta property="og:site_name" content="SOLARAUDIT.ONLINE">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_def['title']}">
  <meta name="twitter:description" content="{page_def['description']}">
  <meta name="twitter:image" content="https://solaraudit.online/og-image.png">

  <!-- Standalone High-Speed Compiled CSS -->
  <link rel="stylesheet" href="css/style.min.css?v={ASSET_VERSION}">

  <!-- Schema.org Structured Data (WebApplication, FAQPage, HowTo) -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen pb-24 lg:pb-0" {page_def['body_attrs']}>

  <!-- Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="/" class="font-bold text-base tracking-tight text-slate-900 flex items-center gap-2">
          <span class="w-7 h-7 rounded bg-slate-900 text-white flex items-center justify-center text-xs font-bold">SA</span>
          <span>SOLARAUDIT<span class="text-slate-600 font-normal">.ONLINE</span></span>
        </a>
        <span class="hidden sm:inline-block text-[11px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
          2026 Tariffs
        </span>
      </div>

      <!-- City & DISCO Selector -->
      <div class="flex items-center space-x-2">
        <label for="citySelect" class="text-xs text-slate-700 font-medium hidden sm:inline">Region:</label>
        <select id="citySelect" aria-label="Select City and Electric Utility Company" class="bg-white border border-slate-300 text-xs sm:text-sm text-slate-800 rounded-md px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-slate-900 cursor-pointer font-medium">
{city_options_html}        </select>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-8">

    <!-- Page Introduction -->
    <div class="mb-4">
      <h1 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
        {page_def['h1']}
      </h1>
      <p class="text-sm text-slate-700 mt-1 max-w-2xl leading-relaxed">
        {page_def['lead']}
      </p>
    </div>

    <!-- City Climate & Solar Irradiance Pill -->
    <div id="cityIrradiancePill" class="flex flex-wrap items-center gap-x-2.5 gap-y-1 text-xs text-slate-700 bg-white border border-slate-200 px-3.5 py-2 rounded-lg mb-6 shadow-2xs">
      <span class="inline-flex items-center gap-1.5 font-bold text-slate-900">
        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
        <span id="cityIrradiancePsh">5.4 Peak Sun Hours / Day</span>
      </span>
      <span class="text-slate-600 hidden sm:inline" aria-hidden="true">&#8226;</span>
      <span id="cityIrradianceClimate" class="text-slate-700">Coastal haze &#8226; High year-round sun</span>
      <span class="text-slate-600 hidden md:inline" aria-hidden="true">&#8226;</span>
      <span class="text-slate-600 text-[11px] hidden md:inline">0.78 summer derating (temp &amp; dust) factored</span>
    </div>

    <!-- Mode Selector -->
    <div class="inline-flex bg-slate-200/80 p-1 rounded-lg mb-6 border border-slate-200">
      <button id="modeBillBtn" aria-label="Calculate sizing by monthly electricity bill" class="min-h-[44px] py-2 px-4 rounded-md bg-white text-slate-900 font-semibold shadow-sm border border-slate-200 text-xs sm:text-sm transition-all cursor-pointer">
        By Monthly Bill
      </button>
      <button id="modeApplianceBtn" aria-label="Calculate sizing by household appliances" class="min-h-[44px] py-2 px-4 rounded-md text-slate-700 hover:text-slate-900 font-semibold text-xs sm:text-sm transition-all cursor-pointer">
        By Appliances
      </button>
    </div>

    <!-- Two-Column Tool Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

      <!-- LEFT COLUMN: INPUTS (5 Cols) -->
      <div class="lg:col-span-5 space-y-5">

        <!-- Input Box 1: Electricity Consumption -->
        <div class="tool-card p-5">
          <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">Electricity Usage</h2>

          <!-- Bill Slider Mode -->
          <div id="billInputSection" class="space-y-3">
            <div class="flex justify-between items-baseline">
              <label for="billSlider" class="text-xs font-semibold text-slate-800">Average Monthly Bill</label>
              <span id="billValueDisplay" class="text-lg font-bold font-mono text-slate-900">Rs. 48,000</span>
            </div>

            <input type="range" id="billSlider" min="8000" max="500000" step="2500" value="48000" aria-label="Average Monthly Electricity Bill in PKR">

            <div class="flex justify-between text-[11px] text-slate-600 font-medium">
              <span>Rs. 8k</span>
              <span>Rs. 250k</span>
              <span>Rs. 500k</span>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center text-xs text-slate-700">
              <span class="font-medium">Estimated Consumption:</span>
              <span id="outEstimatedUnits" class="font-bold text-slate-900 font-mono">~780 units</span>
            </div>

            <!-- Shortcut to Appliance Mode -->
            <div class="pt-1 flex items-center justify-between text-xs">
              <span class="text-slate-600">Don't have your bill handy?</span>
              <button id="shortcutToApplianceBtn" type="button" class="text-emerald-700 hover:text-emerald-800 font-bold hover:underline cursor-pointer">
                Estimate by appliances &rarr;
              </button>
            </div>
          </div>

          <!-- Appliance Mode (Hidden by default) -->
          <div id="applianceInputSection" class="hidden space-y-3">
            <div class="flex items-center justify-between pb-1 border-b border-slate-200">
              <span class="text-xs font-semibold text-slate-800">Household Appliance Load:</span>
              <button id="shortcutBackToBillBtn" type="button" class="text-xs text-emerald-700 hover:text-emerald-800 font-bold hover:underline cursor-pointer">
                &larr; Back to bill slider
              </button>
            </div>

            <!-- 1.5-Ton Inverter AC -->
            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-slate-900">1.5-Ton Inverter AC</div>
                  <div class="text-[11px] text-slate-600">750W continuous @ 26&#176;C Econ</div>
                </div>
                <div class="flex items-center space-x-2">
                  <button id="dec_ac15" aria-label="Decrease 1.5-Ton Inverter AC count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                  <span id="val_ac15" class="min-w-[32px] text-center font-bold text-sm text-slate-900">2</span>
                  <button id="inc_ac15" aria-label="Increase 1.5-Ton Inverter AC count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
                </div>
              </div>
              <div class="pt-1 border-t border-slate-200/80 flex items-center justify-between text-[11px]">
                <span class="text-slate-600">Daily Running Hours:</span>
                <div id="hoursGroup_ac15" class="inline-flex gap-1">
                  <button type="button" data-hours="4" aria-label="4 hours per day" class="min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 cursor-pointer">4h</button>
                  <button type="button" data-hours="8" aria-label="8 hours per day" class="min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-900 bg-slate-900 text-white cursor-pointer">8h</button>
                  <button type="button" data-hours="12" aria-label="12 hours per day" class="min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 cursor-pointer">12h</button>
                </div>
              </div>
            </div>

            <!-- 1.0-Ton Inverter AC -->
            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-slate-900">1.0-Ton Inverter AC</div>
                  <div class="text-[11px] text-slate-600">550W continuous @ 26&#176;C Econ</div>
                </div>
                <div class="flex items-center space-x-2">
                  <button id="dec_ac10" aria-label="Decrease 1.0-Ton Inverter AC count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                  <span id="val_ac10" class="min-w-[32px] text-center font-bold text-sm text-slate-900">0</span>
                  <button id="inc_ac10" aria-label="Increase 1.0-Ton Inverter AC count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
                </div>
              </div>
              <div class="pt-1 border-t border-slate-200/80 flex items-center justify-between text-[11px]">
                <span class="text-slate-600">Daily Running Hours:</span>
                <div id="hoursGroup_ac10" class="inline-flex gap-1">
                  <button type="button" data-hours="4" aria-label="4 hours per day" class="min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 cursor-pointer">4h</button>
                  <button type="button" data-hours="8" aria-label="8 hours per day" class="min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-900 bg-slate-900 text-white cursor-pointer">8h</button>
                  <button type="button" data-hours="12" aria-label="12 hours per day" class="min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 cursor-pointer">12h</button>
                </div>
              </div>
            </div>

            <!-- Ceiling Fans -->
            <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div class="text-xs font-bold text-slate-900">Ceiling Fans</div>
                <div class="text-[11px] text-slate-600">55W (14 hrs/day)</div>
              </div>
              <div class="flex items-center space-x-2">
                <button id="dec_fans" aria-label="Decrease ceiling fans count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                <span id="val_fans" class="min-w-[32px] text-center font-bold text-sm text-slate-900">5</span>
                <button id="inc_fans" aria-label="Increase ceiling fans count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
              </div>
            </div>

            <!-- Inverter Refrigerator -->
            <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div class="text-xs font-bold text-slate-900">Inverter Refrigerator</div>
                <div class="text-[11px] text-slate-600">150W continuous</div>
              </div>
              <div class="flex items-center space-x-2">
                <button id="dec_fridge" aria-label="Decrease refrigerator count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                <span id="val_fridge" class="min-w-[32px] text-center font-bold text-sm text-slate-900">1</span>
                <button id="inc_fridge" aria-label="Increase refrigerator count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
              </div>
            </div>

            <!-- Deep Freezer -->
            <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div class="text-xs font-bold text-slate-900">Deep Freezer</div>
                <div class="text-[11px] text-slate-600">180W continuous</div>
              </div>
              <div class="flex items-center space-x-2">
                <button id="dec_freezer" aria-label="Decrease deep freezer count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                <span id="val_freezer" class="min-w-[32px] text-center font-bold text-sm text-slate-900">0</span>
                <button id="inc_freezer" aria-label="Increase deep freezer count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
              </div>
            </div>

            <!-- Water Pump -->
            <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div class="text-xs font-bold text-slate-900">1.0 HP Water Pump</div>
                <div class="text-[11px] text-slate-600">1100W (1 hr/day)</div>
              </div>
              <div class="flex items-center space-x-2">
                <button id="dec_pump" aria-label="Decrease water pump count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                <span id="val_pump" class="min-w-[32px] text-center font-bold text-sm text-slate-900">1</span>
                <button id="inc_pump" aria-label="Increase water pump count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
              </div>
            </div>

            <!-- LED Lights / TV -->
            <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div class="text-xs font-bold text-slate-900">LED Lights &amp; TV / Wi-Fi</div>
                <div class="text-[11px] text-slate-600">150W (6 hrs/day)</div>
              </div>
              <div class="flex items-center space-x-2">
                <button id="dec_lights" aria-label="Decrease lights and TV count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">-</button>
                <span id="val_lights" class="min-w-[32px] text-center font-bold text-sm text-slate-900">1</span>
                <button id="inc_lights" aria-label="Increase lights and TV count" class="w-11 h-11 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-800 flex items-center justify-center font-bold text-base active:scale-95 transition-all cursor-pointer">+</button>
              </div>
            </div>

            <!-- Appliance Breakdown Summary Pill -->
            <div id="applianceBreakdownPill" class="p-3 rounded-lg bg-slate-100 border border-slate-200 space-y-1 text-xs">
              <div class="flex justify-between font-semibold text-slate-900">
                <span>Calculated Total:</span>
                <span id="applianceTotalUnitsDisplay" class="font-mono">~780 Units</span>
              </div>
              <div class="flex justify-between text-slate-700">
                <span>Estimated Grid Bill:</span>
                <span id="applianceTotalBillDisplay" class="font-mono font-bold text-slate-900">~Rs. 48,000</span>
              </div>
              <div class="text-[11px] text-emerald-800 font-semibold pt-1 border-t border-slate-200">
                Top Energy User: <span id="applianceDominantText" class="font-bold">1.5-Ton Inverter AC (58% of bill)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Box 2: Rooftop Structure Type -->
        <div class="tool-card p-5">
          <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">Rooftop Structure Type</h2>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <button id="structStandardBtn" type="button" aria-label="Standard L2 ground or roof mounting structure" class="min-h-[44px] p-2.5 rounded-lg border border-slate-900 bg-slate-900 text-white font-semibold text-left transition-all cursor-pointer">
              <div class="font-bold">Standard L2 Mount</div>
              <div class="text-[11px] text-slate-300">Ground/Low roof profile</div>
            </button>
            <button id="structElevatedBtn" type="button" aria-label="Elevated L3 pergola structure with walkable terrace" class="min-h-[44px] p-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold text-left hover:border-slate-400 transition-all cursor-pointer">
              <div class="font-bold text-slate-900">Elevated L3 Pergola</div>
              <div class="text-[11px] text-slate-600">Walkable (+Rs. 13/W)</div>
            </button>
          </div>
        </div>

        <!-- Input Box 3: Grid Meter Connection -->
        <div class="tool-card p-5">
          <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">Grid Meter Phase</h2>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <button id="meterThreePhaseBtn" type="button" aria-label="Three phase electricity connection ready for net metering" class="min-h-[44px] p-2.5 rounded-lg border border-slate-900 bg-slate-900 text-white font-semibold text-left transition-all cursor-pointer">
              <div class="font-bold">3-Phase Ready</div>
              <div class="text-[11px] text-slate-300">Net-metering eligible</div>
            </button>
            <button id="meterSinglePhaseBtn" type="button" aria-label="Single phase electricity connection requiring three phase upgrade" class="min-h-[44px] p-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold text-left hover:border-slate-400 transition-all cursor-pointer">
              <div class="font-bold text-slate-900">Single-Phase</div>
              <div class="text-[11px] text-slate-600">Upgrade required</div>
            </button>
          </div>
          <div id="singlePhaseNotice" class="hidden mt-2 p-2.5 rounded bg-amber-50 border border-amber-200 text-[11px] text-amber-900 leading-relaxed">
            <strong>NEPRA Advisory:</strong> Net-metering strictly requires a 3-phase green meter. Single-phase homes must apply to their DISCO for Phase Conversion and Sanctioned Load Extension (~Rs. 35k - 45k demand notice).
          </div>
        </div>

        <!-- Input Box 4: Overnight Battery Storage -->
        <div class="tool-card p-5 space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Night AC Battery Storage</h2>
              <p class="text-[11px] text-slate-600">Run inverter AC during night loadshedding</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" id="nightAcToggle" class="sr-only" checked aria-label="Toggle Night AC Battery Storage">
              <div class="toggle-switch-track"></div>
            </label>
          </div>

          <div id="nightBatteryOptions" class="space-y-4 pt-2 border-t border-slate-200">
            <!-- Number of ACs to run -->
            <div>
              <div class="flex justify-between items-baseline mb-1">
                <label for="nightAcCountSlider" class="text-xs text-slate-700 font-medium">Inverter ACs Running at Night</label>
                <span id="nightAcCountDisplay" class="text-xs font-bold font-mono text-slate-900">1 AC</span>
              </div>
              <input type="range" id="nightAcCountSlider" min="1" max="8" step="1" value="1" aria-label="Number of Inverter ACs Running Overnight">
            </div>

            <!-- Hours of operation -->
            <div>
              <div class="flex justify-between items-baseline mb-1">
                <label for="nightHoursSlider" class="text-xs text-slate-700 font-medium">Night Backup Required</label>
                <span id="nightHoursDisplay" class="text-xs font-bold font-mono text-slate-900">8 Hours</span>
              </div>
              <input type="range" id="nightHoursSlider" min="4" max="12" step="1" value="8" aria-label="Hours of Overnight Battery Backup">
            </div>

            <!-- Battery Chemistry Selection -->
            <div>
              <label class="text-xs text-slate-700 font-medium block mb-1.5">Battery Chemistry</label>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <button id="batteryTypeLithium" type="button" aria-label="Lithium Iron Phosphate LiFePO4 battery chemistry" class="min-h-[44px] p-2.5 rounded-lg border border-slate-900 bg-slate-900 text-white font-semibold text-left transition-all cursor-pointer">
                  <div class="font-bold">Lithium (LiFePO4)</div>
                  <div class="text-[11px] text-slate-300">85% DoD &#8226; 10-Yr Life</div>
                </button>
                <button id="batteryTypeTubular" type="button" aria-label="Deep cycle lead-acid tubular battery chemistry" class="min-h-[44px] p-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold text-left hover:border-slate-400 transition-all cursor-pointer">
                  <div class="font-bold text-slate-900">Tubular (Lead-Acid)</div>
                  <div class="text-[11px] text-slate-600">50% DoD &#8226; 2-Yr Life</div>
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- RIGHT COLUMN: RESULTS & SPECIFICATIONS (7 Cols) -->
      <div class="lg:col-span-7 space-y-5" id="resultsSection">
        <div id="resultsSummaryAnchor" class="scroll-mt-20"></div>

        <!-- Hardware System Sizing Card -->
        <div class="tool-card p-5">
          <div class="flex items-center justify-between mb-4 pb-2 border-b border-slate-200">
            <div>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Recommended System Architecture</h2>
              <p class="text-[11px] text-slate-600 mt-0.5">Calibrated for Tier-1 580W N-Type Bifacial TOPCon Modules</p>
            </div>
            <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">ENGINEERING SPEC</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div class="text-[11px] text-slate-600 font-medium">Solar Array Capacity</div>
              <div id="outDcKw" class="text-lg font-extrabold text-slate-900 mt-0.5 font-mono">6.4 kW</div>
              <div class="text-[10px] text-slate-600">Rated DC capacity</div>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div class="text-[11px] text-slate-600 font-medium">580W Panel Count</div>
              <div id="outPanelCount" class="text-lg font-extrabold text-slate-900 mt-0.5 font-mono">11 Panels</div>
              <div class="text-[10px] text-slate-600">580W Bifacial TOPCon</div>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div class="text-[11px] text-slate-600 font-medium">Inverter Sizing</div>
              <div id="outInverter" class="text-lg font-extrabold text-slate-900 mt-0.5 font-mono">6 kW Hybrid</div>
              <div class="text-[10px] text-slate-600">48V Pure Sine Wave</div>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200 sm:col-span-2">
              <div class="text-[11px] text-slate-600 font-medium">Required Roof Space</div>
              <div class="flex items-baseline space-x-2 mt-0.5">
                <span id="outRoofSpace" class="text-lg font-extrabold text-slate-900 font-mono">308 sq ft</span>
                <span id="outRoofMarla" class="text-xs text-slate-600 font-semibold">(~1.4 Marla)</span>
              </div>
              <div class="text-[10px] text-slate-600">Clear unshaded south/south-west exposure</div>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div class="text-[11px] text-slate-600 font-medium">Structure Rating</div>
              <div id="outStructureSpec" class="text-xs font-bold text-slate-900 mt-1">12-Gauge Galvanized</div>
              <div class="text-[10px] text-slate-600">130 km/h wind certified</div>
            </div>
          </div>

          <!-- Battery Storage Requirement -->
          <div class="mt-3 p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex justify-between items-baseline">
              <span class="text-xs font-bold text-slate-900">Night AC Battery Bank:</span>
              <span id="outBatterySpec" class="text-xs font-bold text-slate-900 font-mono">2x 5.12 kWh LiFePO4 (51.2V 100Ah)</span>
            </div>
            <p id="outBatteryNote" class="text-xs text-slate-700 mt-1 leading-relaxed">Optimal for continuous AC loads. 4,000+ deep cycle lifespan (approx. 10 years).</p>
          </div>
        </div>

        <!-- Financial Summary Card (High-Contrast Linear Style) -->
        <div class="tool-card p-5">
          <div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-200">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Financial Returns &amp; Net-Billing Payback</h2>
            <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">2026 NEPRA MODEL</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3.5 rounded-lg bg-slate-50 border border-slate-200">
            <div>
              <div class="text-[11px] text-slate-600 font-medium">Estimated Turnkey Capex</div>
              <div id="outCapexRange" class="text-sm font-extrabold text-slate-900 mt-0.5 font-mono">Rs. 9.5L – 10.7L</div>
              <div class="text-[10px] text-slate-600">Tier-1 Hardware &amp; Labor</div>
            </div>
            <div>
              <div class="text-[11px] text-slate-600 font-medium">Monthly Savings</div>
              <div id="outMonthlySavings" class="text-sm font-extrabold text-emerald-700 mt-0.5 font-mono">Rs. 46,947 / mo</div>
              <div class="text-[10px] text-slate-600">Slab avoidance</div>
            </div>
            <div>
              <div class="text-[11px] text-slate-600 font-medium">Payback Period</div>
              <div id="outPaybackPeriod" class="text-sm font-extrabold text-slate-900 mt-0.5 font-mono">~1.8 Years</div>
              <div class="text-[10px] text-slate-600">55% annual ROI</div>
            </div>
            <div>
              <div class="text-[11px] text-slate-600 font-medium">5-Year Net Profit</div>
              <div id="out5YearProfit" class="text-sm font-extrabold text-emerald-700 mt-0.5 font-mono">Rs. 18.0 Lakhs</div>
              <div class="text-[10px] text-slate-600">Cumulative net savings</div>
            </div>
          </div>
          <!-- 2026 Net-Billing Breakdown Grid -->
          <div class="mt-3.5 pt-3 border-t border-slate-200">
            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-700 mb-2">2026 Net-Billing Energy &amp; Tariff Balance</div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              <div class="p-2.5 rounded-lg bg-emerald-50/70 border border-emerald-200">
                <div class="text-[11px] font-medium text-emerald-800">Solar Self-Consumption</div>
                <div id="nbSelfConsumption" class="text-sm font-extrabold text-emerald-950 font-mono mt-0.5">~35% Solar Offset</div>
                <div class="text-[10px] text-emerald-700">Displaces top progressive retail slabs</div>
              </div>
              <div class="p-2.5 rounded-lg bg-sky-50/70 border border-sky-200">
                <div class="text-[11px] font-medium text-sky-800">Grid Export Credit (NAEPP)</div>
                <div id="nbExportCredit" class="text-sm font-extrabold text-sky-950 font-mono mt-0.5">~533 units (Rs. 11,460)</div>
                <div class="text-[10px] text-sky-700">Wholesale credit @ Rs. 21.50/kWh</div>
              </div>
              <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                <div class="text-[11px] font-medium text-slate-700">Net Post-Solar Bill</div>
                <div id="nbPostBill" class="text-sm font-extrabold text-slate-900 font-mono mt-0.5">Rs. 15,977 / mo</div>
                <div class="text-[10px] text-slate-600">Residual bill to local utility</div>
              </div>
            </div>
            <div class="mt-2.5 p-2.5 rounded-lg bg-slate-100/90 border border-slate-200 flex items-start gap-2 text-xs text-slate-700 leading-normal">
              <span class="text-emerald-700 mt-0.5 font-bold" aria-hidden="true">&#10003;</span>
              <span id="nbNote"><strong>2026 Net-Billing Calibrated:</strong> Direct daytime consumption immediately displaces top progressive slabs (~Rs. 45-60/kWh). Exported daytime solar is credited at the wholesale NAEPP rate (~Rs. 21.50/kWh), protecting payback horizons.</span>
            </div>
          </div>
        </div>

        <!-- Slab-Breaker Strategy Box -->
        <div id="sweetSpotContainer" class="p-4 rounded-xl bg-blue-50/80 border border-blue-200 text-xs text-blue-950 space-y-2.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-blue-950 uppercase tracking-wider text-[11px]">Budget Alternative: Daytime "Slab-Breaker" Setup</span>
            <span id="sweetSpotCapexSave" class="px-2 py-0.5 rounded bg-blue-100 text-blue-900 font-semibold text-[10px]">55% Lower Capex</span>
          </div>
          <p class="text-blue-900 leading-relaxed">
            If hybrid storage exceeds your upfront budget, install a smaller daytime system without night batteries:
          </p>
          <div class="grid grid-cols-3 gap-2 pt-0.5 font-mono">
            <div class="p-2.5 rounded-lg bg-white border border-blue-200">
              <div class="text-[10px] text-blue-700 font-sans font-medium">Array Sizing</div>
              <div class="text-xs font-bold text-blue-950 mt-0.5"><span id="sweetSpotKw">3.5 kW</span> (<span id="sweetSpotPanels">6 panels</span>)</div>
            </div>
            <div class="p-2.5 rounded-lg bg-white border border-blue-200">
              <div class="text-[10px] text-blue-700 font-sans font-medium">Estimated Capex</div>
              <div id="sweetSpotCost" class="text-xs font-bold text-blue-950 mt-0.5">Rs. 4.1L – 4.6L</div>
            </div>
            <div class="p-2.5 rounded-lg bg-white border border-blue-200">
              <div class="text-[10px] text-blue-700 font-sans font-medium">Monthly Savings</div>
              <div id="sweetSpotBillSave" class="text-xs font-bold text-emerald-800 mt-0.5">Rs. 29,170 / mo</div>
            </div>
          </div>
          <p class="text-[11px] text-blue-800 leading-normal">
            *Skips expensive batteries. Runs your household and ACs on solar during the day, dropping your grid consumption below 200 units to qualify for base tariff slabs.
          </p>
        </div>

        <!-- Contractor Quotation Validator ("BS Detector") -->
        <div class="tool-card p-5 space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-700">Contractor Quotation Validator</h2>
              <p class="text-[11px] text-slate-600 mt-0.5">Have a quote from a local installer? Verify if you're being overcharged.</p>
            </div>
            <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">BS DETECTOR</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
            <div>
              <label for="quoteKwInput" class="text-[11px] text-slate-700 font-medium block mb-1">Quoted Size (kW)</label>
              <input type="number" id="quoteKwInput" step="0.5" min="1" max="50" placeholder="e.g. 6.0" aria-label="Quoted solar capacity in kilowatts" class="w-full text-xs font-mono p-2 rounded-lg border border-slate-300 focus:border-slate-900 focus:outline-none bg-slate-50">
            </div>
            <div>
              <label for="quotePriceInput" class="text-[11px] text-slate-700 font-medium block mb-1">Quoted Price (PKR)</label>
              <input type="number" id="quotePriceInput" step="10000" min="50000" placeholder="e.g. 950000" aria-label="Quoted turnkey price in Pakistani Rupees" class="w-full text-xs font-mono p-2 rounded-lg border border-slate-300 focus:border-slate-900 focus:outline-none bg-slate-50">
            </div>
            <div>
              <label for="quoteSystemType" class="text-[11px] text-slate-700 font-medium block mb-1">System Scope</label>
              <select id="quoteSystemType" aria-label="Quoted system hardware scope" class="w-full text-xs p-2 rounded-lg border border-slate-300 focus:border-slate-900 focus:outline-none bg-white">
                <option value="hybrid">Hybrid + Battery Bank</option>
                <option value="ongrid">On-Grid Only (No Battery)</option>
              </select>
            </div>
          </div>

          <!-- Validator Feedback Box (Hidden by default) -->
          <div id="quoteValidatorResult" class="hidden p-3.5 rounded-lg border text-xs space-y-1.5 transition-all">
            <div class="flex items-center justify-between">
              <span id="quoteResultBadge" class="font-bold text-xs"></span>
              <span id="quoteRateDisplay" class="font-mono text-xs font-semibold text-slate-700"></span>
            </div>
            <p id="quoteResultDesc" class="text-xs leading-relaxed text-slate-700"></p>
          </div>
        </div>

        <!-- Action Buttons Row 1: WhatsApp & PDF -->
        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button id="shareWhatsAppBtn" type="button" aria-label="Share solar audit summary on WhatsApp" class="min-h-[44px] flex-1 py-2.5 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all shadow-sm cursor-pointer">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-5.46-4.45-9.92-9.91-9.92zm0 18.15c-1.47 0-2.92-.39-4.18-1.15l-.3-.18-3.11.82.83-3.04-.2-.31c-.83-1.33-1.27-2.88-1.27-4.49 0-4.54 3.7-8.24 8.24-8.24 4.54 0 8.24 3.7 8.24 8.24 0 4.54-3.7 8.25-8.25 8.25zm4.52-6.17c-.25-.12-1.47-.72-1.69-.81-.23-.09-.39-.12-.56.12-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43s-.56-1.34-.76-1.84c-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.12.17 1.77 2.71 4.3 3.8 2.52 1.09 2.52.73 2.98.69.45-.05 1.47-.6 1.68-1.18.21-.59.21-1.09.15-1.19-.06-.1-.22-.16-.47-.28z"/></svg>
            <span>Share Audit on WhatsApp</span>
          </button>
          <button id="downloadPdfBtn" type="button" aria-label="Download solar engineering audit sheet as PDF" class="min-h-[44px] flex-1 py-2.5 px-4 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all shadow-sm cursor-pointer">
            <span>Download Engineering Sheet (PDF)</span>
          </button>
        </div>

        <!-- Action Buttons Row 2: Visual Card & Contractor Tender RFP -->
        <div class="flex flex-col sm:flex-row gap-2.5 pt-1">
          <button id="downloadPngCardBtn" type="button" aria-label="Download visual audit card as PNG image" class="min-h-[44px] flex-1 py-2 px-3 rounded-lg bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-semibold text-xs flex items-center justify-center gap-1.5 transition-all shadow-2xs cursor-pointer">
            <span>Download Visual Card (PNG)</span>
          </button>
          <button id="copyTenderBtn" type="button" aria-label="Copy contractor tender RFP specification to clipboard" class="min-h-[44px] flex-1 py-2 px-3 rounded-lg bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-semibold text-xs flex items-center justify-center gap-1.5 transition-all shadow-2xs cursor-pointer">
            <span>Copy Contractor Tender Spec</span>
          </button>
        </div>

        <!-- Copy Feedback Alert -->
        <div id="copyFeedback" class="hidden text-center text-xs text-emerald-800 font-semibold py-1.5 bg-emerald-50 rounded-lg border border-emerald-200">
          &#10003; Summary copied to clipboard. Ready to paste in WhatsApp.
        </div>

      </div>
    </div>

    <!-- Editorial Guide Section -->
    <section class="mt-14 border-t border-slate-200 pt-10 text-slate-700 text-sm leading-relaxed max-w-3xl mx-auto space-y-8">
{page_def['editorial']}

      <!-- System Sizing Navigation Highway -->
      <div class="p-5 rounded-xl bg-slate-100 border border-slate-200 space-y-3">
        <h3 class="text-sm font-bold uppercase tracking-wider text-slate-800">
          Explore Solar Sizing Guides &amp; Cost Breakdowns (Pakistan 2026)
        </h3>
        <p class="text-xs text-slate-600 leading-relaxed">
          Detailed engineering specs, monthly unit yields, 580W panel counts, and turnkey cost breakdowns by system capacity:
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 pt-1 text-xs">
          <a href="/3kw-solar-system-pakistan.html" class="p-3 rounded-lg bg-white border border-slate-200 hover:border-slate-400 transition-all group block shadow-2xs">
            <div class="font-bold text-slate-900 group-hover:text-emerald-700 flex items-center justify-between">
              <span>3kW Solar System</span>
              <span>&rarr;</span>
            </div>
            <p class="text-[11px] text-slate-600 mt-1">5–6 Marla homes running fans, lights, fridge, &amp; 1 inverter AC. ~350–420 units/mo.</p>
          </a>
          <a href="/5kw-solar-system-pakistan.html" class="p-3 rounded-lg bg-white border border-slate-200 hover:border-slate-400 transition-all group block shadow-2xs">
            <div class="font-bold text-slate-900 group-hover:text-emerald-700 flex items-center justify-between">
              <span>5kW Solar System</span>
              <span>&rarr;</span>
            </div>
            <p class="text-[11px] text-slate-600 mt-1">10 Marla homes running 2 Inverter ACs + household load. ~600–750 units/mo.</p>
          </a>
          <a href="/10kw-solar-system-pakistan.html" class="p-3 rounded-lg bg-white border border-slate-200 hover:border-slate-400 transition-all group block shadow-2xs">
            <div class="font-bold text-slate-900 group-hover:text-emerald-700 flex items-center justify-between">
              <span>10kW Solar System</span>
              <span>&rarr;</span>
            </div>
            <p class="text-[11px] text-slate-600 mt-1">1 Kanal residences with 3–4 ACs &amp; net-metering. ~1,250–1,500 units/mo.</p>
          </a>
          <a href="/15kw-20kw-solar-system-pakistan.html" class="p-3 rounded-lg bg-white border border-slate-200 hover:border-slate-400 transition-all group block shadow-2xs">
            <div class="font-bold text-slate-900 group-hover:text-emerald-700 flex items-center justify-between">
              <span>15kW – 20kW Systems</span>
              <span>&rarr;</span>
            </div>
            <p class="text-[11px] text-slate-600 mt-1">Commercial plazas, schools, clinics, &amp; large joint families. ~2,000–3,000+ units/mo.</p>
          </a>
        </div>
        <div class="pt-2 flex flex-wrap gap-2 text-xs">
          <a href="/solar-panels-for-ac-pakistan.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">
            <span>Solar Panels for AC Guide</span>
          </a>
          <a href="/solar-batteries-pakistan.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">
            <span>Lithium LiFePO4 Battery Guide</span>
          </a>
          <a href="/solar-quote-validator.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium">
            <span>Contractor Quotation Validator</span>
          </a>
          <a href="/embed.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 font-medium text-emerald-800">
            <span>Free Embeddable Calculator Widget</span>
          </a>
        </div>
      </div>

      <!-- Visible FAQ Accordion Section (Google Rich Result Eligible) -->
      <div id="faq-section" class="space-y-4 pt-4">
        <h2 class="text-base sm:text-lg font-bold text-slate-900">
          Frequently Asked Questions (Solar Sizing &amp; NEPRA Tariffs)
        </h2>
        <div class="space-y-2.5">
{faq_html}
        </div>
      </div>
    </section>

  </main>

  <!-- Sticky Mobile Summary Bar (<1024px) -->
  <aside id="stickyMobileSummary" aria-label="Live Solar Sizing Summary" class="lg:hidden fixed bottom-0 left-0 right-0 z-30 bg-white/95 backdrop-blur-md border-t border-slate-200 px-4 py-2.5 sticky-mobile-bar shadow-lg flex items-center justify-between">
    <div class="flex flex-col">
      <span class="text-[10px] uppercase font-bold tracking-wider text-slate-600">Calculated System</span>
      <div class="flex items-baseline gap-1.5">
        <span id="mobileStickyKw" class="text-base font-extrabold text-slate-900 font-mono">6.4 kW</span>
        <span id="mobileStickyPanels" class="text-xs text-slate-600 font-medium">(11 panels)</span>
      </div>
      <span class="text-[11px] text-emerald-700 font-semibold">Saves <span id="mobileStickySavings">Rs. 46,947</span>/mo</span>
    </div>
    <a href="#resultsSummaryAnchor" id="mobileViewBreakdownBtn" aria-label="Scroll to detailed specifications" class="min-h-[44px] px-4 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-lg shadow-sm transition-all flex items-center gap-1.5 cursor-pointer select-none">
      <span>View Specs</span>
      <span aria-hidden="true">&darr;</span>
    </a>
  </aside>

  <!-- Footer -->
  <footer class="border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-600 mt-12">
    <div class="max-w-5xl mx-auto px-4 space-y-3">
      <div class="flex flex-wrap justify-center gap-x-4 gap-y-2 text-slate-700 font-medium text-xs sm:text-sm">
        <a href="/" class="text-slate-900 font-semibold">Solar Calculator</a>
        <a href="/ke-bill-calculator.html" class="hover:text-slate-900 transition-colors">K-Electric</a>
        <a href="/lesco-solar-calculator.html" class="hover:text-slate-900 transition-colors">LESCO</a>
        <a href="/iesco-solar-calculator.html" class="hover:text-slate-900 transition-colors">IESCO</a>
        <a href="/mepco-solar-calculator.html" class="hover:text-slate-900 transition-colors">MEPCO</a>
        <a href="/gepco-solar-calculator.html" class="hover:text-slate-900 transition-colors">GEPCO</a>
        <a href="/fesco-solar-calculator.html" class="hover:text-slate-900 transition-colors">FESCO</a>
        <a href="/pesco-solar-calculator.html" class="hover:text-slate-900 transition-colors">PESCO</a>
        <a href="/3kw-solar-system-pakistan.html" class="hover:text-slate-900 transition-colors">3kW Cost</a>
        <a href="/5kw-solar-system-pakistan.html" class="hover:text-slate-900 transition-colors">5kW Cost</a>
        <a href="/10kw-solar-system-pakistan.html" class="hover:text-slate-900 transition-colors">10kW Cost</a>
        <a href="/15kw-20kw-solar-system-pakistan.html" class="hover:text-slate-900 transition-colors">15kW-20kW Cost</a>
        <a href="/solar-panels-for-ac-pakistan.html" class="hover:text-slate-900 transition-colors">Solar for AC</a>
        <a href="/solar-batteries-pakistan.html" class="hover:text-slate-900 transition-colors">Batteries</a>
        <a href="/solar-quote-validator.html" class="hover:text-slate-900 transition-colors">Quote Validator</a>
        <a href="/about.html" class="hover:text-slate-900 transition-colors">About</a>
        <a href="/privacy-policy.html" class="hover:text-slate-900 transition-colors">Privacy</a>
        <a href="/terms.html" class="hover:text-slate-900 transition-colors">Terms</a>
      </div>
      <p class="font-medium text-slate-700">SOLARAUDIT.ONLINE &copy; 2026. Independent Solar Audit Tool.</p>
      <p class="text-slate-500">Calculations reflect NEPRA determination formulas and active wholesale hardware benchmarks in Pakistan.</p>
    </div>
  </footer>

  <!-- Core Scripts with Cache Busting -->
  <script src="js/tariff-data.js?v={ASSET_VERSION}"></script>
  <script src="js/calculator-engine.js?v={ASSET_VERSION}"></script>
  <script src="js/pdf-generator.js?v={ASSET_VERSION}"></script>
  <script src="js/visual-card.js?v={ASSET_VERSION}"></script>
  <script src="js/app.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""
    return html

# ─────────────────────────────────────────────────────────────
# 3. CSS COMPILATION & BUNDLING
# ─────────────────────────────────────────────────────────────

def compile_css():
    print(">>> Compiling standalone CSS (removing cdn.tailwindcss.com)...")
    
    # 1. Collect all classes from HTML files and JS files
    all_classes = set()
    for root, dirs, files in os.walk(WORKSPACE):
        if any(x in root for x in [".git", "__pycache__", ".agents", "test", "node_modules"]):
            continue
        for f in files:
            if f.endswith((".html", ".js")):
                with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                    for match in re.finditer(r'class="([^"]+)"|class=\'([^\']+)\'', content):
                        matched_str = match.group(1) if match.group(1) is not None else match.group(2)
                        for cls in matched_str.split():
                            all_classes.add(cls)

    # Add dynamic classes from JS and state transitions
    extra_classes = [
        "text-emerald-900", "bg-emerald-50", "border-emerald-200",
        "text-emerald-950", "text-emerald-800", "text-emerald-700",
        "bg-emerald-50/70", "bg-sky-50/70", "border-sky-200",
        "text-sky-800", "text-sky-950", "text-sky-700",
        "text-amber-900", "bg-amber-50", "border-amber-200",
        "text-rose-900", "bg-rose-50", "border-rose-200",
        "bg-slate-100/90",
        "after:absolute", "after:top-[2px]", "after:left-[2px]",
        "after:bg-white", "after:border-slate-300", "after:rounded-full",
        "after:h-4", "after:w-4", "after:transition-all",
        "peer-checked:bg-slate-900", "peer-checked:after:translate-x-full",
        "peer-checked:after:border-white",
        "hidden", "opacity-40", "pointer-events-none"
    ]
    for c in extra_classes:
        all_classes.add(c)

    classes_str = " ".join(sorted(all_classes))
    synthetic_html = f"""<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="{classes_str}">
  <div class="{classes_str}"></div>
</body>
</html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=True)
        page = browser.new_page()
        page.set_content(synthetic_html)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(600)

        tailwind_css = page.evaluate("""() => {
            const styles = Array.from(document.querySelectorAll('style'));
            return styles.map(s => s.textContent || s.innerText).join('\\n');
        }""")
        browser.close()

    # Read custom style.css
    style_css_path = os.path.join(WORKSPACE, "css", "style.css")
    custom_css = ""
    if os.path.exists(style_css_path):
        with open(style_css_path, "r", encoding="utf-8") as f:
            custom_css = f.read()

    combined_css = tailwind_css + "\n\n" + custom_css

    # Lightweight CSS minification: remove comments, extra spaces, line breaks
    minified_css = re.sub(r'/\*.*?\*/', '', combined_css, flags=re.DOTALL)
    minified_css = re.sub(r'\s+', ' ', minified_css)
    minified_css = re.sub(r'\s*([\{\}:;,>])\s*', r'\1', minified_css)
    minified_css = minified_css.replace(';}', '}').strip()

    css_output_path = os.path.join(WORKSPACE, "css", "style.min.css")
    with open(css_output_path, "w", encoding="utf-8") as f:
        f.write(minified_css)

    print(f"[OK] css/style.min.css compiled ({len(minified_css)} bytes, ~{len(minified_css)//1024} KB).")

# ─────────────────────────────────────────────────────────────
# 4. SATELLITE PAGES & STATIC PAGES BUILD
# ─────────────────────────────────────────────────────────────

def build_all_pages():
    print(">>> Generating master template pages...")
    for page in PAGES:
        html = render_master_page(page)
        file_path = os.path.join(WORKSPACE, page["filename"])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [Built] {page['filename']} -> h1: {page['h1'][:45]}...")

    # Update static pages to use style.min.css and remove tailwind cdn
    static_pages = ["about.html", "privacy-policy.html", "terms.html", "embed.html"]
    for sp in static_pages:
        sp_path = os.path.join(WORKSPACE, sp)
        if os.path.exists(sp_path):
            with open(sp_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Remove cdn.tailwindcss.com
            content = re.sub(r'<script src="https://cdn\.tailwindcss\.com"></script>\s*', '', content)
            # Remove jspdf from head if present
            content = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jspdf/[^"]+"></script>\s*', '', content)
            # Replace css/style.css with css/style.min.css?v=2026.2
            content = re.sub(r'<link rel="stylesheet" href="css/style\.css[^"]*">', f'<link rel="stylesheet" href="css/style.min.css?v={ASSET_VERSION}">', content)
            if 'css/style.min.css' not in content:
                content = content.replace('</head>', f'  <link rel="stylesheet" href="css/style.min.css?v={ASSET_VERSION}">\n</head>')

            # Replace washed-out text-slate-400 with text-slate-600
            content = content.replace('text-slate-400', 'text-slate-600')

            # Fix embed.html version query parameter and ensure noindex
            if sp == "embed.html":
                content = content.replace('widget.html?v=2026.3', f'widget.html?v={ASSET_VERSION}')
                if 'name="robots"' not in content:
                    content = content.replace('<head>', '<head>\n  <meta name="robots" content="noindex, follow">')

            with open(sp_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [Updated static] {sp}")

# ─────────────────────────────────────────────────────────────
# 5. SITEMAP GENERATOR
# ─────────────────────────────────────────────────────────────

def build_sitemap():
    print(">>> Generating sitemap.xml...")
    # Canonical URLs to include (strictly excluding embed.html and widget.html)
    sitemap_urls = [
        ("https://solaraudit.online/", "1.0", "weekly"),
        ("https://solaraudit.online/3kw-solar-system-pakistan.html", "0.9", "weekly"),
        ("https://solaraudit.online/5kw-solar-system-pakistan.html", "0.9", "weekly"),
        ("https://solaraudit.online/10kw-solar-system-pakistan.html", "0.9", "weekly"),
        ("https://solaraudit.online/15kw-20kw-solar-system-pakistan.html", "0.9", "weekly"),
        ("https://solaraudit.online/solar-panels-for-ac-pakistan.html", "0.9", "weekly"),
        ("https://solaraudit.online/solar-batteries-pakistan.html", "0.9", "weekly"),
        ("https://solaraudit.online/solar-quote-validator.html", "0.9", "weekly"),
        ("https://solaraudit.online/ke-bill-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/lesco-solar-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/iesco-solar-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/mepco-solar-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/gepco-solar-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/fesco-solar-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/pesco-solar-calculator.html", "0.8", "weekly"),
        ("https://solaraudit.online/about.html", "0.5", "monthly"),
        ("https://solaraudit.online/privacy-policy.html", "0.5", "monthly"),
        ("https://solaraudit.online/terms.html", "0.5", "monthly")
    ]

    date_str = "2026-10-02"
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio, freq in sitemap_urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{date_str}</lastmod>')
        lines.append(f'    <changefreq>{freq}</changefreq>')
        lines.append(f'    <priority>{prio}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')

    sitemap_path = os.path.join(WORKSPACE, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[OK] sitemap.xml generated with {len(sitemap_urls)} URLs (embed.html excluded).")

# ─────────────────────────────────────────────────────────────
# 6. CPANEL DEPLOYMENT ZIP PACKAGER
# ─────────────────────────────────────────────────────────────

def create_deploy_zip():
    import zipfile
    print(">>> Packaging solaraudit-deploy.zip for cPanel...")
    zip_path = os.path.join(WORKSPACE, "solaraudit-deploy.zip")
    
    files_to_include = [
        "robots.txt", "sitemap.xml", "og-image.png", "favicon.ico", "favicon.png",
        "deploy.php", ".cpanel.yml", ".htaccess", "e52226840b664cb4b1f79749c95f2915.txt"
    ]
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root HTML files
        for f in os.listdir(WORKSPACE):
            if f.endswith(".html"):
                zf.write(os.path.join(WORKSPACE, f), f)
            elif f in files_to_include and os.path.exists(os.path.join(WORKSPACE, f)):
                zf.write(os.path.join(WORKSPACE, f), f)
                
        # Add css directory
        css_dir = os.path.join(WORKSPACE, "css")
        for f in os.listdir(css_dir):
            zf.write(os.path.join(css_dir, f), os.path.join("css", f))
            
        # Add js directory
        js_dir = os.path.join(WORKSPACE, "js")
        for f in os.listdir(js_dir):
            zf.write(os.path.join(js_dir, f), os.path.join("js", f))

    zip_size = os.path.getsize(zip_path)
    print(f"[OK] solaraudit-deploy.zip packaged successfully ({zip_size} bytes, ~{zip_size//1024} KB).")

# ─────────────────────────────────────────────────────────────
# MAIN BUILD ENTRY POINT
# ─────────────────────────────────────────────────────────────

def main():
    print("==================================================")
    print("SOLARAUDIT.ONLINE - BUILD & COMPILATION PIPELINE")
    print("==================================================")
    build_all_pages()
    compile_css()
    build_sitemap()
    create_deploy_zip()
    print("==================================================")
    print("BUILD COMPLETE! ALL PAGES SYNCHRONIZED.")
    print("==================================================")

if __name__ == "__main__":
    main()

