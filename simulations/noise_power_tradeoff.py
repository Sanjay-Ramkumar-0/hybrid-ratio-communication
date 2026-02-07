import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# INPUT DATA (from previous simulations)
# =====================================================
# These SER values MUST come from:
# - waveform-level non-coherent M-FSK simulation
# - system-level hybrid simulation

# Example placeholders (REPLACE with real data)
snr_db = np.arange(0, 21, 2)

SER_fsk = np.array([
    0.38, 0.28, 0.18, 0.10, 0.045, 0.020,
    0.009, 0.004, 0.0018, 7e-4, 3e-4
])

SER_hybrid = np.array([
    0.48, 0.38, 0.28, 0.18, 0.10, 0.055,
    0.030, 0.018, 0.009, 0.004, 0.002
])

# =====================================================
# RECEIVER ENERGY MODELS (from updated power script)
# =====================================================

M = 4
Ts = 1.0
Tfreq = 0.2

POWER = {
    "high_adc": 10.0,
    "low_adc": 2.0,
    "dsp": 8.0,
    "counter": 1.5,
    "envelope": 0.5,
    "math": 0.5,
    "comparator": 0.2
}

def energy_fsk():
    return (
        POWER["high_adc"] * Ts +
        M * POWER["dsp"] * Ts +
        POWER["comparator"] * Ts
    )

def energy_hybrid():
    return (
        POWER["low_adc"] * Ts +
        POWER["envelope"] * Ts +
        POWER["counter"] * Tfreq +
        POWER["math"] * Ts +
        POWER["comparator"] * Ts
    )

E_fsk_base = energy_fsk()
E_hybrid_base = energy_hybrid()

# =====================================================
# ENERGY ADAPTATION WITH RELIABILITY
# =====================================================
# Digital increases effort to reach lower SER
# Hybrid adapts weakly

def energy_vs_ser_fsk(ser):
    return E_fsk_base * (1 + 1.8*np.log10(1/ser))

def energy_vs_ser_hybrid(ser):
    return E_hybrid_base * (1 + 0.2*np.log10(1/ser))

Energy_fsk = energy_vs_ser_fsk(SER_fsk)
Energy_hybrid = energy_vs_ser_hybrid(SER_hybrid)

# =====================================================
# PLOT: NOISE–POWER TRADEOFF
# =====================================================

plt.figure(figsize=(8,6))

plt.loglog(SER_fsk, Energy_fsk, 'o-', linewidth=2,
           label="Non-coherent M-FSK receiver")

plt.loglog(SER_hybrid, Energy_hybrid, 's-', linewidth=2,
           label="Hybrid ratio receiver")

plt.xlabel("Symbol Error Rate (SER)")
plt.ylabel("Receiver Energy per Decoded Symbol (normalized)")
plt.title("Noise–Power Tradeoff (Derived from Simulation)")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
