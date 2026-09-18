/**
 * SOLARAUDIT.ONLINE - UI Controller & Reactive State Manager
 * Clean, minimal, utility-focused interaction handling.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Read body dataset presets or URL search params for programmatic landing pages
  const bodyData = document.body.dataset || {};
  const urlParams = new URLSearchParams(window.location.search);

  const initialCity = urlParams.get("city") || bodyData.presetCity || "karachi";
  const cityMeta = (typeof TARIFF_DATA !== "undefined" && TARIFF_DATA.cities && TARIFF_DATA.cities[initialCity]) ? TARIFF_DATA.cities[initialCity] : null;
  const initialDisco = urlParams.get("disco") || bodyData.presetDisco || (cityMeta ? cityMeta.disco : "kelectric");
  const initialBill = parseInt(urlParams.get("bill") || bodyData.presetBill || "48000", 10);
  const initialMode = urlParams.get("mode") || bodyData.presetMode || "bill";
  const initialNightAc = bodyData.presetNightAc !== undefined ? bodyData.presetNightAc === "true" : true;

  // App State
  const state = {
    cityKey: initialCity,
    discoKey: initialDisco,
    inputMode: initialMode, // "bill" or "appliances"
    billPkr: initialBill,
    appliances: {
      ac15: 2,
      ac10: 0,
      fans: 5,
      fridge: 1,
      pump: 1
    },
    nightAcEnabled: initialNightAc,
    nightAcCount: 1,
    nightHours: 8,
    batteryPreference: "lithium", // "lithium" or "tubular"
    meterType: "three_phase", // "three_phase" or "single_phase"
    mountingType: "standard", // "standard" or "elevated"
    includeNetMetering: true,
    calculatedState: null
  };

  // DOM Elements - Inputs
  const citySelect = document.getElementById("citySelect");
  const billSlider = document.getElementById("billSlider");
  const billValueDisplay = document.getElementById("billValueDisplay");
  const inputModeBillBtn = document.getElementById("modeBillBtn");
  const inputModeApplianceBtn = document.getElementById("modeApplianceBtn");
  const billInputSection = document.getElementById("billInputSection");
  const applianceInputSection = document.getElementById("applianceInputSection");

  // Meter Phase Controls
  const meterThreePhaseBtn = document.getElementById("meterThreePhaseBtn");
  const meterSinglePhaseBtn = document.getElementById("meterSinglePhaseBtn");
  const singlePhaseNotice = document.getElementById("singlePhaseNotice");

  // Night Battery Controls
  const nightAcToggle = document.getElementById("nightAcToggle");
  const nightBatteryOptions = document.getElementById("nightBatteryOptions");
  const nightAcCountSlider = document.getElementById("nightAcCountSlider");
  const nightAcCountDisplay = document.getElementById("nightAcCountDisplay");
  const nightHoursSlider = document.getElementById("nightHoursSlider");
  const nightHoursDisplay = document.getElementById("nightHoursDisplay");
  const batteryTypeLithium = document.getElementById("batteryTypeLithium");
  const batteryTypeTubular = document.getElementById("batteryTypeTubular");

  // Rooftop Structure Controls
  const structStandardBtn = document.getElementById("structStandardBtn");
  const structElevatedBtn = document.getElementById("structElevatedBtn");

  // Output Cards
  const outDcKw = document.getElementById("outDcKw");
  const outPanelCount = document.getElementById("outPanelCount");
  const outInverter = document.getElementById("outInverter");
  const outRoofSpace = document.getElementById("outRoofSpace");
  const outRoofMarla = document.getElementById("outRoofMarla");
  const outBatterySpec = document.getElementById("outBatterySpec");
  const outBatteryNote = document.getElementById("outBatteryNote");
  const outCapexRange = document.getElementById("outCapexRange");
  const outMonthlySavings = document.getElementById("outMonthlySavings");
  const outPaybackPeriod = document.getElementById("outPaybackPeriod");
  const out5YearProfit = document.getElementById("out5YearProfit");
  const outEstimatedUnits = document.getElementById("outEstimatedUnits");

  // Sweet Spot Elements
  const sweetSpotContainer = document.getElementById("sweetSpotContainer");
  const sweetSpotKw = document.getElementById("sweetSpotKw");
  const sweetSpotPanels = document.getElementById("sweetSpotPanels");
  const sweetSpotCapexSave = document.getElementById("sweetSpotCapexSave");
  const sweetSpotBillSave = document.getElementById("sweetSpotBillSave");

  // Quote Validator Elements
  const quoteKwInput = document.getElementById("quoteKwInput");
  const quotePriceInput = document.getElementById("quotePriceInput");
  const quoteSystemType = document.getElementById("quoteSystemType");
  const quoteValidatorResult = document.getElementById("quoteValidatorResult");
  const quoteResultBadge = document.getElementById("quoteResultBadge");
  const quoteRateDisplay = document.getElementById("quoteRateDisplay");
  const quoteResultDesc = document.getElementById("quoteResultDesc");

  // Action Buttons
  const shareWhatsAppBtn = document.getElementById("shareWhatsAppBtn");
  const copyFeedback = document.getElementById("copyFeedback");
  const downloadPdfBtn = document.getElementById("downloadPdfBtn");

  // Expose state for automated testing & browser inspections
  window.appState = state;

  // Initialize Appliance Counters
  const applianceKeys = ["ac15", "ac10", "fans", "fridge", "pump"];
  applianceKeys.forEach((key) => {
    const decBtn = document.getElementById(`dec_${key}`);
    const incBtn = document.getElementById(`inc_${key}`);
    const valSpan = document.getElementById(`val_${key}`);

    if (decBtn && incBtn && valSpan) {
      decBtn.addEventListener("click", () => {
        if (state.appliances[key] > 0) {
          state.appliances[key]--;
          valSpan.textContent = state.appliances[key];
          recalculate();
        }
      });

      incBtn.addEventListener("click", () => {
        if (state.appliances[key] < 15) {
          state.appliances[key]++;
          valSpan.textContent = state.appliances[key];
          recalculate();
        }
      });
    }
  });

  // Event Listeners: City & DISCO
  citySelect.addEventListener("change", (e) => {
    state.cityKey = e.target.value;
    const cityInfo = TARIFF_DATA.cities[state.cityKey] || TARIFF_DATA.cities.karachi;
    state.discoKey = cityInfo.disco;
    recalculate();
  });

  // Event Listeners: Input Mode
  inputModeBillBtn.addEventListener("click", () => {
    state.inputMode = "bill";
    inputModeBillBtn.className = "flex-1 py-1.5 px-3 rounded-md bg-white text-slate-900 font-semibold shadow-sm border border-slate-200 text-xs";
    inputModeApplianceBtn.className = "flex-1 py-1.5 px-3 rounded-md text-slate-600 hover:text-slate-900 text-xs";
    billInputSection.classList.remove("hidden");
    applianceInputSection.classList.add("hidden");
    recalculate();
  });

  inputModeApplianceBtn.addEventListener("click", () => {
    state.inputMode = "appliances";
    inputModeApplianceBtn.className = "flex-1 py-1.5 px-3 rounded-md bg-white text-slate-900 font-semibold shadow-sm border border-slate-200 text-xs";
    inputModeBillBtn.className = "flex-1 py-1.5 px-3 rounded-md text-slate-600 hover:text-slate-900 text-xs";
    applianceInputSection.classList.remove("hidden");
    billInputSection.classList.add("hidden");
    recalculate();
  });

  // Bill Slider
  billSlider.addEventListener("input", (e) => {
    state.billPkr = parseInt(e.target.value, 10);
    billValueDisplay.textContent = `Rs. ${state.billPkr.toLocaleString()}`;
    recalculate();
  });

  // Meter Phase Selection
  meterThreePhaseBtn.addEventListener("click", () => {
    state.meterType = "three_phase";
    meterThreePhaseBtn.className = "py-1 px-3 rounded font-medium text-slate-900 bg-white shadow-xs transition-all";
    meterSinglePhaseBtn.className = "py-1 px-3 rounded font-medium text-slate-500 hover:text-slate-800 transition-all";
    singlePhaseNotice.classList.add("hidden");
    recalculate();
  });

  meterSinglePhaseBtn.addEventListener("click", () => {
    state.meterType = "single_phase";
    meterSinglePhaseBtn.className = "py-1 px-3 rounded font-medium text-slate-900 bg-white shadow-xs transition-all";
    meterThreePhaseBtn.className = "py-1 px-3 rounded font-medium text-slate-500 hover:text-slate-800 transition-all";
    singlePhaseNotice.classList.remove("hidden");
    recalculate();
  });

  // Night AC Controls
  nightAcToggle.addEventListener("change", (e) => {
    state.nightAcEnabled = e.target.checked;
    if (state.nightAcEnabled) {
      nightBatteryOptions.classList.remove("opacity-40", "pointer-events-none");
    } else {
      nightBatteryOptions.classList.add("opacity-40", "pointer-events-none");
    }
    recalculate();
  });

  nightAcCountSlider.addEventListener("input", (e) => {
    state.nightAcCount = parseInt(e.target.value, 10);
    nightAcCountDisplay.textContent = `${state.nightAcCount} AC${state.nightAcCount > 1 ? "s" : ""}`;
    recalculate();
  });

  nightHoursSlider.addEventListener("input", (e) => {
    state.nightHours = parseInt(e.target.value, 10);
    nightHoursDisplay.textContent = `${state.nightHours} Hours`;
    recalculate();
  });

  batteryTypeLithium.addEventListener("click", () => {
    state.batteryPreference = "lithium";
    batteryTypeLithium.className = "p-3 rounded-lg border-2 border-slate-900 bg-slate-50 text-slate-900 text-left transition-all";
    batteryTypeTubular.className = "p-3 rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-slate-300 text-left transition-all";
    recalculate();
  });

  batteryTypeTubular.addEventListener("click", () => {
    state.batteryPreference = "tubular";
    batteryTypeTubular.className = "p-3 rounded-lg border-2 border-slate-900 bg-slate-50 text-slate-900 text-left transition-all";
    batteryTypeLithium.className = "p-3 rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-slate-300 text-left transition-all";
    recalculate();
  });

  // Rooftop Structure Selection
  structStandardBtn.addEventListener("click", () => {
    state.mountingType = "standard";
    structStandardBtn.className = "p-3 rounded-lg border-2 border-slate-900 bg-slate-50 text-slate-900 text-left transition-all";
    structElevatedBtn.className = "p-3 rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-slate-300 text-left transition-all";
    recalculate();
  });

  structElevatedBtn.addEventListener("click", () => {
    state.mountingType = "elevated";
    structElevatedBtn.className = "p-3 rounded-lg border-2 border-slate-900 bg-slate-50 text-slate-900 text-left transition-all";
    structStandardBtn.className = "p-3 rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-slate-300 text-left transition-all";
    recalculate();
  });

  // Contractor Quote Validator Inputs
  function runQuoteValidator() {
    const kw = parseFloat(quoteKwInput.value);
    const price = parseFloat(quotePriceInput.value);
    const sysType = quoteSystemType.value;

    if (!kw || kw <= 0 || !price || price <= 0) {
      quoteValidatorResult.classList.add("hidden");
      return;
    }

    const res = CalculatorEngine.validateInstallerQuote(kw, price, sysType);
    if (!res) {
      quoteValidatorResult.classList.add("hidden");
      return;
    }

    quoteValidatorResult.className = `p-3 rounded-lg border text-xs space-y-1 transition-all ${res.statusClass}`;
    quoteResultBadge.textContent = res.badgeText;
    quoteRateDisplay.textContent = `Turnkey: Rs. ${res.ratePerWatt.toLocaleString()} / W`;
    quoteResultDesc.textContent = res.description;
    quoteValidatorResult.classList.remove("hidden");
  }

  quoteKwInput.addEventListener("input", runQuoteValidator);
  quotePriceInput.addEventListener("input", runQuoteValidator);
  quoteSystemType.addEventListener("change", runQuoteValidator);

  // Core Recalculation Routine
  function recalculate() {
    let monthlyUnits = 0;
    let targetBill = 0;

    if (state.inputMode === "bill") {
      targetBill = state.billPkr;
      monthlyUnits = CalculatorEngine.estimateUnitsFromBill(targetBill, state.discoKey);
    } else {
      // Calculate units based on appliances
      const app = state.appliances;
      const dailyKwh =
        (app.ac15 * 0.75 * 8) +
        (app.ac10 * 0.55 * 8) +
        (app.fans * 0.055 * 14) +
        (app.fridge * 0.15 * 24) +
        (app.pump * 1.1 * 1);
      monthlyUnits = Math.round(dailyKwh * 30);
      const billRes = CalculatorEngine.calculateBillFromUnits(monthlyUnits, state.discoKey);
      targetBill = billRes.totalBill;
      state.billPkr = targetBill;
      billValueDisplay.textContent = `Rs. ${targetBill.toLocaleString()}`;
      billSlider.value = Math.min(180000, targetBill);
    }

    outEstimatedUnits.textContent = `~${monthlyUnits.toLocaleString()} units`;

    // 1. Solar Sizing
    const sizing = CalculatorEngine.calculateSolarSizing(monthlyUnits, state.cityKey);

    // 2. Battery Storage
    let battery = null;
    if (state.nightAcEnabled) {
      battery = CalculatorEngine.calculateNightBattery(state.nightAcCount, state.nightHours, state.batteryPreference);
    }

    // 3. Financials & Payback (with mounting and meter options)
    const options = {
      mountingType: state.mountingType,
      meterType: state.meterType
    };
    const financials = CalculatorEngine.calculateFinancials(sizing, battery, targetBill, state.discoKey, state.includeNetMetering, options);

    // 4. Sweet Spot calculation (compares against full turnkey capex)
    const sweetSpot = CalculatorEngine.calculateSweetSpot(monthlyUnits, state.discoKey, financials.avgCapex, options);

    // Store calculated state for PDF and sharing
    state.calculatedState = {
      preBillPkr: targetBill,
      monthlyUnits,
      sizing,
      battery,
      financials,
      sweetSpot,
      mountingType: state.mountingType,
      meterType: state.meterType
    };

    // Update DOM UI elements
    updateUI(state.calculatedState);
  }

  function updateUI(c) {
    // Hardware Cards
    outDcKw.textContent = `${c.sizing.actualDcKw} kW`;
    outPanelCount.textContent = `${c.sizing.panelCount} panels (580W N-Type)`;
    outInverter.textContent = `${c.sizing.inverterKw} kW Hybrid (48V)`;
    outRoofSpace.textContent = `${c.sizing.areaSqFt} sq ft`;
    outRoofMarla.textContent = `~${c.sizing.areaMarlas} Marla`;

    // Battery Specs
    if (c.battery) {
      outBatterySpec.textContent = c.battery.unitSpec;
      outBatteryNote.textContent = c.battery.warningNote;
      outBatteryNote.className = c.battery.batteryPreference === "lithium" 
        ? "text-xs text-slate-600 mt-1.5" 
        : "text-xs text-amber-900 bg-amber-50 p-2 rounded border border-amber-200 mt-1.5";
    } else {
      outBatterySpec.textContent = "None (On-Grid Net-Metering)";
      outBatteryNote.textContent = "Daytime generation will export to grid. System will turn off during power outages.";
      outBatteryNote.className = "text-xs text-slate-500 mt-1.5";
    }

    // Financial Cards
    const minLakhs = (c.financials.capexMin / 100000).toFixed(1);
    const maxLakhs = (c.financials.capexMax / 100000).toFixed(1);
    outCapexRange.textContent = `Rs. ${minLakhs} – ${maxLakhs} Lakhs`;
    outMonthlySavings.textContent = `Rs. ${c.financials.monthlySavings.toLocaleString()} / mo`;
    outPaybackPeriod.textContent = `${c.financials.paybackYears} Years`;
    out5YearProfit.textContent = `Rs. ${(c.financials.fiveYearNetSavings / 100000).toFixed(1)} Lakhs`;

    // Sweet Spot / Slab-Breaker Box
    if (c.sweetSpot && c.sweetSpot.capexReductionPercent > 15) {
      sweetSpotContainer.classList.remove("hidden");
      sweetSpotKw.textContent = `${c.sweetSpot.recommendedKw} kW`;
      sweetSpotPanels.textContent = `${c.sweetSpot.panelCount} panels`;
      const sweetMin = (c.sweetSpot.sweetCapexMin / 100000).toFixed(1);
      const sweetMax = (c.sweetSpot.sweetCapexMax / 100000).toFixed(1);
      const costEl = document.getElementById("sweetSpotCost");
      if (costEl) {
        costEl.textContent = `Rs. ${sweetMin}L – ${sweetMax}L`;
      }
      sweetSpotCapexSave.textContent = `${c.sweetSpot.capexReductionPercent}% Lower Capex`;
      sweetSpotBillSave.textContent = `Rs. ${c.sweetSpot.monthlySavings.toLocaleString()} / mo`;
    } else {
      sweetSpotContainer.classList.add("hidden");
    }
  }

  // Action: WhatsApp Sharing Generator
  shareWhatsAppBtn.addEventListener("click", () => {
    if (!state.calculatedState) return;
    const c = state.calculatedState;

    const shareText =
`Solar & Electricity Bill Audit (via SOLARAUDIT.ONLINE):
--------------------------------------------------
Monthly Bill: Rs. ${c.preBillPkr.toLocaleString()} (~${c.monthlyUnits} units)
Recommended Solar: ${c.sizing.actualDcKw} kW (${c.sizing.panelCount}x 580W Panels)
Inverter Architecture: ${c.sizing.inverterKw} kW Hybrid (48V Pure Sine)
Roof Footprint: ~${c.sizing.areaSqFt} sq. ft. (~${c.sizing.areaMarlas} Marla)
Structure: ${c.mountingType === "elevated" ? "Elevated Walkable L3 Pergola (8-10 ft)" : "Standard L2 Ground/Roof Mount"}
Meter Connection: ${c.meterType === "single_phase" ? "Single-Phase (3-Phase Upgrade Required)" : "3-Phase Ready"}
${c.battery ? `Night AC Storage: ${c.battery.unitSpec}` : "Storage: None (Daytime Net-Metering)"}
Turnkey Capex: Rs. ${(c.financials.capexMin / 100000).toFixed(1)}L – ${(c.financials.capexMax / 100000).toFixed(1)} Lakhs
Monthly Savings: Rs. ${c.financials.monthlySavings.toLocaleString()}/mo
Payback Period: ~${c.financials.paybackYears} Years
--------------------------------------------------
Free Independent Audit: https://solaraudit.online
Contractor Quote Validator: https://solaraudit.online/solar-quote-validator.html`;

    navigator.clipboard.writeText(shareText).then(() => {
      copyFeedback.classList.remove("hidden");
      setTimeout(() => {
        copyFeedback.classList.add("hidden");
      }, 3000);
    });
  });

  // Action: Download PDF Specification Sheet
  downloadPdfBtn.addEventListener("click", () => {
    if (!state.calculatedState) return;
    PdfGenerator.generateSpecificationSheet(state.calculatedState);
  });

  // Sync initial DOM inputs with parsed state
  if (citySelect) {
    citySelect.value = state.cityKey;
  }
  if (billSlider && billValueDisplay) {
    billSlider.value = state.billPkr;
    billValueDisplay.textContent = `Rs. ${state.billPkr.toLocaleString()}`;
  }
  if (nightAcToggle) {
    nightAcToggle.checked = state.nightAcEnabled;
    if (state.nightAcEnabled) {
      nightBatteryOptions.classList.remove("opacity-40", "pointer-events-none");
    } else {
      nightBatteryOptions.classList.add("opacity-40", "pointer-events-none");
    }
  }

  // Initial Calculation Run
  recalculate();

  // Scroll to targeted focus section if specified
  if (bodyData.focusSection === "validator" || urlParams.get("focus") === "validator") {
    setTimeout(() => {
      const validatorCard = document.getElementById("quoteKwInput");
      if (validatorCard) {
        validatorCard.closest(".tool-card")?.scrollIntoView({ behavior: "smooth", block: "center" });
        validatorCard.focus();
      }
    }, 450);
  }
});
