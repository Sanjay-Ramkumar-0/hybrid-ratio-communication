import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# SIGNAL & SIMULATION PARAMETERS
# =====================================================

fs = 200e3                # sampling frequency (Hz)
f0 = 10e3                 # true signal frequency (Hz)
Ts = 1 / f0               # signal period
A = 1.0                   # signal amplitude

SNR_DB = [0, 5, 10, 15, 20]
OBS_CYCLES = [4, 8, 12, 16, 24, 32]   # observation length in cycles
TRIALS = 1000

# =====================================================
# SIGNAL GENERATION
# =====================================================

def generate_signal(f, cycles):
    t = np.arange(0, cycles / f, 1/fs)
    s = A * np.sin(2 * np.pi * f * t)
    return t, s

# =====================================================
# AWGN CHANNEL
# =====================================================

def add_awgn(signal, snr_db):
    snr = 10**(snr_db / 10)
    power = np.mean(signal**2)
    noise_power = power / snr
    noise = np.sqrt(noise_power) * np.random.randn(len(signal))
    return signal + noise

# =====================================================
# ZERO-CROSSING FREQUENCY ESTIMATOR
# =====================================================

def estimate_frequency_zero_crossing(signal, fs):
    """
    Non-coherent frequency estimator using zero-crossing counting.
    Hardware-friendly and low complexity.
    """
    zero_crossings = np.where(np.diff(np.sign(signal)))[0]

    if len(zero_crossings) < 2:
        return np.nan

    periods = np.diff(zero_crossings) / fs
    return 1.0 / np.mean(periods)

# =====================================================
# MONTE CARLO SIMULATION
# =====================================================

results = {snr: [] for snr in SNR_DB}

for snr in SNR_DB:
    print(f"Simulating SNR = {snr} dB")

    for cycles in OBS_CYCLES:
        estimates = []

        for _ in range(TRIALS):
            _, s = generate_signal(f0, cycles)
            r = add_awgn(s, snr)

            f_hat = estimate_frequency_zero_crossing(r, fs)
            if not np.isnan(f_hat):
                estimates.append(f_hat)

        if len(estimates) == 0:
            variance = np.nan
        else:
            variance = np.var(estimates)

        results[snr].append(variance)

# =====================================================
# PLOT RESULTS
# =====================================================

plt.figure(figsize=(9, 6))

for snr in SNR_DB:
    plt.semilogy(OBS_CYCLES, results[snr], marker='o', linewidth=2,
                 label=f"SNR = {snr} dB")

plt.xlabel("Observation Length (Number of Cycles)")
plt.ylabel("Frequency Estimate Variance (Hz²)")
plt.title("Frequency Estimation Accuracy vs Observation Time\n(Zero-Crossing Estimator)")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
