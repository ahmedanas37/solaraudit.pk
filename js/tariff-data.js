/**
 * SOLARAUDIT.ONLINE - Tariff & Hardware Pricing Configurations (2026 Edition)
 * Centralized data file: update this file whenever NEPRA or market rates change.
 */

const TARIFF_DATA = {
  version: "2026.1",
  lastUpdated: "September 2026",

  // Solar Insolation & Climate factors
  cities: {
    karachi: { name: "Karachi (K-Electric)", psh: 5.4, disco: "kelectric", climate: "Coastal haze • High year-round sun" },
    lahore: { name: "Lahore (LESCO)", psh: 5.0, disco: "lesco", climate: "High summer sun • Winter smog factored" },
    islamabad: { name: "Islamabad / RWP (IESCO)", psh: 5.1, disco: "iesco", climate: "Clean air clearance • Moderate winters" },
    multan: { name: "Multan / South Punjab (MEPCO)", psh: 5.3, disco: "mepco", climate: "Intense solar insolation • Extreme heat" },
    faisalabad: { name: "Faisalabad (FESCO)", psh: 5.1, disco: "fesco", climate: "High solar hours • Seasonal dust" },
    gujranwala: { name: "Gujranwala / Sialkot (GEPCO)", psh: 5.0, disco: "gepco", climate: "Robust summer sun • Dense residential load" },
    peshawar: { name: "Peshawar (PESCO)", psh: 4.9, disco: "pesco", climate: "High solar angle • Cooler winter months" },
    quetta: { name: "Quetta / Balochistan (QESCO)", psh: 5.8, disco: "qesco", climate: "Highest solar potential in Pakistan (5.8 PSH)" },
    sukkur: { name: "Sukkur / Upper Sindh (SEPCO)", psh: 5.5, disco: "sepco", climate: "Intense solar insolation (5.5 PSH)" },
    hyderabad: { name: "Hyderabad / Lower Sindh (HESCO)", psh: 5.3, disco: "hesco", climate: "Strong wind corridors & reliable sunny days" }
  },

  // DISCO Base Tariffs & Taxes (NEPRA 2026 residential baseline)
  discos: {
    kelectric: {
      name: "K-Electric",
      fuelPriceAdjustment: 4.25, // Rs./kWh avg
      financingSurcharge: 3.23, // Rs./kWh
      electricityDutyPercent: 1.5, // %
      gstPercent: 18.0, // 18% GST
      tvFee: 35.0,
      fixedChargePerKw: 400.0, // For >5kW sanctioned load
      // Progressive base tariffs (Rs./unit)
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    lesco: {
      name: "LESCO (Lahore)",
      fuelPriceAdjustment: 3.90,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    iesco: {
      name: "IESCO (Islamabad)",
      fuelPriceAdjustment: 3.75,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    mepco: {
      name: "MEPCO (Multan)",
      fuelPriceAdjustment: 4.10,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    fesco: {
      name: "FESCO (Faisalabad)",
      fuelPriceAdjustment: 3.85,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    gepco: {
      name: "GEPCO (Gujranwala)",
      fuelPriceAdjustment: 3.95,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    pesco: {
      name: "PESCO (Peshawar)",
      fuelPriceAdjustment: 4.15,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    qesco: {
      name: "QESCO (Quetta)",
      fuelPriceAdjustment: 3.70,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    sepco: {
      name: "SEPCO (Sukkur)",
      fuelPriceAdjustment: 4.30,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    },
    hesco: {
      name: "HESCO (Hyderabad)",
      fuelPriceAdjustment: 4.20,
      financingSurcharge: 3.23,
      electricityDutyPercent: 1.5,
      gstPercent: 18.0,
      tvFee: 35.0,
      fixedChargePerKw: 400.0,
      slabs: {
        protected_1_100: 11.69,
        protected_101_200: 14.16,
        unprotected_1_100: 23.59,
        unprotected_101_200: 30.07,
        unprotected_201_300: 34.26,
        unprotected_301_400: 39.15,
        unprotected_401_500: 41.36,
        unprotected_501_600: 42.78,
        unprotected_601_700: 43.92,
        unprotected_above_700: 48.84
      }
    }
  },

  // Hardware Pricing & Engineering Constants (Karachi wholesale / retail benchmark)
  hardware: {
    panel: {
      standardWattage: 580, // N-Type TOPCon / Bifacial 580W
      pricePerWattPkr: 33.0, // Rs./watt (wholesale benchmark)
      areaSqFtPerPanel: 28.0, // ~2.27m x 1.13m = ~2.56 m² = 27.5-28 sq ft
      deratingFactor: 0.78 // Temperature degradation (40°C+ ambient), dust, DC wiring losses
    },
    inverters: {
      // Benchmark costs for Tier-1 hybrid inverters (Inverex, Knox, Huawei, Deye)
      hybrid_3kw: 165000,
      // Hybrid inverters (pure sine wave 48V / high-voltage 3-phase)
      hybrid_6kw: 230000,
      hybrid_8kw: 310000,
      hybrid_10kw: 380000,
      hybrid_12kw: 450000,
      hybrid_15kw: 540000,
      // On-grid string inverters
      ongrid_5kw: 155000,
      ongrid_10kw: 235000,
      ongrid_15kw: 310000,
      ongrid_20kw: 380000
    },
    battery: {
      // 51.2V 100Ah Lithium (LiFePO4) = 5.12 kWh (Current 2026 Hall Road / Saddar wholesale)
      lithium_5kwh_unit_cost: 225000,
      lithium_dod: 0.85, // 85% usable depth of discharge
      lithium_lifespan_years: 10,

      // 12V 230Ah Deep Cycle Tubular Lead Acid = 2.76 kWh nominal, 1.38 kWh usable
      tubular_unit_cost: 58000,
      tubular_dod: 0.50, // 50% max discharge before sulfation
      tubular_lifespan_years: 2.0
    },
    balanceOfSystem: {
      // Mounting structure, pure copper 6mm DC wire, AC cables, breakers, changeovers, earthing
      bosCostPerWatt: 20.0,
      elevatedL3ExtraPerWatt: 13.0, // Additional cost per watt for heavy-duty elevated pergola
      netMeteringProcessCost: 65000, // DisCo application, testing, green meter installation
      singlePhaseUpgradeEstCost: 35000 // Estimated DISCO demand notice fee to convert 1-phase to 3-phase
    },
    quoteBenchmarks: {
      hybridWithBattery: {
        minFair: 105, // Rs./W
        maxFair: 135,
        cutCornerThreshold: 95,
        overpricedThreshold: 150
      },
      onGridNoBattery: {
        minFair: 75,
        maxFair: 95,
        cutCornerThreshold: 65,
        overpricedThreshold: 110
      }
    }
  },

  // Appliance Power Ratings (Average Pakistani household specs)
  appliances: {
    inverter_ac_1_5ton: {
      name: "1.5-Ton Inverter AC (26°C Econ)",
      startupWatts: 1600,
      avgRunningWatts: 750,
      dailyHoursDefault: 8
    },
    inverter_ac_1ton: {
      name: "1.0-Ton Inverter AC (26°C Econ)",
      startupWatts: 1200,
      avgRunningWatts: 550,
      dailyHoursDefault: 8
    },
    ceiling_fan: {
      name: "Standard / BLDC Ceiling Fan",
      avgRunningWatts: 55,
      dailyHoursDefault: 14
    },
    refrigerator: {
      name: "Inverter Refrigerator",
      avgRunningWatts: 150,
      dailyHoursDefault: 24
    },
    water_pump_1hp: {
      name: "1.0 HP Water Pump",
      avgRunningWatts: 1100,
      dailyHoursDefault: 1
    },
    deep_freezer: {
      name: "Chest Deep Freezer",
      avgRunningWatts: 180,
      dailyHoursDefault: 24
    },
    led_lights_tv: {
      name: "LED Lights & TV / Wi-Fi",
      avgRunningWatts: 150,
      dailyHoursDefault: 6
    }
  }
};

// Export for browser or node test environments
if (typeof module !== "undefined" && module.exports) {
  module.exports = TARIFF_DATA;
}
