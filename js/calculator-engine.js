/**
 * SOLARAUDIT.ONLINE - Mathematical & Physics Engine
 * Pure computation module: billing slabs, solar physics, energy storage & payback models.
 */

const CalculatorEngine = (function () {
  const data = typeof TARIFF_DATA !== "undefined" ? TARIFF_DATA : require("./tariff-data.js");

  /**
   * Calculate total PKR bill from monthly consumed units based on NEPRA 2026 progressive slabs.
   */
  function calculateBillFromUnits(units, discoKey = "kelectric") {
    const disco = data.discos[discoKey] || data.discos.kelectric;
    const slabs = disco.slabs;

    if (units <= 0) return 0;

    let baseEnergyCost = 0;
    const isProtected = units <= 200; // Protected threshold in Pakistan

    if (isProtected) {
      if (units <= 100) {
        baseEnergyCost = units * slabs.protected_1_100;
      } else {
        baseEnergyCost = (100 * slabs.protected_1_100) + ((units - 100) * slabs.protected_101_200);
      }
    } else {
      // Unprotected progressive slabs
      if (units <= 100) {
        baseEnergyCost = units * slabs.unprotected_1_100;
      } else if (units <= 200) {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + ((units - 100) * slabs.unprotected_101_200);
      } else if (units <= 300) {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + (100 * slabs.unprotected_101_200) + ((units - 200) * slabs.unprotected_201_300);
      } else if (units <= 400) {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + (100 * slabs.unprotected_101_200) + (100 * slabs.unprotected_201_300) + ((units - 300) * slabs.unprotected_301_400);
      } else if (units <= 500) {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + (100 * slabs.unprotected_101_200) + (100 * slabs.unprotected_201_300) + (100 * slabs.unprotected_301_400) + ((units - 400) * slabs.unprotected_401_500);
      } else if (units <= 600) {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + (100 * slabs.unprotected_101_200) + (100 * slabs.unprotected_201_300) + (100 * slabs.unprotected_301_400) + (100 * slabs.unprotected_401_500) + ((units - 500) * slabs.unprotected_501_600);
      } else if (units <= 700) {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + (100 * slabs.unprotected_101_200) + (100 * slabs.unprotected_201_300) + (100 * slabs.unprotected_301_400) + (100 * slabs.unprotected_401_500) + (100 * slabs.unprotected_501_600) + ((units - 600) * slabs.unprotected_601_700);
      } else {
        baseEnergyCost = (100 * slabs.unprotected_1_100) + (100 * slabs.unprotected_101_200) + (100 * slabs.unprotected_201_300) + (100 * slabs.unprotected_301_400) + (100 * slabs.unprotected_401_500) + (100 * slabs.unprotected_501_600) + (100 * slabs.unprotected_601_700) + ((units - 700) * slabs.unprotected_above_700);
      }
    }

    // Surcharges and Adjustments
    const fpaCost = units * disco.fuelPriceAdjustment;
    const financingSurchargeCost = units * disco.financingSurcharge;

    // Fixed capacity charges (applicable for higher sanctioned loads/slabs >300 units)
    let fixedCharges = 0;
    if (units > 300 && units <= 700) {
      fixedCharges = disco.fixedChargePerKw * 5; // Assumed 5 kW sanctioned
    } else if (units > 700) {
      fixedCharges = disco.fixedChargePerKw * 10; // Assumed 10 kW sanctioned
    }

    const subtotalEnergy = baseEnergyCost + fixedCharges;
    const electricityDuty = subtotalEnergy * (disco.electricityDutyPercent / 100);
    const taxableAmount = subtotalEnergy + fpaCost + financingSurchargeCost + electricityDuty;
    const gst = taxableAmount * (disco.gstPercent / 100);
    const totalBill = Math.round(taxableAmount + gst + disco.tvFee);

    return {
      units,
      baseEnergyCost: Math.round(baseEnergyCost),
      fpaCost: Math.round(fpaCost),
      financingSurchargeCost: Math.round(financingSurchargeCost),
      fixedCharges: Math.round(fixedCharges),
      electricityDuty: Math.round(electricityDuty),
      gst: Math.round(gst),
      tvFee: disco.tvFee,
      totalBill
    };
  }

  /**
   * Reverse-engineers unit consumption from a monthly PKR bill using binary search.
   */
  function estimateUnitsFromBill(billPkr, discoKey = "kelectric") {
    if (!billPkr || billPkr <= 0) return 0;

    let low = 1;
    let high = 5000;
    let bestUnits = 1;
    let minDiff = Infinity;

    // Binary search over 0 - 5000 units range
    for (let i = 0; i < 25; i++) {
      const mid = Math.round((low + high) / 2);
      const res = calculateBillFromUnits(mid, discoKey);
      const diff = Math.abs(res.totalBill - billPkr);

      if (diff < minDiff) {
        minDiff = diff;
        bestUnits = mid;
      }

      if (res.totalBill < billPkr) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }

    return bestUnits;
  }

  /**
   * Calculates required Solar System DC Capacity, panel count, and roof space.
   */
  function calculateSolarSizing(monthlyUnits, cityKey = "karachi") {
    const city = data.cities[cityKey] || data.cities.karachi;
    const psh = city.psh;
    const derating = data.hardware.panel.deratingFactor; // 0.78
    const panelWatts = data.hardware.panel.standardWattage; // 580W

    const dailyUnitsTarget = monthlyUnits / 30;
    // DC kW = Daily Units / (PSH * Derating)
    const rawKwRequired = dailyUnitsTarget / (psh * derating);

    // Calculate physical panels needed
    const panelCount = Math.max(4, Math.ceil((rawKwRequired * 1000) / panelWatts));
    const actualDcKw = (panelCount * panelWatts) / 1000;

    // Monthly units generated by this system
    const estimatedMonthlyGenerationUnits = Math.round(actualDcKw * psh * derating * 30);

    // Recommended Inverter capacity (kW)
    let inverterKw = 3;
    let inverterType = "hybrid_3kw";
    if (actualDcKw > 3.5 && actualDcKw <= 7.0) {
      inverterKw = 6;
      inverterType = "hybrid_6kw";
    } else if (actualDcKw > 7.0 && actualDcKw <= 9.0) {
      inverterKw = 8;
      inverterType = "hybrid_8kw";
    } else if (actualDcKw > 9.0 && actualDcKw <= 11.5) {
      inverterKw = 10;
      inverterType = "hybrid_10kw";
    } else if (actualDcKw > 11.5 && actualDcKw <= 14.0) {
      inverterKw = 12;
      inverterType = "hybrid_12kw";
    } else if (actualDcKw > 14.0) {
      inverterKw = 15;
      inverterType = "hybrid_15kw";
    }

    // Roof space requirements
    const areaSqFt = panelCount * data.hardware.panel.areaSqFtPerPanel;
    const areaMarlas = (areaSqFt / 225).toFixed(1); // 1 Marla = 225 sq. ft. in Pakistan standard

    return {
      monthlyUnitsTarget: monthlyUnits,
      actualDcKw: parseFloat(actualDcKw.toFixed(2)),
      panelCount,
      panelWattage: panelWatts,
      inverterKw,
      inverterType,
      areaSqFt,
      areaMarlas,
      estimatedMonthlyGenerationUnits,
      city: city.name,
      psh
    };
  }

  /**
   * Calculates night battery storage requirements for ACs & household baseline.
   */
  function calculateNightBattery(acCount = 1, nightHours = 8, batteryPreference = "lithium") {
    const acWatts = data.appliances.inverter_ac_1_5ton.avgRunningWatts; // 750W
    const baseFansLightsWatts = 200; // Fans + Wi-Fi + LED lights baseline

    const totalHourlyWatts = (acCount * acWatts) + baseFansLightsWatts;
    const totalEnergyWh = totalHourlyWatts * nightHours;
    const totalEnergyKwh = totalEnergyWh / 1000;

    const isLithium = batteryPreference === "lithium";

    let requiredNominalKwh = 0;
    let unitCount = 0;
    let estimatedCost = 0;
    let unitSpec = "";
    let warningNote = "";
    let lifespanYears = 0;

    if (isLithium) {
      const dod = data.hardware.battery.lithium_dod; // 85%
      const inverterEff = 0.92;
      requiredNominalKwh = totalEnergyKwh / (dod * inverterEff);
      unitCount = Math.max(1, Math.ceil(requiredNominalKwh / 5.12));
      estimatedCost = unitCount * data.hardware.battery.lithium_5kwh_unit_cost;
      unitSpec = `${unitCount}x 5.12 kWh LiFePO4 (51.2V 100Ah)`;
      lifespanYears = data.hardware.battery.lithium_lifespan_years;
      warningNote = "Optimal for continuous AC loads. 4,000+ deep cycle lifespan (approx. 10 years).";
    } else {
      // Tubular Lead Acid
      const dod = data.hardware.battery.tubular_dod; // 50%
      const inverterEff = 0.85;
      requiredNominalKwh = totalEnergyKwh / (dod * inverterEff);
      // 12V 230Ah = 2.76 kWh nominal
      const rawCount = Math.ceil(requiredNominalKwh / 2.76);
      // Tubular batteries must be in multiples of 4 for 48V hybrid inverters
      unitCount = Math.max(4, Math.ceil(rawCount / 4) * 4);
      estimatedCost = unitCount * data.hardware.battery.tubular_unit_cost;
      unitSpec = `${unitCount}x 12V 230Ah Deep Cycle Tubular Batteries`;
      lifespanYears = data.hardware.battery.tubular_lifespan_years;
      warningNote = "CAUTION: Heavy AC loads accelerate tubular plate sulfation. Expected replacement every 2 to 2.5 years.";
    }

    return {
      acCount,
      nightHours,
      batteryPreference,
      totalEnergyKwh: parseFloat(totalEnergyKwh.toFixed(1)),
      requiredNominalKwh: parseFloat(requiredNominalKwh.toFixed(1)),
      unitCount,
      unitSpec,
      estimatedCost,
      lifespanYears,
      warningNote
    };
  }

  /**
   * Comprehensive Turnkey Financials & Payback Period.
   * @param {Object} options - { mountingType: 'standard'|'elevated', meterType: 'three_phase'|'single_phase' }
   */
  function calculateFinancials(sizingResult, batteryResult, preBillPkr, discoKey = "kelectric", includeNetMetering = true, options = {}) {
    const mountingType = options.mountingType || "standard";
    const meterType = options.meterType || "three_phase";

    const panelsCost = sizingResult.actualDcKw * 1000 * data.hardware.panel.pricePerWattPkr;
    const inverterCost = data.hardware.inverters[sizingResult.inverterType] || 280000;
    
    // Balance of system (adds extra per watt if elevated L3 structure selected)
    const baseBosCostPerWatt = data.hardware.balanceOfSystem.bosCostPerWatt;
    const l3ExtraPerWatt = mountingType === "elevated" ? (data.hardware.balanceOfSystem.elevatedL3ExtraPerWatt || 14.0) : 0;
    const totalBosRate = baseBosCostPerWatt + l3ExtraPerWatt;
    const bosCost = sizingResult.actualDcKw * 1000 * totalBosRate;

    const netMeteringCost = includeNetMetering ? data.hardware.balanceOfSystem.netMeteringProcessCost : 0;
    const batteryCost = batteryResult ? batteryResult.estimatedCost : 0;

    const baseCapex = panelsCost + inverterCost + bosCost + netMeteringCost + batteryCost;
    const capexMin = Math.round(baseCapex * 0.94);
    const capexMax = Math.round(baseCapex * 1.06);
    const avgCapex = Math.round((capexMin + capexMax) / 2);

    // Calculate Residual Bill after solar offset
    const residualUnits = Math.max(0, sizingResult.monthlyUnitsTarget - sizingResult.estimatedMonthlyGenerationUnits);
    const postBill = residualUnits > 0 ? calculateBillFromUnits(residualUnits, discoKey).totalBill : 0;

    // Monthly Savings
    const monthlySavings = Math.max(0, preBillPkr - postBill);
    const annualSavings = monthlySavings * 12;

    // Payback Period (Months)
    const paybackMonths = annualSavings > 0 ? Math.round((avgCapex / annualSavings) * 12) : 0;
    const paybackYears = (paybackMonths / 12).toFixed(1);

    // 5-Year & 10-Year Net Financial Gain
    const fiveYearNetSavings = Math.round((annualSavings * 5) - avgCapex);
    const tenYearNetSavings = Math.round((annualSavings * 10) - avgCapex);

    // Single phase upgrade requirement notice
    const singlePhaseUpgradeFee = meterType === "single_phase" ? (data.hardware.balanceOfSystem.singlePhaseUpgradeEstCost || 40000) : 0;

    return {
      breakdown: {
        panelsCost: Math.round(panelsCost),
        inverterCost,
        bosCost: Math.round(bosCost),
        batteryCost,
        netMeteringCost,
        l3StructureCost: Math.round(sizingResult.actualDcKw * 1000 * l3ExtraPerWatt),
        singlePhaseUpgradeFee
      },
      mountingType,
      meterType,
      capexMin,
      capexMax,
      avgCapex,
      preBillPkr,
      postBillPkr: postBill,
      monthlySavings,
      annualSavings,
      paybackMonths,
      paybackYears,
      fiveYearNetSavings,
      tenYearNetSavings
    };
  }

  /**
   * The "Slab-Breaker" Sweet-Spot Strategy:
   * Calculates minimum viable solar (daytime-only, no battery) to drop user into base tariff bracket.
   */
  function calculateSweetSpot(monthlyUnits, discoKey = "kelectric", currentTotalCapex = null, options = {}) {
    if (monthlyUnits <= 300) {
      return null; // Already in a low/moderate bracket
    }

    const mountingType = options.mountingType || "standard";

    // Target dropping consumption to 200 units (protected/low-slab threshold)
    const unitsToShave = monthlyUnits - 200;
    const sweetSpotSizing = calculateSolarSizing(unitsToShave);

    // Turnkey capex for smaller daytime system (smaller 3kW/3.6kW inverter, no battery)
    const sweetPanelsCost = sweetSpotSizing.actualDcKw * 1000 * data.hardware.panel.pricePerWattPkr;
    const sweetInverterCost = data.hardware.inverters.hybrid_3kw || 165000;
    const l3Extra = mountingType === "elevated" ? (data.hardware.balanceOfSystem.elevatedL3ExtraPerWatt || 14.0) : 0;
    const sweetBosCost = sweetSpotSizing.actualDcKw * 1000 * (data.hardware.balanceOfSystem.bosCostPerWatt + l3Extra);
    const sweetNetMetering = data.hardware.balanceOfSystem.netMeteringProcessCost;

    const sweetCapexBase = sweetPanelsCost + sweetInverterCost + sweetBosCost + sweetNetMetering;
    const sweetCapexMin = Math.round(sweetCapexBase * 0.94);
    const sweetCapexMax = Math.round(sweetCapexBase * 1.06);
    const sweetAvgCapex = Math.round((sweetCapexMin + sweetCapexMax) / 2);

    const fullBill = calculateBillFromUnits(monthlyUnits, discoKey).totalBill;
    const residualBill = calculateBillFromUnits(200, discoKey).totalBill;
    const sweetSpotSavings = Math.max(0, fullBill - residualBill);

    // Compare with full configured capex if provided
    const baselineCapex = currentTotalCapex || (sweetAvgCapex * 2.2);
    const capexSavingsPkr = Math.max(0, baselineCapex - sweetAvgCapex);
    const capexReductionPercent = Math.min(85, Math.max(25, Math.round((capexSavingsPkr / baselineCapex) * 100)));

    return {
      currentUnits: monthlyUnits,
      targetUnits: 200,
      recommendedKw: sweetSpotSizing.actualDcKw,
      panelCount: sweetSpotSizing.panelCount,
      sweetCapexMin,
      sweetCapexMax,
      sweetAvgCapex,
      capexSavingsPkr,
      capexReductionPercent,
      monthlySavings: sweetSpotSavings,
      residualBill
    };
  }

  /**
   * Validates an installer quotation against wholesale equipment and labor benchmarks.
   */
  function validateInstallerQuote(quotedKw, quotedPricePkr, systemType = "hybrid") {
    if (!quotedKw || quotedKw <= 0 || !quotedPricePkr || quotedPricePkr <= 0) {
      return null;
    }
    const totalWatts = quotedKw * 1000;
    const ratePerWatt = Math.round(quotedPricePkr / totalWatts);
    const benchmarks = systemType === "ongrid"
      ? (data.hardware.quoteBenchmarks ? data.hardware.quoteBenchmarks.onGridNoBattery : { minFair: 85, maxFair: 115, cutCornerThreshold: 75, overpricedThreshold: 125 })
      : (data.hardware.quoteBenchmarks ? data.hardware.quoteBenchmarks.hybridWithBattery : { minFair: 130, maxFair: 165, cutCornerThreshold: 115, overpricedThreshold: 175 });

    let status = "fair";
    let statusClass = "text-emerald-900 bg-emerald-50 border-emerald-200";
    let badgeText = "✓ Fair Market Pricing";
    let title = `Rs. ${ratePerWatt.toLocaleString()} / Watt — Competitive Turnkey Rate`;
    let description = "This quotation aligns with current wholesale Tier-1 component costs and healthy contractor engineering margins in Pakistan.";

    if (ratePerWatt < benchmarks.cutCornerThreshold) {
      status = "cheap";
      statusClass = "text-amber-900 bg-amber-50 border-amber-200";
      badgeText = "⚠️ Suspiciously Low (Quality Risk)";
      title = `Rs. ${ratePerWatt.toLocaleString()} / Watt — High Cut-Corner Risk`;
      description = "At this price, installers frequently cut corners using B-grade/refurbished panels, non-copper aluminum wiring, or 24V inverters without surge protection. Verify Tier-1 flash-test barcodes and written warranties.";
    } else if (ratePerWatt > benchmarks.overpricedThreshold) {
      const benchmarkAvg = (benchmarks.minFair + benchmarks.maxFair) / 2;
      const excessPkr = Math.round((ratePerWatt - benchmarkAvg) * totalWatts);
      status = "overpriced";
      statusClass = "text-rose-900 bg-rose-50 border-rose-200";
      badgeText = "⚠️ High Contractor Markup";
      title = `Rs. ${ratePerWatt.toLocaleString()} / Watt — Quoted Above Benchmark`;
      description = `This quote is approximately Rs. ${(excessPkr / 100000).toFixed(1)} Lakhs above standard market pricing for equivalent Tier-1 hardware. Request an itemized Bill of Materials (BOM) or seek a competing bid.`;
    }

    return {
      quotedKw,
      quotedPricePkr,
      systemType,
      ratePerWatt,
      status,
      statusClass,
      badgeText,
      title,
      description
    };
  }

  return {
    calculateBillFromUnits,
    estimateUnitsFromBill,
    calculateSolarSizing,
    calculateNightBattery,
    calculateFinancials,
    calculateSweetSpot,
    validateInstallerQuote
  };
})();

// Export for browser or node test environments
if (typeof module !== "undefined" && module.exports) {
  module.exports = CalculatorEngine;
}
