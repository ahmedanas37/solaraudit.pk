/**
 * SOLARAUDIT.ONLINE - Professional Client-Side PDF Generator
 * Generates an impeccably balanced 1-Page "Solar Engineering Audit & Specification Sheet"
 * Uses window.jspdf (A4 format: 210mm x 297mm)
 */

const PdfGenerator = (function () {
  function ensureJsPdfLoaded(callback, onError) {
    if (window.jspdf && window.jspdf.jsPDF) {
      callback();
      return;
    }
    const existing = document.getElementById("jspdf-script");
    if (existing) {
      if (window.jspdf && window.jspdf.jsPDF) {
        callback();
      } else {
        existing.addEventListener("load", () => callback());
        existing.addEventListener("error", (e) => {
          if (typeof onError === "function") onError(e);
        });
      }
      return;
    }
    const script = document.createElement("script");
    script.id = "jspdf-script";
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js";
    script.onload = () => callback();
    script.onerror = () => {
      // Try fallback to unpkg CDN if cdnjs fails
      const fallbackScript = document.createElement("script");
      fallbackScript.id = "jspdf-script-fallback";
      fallbackScript.src = "https://unpkg.com/jspdf@2.5.1/dist/jspdf.umd.min.js";
      fallbackScript.onload = () => callback();
      fallbackScript.onerror = (err) => {
        alert("Could not load PDF generation library. Please check your internet connection and ad-blocker settings.");
        if (typeof onError === "function") onError(err);
      };
      document.head.appendChild(fallbackScript);
    };
    document.head.appendChild(script);
  }

  function generateSpecificationSheet(calcState, onComplete, onError) {
    ensureJsPdfLoaded(
      () => {
        try {
          renderPdf(calcState);
        } catch (err) {
          console.error("PDF rendering error:", err);
          if (typeof onError === "function") onError(err);
        } finally {
          if (typeof onComplete === "function") onComplete();
        }
      },
      (err) => {
        if (typeof onError === "function") onError(err);
        if (typeof onComplete === "function") onComplete();
      }
    );
  }

  function renderPdf(calcState) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4"
    });

    // Color Palette: Clean, professional engineering print palette
    const slate900 = [15, 23, 42];   // Primary headings & values
    const slate800 = [30, 41, 59];   // Text
    const slate700 = [51, 65, 85];   // Body subheadings
    const slate600 = [71, 85, 105];  // Secondary text & notes
    const slate500 = [100, 116, 139];// Labels
    const slate300 = [203, 213, 225];// Box borders
    const slate200 = [226, 232, 240];// Cell borders
    const slate100 = [241, 245, 249];// Header fill
    const slate50  = [248, 250, 252];// Zebra fill

    const left = 14;
    const right = 196;
    const contentWidth = right - left; // 182mm

    // ─────────────────────────────────────────────────────────────
    // 1. TOP HEADER & LETTERHEAD (Symmetrical 2-Row Alignment)
    // ─────────────────────────────────────────────────────────────
    // Top decorative bar
    doc.setFillColor(slate900[0], slate900[1], slate900[2]);
    doc.rect(left, 10, contentWidth, 1.5, "F");

    const refCode = `SA-${Math.floor(100000 + Math.random() * 900000)}`;
    const dateStr = new Date().toLocaleDateString("en-GB");
    const cityName = calcState.sizing.city || "Karachi (K-Electric)";

    // Row 1: Brand & Reference (y = 17.5)
    doc.setFont("helvetica", "bold");
    doc.setFontSize(14.5);
    doc.setTextColor(slate900[0], slate900[1], slate900[2]);
    doc.text("SOLARAUDIT.ONLINE", left, 17.5);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(slate500[0], slate500[1], slate500[2]);
    doc.text(`Audit Ref: ${refCode}  •  Issued: ${dateStr}`, right, 17.5, { align: "right" });

    // Row 2: Subtitle & Standard Determination (y = 22.5)
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8);
    doc.setTextColor(slate600[0], slate600[1], slate600[2]);
    doc.text("Independent Solar Audit & Engineering Specification", left, 22.5);

    doc.setFontSize(7.5);
    doc.setTextColor(slate500[0], slate500[1], slate500[2]);
    doc.text(`Standard: NEPRA 2026 Tariff  •  ${cityName}`, right, 22.5, { align: "right" });

    // Divider line
    doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
    doc.setLineWidth(0.35);
    doc.line(left, 26.0, right, 26.0);

    // Helper: Draw Section Header
    function drawSectionHeader(yPos, titleNumber, titleText) {
      doc.setFillColor(slate100[0], slate100[1], slate100[2]);
      doc.setDrawColor(slate300[0], slate300[1], slate300[2]);
      doc.rect(left, yPos, contentWidth, 6, "FD");

      doc.setFont("helvetica", "bold");
      doc.setFontSize(8.5);
      doc.setTextColor(slate900[0], slate900[1], slate900[2]);
      doc.text(`${titleNumber}. ${titleText.toUpperCase()}`, left + 3, yPos + 4.2);
    }

    // Helper: Draw Key-Value Table Cell
    function drawCell(x, y, w, h, label, value) {
      doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
      doc.setFillColor(255, 255, 255);
      doc.rect(x, y, w, h, "FD");

      doc.setFont("helvetica", "normal");
      doc.setFontSize(7);
      doc.setTextColor(slate500[0], slate500[1], slate500[2]);
      doc.text(label, x + 2.5, y + 3.8);

      doc.setFont("helvetica", "bold");
      doc.setFontSize(8);
      doc.setTextColor(slate900[0], slate900[1], slate900[2]);
      doc.text(String(value), x + 2.5, y + 8.2);
    }

    // ─────────────────────────────────────────────────────────────
    // 2. SECTION 1: ENERGY BASELINE & SYSTEM SIZING (Flawless 3x3 Grid)
    // ─────────────────────────────────────────────────────────────
    let curY = 29.5;
    drawSectionHeader(curY, "1", "Energy Baseline & Solar Array Sizing");
    curY += 6;

    const colW3 = contentWidth / 3; // Exactly 60.66mm
    const rowH = 10.5;

    // Row 1: Baseline Energy (3 cells)
    drawCell(left, curY, colW3, rowH, "Current Monthly Bill", `Rs. ${calcState.preBillPkr.toLocaleString()}`);
    drawCell(left + colW3, curY, colW3, rowH, "Monthly Grid Consumption", `~${calcState.monthlyUnits.toLocaleString()} kWh / Units`);
    drawCell(left + (colW3 * 2), curY, colW3, rowH, "Grid Provider / Tariff", calcState.sizing.city || "Karachi (K-Electric)");
    curY += rowH;

    // Row 2: Solar Hardware (3 cells)
    drawCell(left, curY, colW3, rowH, "Recommended Solar Capacity", `${calcState.sizing.actualDcKw} kWp DC Array`);
    drawCell(left + colW3, curY, colW3, rowH, "PV Modules (580W N-Type)", `${calcState.sizing.panelCount} Panels (Bifacial TOPCon)`);
    drawCell(left + (colW3 * 2), curY, colW3, rowH, "Roof Area Required", `~${calcState.sizing.areaSqFt} sq ft (~${calcState.sizing.areaMarlas} Marla)`);
    curY += rowH;

    // Row 3: Inverter, Structure & Meter (3 cells - perfectly aligned with rows 1 & 2!)
    const structLabel = calcState.mountingType === "elevated" ? "Elevated L3 Pergola (Walkable)" : "Standard L2 Low-Mount";
    const meterLabel = calcState.meterType === "single_phase" ? "Single-Phase (Upgrade Req.)" : "3-Phase Export Ready";
    drawCell(left, curY, colW3, rowH, "Inverter Architecture", `${calcState.sizing.inverterKw} kW Hybrid (48V Pure Sine)`);
    drawCell(left + colW3, curY, colW3, rowH, "Mounting Structure", structLabel);
    drawCell(left + (colW3 * 2), curY, colW3, rowH, "Grid Connection / Meter", meterLabel);
    curY += rowH + 3.5;

    // ─────────────────────────────────────────────────────────────
    // 3. SECTION 2: NIGHT ENERGY STORAGE SPECIFICATIONS
    // ─────────────────────────────────────────────────────────────
    drawSectionHeader(curY, "2", "Night Storage Specifications (AC & Essential Load)");
    curY += 6;

    const colW2 = contentWidth / 2; // Exactly 91mm

    if (calcState.battery) {
      drawCell(left, curY, colW2, rowH, "Night AC Backup Target", `${calcState.battery.acCount} Inverter AC(s) for ${calcState.battery.nightHours} Hours`);
      drawCell(left + colW2, curY, colW2, rowH, "Total Required Usable Energy", `${calcState.battery.totalEnergyKwh} kWh Overnight`);
      curY += rowH;

      drawCell(left, curY, colW2, rowH, "Recommended Battery Bank", calcState.battery.unitSpec);
      drawCell(left + colW2, curY, colW2, rowH, "Design Usable Lifespan", `~${calcState.battery.lifespanYears} Years (${calcState.battery.batteryPreference === "lithium" ? "4,000+ Cycles" : "800 Cycles"})`);
      curY += rowH;

      // Engineering Warning Box
      const isLithium = calcState.battery.batteryPreference === "lithium";
      doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
      doc.setFillColor(slate50[0], slate50[1], slate50[2]);
      doc.rect(left, curY, contentWidth, 7, "FD");

      doc.setFont("helvetica", "bold");
      doc.setFontSize(7);
      doc.setTextColor(slate900[0], slate900[1], slate900[2]);
      doc.text("ENGINEERING ADVISORY:", left + 2.5, curY + 4.5);

      doc.setFont("helvetica", "normal");
      doc.setTextColor(slate600[0], slate600[1], slate600[2]);
      doc.text(calcState.battery.warningNote, left + 40, curY + 4.5, { maxWidth: contentWidth - 43 });
      curY += 7 + 3.5;
    } else {
      drawCell(left, curY, contentWidth, rowH, "Battery Storage Configuration", "None Configured (Daytime On-Grid Net-Metering Only. System shuts down during grid outages).");
      curY += rowH + 3.5;
    }

    // ─────────────────────────────────────────────────────────────
    // 4. SECTION 3: FAIR MARKET CAPEX & PAYBACK BENCHMARKS
    // ─────────────────────────────────────────────────────────────
    drawSectionHeader(curY, "3", "Fair Market Turnkey Capex & Financial Estimates");
    curY += 6;

    const colW4 = contentWidth / 4; // Exactly 45.5mm
    const minLakhs = (calcState.financials.capexMin / 100000).toFixed(2);
    const maxLakhs = (calcState.financials.capexMax / 100000).toFixed(2);

    drawCell(left, curY, colW4, rowH, "Estimated Turnkey Capex", `Rs. ${minLakhs}L – ${maxLakhs}L`);
    drawCell(left + colW4, curY, colW4, rowH, "Est. Monthly Savings", `Rs. ${calcState.financials.monthlySavings.toLocaleString()} / mo`);
    drawCell(left + (colW4 * 2), curY, colW4, rowH, "Payback Horizon", `~${calcState.financials.paybackYears} Yrs (${calcState.financials.paybackMonths} Mo)`);
    drawCell(left + (colW4 * 3), curY, colW4, rowH, "5-Year Cumulative Gain", `Rs. ${calcState.financials.fiveYearNetSavings.toLocaleString()}`);
    curY += rowH;

    // Row 2: 2026 NEPRA Net-Billing Financial Balance
    const nb = calcState.financials.netBilling || {};
    const sysTypeLabel = nb.systemType === "hybrid_storage" ? "Hybrid LiFePO4" : "On-Grid Net-Billing";
    const exportUnits = nb.gridExportUnits || 0;
    const exportCredit = nb.exportCreditPkr || 0;
    const selfConsPct = nb.selfConsumptionPercent || 0;
    const postBill = calcState.financials.postBillPkr || 0;

    drawCell(left, curY, colW4, rowH, "2026 Regulatory Regime", `${sysTypeLabel}`);
    drawCell(left + colW4, curY, colW4, rowH, "Self-Consumption Offset", `${selfConsPct}% Daylight & Storage`);
    drawCell(left + (colW4 * 2), curY, colW4, rowH, "Monthly Grid Export", `${exportUnits} kWh (Rs. ${exportCredit.toLocaleString()})`);
    drawCell(left + (colW4 * 3), curY, colW4, rowH, "Post-Solar Residual Bill", `Rs. ${postBill.toLocaleString()} / mo`);
    curY += rowH + 3.5;

    // ─────────────────────────────────────────────────────────────
    // 5. SECTION 4: INSTALLER AUDIT CHECKLIST (Verify Before Advance)
    // ─────────────────────────────────────────────────────────────
    drawSectionHeader(curY, "4", "Installer Audit Checklist (Mandatory Pre-Advance Checks)");
    curY += 6;

    const auditChecks = [
      {
        item: "PV Modules:",
        desc: "Tier-1 Bloomberg certified (Jinko, Longi, JA, Trina) with genuine serial barcode scanned on flash-test database."
      },
      {
        item: "Inverter Voltage:",
        desc: "48V system architecture (Avoid 24V inverters for inductive loads exceeding 2.5 kW to prevent thermal shutdown)."
      },
      {
        item: "DC Cabling:",
        desc: "TUV-certified double-insulated pure copper 6mm² solar wire (Reject copper-clad aluminum / sub-standard wiring)."
      },
      {
        item: "Mounting Frame:",
        desc: calcState.mountingType === "elevated"
          ? "Heavy-gauge hot-dip galvanized (GI) elevated L3 pergola anchored for 120 km/h wind gusts."
          : "Hot-dip galvanized (GI) or anodized L2 aluminum frame engineered for 120 km/h wind gusts."
      },
      {
        item: "DC Protection:",
        desc: "Separate 1000V DC miniature circuit breakers & Type-II DC Surge Protection Devices (SPD) installed per PV string."
      },
      {
        item: "Earthing / Grounding:",
        desc: "Dedicated earthing pit for surge arrester and AC/DC chassis grounding with measured resistance verified below 5 Ohms."
      },
      {
        item: "Net-Metering Guarantee:",
        desc: calcState.meterType === "single_phase"
          ? "DISCO 3-Phase conversion and load extension demand notice paperwork submitted in writing."
          : "DISCO bi-directional green meter documentation, testing, and approval timeline explicitly bound in writing."
      }
    ];

    const checkRowH = 6.4;
    doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
    doc.rect(left, curY, contentWidth, auditChecks.length * checkRowH, "S");

    auditChecks.forEach((c, idx) => {
      const rowY = curY + (idx * checkRowH);
      
      // Alternate zebra row shading
      if (idx % 2 === 0) {
        doc.setFillColor(slate50[0], slate50[1], slate50[2]);
        doc.rect(left + 0.2, rowY + 0.2, contentWidth - 0.4, checkRowH - 0.4, "F");
      }

      // Checkbox square
      doc.setDrawColor(slate500[0], slate500[1], slate500[2]);
      doc.setFillColor(255, 255, 255);
      doc.rect(left + 3, rowY + 1.8, 3, 3, "FD");

      // Item Bold Prefix
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.2);
      doc.setTextColor(slate900[0], slate900[1], slate900[2]);
      doc.text(c.item, left + 8, rowY + 4.3);

      // Description
      const prefixWidth = doc.getTextWidth(c.item) + 1.5;
      doc.setFont("helvetica", "normal");
      doc.setFontSize(7.0);
      doc.setTextColor(slate600[0], slate600[1], slate600[2]);
      doc.text(c.desc, left + 8 + prefixWidth, rowY + 4.3);
    });

    curY += (auditChecks.length * checkRowH) + 3.5;

    // ─────────────────────────────────────────────────────────────
    // 6. SECTION 5: COMMERCIAL VERIFICATION & SIGN-OFF (Clean White Boxes)
    // ─────────────────────────────────────────────────────────────
    drawSectionHeader(curY, "5", "Pre-Contract Verification & Engineering Sign-Off");
    curY += 6;

    const signBoxW = (contentWidth - 4) / 2; // Exactly 89mm
    const signBoxH = 35;

    // IMPORTANT: Explicitly reset fill color and draw color so no dark fills occur!
    doc.setDrawColor(slate300[0], slate300[1], slate300[2]);
    doc.setFillColor(255, 255, 255);

    // Box A: Homeowner / Client
    doc.rect(left, curY, signBoxW, signBoxH, "FD");

    doc.setFont("helvetica", "bold");
    doc.setFontSize(8);
    doc.setTextColor(slate900[0], slate900[1], slate900[2]);
    doc.text("CLIENT / HOMEOWNER ACKNOWLEDGEMENT", left + 3.5, curY + 5);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(slate600[0], slate600[1], slate600[2]);
    doc.text("Client Name: _________________________________", left + 3.5, curY + 12);
    doc.text("CNIC / Phone: ________________________________", left + 3.5, curY + 19);
    doc.text("Signature: ___________________ Date: ___________", left + 3.5, curY + 28);

    // Box B: Solar EPC Contractor / Installer (EXPLICIT WHITE FILL!)
    const boxBX = left + signBoxW + 4;
    doc.setDrawColor(slate300[0], slate300[1], slate300[2]);
    doc.setFillColor(255, 255, 255);
    doc.rect(boxBX, curY, signBoxW, signBoxH, "FD");

    doc.setFont("helvetica", "bold");
    doc.setFontSize(8);
    doc.setTextColor(slate900[0], slate900[1], slate900[2]);
    doc.text("SOLAR EPC CONTRACTOR / INSTALLER", boxBX + 3.5, curY + 5);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(slate600[0], slate600[1], slate600[2]);
    doc.text("Company Name: ______________________________", boxBX + 3.5, curY + 12);
    doc.text("Rep Name / Phone: ___________________________", boxBX + 3.5, curY + 19);
    doc.text("Agreed Turnkey Price: Rs. ____________________", boxBX + 3.5, curY + 25);
    doc.text("Stamp & Signature: __________________________", boxBX + 3.5, curY + 31);

    // ─────────────────────────────────────────────────────────────
    // 7. FOOTER (Zero Overlap, Clean 2-Line Layout)
    // ─────────────────────────────────────────────────────────────
    const footerY = 283.5;
    doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
    doc.setLineWidth(0.3);
    doc.line(left, footerY, right, footerY);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(6.8);
    doc.setTextColor(slate500[0], slate500[1], slate500[2]);

    // Line 1
    doc.text("SOLARAUDIT.ONLINE • Page 1 of 2 • Solar Engineering Audit & Specification Sheet", left, footerY + 3.8);
    doc.text("Verify or recalculate online: https://solaraudit.online", right, footerY + 3.8, { align: "right" });

    // Line 2
    doc.text("Calculations calibrated against NEPRA 2026 tariff determinations and wholesale equipment benchmarks in Pakistan.", left, footerY + 7.2);
    doc.text(`Doc ID: ${refCode}`, right, footerY + 7.2, { align: "right" });

    // ─────────────────────────────────────────────────────────────
    // 8. PAGE 2: CONTRACTOR TENDER SPECIFICATION & BUYER'S DEFENSE
    // ─────────────────────────────────────────────────────────────
    doc.addPage("a4", "portrait");

    // Decorative top bar
    doc.setFillColor(slate900[0], slate900[1], slate900[2]);
    doc.rect(left, 10, contentWidth, 1.5, "F");

    // Row 1: Brand & Reference
    doc.setFont("helvetica", "bold");
    doc.setFontSize(14.5);
    doc.setTextColor(slate900[0], slate900[1], slate900[2]);
    doc.text("SOLARAUDIT.ONLINE", left, 17.5);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(slate500[0], slate500[1], slate500[2]);
    doc.text(`Audit Ref: ${refCode}  •  Page 2 of 2  •  ${dateStr}`, right, 17.5, { align: "right" });

    // Row 2: Subtitle
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8);
    doc.setTextColor(slate600[0], slate600[1], slate600[2]);
    doc.text("Annexure B: Contractor Tender RFP & Hardware Verification Standards", left, 22.5);

    doc.setFontSize(7.5);
    doc.setTextColor(slate500[0], slate500[1], slate500[2]);
    doc.text(`Target City: ${cityName}  •  Competitive EPC Bidding`, right, 22.5, { align: "right" });

    // Divider line
    doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
    doc.setLineWidth(0.35);
    doc.line(left, 26.0, right, 26.0);

    let p2Y = 30.0;

    // SECTION 6: MANDATORY BILL OF QUANTITIES (BoQ) SIZING TARGETS
    drawSectionHeader(p2Y, "6", "Mandatory Engineering Scope & Hardware Sizing Targets");
    p2Y += 6;

    const rowH2 = 9.5;
    const p2ColW = contentWidth / 2;

    const boqItems = [
      { l1: "Target DC Array Capacity", v1: `${calcState.sizing.actualDcKw} kW DC (${calcState.sizing.panelCount}x 580W)`, l2: "Approved PV Modules", v2: "Tier-1 N-Type TOPCon Bifacial" },
      { l1: "Inverter Specification", v1: `${calcState.sizing.inverterKw} kW Hybrid (Dual MPPT, IP65)`, l2: "Mounting Structure", v2: calcState.mountingType === "elevated" ? "Elevated Walkable L3 Pergola (8-10ft)" : "Standard L2 Ground / Low Profile" },
      { l1: "Energy Storage Scope", v1: calcState.battery ? calcState.battery.unitSpec : "None (Daytime Net-Metering)", l2: "Fair Turnkey Target Budget", v2: `Rs. ${(calcState.financials.capexMin / 100000).toFixed(1)}L – ${(calcState.financials.capexMax / 100000).toFixed(1)} Lakhs` },
      { l1: "Grid Meter Phase Conversion", v1: calcState.meterType === "single_phase" ? "Single-Phase (3-Phase Upgrade Mandated)" : "3-Phase Ready (Net-Metering)", l2: "Estimated Daylight Yield", v2: `~${calcState.monthlyUnits} Units/mo Generation` }
    ];

    boqItems.forEach((r, idx) => {
      const y = p2Y + idx * rowH2;
      drawCell(left, y, p2ColW, rowH2, r.l1, r.v1);
      drawCell(left + p2ColW, y, p2ColW, rowH2, r.l2, r.v2);
    });
    p2Y += boqItems.length * rowH2 + 4.5;

    // SECTION 7: HARDWARE INTEGRITY & FRAUD-PREVENTION CLAUSES (Buyer's Shield)
    drawSectionHeader(p2Y, "7", "Mandatory EPC Hardware Verification Clauses (Zero-Tolerance)");
    p2Y += 6;

    const clauses = [
      { code: "CLAUSE 7.1", title: "Tier-1 Barcode Authenticity", text: "All modules must carry laser-etched serial barcodes verifiable via official manufacturer database (Longi, Jinko, JA Solar, Canadian Solar). Re-labeled or B-grade flash-test modules will result in immediate contract cancellation and refund." },
      { code: "CLAUSE 7.2", title: "100% Pure Tinned Copper DC Cabling", text: "DC string wiring must strictly be 100% pure annealed tinned copper (min 6mm², double-insulated, UV-resistant XLPE). Copper-clad aluminum (CCA) or undersized 4mm² wire on long runs will be rejected upon site electrical inspection." },
      { code: "CLAUSE 7.3", title: "Comprehensive Surge Protection & Earthing", text: "Installer must provide genuine Type-II DC SPDs for each MPPT tracker, Type-II AC SPD in DB, and dedicated copper earthing with measured soil resistance under 5.0 Ohms certified with a digital earth tester." },
      { code: "CLAUSE 7.4", title: "Neutral-to-Ground Bonding & Grid Safety", text: "Inverter AC output must maintain zero floating voltage (neutral-to-ground voltage < 2.0V) to prevent appliance compressor damage. Anti-islanding grid disconnection must be verified prior to commissioning." },
      { code: "CLAUSE 7.5", title: "Net-Metering Regulatory SLA & Green Meter", text: "The EPC contractor is contractually responsible for end-to-end DISCO documentation, preparation of Single-Line Diagrams (SLD), NEPRA SRO compliance, and green meter installation within 45 days of roof mechanical completion." },
      { code: "CLAUSE 7.6", title: "Linear Output & Equipment Warranties", text: "Deliverable includes: 25-Year 84.8% minimum linear panel output warranty, 5-Year full inverter replacement warranty, and 1-Year on-site EPC workmanship guarantee covering structural mounts and weather seals." }
    ];

    const clauseH = 14.5;
    clauses.forEach((c, idx) => {
      const rowY = p2Y + idx * clauseH;
      doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
      doc.setFillColor(idx % 2 === 0 ? 255 : slate50[0], idx % 2 === 0 ? 255 : slate50[1], idx % 2 === 0 ? 255 : slate50[2]);
      doc.rect(left, rowY, contentWidth, clauseH, "FD");

      // Checkbox square
      doc.setDrawColor(slate500[0], slate500[1], slate500[2]);
      doc.setFillColor(255, 255, 255);
      doc.rect(left + 3, rowY + 3.5, 3.5, 3.5, "FD");

      // Clause Tag
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.2);
      doc.setTextColor(slate900[0], slate900[1], slate900[2]);
      doc.text(`${c.code}: ${c.title.toUpperCase()}`, left + 9, rowY + 5.2);

      // Clause Body Text (wrapped)
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.8);
      doc.setTextColor(slate600[0], slate600[1], slate600[2]);
      const splitText = doc.splitTextToSize(c.text, contentWidth - 12);
      doc.text(splitText, left + 9, rowY + 9.2);
    });
    p2Y += clauses.length * clauseH + 4.5;

    // SECTION 8: CONTRACTOR BIDDING SCHEDULE & QUOTATION SUBMISSION
    drawSectionHeader(p2Y, "8", "Contractor Price & Equipment Tender Schedule (To Be Filled by Installer)");
    p2Y += 6;

    const bidTableH = 34;
    doc.setDrawColor(slate300[0], slate300[1], slate300[2]);
    doc.setFillColor(255, 255, 255);
    doc.rect(left, p2Y, contentWidth, bidTableH, "FD");

    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(slate700[0], slate700[1], slate700[2]);

    // Row 1
    doc.text("Quoted Module Brand & Model: ___________________________", left + 4, p2Y + 6);
    doc.text("Total Quoted Panels: ______ x ______ Watts", left + p2ColW + 4, p2Y + 6);

    // Row 2
    doc.text("Quoted Inverter Brand & Model: __________________________", left + 4, p2Y + 13);
    doc.text("Inverter Warranty: ______ Years Full Replacement", left + p2ColW + 4, p2Y + 13);

    // Row 3
    doc.text("DC Cable Brand (6mm² Tinned Cu): _______________________", left + 4, p2Y + 20);
    doc.text("Battery Bank Quoted (if any): __________________________", left + p2ColW + 4, p2Y + 20);

    // Row 4
    doc.setFont("helvetica", "bold");
    doc.text("TOTAL ALL-INCLUSIVE TURNKEY PRICE: Rs. _________________", left + 4, p2Y + 28);
    doc.setFont("helvetica", "normal");
    doc.text("Agreed Completion Timeline: ______ Days | Stamp: [           ]", left + p2ColW + 4, p2Y + 28);

    // SECTION 9: BUYER AUDIT & COMPLAINT ADVISORY
    p2Y += bidTableH + 3.5;
    doc.setFillColor(slate100[0], slate100[1], slate100[2]);
    doc.setDrawColor(slate300[0], slate300[1], slate300[2]);
    doc.rect(left, p2Y, contentWidth, 11, "FD");

    doc.setFont("helvetica", "bold");
    doc.setFontSize(7.2);
    doc.setTextColor(slate900[0], slate900[1], slate900[2]);
    doc.text("INDEPENDENT QUOTATION VALIDATION & NEPRA CONSUMER ADVISORY:", left + 3.5, p2Y + 4.2);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(6.7);
    doc.setTextColor(slate600[0], slate600[1], slate600[2]);
    doc.text("Homeowners: Enter the contractor's quoted price into our automated BS Detector at https://solaraudit.online/solar-quote-validator.html", left + 3.5, p2Y + 8.2);

    // PAGE 2 FOOTER
    doc.setDrawColor(slate200[0], slate200[1], slate200[2]);
    doc.setLineWidth(0.3);
    doc.line(left, footerY, right, footerY);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(6.8);
    doc.setTextColor(slate500[0], slate500[1], slate500[2]);

    doc.text("SOLARAUDIT.ONLINE • Page 2 of 2 • Annexure B: Contractor Tender RFP Dossier", left, footerY + 3.8);
    doc.text("Verify or recalculate online: https://solaraudit.online", right, footerY + 3.8, { align: "right" });

    doc.text("Independent consumer protection standard. Zero contractor commercial interest. Free public access across Pakistan.", left, footerY + 7.2);
    doc.text(`Doc ID: ${refCode}`, right, footerY + 7.2, { align: "right" });

    // Save PDF
    if (!calcState.skipAutoDownload) {
      doc.save(`SolarAudit-Specification-${Date.now().toString().slice(-4)}.pdf`);
    }
    return doc;
  }

  const pdfGenObj = {
    generateSpecificationSheet
  };

  if (typeof window !== "undefined") {
    window.PdfGenerator = pdfGenObj;
  }
  return pdfGenObj;
})();

if (typeof module !== "undefined" && module.exports) {
  module.exports = PdfGenerator;
}
