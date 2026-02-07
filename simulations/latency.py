import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# SYSTEM PARAMETERS (normalized)
# =====================================================

snr_db = np.arange(0, 21, 2)

Ts = 1.0                  # symbol duration (normalized)
TRIALS = 10000

# =====================================================
# DIGITAL FSK LATENCY MODEL
# =====================================================

FSK_FRAME_LEN = 80        # symbols per frame
FSK_SYNC_TIME = 10        # sync overhead (symbols)

def retry_prob_fsk(snr):
    """
    Non-coherent FSK retry probability.
    Decreases with SNR.
    """
    return np.exp(-snr / 6)

def latency_fsk(snr):
    """
    Latency per decoded symbol for non-coherent M-FSK.
    """
    base_time = (FSK_SYNC_TIME + FSK_FRAME_LEN) * Ts

    if np.random.rand() < retry_prob_fsk(snr):
        return 2 * base_time
    return base_time


# =====================================================
# HYBRID RATIO LATENCY MODEL
# =====================================================

AMP_OBS_TIME = 0.2 * Ts        # amplitude observation
FREQ_CYCLES = 12               # number of cycles required
FREQ_PERIOD = 0.08 * Ts        # normalized period

def retry_prob_hybrid(snr):
    """
    Hybrid retry probability.
    """
    return np.exp(-snr / 10)

def latency_hybrid(snr):
    """
    Latency per decoded symbol for hybrid ratio receiver.
    """
    freq_time = FREQ_CYCLES * FREQ_PERIOD
    decision_time = 0.1 * Ts

    base_time = AMP_OBS_TIME + freq_time + decision_time

    if np.random.rand() < retry_prob_hybrid(snr):
        return 2 * base_time
    return base_time


# =====================================================
# MONTE CARLO SIMULATION
# =====================================================

lat_fsk = []
lat_hybrid = []

for snr in snr_db:
    fsk_times = []
    hybrid_times = []

    for _ in range(TRIALS):
        fsk_times.append(latency_fsk(snr))
        hybrid_times.append(latency_hybrid(snr))

    lat_fsk.append(np.mean(fsk_times))
    lat_hybrid.append(np.mean(hybrid_times))


# =====================================================
# PLOT RESULTS
# =====================================================

plt.figure(figsize=(8,6))
plt.plot(snr_db, lat_fsk, linewidth=2,
         label="Non-coherent M-FSK (frame-based)")
plt.plot(snr_db, lat_hybrid, linewidth=2,
         label="Hybrid ratio receiver (single-symbol)")

plt.xlabel("SNR (dB)")
plt.ylabel("Average Decode Latency (symbol times)")
plt.title("Latency Comparison with Frequency Estimation")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
