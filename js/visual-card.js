/**
 * SOLARAUDIT.ONLINE - Visual Card & Contractor RFP Generator
 * Client-side HTML5 Canvas rendering for WhatsApp sharing & Contractor Tenders
 * Calibrated for 2026 NEPRA progressive tariff slabs
 */

const VisualCard = (function() {

  function renderCanvas(state) {
    if (!state) return null;

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

    // 2. Top Accent Line (Emerald -> Sky -> Amber)
    const accentGrad = ctx.createLinearGradient(0, 0, 1200, 0);
    accentGrad.addColorStop(0, "#10b981");
    accentGrad.addColorStop(0.5, "#0284c7");
    accentGrad.addColorStop(1, "#f59e0b");
    ctx.fillStyle = accentGrad;
    ctx.fillRect(0, 0, 1200, 8);

    // 3. Header Branding
    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 32px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.fillText("SOLARAUDIT", 55, 68);
    
    ctx.fillStyle = "#64748b";
    ctx.font = "32px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.fillText(".ONLINE", 270, 68);

    // Verified Audit Badge
    ctx.fillStyle = "#ecfdf5";
    ctx.strokeStyle = "#a7f3d0";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(55, 84, 335, 26, 6);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#047857";
    ctx.font = "bold 12px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("INDEPENDENT AUDIT • 2026 NEPRA PROGRESSIVE MODEL", 65, 101);

    // City & Date Stamp
    const cityText = state.sizing.city ? state.sizing.city.toUpperCase() : "PAKISTAN";
    const dateText = new Date().toLocaleDateString("en-PK", { day: "numeric", month: "short", year: "numeric" });
    ctx.fillStyle = "#64748b";
    ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText(`${cityText} • ${dateText}`, 1200 - 55 - ctx.measureText(`${cityText} • ${dateText}`).width, 68);

    // 4. "BEFORE VS AFTER" BILL SHOCK BANNER (Viral Hook)
    const postBill = state.financials.postBillPkr !== undefined 
      ? state.financials.postBillPkr 
      : Math.max(0, state.preBillPkr - state.financials.monthlySavings);
    const savingsPercent = state.preBillPkr > 0 
      ? Math.min(100, Math.round((state.financials.monthlySavings / state.preBillPkr) * 100))
      : 0;

    const bannerX = 55;
    const bannerY = 125;
    const bannerW = 1090;
    const bannerH = 88;

    // Banner Shadow & Background
    ctx.fillStyle = "rgba(15, 23, 42, 0.04)";
    ctx.beginPath();
    ctx.roundRect(bannerX + 2, bannerY + 3, bannerW, bannerH, 12);
    ctx.fill();

    ctx.fillStyle = "#ffffff";
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(bannerX, bannerY, bannerW, bannerH, 12);
    ctx.fill();
    ctx.stroke();

    // Column 1: Pre-Solar Utility Bill
    ctx.fillStyle = "#64748b";
    ctx.font = "bold 12px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("PRE-SOLAR DISCO BILL", bannerX + 24, bannerY + 30);
    ctx.fillStyle = "#dc2626";
    ctx.font = "bold 28px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText(`Rs. ${state.preBillPkr.toLocaleString()}`, bannerX + 24, bannerY + 65);

    // Arrow Divider
    ctx.fillStyle = "#94a3b8";
    ctx.font = "bold 24px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("➔", bannerX + 270, bannerY + 54);

    // Column 2: Post-Solar Bill
    ctx.fillStyle = "#64748b";
    ctx.font = "bold 12px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("ESTIMATED POST-SOLAR BILL", bannerX + 325, bannerY + 30);
    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 28px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText(`Rs. ${postBill.toLocaleString()}`, bannerX + 325, bannerY + 65);

    // Column 3: Net Bill Reduction Highlight
    const badgeX = bannerX + 650;
    const badgeY = bannerY + 14;
    const badgeW = 415;
    const badgeH = 60;

    ctx.fillStyle = "#ecfdf5";
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 10);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#047857";
    ctx.font = "bold 11px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("ELIMINATING TOP PROGRESSIVE SLABS", badgeX + 18, badgeY + 22);

    ctx.fillStyle = "#065f46";
    ctx.font = "bold 24px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText(`Saves Rs. ${state.financials.monthlySavings.toLocaleString()}/mo (${savingsPercent}% CUT)`, badgeX + 18, badgeY + 49);

    // 5. 4-METRIC GRID (Pure White Cards with Subtle Elevation)
    const cards = [
      {
        label: "RECOMMENDED SOLAR ARRAY",
        value: `${state.sizing.actualDcKw} kW DC`,
        sub: `${state.sizing.panelCount}x 580W Tier-1 Bifacial Panels`,
        color: "#0f172a"
      },
      {
        label: "FAIR TURNKEY CAPEX (MARKET BENCHMARK)",
        value: `Rs. ${(state.financials.capexMin / 100000).toFixed(1)}L – ${(state.financials.capexMax / 100000).toFixed(1)}L`,
        sub: "Tier-1 Hardware, Protections & Labor",
        color: "#0284c7"
      },
      {
        label: "ESTIMATED PAYBACK PERIOD",
        value: `~${state.financials.paybackYears} Years`,
        sub: `Annual ROI: ~${(100 / state.financials.paybackYears).toFixed(0)}% (Risk-Free)`,
        color: "#d97706"
      },
      {
        label: "5-YEAR CUMULATIVE NET SAVINGS",
        value: `Rs. ${((state.financials.fiveYearNetSavings !== undefined ? state.financials.fiveYearNetSavings : (state.financials.monthlySavings * 60 - (state.financials.capexMin + state.financials.capexMax) / 2)) / 100000).toFixed(1)} Lakhs`,
        sub: "Net progressive savings after Capex recovery",
        color: "#059669"
      }
    ];

    const cardWidth = 525;
    const cardHeight = 155;
    const startX = 55;
    const startY = 230;
    const gapX = 40;
    const gapY = 20;

    cards.forEach((card, idx) => {
      const col = idx % 2;
      const row = Math.floor(idx / 2);
      const x = startX + col * (cardWidth + gapX);
      const y = startY + row * (cardHeight + gapY);

      // Card Shadow
      ctx.fillStyle = "rgba(15, 23, 42, 0.03)";
      ctx.beginPath();
      ctx.roundRect(x + 2, y + 3, cardWidth, cardHeight, 12);
      ctx.fill();

      // Card Background
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#e2e8f0";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(x, y, cardWidth, cardHeight, 12);
      ctx.fill();
      ctx.stroke();

      // Card Label
      ctx.fillStyle = "#64748b";
      ctx.font = "bold 12px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.label, x + 24, y + 36);

      // Card Value
      ctx.fillStyle = card.color;
      ctx.font = "bold 34px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.value, x + 24, y + 90);

      // Card Subtext
      ctx.fillStyle = "#475569";
      ctx.font = "14px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(card.sub, x + 24, y + 126);
    });

    // 6. FOOTER SPECS & VERIFICATION BAR
    const footerY = 585;
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, footerY, 1200, 90);
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, footerY);
    ctx.lineTo(1200, footerY);
    ctx.stroke();

    ctx.fillStyle = "#334155";
    ctx.font = "14px -apple-system, BlinkMacSystemFont, sans-serif";
    const specsSummary = `Inverter: ${state.sizing.inverterKw}kW Hybrid | Roof: ~${state.sizing.areaSqFt} sq.ft (${state.sizing.areaMarlas} Marla) | ${state.battery ? state.battery.unitSpec : "Daytime Net-Metering"}`;
    ctx.fillText(specsSummary, 55, footerY + 38);

    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 15px -apple-system, BlinkMacSystemFont, sans-serif";
    const siteCta = "Audit Your Bill Free: solaraudit.online";
    ctx.fillText(siteCta, 1200 - 55 - ctx.measureText(siteCta).width, footerY + 38);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "12px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.fillText("Independent engineering model • No contractor bias • Calibrated with active 2026 DISCO tariffs", 55, footerY + 62);

    return canvas;
  }

  function generatePngCard(state) {
    const canvas = renderCanvas(state);
    if (!canvas) return;

    const dataUrl = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.download = `SolarAudit-${state.sizing.actualDcKw}kW-Bill-Shock-Card.png`;
    link.href = dataUrl;
    link.click();
  }

  // Web Share API Helper (1-Tap Share with native PNG file attachment)
  async function shareAuditCard(state, shareText) {
    const canvas = renderCanvas(state);
    if (!canvas) return false;

    // Check if navigator.share exists
    if (typeof navigator !== "undefined" && navigator.share) {
      try {
        const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/png"));
        if (blob) {
          const file = new File([blob], `SolarAudit-${state.sizing.actualDcKw}kW-Audit.png`, { type: "image/png" });
          if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
              title: "My Independent Solar & Electricity Audit (SOLARAUDIT.ONLINE)",
              text: shareText,
              files: [file]
            });
            return true;
          }
        }
        // Fallback to text + URL native share if file sharing isn't supported
        await navigator.share({
          title: "My Independent Solar & Electricity Audit (SOLARAUDIT.ONLINE)",
          text: shareText,
          url: "https://solaraudit.online"
        });
        return true;
      } catch (err) {
        // User aborted/cancelled share dialog, or browser denied
        if (err.name === "AbortError") return true;
        console.warn("Native share failed, falling back to URL copy:", err);
      }
    }
    return false;
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
   • Approved Brands: Longi Hi-MO X6 / Jinko Tiger Neo / JA Solar / Canadian Solar
   • Required Roof Space: ~${c.sizing.areaSqFt} sq. ft. (~${c.sizing.areaMarlas} Marla)
   • Structure Type: ${c.mountingType === "elevated" ? "Elevated Walkable L3 Pergola (8-10 ft heavy GI)" : "Standard L2 Roof Mount"}

