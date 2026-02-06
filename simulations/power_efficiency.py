import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# ENERGY MODEL (normalized units)
# ==========================================

ENERGY = {
    "high_adc": 10,
    "low_adc": 2,
    "dsp": 15,
    "counter": 2,
    "comparator": 0.5,
    "envelope": 0.5,
    "math": 1
}

# ==========================================
# RECEIVER ENERGY PER SYMBOL
# ==========================================

def energy_fsk():
    return (
        ENERGY["high_adc"] +
        ENERGY["dsp"] +
        ENERGY["comparator"]
    )

def energy_hybrid():
    return (
        ENERGY["low_adc"] +
        ENERGY["envelope"] +
        ENERGY["counter"] +
        ENERGY["math"] +
        ENERGY["comparator"]
    )

E_fsk = energy_fsk()
E_hybrid = energy_hybrid()

print("FSK energy per symbol:", E_fsk)
print("Hybrid energy per symbol:", E_hybrid)

# ==========================================
# SIMULATE ENERGY VS TARGET ERROR RATE
# (lower SER usually requires more processing)
# ==========================================

target_SER = np.logspace(-1, -4, 20)

# Digital system often increases DSP effort at low SER
energy_fsk_curve = E_fsk * (1 + 2*np.log10(1/target_SER))

# Hybrid stays mostly constant (simple hardware)
energy_hybrid_curve = np.ones_like(target_SER) * E_hybrid

# ==========================================
# PLOT
# ==========================================

plt.figure(figsize=(8,6))
plt.semilogx(target_SER, energy_fsk_curve, linewidth=2, label="FSK Receiver")
plt.semilogx(target_SER, energy_hybrid_curve, linewidth=2, label="Hybrid Ratio Receiver")
plt.gca().invert_xaxis()
plt.xlabel("Target Symbol Error Rate (SER)")
plt.ylabel("Energy per Decoded Symbol (normalized units)")
plt.title("Power Efficiency Comparison")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
