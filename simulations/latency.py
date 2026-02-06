import numpy as np
import matplotlib.pyplot as plt

# =====================================
# PARAMETERS
# =====================================

snr_db = np.arange(0, 21, 2)

symbol_time = 1.0   # normalized time per symbol

# Digital system frame size (symbols)
DIGITAL_FRAME = 80

# Hybrid symbols needed
HYBRID_BASE = 1.5

# Retry probability vs SNR (simple realistic model)
def retry_prob_digital(snr):
    return np.exp(-snr/5)   # high retries at low SNR

def retry_prob_hybrid(snr):
    return np.exp(-snr/8)   # more robust due to simple detection

# =====================================
# MONTE CARLO LATENCY
# =====================================

TRIALS = 10000

lat_digital = []
lat_hybrid = []

for snr in snr_db:

    digital_times = []
    hybrid_times = []

    for _ in range(TRIALS):

        # ---- Digital ----
        time_d = DIGITAL_FRAME * symbol_time
        if np.random.rand() < retry_prob_digital(snr):
            time_d *= 2   # retransmission
        digital_times.append(time_d)

        # ---- Hybrid ----
        time_h = HYBRID_BASE * symbol_time
        if np.random.rand() < retry_prob_hybrid(snr):
            time_h *= 2
        hybrid_times.append(time_h)

    lat_digital.append(np.mean(digital_times))
    lat_hybrid.append(np.mean(hybrid_times))


# =====================================
# PLOT
# =====================================

plt.figure(figsize=(8,6))
plt.plot(snr_db, lat_digital, linewidth=2, label="Digital FSK-style system")
plt.plot(snr_db, lat_hybrid, linewidth=2, label="Hybrid ratio system")
plt.xlabel("SNR (dB)")
plt.ylabel("Average Decode Latency (symbol times)")
plt.title("Latency Comparison")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
