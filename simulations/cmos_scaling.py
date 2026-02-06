import numpy as np
import matplotlib.pyplot as plt

# ======================================
# CMOS POWER PARAMETERS (normalized)
# ======================================

Vdd = 1.0          # normalized supply voltage
alpha = 0.5       # switching activity

# Relative capacitance (complexity proxy)
C = {
    "DSP": 100,
    "ADC_high": 60,
    "ADC_low": 10,
    "counter": 8,
    "comparator": 2,
    "envelope": 2,
    "math": 4
}

# Operating frequencies (relative)
f_digital = 100      # high-speed DSP system
f_hybrid = 5         # slow simple processing

# ======================================
# CMOS power function
# ======================================

def cmos_power(cap_list, freq):
    total_C = sum(cap_list)
    return alpha * total_C * (Vdd**2) * freq


# ======================================
# Receiver power
# ======================================

P_fsk = cmos_power(
    [C["DSP"], C["ADC_high"], C["comparator"]],
    f_digital
)

P_hybrid = cmos_power(
    [C["ADC_low"], C["counter"], C["envelope"], C["math"], C["comparator"]],
    f_hybrid
)

print("Digital FSK power:", P_fsk)
print("Hybrid ratio power:", P_hybrid)
print("Power reduction factor:", P_fsk / P_hybrid)

# ======================================
# Show scaling vs speed
# ======================================

freq_range = np.linspace(1, 150, 50)

power_fsk_curve = alpha * (C["DSP"] + C["ADC_high"] + C["comparator"]) * freq_range
power_hybrid_curve = alpha * (C["ADC_low"] + C["counter"] + C["envelope"] + C["math"] + C["comparator"]) * freq_range

# ======================================
# Plot
# ======================================

plt.figure(figsize=(8,6))
plt.plot(freq_range, power_fsk_curve, linewidth=2, label="Digital Receiver (DSP based)")
plt.plot(freq_range, power_hybrid_curve, linewidth=2, label="Hybrid Ratio Receiver")
plt.xlabel("Operating Frequency (relative)")
plt.ylabel("Dynamic Power (normalized)")
plt.title("CMOS-Style Power Scaling Comparison")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
