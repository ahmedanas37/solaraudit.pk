# Reddit Communities Launch Kit (`r/pakistan`, `r/karachi`, `r/lahore`)

**Target Subreddits**:
- `r/pakistan` (Flair: `Economy / Tech / Discussion`)
- `r/karachi` (Flair: `AskKarachi / Discussion`)
- `r/lahore` (Flair: `Discussion`)

**Tone**: Honest Pakistani indie engineer / builder, anti-middleman, authentic, helpful.

---

### Post Title:
> **I built an independent, 100% free tool to calculate real solar sizing & bills under Pakistan's 2026 NEPRA progressive tariffs (No sales bias, no lead gates) — SOLARAUDIT.ONLINE**

---

### Post Body (Copy & Paste Ready):

Hey everyone,

Like most Pakistani households, my family's electricity bill has become an absolute nightmare over the past year. We've seen unit rates skyrocket past Rs. 60–70/unit for peak and upper progressive slabs on K-Electric and LESCO.

When my family started getting quotes from local solar contractors, I was shocked by the blatant misdirection:
- Sizing formulas that ignore high summer temperatures and dust derating (which drops panel yield by ~22% in Pakistani cities).
- "Zero Bill" claims that completely ignore NEPRA's Net-Billing policy (where exported daytime units are credited at ~Rs. 21/unit wholesale NAEPP, while nighttime retail imports cost Rs. 50–65/unit).
- Absurd turnkey pricing markups (contractors charging Rs. 160–180/watt for standard hardware that wholesales at Rs. 85/watt).

I'm a software engineer and energy geek, so instead of arguing with contractors one by one, I decided to build a proper, open engineering tool tailored specifically for Pakistani homeowners:

🌐 **https://solaraudit.online**

---

### What Makes This Different from Typical Contractor Websites:
1. **100% Independent & Un-Gated**:
   - No phone number requirement.
   - No email capture wall.
   - No salesman calling you 5 minutes later trying to sell you Longi panels.
   - The entire calculation engine runs 100% client-side in your browser in milliseconds.

2. **Accurate 2026 Progressive Slab Modeling**:
   - Accounts for exact progressive residential tariffs for **K-Electric, LESCO, IESCO, MEPCO, GEPCO, FESCO, and PESCO**.
   - Calculates the real financial balance between daytime self-consumption (displacing high retail slabs) and wholesale grid export credits.

3. **Contractor Quotation Validator ("BS Detector")**:
   - Already got a quote from an installer in Lahore, Karachi, or Islamabad?
   - Plug in their quoted kW and price in PKR. It instantly evaluates whether the price is within fair market wholesale benchmarks, overpriced, or suspiciously cheap (which usually indicates B-grade panels or aluminum CCA wiring).

4. **1-Click Contractor Tender RFP & Buyer Defense Dossier (PDF)**:
   - Hit "Download Engineering Sheet" to get a clean, 2-page print-ready specification.
   - Page 1 contains your technical sizing and electrical balance.
   - Page 2 contains a formal **Contractor Verification Checklist** with anti-fraud clauses (verifying Tier-1 barcodes, demanding 100% pure tinned copper wiring, grounding resistance under 5 Ohms, and a 45-day green meter SLA) plus a fillable bidding schedule.

---

### What I'd Love from the Community:
- Try plugging in your last month's bill or unit count and see if the numbers match your expectations.
- If you've already installed solar recently, let me know how your actual generation compares to the model.
- Feedback on any edge-case tariffs, commercial slabs, or 3-phase vs single-phase conversion costs you've experienced in your city.

It’s completely free and open for everyone to use: **https://solaraudit.online**

Hope this helps protect your families from getting ripped off by shady installers!
