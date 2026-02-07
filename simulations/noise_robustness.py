import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# GLOBAL PARAMETERS
# =====================================================

NUM_SYMBOLS = 3000          # Monte Carlo symbols (waveform-level → keep reasonable)
SYMBOL_SET = np.array([0,1,2,3])   # M = 4 FSK
M = len(SYMBOL_SET)

SNR_DB = np.arange(0, 21, 2)

# Hybrid parameters (system-level)
A1 = 1.0
F1 = 1.0

# FSK waveform parameters
Ts = 1e-3                  # symbol duration
fs = 100e3                 # sampling frequency
fc = 10e3                  # carrier frequency
df = 1 / Ts                # orthogonal spacing
Es = 1.0                   # symbol energy

t = np.arange(0, Ts, 1/fs)

# =====================================================
# AWGN CHANNEL (WAVEFORM)
# =====================================================

def add_awgn_waveform(x, snr_db, Es):
    snr = 10**(snr_db/10)
    N0 = Es / snr
    noise_var = N0 * fs / 2
    noise = np.sqrt(noise_var) * np.random.randn(len(x))
    return x + noise


# =====================================================
# HYBRID RATIO TRANSMITTER
# =====================================================

def hybrid_transmit(symbols):
    A2 = symbols * A1
    F2 = symbols * F1
    return A2, F2


# =====================================================
# HYBRID RATIO RECEIVER
# =====================================================

def hybrid_decode(A1n, A2n, F1n, F2n):

    n_amp = A2n / A1n
    n_hat = np.round(n_amp)
    n_hat = np.clip(n_hat, SYMBOL_SET.min()+1, SYMBOL_SET.max()+1)

    n_freq = F2n / F1n

    lower = n_hat - 0.5
    upper = n_hat + 0.5
    n_freq_bounded = np.clip(n_freq, lower, upper)

    n_final = np.round(n_freq_bounded)
    n_final = np.clip(n_final, SYMBOL_SET.min()+1, SYMBOL_SET.max()+1)

    return n_final.astype(int)


# =====================================================
# NON-COHERENT M-FSK TRANSMITTER
# =====================================================

def fsk_transmit_waveform(symbol):
    fk = fc + symbol * df
    s = np.sqrt(2*Es/Ts) * np.cos(2*np.pi*fk*t)
    return s


# =====================================================
# NON-COHERENT M-FSK ENERGY DETECTOR
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

    # ---------------------------
    # Generate symbols
    # ---------------------------
    tx_symbols = np.random.choice(SYMBOL_SET, NUM_SYMBOLS)

    # ===========================
    # HYBRID SYSTEM (SYSTEM LEVEL)
    # ===========================

    A2, F2 = hybrid_transmit(tx_symbols + 1)

    A1_signal = A1 * np.ones(NUM_SYMBOLS)
    F1_signal = F1 * np.ones(NUM_SYMBOLS)

    def add_awgn_scalar(x, snr_db):
        snr = 10**(snr_db/10)
        noise_power = np.mean(x**2) / snr
        return x + np.sqrt(noise_power) * np.random.randn(len(x))

    A1n = add_awgn_scalar(A1_signal, snr)
    A2n = add_awgn_scalar(A2, snr)
    F1n = add_awgn_scalar(F1_signal, snr)
    F2n = add_awgn_scalar(F2, snr)

    rx_hybrid = hybrid_decode(A1n, A2n, F1n, F2n) - 1
    ser_h = np.mean(rx_hybrid != tx_symbols)
    hybrid_SER.append(ser_h)

    # ===========================
    # FSK BASELINE (WAVEFORM LEVEL)
    # ===========================

    errors = 0

    for sym in tx_symbols:
        s = fsk_transmit_waveform(sym)
        r = add_awgn_waveform(s, snr, Es)
        detected = fsk_energy_detector(r)

        if detected != sym:
            errors += 1

    ser_f = errors / NUM_SYMBOLS
    fsk_SER.append(ser_f)

    print(f"SNR {snr:2d} dB | Hybrid SER = {ser_h:.4f} | FSK SER = {ser_f:.4f}")

# =====================================================
# PLOT RESULTS
# =====================================================

plt.figure(figsize=(8,6))
plt.semilogy(SNR_DB, fsk_SER, 'o-', linewidth=2, label="Non-coherent M-FSK (energy detection)")
plt.semilogy(SNR_DB, hybrid_SER, 's-', linewidth=2, label="Hybrid Ratio Scheme (system-level)")
plt.xlabel("SNR (dB)")
plt.ylabel("Symbol Error Rate (SER)")
plt.title("Noise Robustness Comparison (Proper FSK Baseline)")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
