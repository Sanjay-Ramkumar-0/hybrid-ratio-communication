import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# GLOBAL PARAMETERS
# =====================================================

NUM_SYMBOLS = 4000                # waveform-level → keep moderate
SYMBOL_SET = np.array([0, 1, 2, 3])
M = len(SYMBOL_SET)

SNR_DB = np.arange(0, 21, 2)

# Hybrid reference parameters
A1 = 1.0
F1 = 1.0

# FSK waveform parameters
Ts = 1e-3
fs = 100e3
fc = 10e3
df = 1 / Ts
Es = 1.0

t = np.arange(0, Ts, 1/fs)

# =====================================================
# CHANNEL MODELS
# =====================================================

def awgn_scalar(x, snr_db):
    snr = 10**(snr_db/10)
    noise_power = np.mean(x**2) / snr
    return x + np.sqrt(noise_power) * np.random.randn(len(x))

def awgn_waveform(x, snr_db):
    snr = 10**(snr_db/10)
    N0 = Es / snr
    noise_var = N0 * fs / 2
    return x + np.sqrt(noise_var) * np.random.randn(len(x))

def rayleigh_fading():
    return np.abs((np.random.randn() + 1j*np.random.randn()) / np.sqrt(2))

# =====================================================
# HYBRID TRANSMITTER
# =====================================================

def hybrid_transmit(symbols):
    A2 = (symbols + 1) * A1
    F2 = (symbols + 1) * F1
    return A2, F2

# =====================================================
# HYBRID RECEIVER (UNCHANGED LOGIC)
# =====================================================

def hybrid_decode(A1n, A2n, F1n, F2n):
    n_amp = A2n / A1n
    n_hat = np.round(n_amp)
    n_hat = np.clip(n_hat, 1, M)

    n_freq = F2n / F1n
    lower = n_hat - 0.5
    upper = n_hat + 0.5
    n_freq_bounded = np.clip(n_freq, lower, upper)

    n_final = np.round(n_freq_bounded)
    n_final = np.clip(n_final, 1, M)

    return n_final.astype(int) - 1

# =====================================================
# NON-COHERENT M-FSK TRANSMITTER
# =====================================================

def fsk_transmit(symbol):
    fk = fc + symbol * df
    return np.sqrt(2*Es/Ts) * np.cos(2*np.pi*fk*t)

# =====================================================
# NON-COHERENT ENERGY DETECTOR
# =====================================================

def fsk_energy_detector(rx):
    energies = np.zeros(M)
    for k in range(M):
        fk = fc + k * df
        cos_ref = np.cos(2*np.pi*fk*t)
        sin_ref = np.sin(2*np.pi*fk*t)
        I = np.sum(rx * cos_ref)
        Q = np.sum(rx * sin_ref)
        energies[k] = I**2 + Q**2
    return np.argmax(energies)

# =====================================================
# MAIN SIMULATION LOOP
# =====================================================

hybrid_SER = []
fsk_SER = []

for snr in SNR_DB:

    tx_symbols = np.random.choice(SYMBOL_SET, NUM_SYMBOLS)

    # ===========================
    # HYBRID SYSTEM (WITH FADING)
    # ===========================

    A2, F2 = hybrid_transmit(tx_symbols)

    A1_sig = A1 * np.ones(NUM_SYMBOLS)
    F1_sig = F1 * np.ones(NUM_SYMBOLS)

    # Independent Rayleigh fading per amplitude path
    h1 = np.array([rayleigh_fading() for _ in range(NUM_SYMBOLS)])
    h2 = np.array([rayleigh_fading() for _ in range(NUM_SYMBOLS)])

    A1n = awgn_scalar(h1 * A1_sig, snr)
    A2n = awgn_scalar(h2 * A2, snr)

    # Frequency paths assumed common (same oscillator)
    F1n = awgn_scalar(F1_sig, snr)
    F2n = awgn_scalar(F2, snr)

    rx_hybrid = hybrid_decode(A1n, A2n, F1n, F2n)
    hybrid_SER.append(np.mean(rx_hybrid != tx_symbols))

    # ===========================
    # FSK BASELINE (NO CHANGE)
    # ===========================

    errors = 0
    for sym in tx_symbols:
        s = fsk_transmit(sym)
        r = awgn_waveform(s, snr)
        if fsk_energy_detector(r) != sym:
            errors += 1

    fsk_SER.append(errors / NUM_SYMBOLS)

    print(f"SNR {snr:2d} dB | Hybrid SER = {hybrid_SER[-1]:.4f} | FSK SER = {fsk_SER[-1]:.4f}")

# =====================================================
# PLOT RESULTS
# =====================================================

plt.figure(figsize=(8,6))
plt.semilogy(SNR_DB, fsk_SER, 'o-', linewidth=2,
             label="Non-coherent M-FSK (AWGN)")
plt.semilogy(SNR_DB, hybrid_SER, 's-', linewidth=2,
             label="Hybrid ratio scheme (Rayleigh fading on amplitude)")
plt.xlabel("SNR (dB)")
plt.ylabel("Symbol Error Rate (SER)")
plt.title("Noise Robustness with Rayleigh Fading on Amplitude Paths")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
