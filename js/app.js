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
  const initialNightAcCount = parseInt(urlParams.get("acCount") || bodyData.presetNightAcCount || "1", 10);

  // App State
  const state = {
    cityKey: initialCity,
    discoKey: initialDisco,
    inputMode: initialMode, // "bill" or "appliances"
    billPkr: initialBill,
    appliances: {
      ac15: 2,
      ac15_hours: 8,
      ac10: 0,
      ac10_hours: 8,
      fans: 5,
      fridge: 1,
      freezer: 0,
      pump: 1,
      lights: 1
    },
    nightAcEnabled: initialNightAc,
    nightAcCount: initialNightAcCount,
    nightHours: 8,
    batteryPreference: "lithium", // "lithium" or "tubular"
    meterType: "three_phase", // "three_phase" or "single_phase"
    mountingType: "standard", // "standard" or "elevated"
    includeNetMetering: true,
    calculatedState: null
  };

  // DOM Elements - Inputs
  const citySelect = document.getElementById("citySelect");
  const cityIrradiancePsh = document.getElementById("cityIrradiancePsh");
  const cityIrradianceClimate = document.getElementById("cityIrradianceClimate");
  const billSlider = document.getElementById("billSlider");
  const billValueDisplay = document.getElementById("billValueDisplay");
  const billInputNumber = document.getElementById("billInputNumber");
  const heroPreBill = document.getElementById("heroPreBill");
  const heroPostBill = document.getElementById("heroPostBill");
  const heroNetPocket = document.getElementById("heroNetPocket");
  const heroSavingsBar = document.getElementById("heroSavingsBar");
  const heroSavingsPercent = document.getElementById("heroSavingsPercent");
  const inputModeBillBtn = document.getElementById("modeBillBtn");
  const inputModeApplianceBtn = document.getElementById("modeApplianceBtn");
  const billInputSection = document.getElementById("billInputSection");
  const applianceInputSection = document.getElementById("applianceInputSection");
  const shortcutToApplianceBtn = document.getElementById("shortcutToApplianceBtn");
  const shortcutBackToBillBtn = document.getElementById("shortcutBackToBillBtn");
  const applianceTotalUnitsDisplay = document.getElementById("applianceTotalUnitsDisplay");
  const applianceTotalBillDisplay = document.getElementById("applianceTotalBillDisplay");
  const applianceDominantText = document.getElementById("applianceDominantText");

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
  const applianceKeys = ["ac15", "ac10", "fans", "fridge", "freezer", "pump", "lights"];
  applianceKeys.forEach((key) => {
    const decBtn = document.getElementById(`dec_${key}`);
    const incBtn = document.getElementById(`inc_${key}`);
    const valSpan = document.getElementById(`val_${key}`);

    if (decBtn && incBtn && valSpan) {
      valSpan.textContent = state.appliances[key] !== undefined ? state.appliances[key] : 0;
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

  // Helper: Toggle Two-State Segmented Cards with Guaranteed Min-44px Touch Targets
  function setCardButtonState(activeBtn, inactiveBtn) {
    if (activeBtn) {
      activeBtn.className = "min-h-[44px] p-2.5 rounded-lg border border-slate-900 bg-slate-900 text-white font-semibold text-left transition-all cursor-pointer";
      const title = activeBtn.querySelector("div:first-child");
      const sub = activeBtn.querySelector("div:nth-child(2)");
      if (title) title.className = "font-bold text-white";
      if (sub) sub.className = "text-[11px] text-slate-300";
    }
    if (inactiveBtn) {
      inactiveBtn.className = "min-h-[44px] p-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold text-left hover:border-slate-400 transition-all cursor-pointer";
      const title = inactiveBtn.querySelector("div:first-child");
      const sub = inactiveBtn.querySelector("div:nth-child(2)");
      if (title) title.className = "font-bold text-slate-900";
      if (sub) sub.className = "text-[11px] text-slate-600";
    }
  }

  // Helper: Toggle Mode Buttons with Min-44px Touch Targets
  function setModeButtonsState(isBill) {
    if (isBill) {
      inputModeBillBtn.className = "min-h-[44px] py-2 px-4 rounded-md bg-white text-slate-900 font-semibold shadow-xs border border-slate-200 text-xs sm:text-sm transition-all cursor-pointer";
      inputModeApplianceBtn.className = "min-h-[44px] py-2 px-4 rounded-md text-slate-700 hover:text-slate-900 font-semibold text-xs sm:text-sm transition-all cursor-pointer";
    } else {
      inputModeApplianceBtn.className = "min-h-[44px] py-2 px-4 rounded-md bg-white text-slate-900 font-semibold shadow-xs border border-slate-200 text-xs sm:text-sm transition-all cursor-pointer";
      inputModeBillBtn.className = "min-h-[44px] py-2 px-4 rounded-md text-slate-700 hover:text-slate-900 font-semibold text-xs sm:text-sm transition-all cursor-pointer";
    }
  }

  // Wire AC Runtime Hours Buttons (Preserving Min-44px Targets)
  ["ac15", "ac10"].forEach((acKey) => {
    const group = document.getElementById(`hoursGroup_${acKey}`);
    if (group) {
      const buttons = group.querySelectorAll("button[data-hours]");
      buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
          buttons.forEach((b) => {
            b.className = "min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 cursor-pointer transition-all";
          });
          btn.className = "min-h-[44px] min-w-[44px] px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-900 bg-slate-900 text-white cursor-pointer transition-all";
          state.appliances[`${acKey}_hours`] = parseInt(btn.getAttribute("data-hours"), 10);
          recalculate();
        });
      });
    }
  });

  // Wire Mode Switching & Shortcuts
  if (shortcutToApplianceBtn) {
    shortcutToApplianceBtn.addEventListener("click", () => {
      inputModeApplianceBtn.click();
    });
  }
  if (shortcutBackToBillBtn) {
    shortcutBackToBillBtn.addEventListener("click", () => {
      inputModeBillBtn.click();
    });
  }

  // City Climate Display Update
  function updateCityClimateDisplay() {
    const cityInfo = TARIFF_DATA.cities[state.cityKey] || TARIFF_DATA.cities.karachi;
    if (cityIrradiancePsh) {
      cityIrradiancePsh.textContent = `${cityInfo.psh} Peak Sun Hours / Day`;
    }
    if (cityIrradianceClimate) {
      cityIrradianceClimate.textContent = cityInfo.climate || "High year-round solar potential";
    }
    if (citySelect && citySelect.value !== state.cityKey) {
      citySelect.value = state.cityKey;
    }
  }

  // Event Listeners: City & DISCO
  citySelect.addEventListener("change", (e) => {
    state.cityKey = e.target.value;
    const cityInfo = TARIFF_DATA.cities[state.cityKey] || TARIFF_DATA.cities.karachi;
    state.discoKey = cityInfo.disco;
    updateCityClimateDisplay();
    recalculate();
  });

  // Event Listeners: Input Mode
  inputModeBillBtn.addEventListener("click", () => {
    state.inputMode = "bill";
    setModeButtonsState(true);
    billInputSection.classList.remove("hidden");
    applianceInputSection.classList.add("hidden");
    recalculate();
  });

  inputModeApplianceBtn.addEventListener("click", () => {
    state.inputMode = "appliances";
    setModeButtonsState(false);
    applianceInputSection.classList.remove("hidden");
    billInputSection.classList.add("hidden");
    recalculate();
  });

  // Bill Preset Chips Helper
  function updatePresetChipsActive(currentVal) {
    document.querySelectorAll(".bill-preset-chip").forEach((btn) => {
      const pVal = parseInt(btn.getAttribute("data-preset-val"), 10);
      if (pVal === currentVal) {
        btn.className = "bill-preset-chip active-preset px-2 py-1.5 text-center font-bold rounded-md border border-slate-900 bg-slate-900 text-white transition-all cursor-pointer";
        const sub = btn.querySelector("span");
        if (sub) sub.className = "text-[10px] text-slate-300 block";
      } else {
        btn.className = "bill-preset-chip px-2 py-1.5 text-center font-medium rounded-md border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 transition-all cursor-pointer";
        const sub = btn.querySelector("span");
        if (sub) sub.className = "text-[10px] text-slate-500 block";
      }
    });
  }

  // Bill Slider
  billSlider.addEventListener("input", (e) => {
    state.billPkr = parseInt(e.target.value, 10);
    if (billValueDisplay) billValueDisplay.textContent = `Rs. ${state.billPkr.toLocaleString()}`;
    if (billInputNumber) billInputNumber.value = state.billPkr;
    updatePresetChipsActive(state.billPkr);
    recalculate();
  });

  // Direct Number Input
  if (billInputNumber) {
    billInputNumber.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      if (!isNaN(val) && val >= 1000) {
        state.billPkr = val;
        if (billSlider) billSlider.value = Math.min(500000, Math.max(8000, val));
        if (billValueDisplay) billValueDisplay.textContent = `Rs. ${val.toLocaleString()}`;
        updatePresetChipsActive(val);
        recalculate();
      }
    });
  }

  // Preset Chips Click Handlers
  document.querySelectorAll(".bill-preset-chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      const presetVal = parseInt(btn.getAttribute("data-preset-val"), 10);
      if (presetVal) {
        state.billPkr = presetVal;
        if (billSlider) billSlider.value = Math.min(500000, presetVal);
        if (billInputNumber) billInputNumber.value = presetVal;
        if (billValueDisplay) billValueDisplay.textContent = `Rs. ${presetVal.toLocaleString()}`;
        updatePresetChipsActive(presetVal);
        recalculate();
      }
    });
  });

  // Meter Phase Selection
  meterThreePhaseBtn.addEventListener("click", () => {
    state.meterType = "three_phase";
    setCardButtonState(meterThreePhaseBtn, meterSinglePhaseBtn);
    singlePhaseNotice.classList.add("hidden");
    recalculate();
  });

  meterSinglePhaseBtn.addEventListener("click", () => {
    state.meterType = "single_phase";
    setCardButtonState(meterSinglePhaseBtn, meterThreePhaseBtn);
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
    setCardButtonState(batteryTypeLithium, batteryTypeTubular);
    recalculate();
  });

  batteryTypeTubular.addEventListener("click", () => {
    state.batteryPreference = "tubular";
    setCardButtonState(batteryTypeTubular, batteryTypeLithium);
    recalculate();
  });

  // Rooftop Structure Selection
  structStandardBtn.addEventListener("click", () => {
    state.mountingType = "standard";
    setCardButtonState(structStandardBtn, structElevatedBtn);
    recalculate();
  });

  structElevatedBtn.addEventListener("click", () => {
    state.mountingType = "elevated";
    setCardButtonState(structElevatedBtn, structStandardBtn);
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
    updateCityClimateDisplay();

    let monthlyUnits = 0;
    let targetBill = 0;

    if (state.inputMode === "bill") {
      targetBill = state.billPkr;
      monthlyUnits = CalculatorEngine.estimateUnitsFromBill(targetBill, state.discoKey);
    } else {
      // Calculate detailed breakdown based on appliances
      const app = state.appliances;
      const breakdown = CalculatorEngine.calculateApplianceBreakdown({
        ac15: { count: app.ac15, hours: app.ac15_hours || 8 },
        ac10: { count: app.ac10, hours: app.ac10_hours || 8 },
        fans: { count: app.fans, hours: 14 },
        fridge: { count: app.fridge, hours: 24 },
        freezer: { count: app.freezer || 0, hours: 24 },
        pump: { count: app.pump, hours: 1 },
        lights: { count: app.lights !== undefined ? app.lights : 1, hours: 6 }
      }, state.discoKey);

      monthlyUnits = breakdown.totalMonthlyUnits;
      targetBill = breakdown.estimatedBillPkr;
      state.billPkr = targetBill;
      if (billValueDisplay) billValueDisplay.textContent = `Rs. ${targetBill.toLocaleString()}`;
      if (billInputNumber) billInputNumber.value = targetBill;
      billSlider.value = Math.min(500000, targetBill);
      updatePresetChipsActive(targetBill);

      if (applianceTotalUnitsDisplay) {
        applianceTotalUnitsDisplay.textContent = `~${monthlyUnits.toLocaleString()} Units`;
      }
      if (applianceTotalBillDisplay) {
        applianceTotalBillDisplay.textContent = `~Rs. ${targetBill.toLocaleString()}`;
      }
      if (applianceDominantText && breakdown.items.length > 0) {
        const topItem = breakdown.items[0];
        if (topItem && topItem.percentOfTotal > 0) {
          applianceDominantText.textContent = `${topItem.name} (${topItem.percentOfTotal}% of bill)`;
        } else {
          applianceDominantText.textContent = "No appliances active";
        }
      }
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
    const sweetSpot = CalculatorEngine.calculateSweetSpot(monthlyUnits, state.discoKey, financials.avgCapex, {
      ...options,
      cityKey: state.cityKey
    });

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
    // Hero Solar Verdict Banner
    if (heroPreBill) heroPreBill.textContent = `Rs. ${c.preBillPkr.toLocaleString()}`;
    if (heroPostBill) heroPostBill.textContent = `Rs. ${c.financials.postBillPkr.toLocaleString()}`;
    if (heroNetPocket) heroNetPocket.textContent = `+Rs. ${c.financials.monthlySavings.toLocaleString()} / mo`;
    const savingsPercent = Math.min(100, Math.max(0, Math.round((c.financials.monthlySavings / (c.preBillPkr || 1)) * 100)));
    if (heroSavingsPercent) heroSavingsPercent.textContent = `-${savingsPercent}% Bill Drop`;
    if (heroSavingsBar) heroSavingsBar.style.width = `${savingsPercent}%`;

    // Hardware Cards
    outDcKw.textContent = `${c.sizing.actualDcKw} kW`;
    outPanelCount.textContent = `${c.sizing.panelCount} panels (580W N-Type)`;
    outInverter.textContent = c.sizing.inverterKw >= 15 
      ? `${c.sizing.inverterKw} kW 3-Phase Commercial Hybrid` 
      : `${c.sizing.inverterKw} kW Hybrid (48V)`;
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

    // 2026 Net-Billing Breakdown Grid
    const nb = c.financials.netBilling;
    if (nb) {
      const nbSelfConsumption = document.getElementById("nbSelfConsumption");
      const nbExportCredit = document.getElementById("nbExportCredit");
      const nbPostBill = document.getElementById("nbPostBill");
      const nbNote = document.getElementById("nbNote");

      if (nbSelfConsumption) {
        const totalSelfCons = nb.daytimeSelfConsumptionUnits + (nb.batterySelfConsumptionUnits || 0);
        nbSelfConsumption.textContent = `~${totalSelfCons} units (${nb.selfConsumptionPercent}%)`;
      }
      if (nbExportCredit) {
        nbExportCredit.textContent = `${nb.gridExportUnits} units (Rs. ${nb.exportCreditPkr.toLocaleString()})`;
      }
      if (nbPostBill) {
        nbPostBill.textContent = `Rs. ${c.financials.postBillPkr.toLocaleString()} / mo`;
      }
      if (nbNote) {
        if (nb.systemType === "hybrid_storage") {
          nbNote.innerHTML = `<strong>2026 Net-Billing (Hybrid LiFePO4):</strong> High-efficiency battery storage captures ~${nb.batterySelfConsumptionUnits} daytime units to run ACs overnight, displacing expensive night retail tariffs (~Rs. 45–60/kWh). Excess ${nb.gridExportUnits} units are credited at wholesale NAEPP rate (~Rs. ${nb.naeppExportRate}/kWh).`;
        } else {
          nbNote.innerHTML = `<strong>2026 Net-Billing (On-Grid):</strong> Daytime generation self-consumes directly (~${nb.daytimeSelfConsumptionUnits} units); surplus ${nb.gridExportUnits} units export at wholesale NAEPP (~Rs. ${nb.naeppExportRate}/kWh). Night load (${nb.gridImportUnits} units) is imported from grid under progressive slabs.`;
        }
      }
    }

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

    // Update Sticky Mobile Summary Bar (<1024px)
    const mobileStickyKw = document.getElementById("mobileStickyKw");
    const mobileStickyPanels = document.getElementById("mobileStickyPanels");
    const mobileStickySavings = document.getElementById("mobileStickySavings");
    if (mobileStickyKw) mobileStickyKw.textContent = `${c.sizing.actualDcKw} kW`;
    if (mobileStickyPanels) mobileStickyPanels.textContent = `(${c.sizing.panelCount} panels)`;
    if (mobileStickySavings) mobileStickySavings.textContent = `Rs. ${c.financials.monthlySavings.toLocaleString()}`;
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

    navigator.clipboard.writeText(shareText).catch(() => {});
    copyFeedback.textContent = "✓ Summary copied! Opening WhatsApp...";
    copyFeedback.classList.remove("hidden");
    setTimeout(() => {
      copyFeedback.classList.add("hidden");
    }, 4000);

    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    const waUrl = isMobile 
      ? `whatsapp://send?text=${encodeURIComponent(shareText)}`
      : `https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}`;
    
    window.open(waUrl, "_blank");
  });

  // Action: Download PDF Specification Sheet (with dynamic lazy-loading and error recovery)
  downloadPdfBtn.addEventListener("click", () => {
    if (!state.calculatedState) return;
    const origText = downloadPdfBtn.innerHTML;
    downloadPdfBtn.innerHTML = "<span>Generating PDF...</span>";
    downloadPdfBtn.disabled = true;
    PdfGenerator.generateSpecificationSheet(
      state.calculatedState,
      () => {
        downloadPdfBtn.innerHTML = origText;
        downloadPdfBtn.disabled = false;
      },
      (err) => {
        downloadPdfBtn.innerHTML = origText;
        downloadPdfBtn.disabled = false;
      }
    );
  });

  // Action: Mobile Sticky Summary - Smooth scroll to results
  const mobileViewBreakdownBtn = document.getElementById("mobileViewBreakdownBtn");
  if (mobileViewBreakdownBtn) {
    mobileViewBreakdownBtn.addEventListener("click", (e) => {
      e.preventDefault();
      const target = document.getElementById("resultsSummaryAnchor") || document.getElementById("outDcKw")?.closest(".tool-card");
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }

  // Action: Download Visual Audit Card (PNG)
  const downloadPngCardBtn = document.getElementById("downloadPngCardBtn");
  if (downloadPngCardBtn) {
    downloadPngCardBtn.addEventListener("click", () => {
      if (!state.calculatedState) return;
      VisualCard.generatePngCard(state.calculatedState);
    });
  }

  // Action: Copy Contractor Tender Spec
  const copyTenderBtn = document.getElementById("copyTenderBtn");
  if (copyTenderBtn) {
    copyTenderBtn.addEventListener("click", () => {
      if (!state.calculatedState) return;
      const tenderText = VisualCard.generateContractorTender(state.calculatedState);
      navigator.clipboard.writeText(tenderText).catch(() => {});
      copyFeedback.textContent = "✓ Contractor Tender Spec copied! Ready to send to installers.";
      copyFeedback.classList.remove("hidden");
      setTimeout(() => copyFeedback.classList.add("hidden"), 4000);
    });
  }

  // Sync initial DOM inputs with parsed state
  if (citySelect) {
    citySelect.value = state.cityKey;
  }
  if (billSlider && billValueDisplay) {
    billSlider.value = state.billPkr;
    billValueDisplay.textContent = `Rs. ${state.billPkr.toLocaleString()}`;
  }
  if (billInputNumber) {
    billInputNumber.value = state.billPkr;
    updatePresetChipsActive(state.billPkr);
  }
  if (nightAcToggle) {
    nightAcToggle.checked = state.nightAcEnabled;
    if (state.nightAcEnabled) {
      nightBatteryOptions.classList.remove("opacity-40", "pointer-events-none");
    } else {
      nightBatteryOptions.classList.add("opacity-40", "pointer-events-none");
    }
  }
  if (nightAcCountSlider && nightAcCountDisplay) {
    nightAcCountSlider.value = state.nightAcCount;
    nightAcCountDisplay.textContent = `${state.nightAcCount} AC${state.nightAcCount > 1 ? "s" : ""}`;
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
