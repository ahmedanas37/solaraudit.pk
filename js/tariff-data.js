/**
 * SOLARAUDIT.ONLINE - Tariff & Hardware Pricing Configurations (2026 Edition)
 * Centralized data file: update this file whenever NEPRA or market rates change.
 */

const TARIFF_DATA = {
  version: "2026.1",
  lastUpdated: "September 2026",

  // Solar Insolation & Climate factors
  cities: {
    karachi: { name: "Karachi (K-Electric)", psh: 5.4, disco: "kelectric" },
    lahore: { name: "Lahore (LESCO)", psh: 5.0, disco: "lesco" },
    islamabad: { name: "Islamabad / Rawalpindi (IESCO)", psh: 5.1, disco: "iesco" },
    multan: { name: "Multan / South Punjab (MEPCO)", psh: 5.3, disco: "mepco" },
    peshawar: { name: "Peshawar (PESCO)", psh: 4.9, disco: "pesco" },
    faisalabad: { name: "Faisalabad (FESCO)", psh: 5.1, disco: "fesco" }
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
      hybrid_6kw: 280000,
      hybrid_8kw: 360000,
      hybrid_10kw: 440000,
      hybrid_12kw: 520000,
      hybrid_15kw: 620000,
      // On-grid string inverters
      ongrid_5kw: 175000,
      ongrid_10kw: 260000,
      ongrid_15kw: 340000,
      ongrid_20kw: 420000
    },
    battery: {
      // 51.2V 100Ah Lithium (LiFePO4) = 5.12 kWh
      lithium_5kwh_unit_cost: 310000,
      lithium_dod: 0.85, // 85% usable depth of discharge
      lithium_lifespan_years: 10,

      // 12V 230Ah Deep Cycle Tubular Lead Acid = 2.76 kWh nominal, 1.38 kWh usable
      tubular_unit_cost: 62000,
      tubular_dod: 0.50, // 50% max discharge before sulfation
      tubular_lifespan_years: 2.5
    },
    balanceOfSystem: {
      // Mounting structure, pure copper 6mm DC wire, AC cables, breakers, changeovers, earthing
      bosCostPerWatt: 22.0,
      elevatedL3ExtraPerWatt: 14.0, // Additional cost per watt for heavy-duty elevated pergola
      netMeteringProcessCost: 75000, // DisCo application, testing, green meter installation
      singlePhaseUpgradeEstCost: 40000 // Estimated DISCO demand notice fee to convert 1-phase to 3-phase
    },
    quoteBenchmarks: {
      hybridWithBattery: {
        minFair: 130, // Rs./W
        maxFair: 165,
        cutCornerThreshold: 115,
        overpricedThreshold: 175
      },
      onGridNoBattery: {
        minFair: 85,
        maxFair: 115,
        cutCornerThreshold: 75,
        overpricedThreshold: 125
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
    }
  }
};

// Export for browser or node test environments
if (typeof module !== "undefined" && module.exports) {
  module.exports = TARIFF_DATA;
}
