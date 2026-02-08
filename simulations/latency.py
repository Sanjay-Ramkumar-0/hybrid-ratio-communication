import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# GLOBAL PARAMETERS (NORMALIZED)
# =====================================================

snr_db = np.arange(0, 21, 2)
TRIALS = 10000

Ts = 1.0                  # symbol duration (normalized units)

# =====================================================
# NON-COHERENT M-FSK LATENCY MODEL
# =====================================================

FSK_FRAME_LEN = 80        # symbols per frame
FSK_SYNC_LEN = 10         # sync overhead (symbols)

def retry_prob_fsk(snr):
    """
    Retransmission probability for non-coherent M-FSK.
    Decreases with SNR.
    """
    return np.exp(-snr / 6)

def latency_fsk(snr):
    """
    End-to-end latency per successfully decoded frame.
    """
    base_latency = (FSK_SYNC_LEN + FSK_FRAME_LEN) * Ts

    if np.random.rand() < retry_prob_fsk(snr):
        return 2 * base_latency
    return base_latency


# =====================================================
# HYBRID RATIO LATENCY MODEL
# =====================================================

# --- Derived from frequency_estimation.py ---
FREQ_CYCLES = 12          # chosen operating point
FREQ_PERIOD = 0.08 * Ts   # normalized period of frequency signal

# Observation windows
AMP_OBS_TIME = 0.2 * Ts
FREQ_OBS_TIME = FREQ_CYCLES * FREQ_PERIOD

# Synchronization & decision
HYBRID_SYNC_TIME = 0.1 * Ts
DECISION_TIME = 0.1 * Ts

def retry_prob_hybrid(snr):
    """
    Hybrid retry probability.
    Lower retries due to bounded decision region.
    """
    return np.exp(-snr / 10)

def latency_hybrid(snr):
    """
    End-to-end latency per decoded symbol for hybrid receiver.
    """
    base_latency = (
        HYBRID_SYNC_TIME +
        AMP_OBS_TIME +
        FREQ_OBS_TIME +
        DECISION_TIME
    )

    if np.random.rand() < retry_prob_hybrid(snr):
        return 2 * base_latency
    return base_latency


# =====================================================
# MONTE CARLO SIMULATION
# =====================================================

lat_fsk = []
lat_hybrid = []

for snr in snr_db:
    fsk_trials = []
    hybrid_trials = []

    for _ in range(TRIALS):
        fsk_trials.append(latency_fsk(snr))
        hybrid_trials.append(latency_hybrid(snr))

    lat_fsk.append(np.mean(fsk_trials))
    lat_hybrid.append(np.mean(hybrid_trials))

    print(f"SNR {snr:2d} dB | "
          f"FSK latency = {lat_fsk[-1]:.2f} Ts | "
          f"Hybrid latency = {lat_hybrid[-1]:.2f} Ts")

# =====================================================
# PLOT RESULTS
# =====================================================

plt.figure(figsize=(8,6))
plt.plot(snr_db, lat_fsk, linewidth=2,
         label="Non-coherent M-FSK (frame-based)")
plt.plot(snr_db, lat_hybrid, linewidth=2,
         label="Hybrid ratio receiver (single-symbol)")

plt.xlabel("SNR (dB)")
plt.ylabel("Average Decode Latency (symbol durations)")
plt.title("Latency Comparison with Explicit Frequency Estimation")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
