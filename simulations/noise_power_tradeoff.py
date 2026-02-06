import numpy as np
import matplotlib.pyplot as plt

# =====================================
# SNR range
# =====================================

snr_db = np.arange(0, 21, 2)
snr_lin = 10**(snr_db/10)

# =====================================
# ERROR MODELS (simplified but realistic)
# =====================================

# Digital system more robust but costly
def SER_digital(snr):
    return np.exp(-0.7 * snr)

# Hybrid system moderate robustness
def SER_hybrid(snr):
    return np.exp(-0.4 * snr)

# =====================================
# CMOS-STYLE POWER MODELS
# =====================================

# normalized power (from earlier scaling)
P_digital_base = 200
P_hybrid_base = 12

# digital burns more power as it pushes for lower error
def power_digital(ser):
    return P_digital_base * (1 + 5*np.log10(1/ser))

# hybrid almost constant low power
def power_hybrid(ser):
    return P_hybrid_base * (1 + 0.3*np.log10(1/ser))

# =====================================
# COMPUTE TRADEOFF CURVES
# =====================================

SER_d = SER_digital(snr_lin)
SER_h = SER_hybrid(snr_lin)

Power_d = power_digital(SER_d)
Power_h = power_hybrid(SER_h)

# =====================================
# PLOT ENERGY vs ERROR
# =====================================

plt.figure(figsize=(8,6))
plt.loglog(SER_d, Power_d, 'o-', linewidth=2, label="Digital FSK-style system")
plt.loglog(SER_h, Power_h, 's-', linewidth=2, label="Hybrid ratio system")

plt.xlabel("Symbol Error Rate (SER)")
plt.ylabel("Energy per decoded symbol (normalized)")
plt.title("Noise–Power Tradeoff Comparison")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
