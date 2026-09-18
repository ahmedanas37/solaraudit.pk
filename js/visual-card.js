/**
 * SOLARAUDIT.ONLINE - Visual Card & Contractor RFP Generator
 * Client-side HTML5 Canvas rendering for WhatsApp sharing & Contractor Tenders
 */

const VisualCard = (function() {

  function generatePngCard(state) {
    if (!state) return;

    const canvas = document.createElement("canvas");
    canvas.width = 1200;
    canvas.height = 675;
    const ctx = canvas.getContext("2d");

    // 1. Background (Clean Light Slate)
    const bgGrad = ctx.createLinearGradient(0, 0, 1200, 675);
    bgGrad.addColorStop(0, "#f8fafc");
    bgGrad.addColorStop(1, "#f1f5f9");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 1200, 675);

    // 2. Decorative Top Accent Line
    const accentGrad = ctx.createLinearGradient(0, 0, 1200, 0);
    accentGrad.addColorStop(0, "#10b981");
    accentGrad.addColorStop(0.5, "#0284c7");
    accentGrad.addColorStop(1, "#f59e0b");
    ctx.fillStyle = accentGrad;
    ctx.fillRect(0, 0, 1200, 8);

    // 3. Header Branding (Dark Crisp Typography on Light Background)
    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 34px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.fillText("SOLARAUDIT", 60, 75);
    
    ctx.fillStyle = "#64748b";
    ctx.font = "34px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.fillText(".ONLINE", 285, 75);

    // Pill Badge
    ctx.fillStyle = "#ecfdf5";
    ctx.strokeStyle = "#a7f3d0";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(60, 95, 340, 28, 6);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#047857";
    ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("INDEPENDENT AUDIT • 2026 NEPRA TARIFFS", 72, 114);

    // 4. Metric Grid (4 Pure White Cards with Light Borders)
    const cards = [
      {
        label: "RECOMMENDED SOLAR ARRAY",
        value: `${state.sizing.actualDcKw} kW DC`,
        sub: `${state.sizing.panelCount}x 580W Tier-1 Bifacial Panels`,
        color: "#0f172a"
      },
      {
        label: "TURNKEY FAIR CAPEX",
        value: `Rs. ${(state.financials.capexMin / 100000).toFixed(1)}L – ${(state.financials.capexMax / 100000).toFixed(1)}L`,
        sub: "Benchmark Hardware & Labor",
        color: "#0284c7"
      },
      {
        label: "ESTIMATED MONTHLY SAVINGS",
        value: `Rs. ${state.financials.monthlySavings.toLocaleString()}/mo`,
        sub: `Pre-Solar Bill: Rs. ${state.preBillPkr.toLocaleString()}`,
        color: "#059669"
      },
      {
        label: "ESTIMATED PAYBACK",
        value: `~${state.financials.paybackYears} Years`,
        sub: `Annual ROI: ~${(100 / state.financials.paybackYears).toFixed(0)}%`,
        color: "#d97706"
      }
    ];

    const cardWidth = 515;
    const cardHeight = 180;
    const startX = 60;
    const startY = 150;
    const gapX = 50;
    const gapY = 25;

    cards.forEach((card, idx) => {
      const col = idx % 2;
      const row = Math.floor(idx / 2);
      const x = startX + col * (cardWidth + gapX);
      const y = startY + row * (cardHeight + gapY);

      // Card Shadow (Subtle drop shadow)
      ctx.fillStyle = "rgba(15, 23, 42, 0.04)";
      ctx.beginPath();
      ctx.roundRect(x + 2, y + 4, cardWidth, cardHeight, 14);
      ctx.fill();

      // Card Background (Pure White)
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#e2e8f0";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(x, y, cardWidth, cardHeight, 14);
      ctx.fill();
      ctx.stroke();

      // Card Label
      ctx.fillStyle = "#64748b";
      ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.label, x + 25, y + 42);

      // Card Value
      ctx.fillStyle = card.color;
      ctx.font = "bold 40px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.value, x + 25, y + 105);

      // Card Subtext
      ctx.fillStyle = "#475569";
      ctx.font = "16px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.sub, x + 25, y + 145);
    });

    // 5. Footer Specs Bar (Light Slate Surface)
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 595, 1200, 80);
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, 595);
    ctx.lineTo(1200, 595);
    ctx.stroke();

    ctx.fillStyle = "#475569";
    ctx.font = "15px -apple-system, BlinkMacSystemFont, sans-serif";
    const specsSummary = `Inverter: ${state.sizing.inverterKw}kW Hybrid | Roof: ~${state.sizing.areaSqFt} sq.ft (${state.sizing.areaMarlas} Marla) | ${state.battery ? state.battery.unitSpec : "Daytime Net-Metering"}`;
    ctx.fillText(specsSummary, 60, 642);

    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 16px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("Verify Contractor Quotes at: solaraudit.online", 780, 642);

    // Trigger Download
    const dataUrl = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.download = `SolarAudit-${state.sizing.actualDcKw}kW-Audit-Card.png`;
    link.href = dataUrl;
    link.click();
  }

  function generateContractorTender(state) {
    if (!state) return "";

    const c = state;
    const dateStr = new Date().toLocaleDateString("en-PK", { day: "numeric", month: "short", year: "numeric" });
    
    return `==================================================
SOLAR SYSTEM TENDER SPECIFICATION (CLIENT COPY)
Generated via SOLARAUDIT.ONLINE — ${dateStr}
==================================================
To Solar Contractor / Installer:
Please provide your formal quotation strictly adhering to the following minimum engineering requirements:

1. ARRAY SIZING & PANELS:
   • Total DC Capacity: ${c.sizing.actualDcKw} kW DC
   • Module Count: ${c.sizing.panelCount}x 580W (Tier-1 N-Type TOPCon Bifacial)
   • Approved Brands: Longi Hi-MO X6 / Jinko Tiger Neo / JA Solar
   • Required Roof Space: ~${c.sizing.areaSqFt} sq. ft. (~${c.sizing.areaMarlas} Marla)
   • Structure Type: ${c.mountingType === "elevated" ? "Elevated Walkable L3 Pergola (8-10 ft heavy GI)" : "Standard L2 Roof Mount"}

2. INVERTER & ARCHITECTURE:
   • Inverter Capacity: ${c.sizing.inverterKw} kW Hybrid (48V Pure Sine Wave / Dual MPPT)
   • Inverter Standards: IEC/UL certified with integrated grid-tie protection

3. CABLING, EARTHING & PROTECTION (MANDATORY):
   • DC Wiring: Pure tinned copper 6mm² solar cable (single-core, UV resistant)
   • Surge Protection: Type-II DC Surge Protection Devices (SPDs) on all strings
   • AC Protection: Type-II AC SPD & dedicated copper earth pit (< 5 Ohms resistance)

4. BATTERY STORAGE:
   • ${c.battery ? `Storage Target: ${c.battery.unitSpec} (${c.battery.batteryPreference === "lithium" ? "48V LiFePO4 Lithium" : "Deep Cycle Tubular"})` : "None (Daytime Net-Metering Configuration)"}

5. FAIR MARKET TURNKEY BUDGET:
   • Target Capex Range: Rs. ${(c.financials.capexMin / 100000).toFixed(1)} Lakhs – ${(c.financials.capexMax / 100000).toFixed(1)} Lakhs

Note: Quotations exceeding standard wholesale benchmarks or substituting CCA (copper-clad aluminum) wiring will be rejected upon audit.
Client Verification Tool: https://solaraudit.online/solar-quote-validator.html`;
  }

  const visualCardObj = {
    generatePngCard,
    generateContractorTender
  };

  if (typeof window !== "undefined") {
    window.VisualCard = visualCardObj;
  }
  return visualCardObj;

})();
