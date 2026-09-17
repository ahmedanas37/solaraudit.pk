# SOLARAUDIT.PK

**Independent Pakistan Solar System Sizer & Electricity Bill Calculator** calibrated for the **2026 NEPRA progressive tariff determinations** (K-Electric, LESCO, IESCO, MEPCO, FESCO, PESCO).

Built as a high-speed, zero-dependency, static micro-utility application designed for instant deployment to shared hosting (cPanel), GitHub Pages, or any static web server.

---

## Key Features

1. **2026 Progressive Slab Calculation Engine**:
   * Inverse bill-to-units conversion matching protected vs. unprotected slabs, Fuel Price Adjustments (FPA), Financing Cost (FC) surcharges, fixed capacity fees, and 18% GST.
2. **Solar Array & Rooftop Sizing**:
   * Calculates DC capacity in kWp, panel count (Tier-1 580W Bifacial TOPCon), and required rooftop footprint in square feet and Marlas.
   * Derating factor applied for extreme ambient summer temperatures and dust accumulation (0.78).
3. **Night AC Battery Physics**:
   * Sizing for continuous overnight air-conditioning loads.
   * Differentiates between 85% usable Depth of Discharge (DoD) on Lithium (LiFePO4) vs. 50% max usable capacity on Deep Cycle Tubular lead-acid batteries.
4. **Contractor Quotation Validator ("BS-Detector")**:
   * Real-time benchmark tool comparing contractor quotations against wholesale hardware rates in Pakistan.
   * Flags overpriced bids and cut-corner risks (B-grade panels, 24V under-spec inverters, non-copper DC wiring).
5. **Rooftop Structure Options**:
   * Sizing for standard low-mount L2 frames vs. elevated walkable L3 pergolas (+Rs. 14/W for 12-gauge hot-dip galvanized columns).
6. **DISCO Meter Requirements**:
   * Single-Phase vs. Three-Phase selection with advisory notices on NEPRA net-metering regulations.
7. **Architectural 1-Page PDF Specification Generator**:
   * Client-side jsPDF generator producing an unbiased, print-ready "Solar Engineering Audit & Contract Specification Sheet" complete with a 7-point installer audit checklist and commercial sign-off blocks.
8. **WhatsApp Sharing**:
   * Generates a clean, copyable summary formatted for Pakistani WhatsApp groups and contractor negotiations.

---

## Tech Stack

* **Frontend**: Pure HTML5, Tailwind CSS (Utility classes), Vanilla JavaScript (ES6+ modular architecture).
* **PDF Engine**: Client-side `jsPDF` (A4 standard format).
* **Backend**: Zero server-side dependencies. 100% client-side execution.

---

## Project Structure

```
├── index.html              # Main application & SEO technical guide
├── css/
│   └── style.css           # Minimal, daylight-readable stylesheet
├── js/
│   ├── tariff-data.js      # NEPRA progressive tariff slabs & hardware costs
│   ├── calculator-engine.js# Mathematical & solar physics engine
│   ├── pdf-generator.js    # 1-page architectural PDF generator
│   └── app.js              # Reactive state manager & UI controller
├── test/
│   └── test_engine.py      # Python test suite for billing and solar math
├── .gitignore              # Standard gitignore rules
└── solaraudit-deploy.zip   # Ready-to-upload cPanel deployment package
```

---

## Deployment to cPanel

### Method 1: cPanel Git Version Control (Recommended)
1. In cPanel, navigate to **Files** > **Git Version Control**.
2. Click **Create**.
3. Set **Clone URL** to: `https://github.com/ahmedanas37/solaraudit.pk.git`.
4. Set **Repository Path**: `public_html` (or `public_html/solar`).
5. Click **Create**.
6. Whenever you push updates to GitHub, simply click **Pull or Deploy** in cPanel to update your live website instantly.

### Method 2: Manual ZIP Upload
1. Upload `solaraudit-deploy.zip` directly into `public_html/` via cPanel File Manager.
2. Extract the archive.

---

## License

MIT License. Designed for public use across Pakistan.
