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

    // 1. Background Gradient
    const bgGrad = ctx.createLinearGradient(0, 0, 1200, 675);
    bgGrad.addColorStop(0, "#0f172a");
    bgGrad.addColorStop(1, "#1e293b");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 1200, 675);

    // 2. Decorative Top Accent Line
    const accentGrad = ctx.createLinearGradient(0, 0, 1200, 0);
    accentGrad.addColorStop(0, "#10b981");
    accentGrad.addColorStop(0.5, "#3b82f6");
    accentGrad.addColorStop(1, "#f59e0b");
    ctx.fillStyle = accentGrad;
    ctx.fillRect(0, 0, 1200, 8);

    // 3. Header Branding
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 34px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.fillText("SOLARAUDIT", 60, 75);
    
    ctx.fillStyle = "#94a3b8";
    ctx.font = "34px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.fillText(".ONLINE", 285, 75);

    // Badge
    ctx.fillStyle = "#10b981";
    ctx.font = "bold 16px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("INDEPENDENT AUDIT • 2026 NEPRA TARIFFS", 60, 110);

    // 4. Metric Grid (4 Cards)
    const cards = [
      {
        label: "RECOMMENDED SOLAR ARRAY",
        value: `${state.sizing.actualDcKw} kW DC`,
        sub: `${state.sizing.panelCount}x 580W Tier-1 Bifacial Panels`,
        color: "#ffffff"
      },
      {
        label: "TURNKEY FAIR CAPEX",
        value: `Rs. ${(state.financials.capexMin / 100000).toFixed(1)}L – ${(state.financials.capexMax / 100000).toFixed(1)}L`,
        sub: "Benchmark Hardware & Labor",
        color: "#38bdf8"
      },
      {
        label: "ESTIMATED MONTHLY SAVINGS",
        value: `Rs. ${state.financials.monthlySavings.toLocaleString()}/mo`,
        sub: `Pre-Solar: Rs. ${state.preBillPkr.toLocaleString()}`,
        color: "#34d399"
      },
      {
        label: "ESTIMATED PAYBACK",
        value: `~${state.financials.paybackYears} Years`,
        sub: `Annual ROI: ~${(100 / state.financials.paybackYears).toFixed(0)}%`,
        color: "#fbbf24"
      }
    ];

    const cardWidth = 515;
    const cardHeight = 180;
    const startX = 60;
    const startY = 160;
    const gapX = 50;
    const gapY = 30;

    cards.forEach((card, idx) => {
      const col = idx % 2;
      const row = Math.floor(idx / 2);
      const x = startX + col * (cardWidth + gapX);
      const y = startY + row * (cardHeight + gapY);

      // Card Background
      ctx.fillStyle = "rgba(30, 41, 59, 0.7)";
      ctx.strokeStyle = "rgba(148, 163, 184, 0.2)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(x, y, cardWidth, cardHeight, 14);
      ctx.fill();
      ctx.stroke();

      // Card Label
      ctx.fillStyle = "#94a3b8";
      ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.label, x + 25, y + 42);

      // Card Value
      ctx.fillStyle = card.color;
      ctx.font = "bold 40px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.value, x + 25, y + 105);

      // Card Sub
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "16px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.sub, x + 25, y + 145);
    });

    // 5. Footer Specs Bar
    ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
    ctx.fillRect(0, 595, 1200, 80);
    ctx.strokeStyle = "rgba(148, 163, 184, 0.2)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, 595);
    ctx.lineTo(1200, 595);
    ctx.stroke();

    ctx.fillStyle = "#94a3b8";
    ctx.font = "15px -apple-system, BlinkMacSystemFont, sans-serif";
    const specsSummary = `Inverter: ${state.sizing.inverterKw}kW Hybrid | Roof: ~${state.sizing.areaSqFt} sq.ft (${state.sizing.areaMarlas} Marla) | ${state.battery ? state.battery.unitSpec : "Daytime Net-Metering"}`;
    ctx.fillText(specsSummary, 60, 642);

    ctx.fillStyle = "#ffffff";
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
