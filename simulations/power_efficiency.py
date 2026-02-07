import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# SYSTEM PARAMETERS (normalized)
# =====================================================

M = 4                  # M-FSK
Ts = 1.0               # symbol duration (normalized)
Tfreq = 0.2            # frequency observation time (fraction of Ts)

# =====================================================
# NORMALIZED POWER PER BLOCK
# (relative, not absolute)
# =====================================================

POWER = {
    "high_adc": 10.0,        # high-rate ADC
    "low_adc": 2.0,          # low-rate ADC
    "dsp": 8.0,              # per correlator DSP
    "counter": 1.5,          # frequency counter
    "envelope": 0.5,         # envelope detector
    "math": 0.5,             # simple arithmetic
    "comparator": 0.2
}

# =====================================================
# ENERGY PER SYMBOL MODELS
# =====================================================

def energy_fsk():
    """
    Non-coherent M-FSK receiver:
    - High-rate ADC active for full Ts
    - M parallel correlators
    - DSP integration over Ts
    """
    E_adc = POWER["high_adc"] * Ts
    E_dsp = M * POWER["dsp"] * Ts
    E_cmp = POWER["comparator"] * Ts
    return E_adc + E_dsp + E_cmp


def energy_hybrid():
    """
    Hybrid ratio receiver:
    - Low-rate ADC / envelope detector
    - Short frequency observation window
    - No continuous DSP
    """
    E_adc = POWER["low_adc"] * Ts
    E_env = POWER["envelope"] * Ts
    E_freq = POWER["counter"] * Tfreq
    E_math = POWER["math"] * Ts
    E_cmp = POWER["comparator"] * Ts
    return E_adc + E_env + E_freq + E_math + E_cmp


E_fsk = energy_fsk()
E_hybrid = energy_hybrid()

print(f"FSK receiver energy per symbol   : {E_fsk:.2f}")
print(f"Hybrid receiver energy per symbol: {E_hybrid:.2f}")
print(f"Energy reduction factor          : {E_fsk / E_hybrid:.1f}x")

# =====================================================
# ENERGY vs RELIABILITY (NOISE–POWER TRADEOFF)
# =====================================================

target_SER = np.logspace(-1, -4, 20)

# Digital FSK burns more energy to improve reliability
energy_fsk_curve = E_fsk * (1 + 1.8*np.log10(1/target_SER))

# Hybrid stays mostly flat (limited adaptation)
energy_hybrid_curve = E_hybrid * (1 + 0.2*np.log10(1/target_SER))

# =====================================================
# PLOT
# =====================================================

plt.figure(figsize=(8,6))
plt.semilogx(target_SER, energy_fsk_curve, linewidth=2,
             label="Non-coherent M-FSK receiver")
plt.semilogx(target_SER, energy_hybrid_curve, linewidth=2,
             label="Hybrid ratio receiver")

plt.gca().invert_xaxis()
plt.xlabel("Target Symbol Error Rate (SER)")
plt.ylabel("Receiver Energy per Decoded Symbol (normalized)")
plt.title("Receiver Power Efficiency Comparison")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()