2. INVERTER & ARCHITECTURE:
   • Inverter Capacity: ${c.sizing.inverterKw} kW Hybrid (48V Pure Sine Wave / Dual MPPT)
   • Inverter Standards: IEC/UL certified with integrated grid-tie protection & anti-islanding

3. CABLING, EARTHING & PROTECTION (MANDATORY):
   • DC Wiring: Pure tinned copper 6mm² solar cable (single-core, UV resistant XLPE)
   • Surge Protection: Genuine Type-II DC SPDs on all strings + Type-II AC SPD
   • Earthing: Dedicated copper earth boring (< 5 Ohms resistance measured)

4. BATTERY STORAGE:
   • ${c.battery ? `Storage Target: ${c.battery.unitSpec} (${c.battery.batteryPreference === "lithium" ? "48V LiFePO4 Lithium" : "Deep Cycle Tubular"})` : "None (Daytime Net-Metering Configuration)"}

5. FAIR MARKET TURNKEY BUDGET:
   • Target Capex Range: Rs. ${(c.financials.capexMin / 100000).toFixed(1)} Lakhs – ${(c.financials.capexMax / 100000).toFixed(1)} Lakhs

Note: Quotations exceeding standard wholesale benchmarks or substituting CCA (copper-clad aluminum) wiring will be rejected upon audit.
Client Verification Tool: https://solaraudit.online/solar-quote-validator.html`;
  }

  const visualCardObj = {
    renderCanvas,
    generatePngCard,
    shareAuditCard,
    generateContractorTender
  };

  if (typeof window !== "undefined") {
    window.VisualCard = visualCardObj;
  }
  return visualCardObj;

})();

