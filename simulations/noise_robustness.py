import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# GLOBAL PARAMETERS
# =====================================================

NUM_SYMBOLS = 200000        # Monte Carlo depth (increase for smoother curves)
SYMBOL_SET = np.array([1,2,3,4])   # transmitted symbol levels
SNR_DB = np.arange(0, 21, 2)

A1 = 1.0                   # reference amplitude
F1 = 1.0                   # reference frequency

# =====================================================
# AWGN NOISE FUNCTION
# =====================================================

def add_awgn(x, snr_db):
    snr_lin = 10**(snr_db/10)
    power = np.mean(x**2)
    noise_power = power / snr_lin
    noise = np.sqrt(noise_power) * np.random.randn(len(x))
    return x + noise


# =====================================================
# HYBRID RATIO TRANSMITTER
# =====================================================

def hybrid_transmit(symbols):
    A2 = symbols * A1
    F2 = symbols * F1
    return A2, F2


# =====================================================
# HYBRID RATIO RECEIVER (CORRECT VERSION)
# =====================================================

def hybrid_decode(A1n, A2n, F1n, F2n):

    # --- Amplitude ratio (coarse anchor) ---
    n_amp = A2n / A1n
    n_hat = np.round(n_amp)

    n_hat = np.clip(n_hat, SYMBOL_SET.min(), SYMBOL_SET.max())

    # --- Frequency ratio (fine info) ---
    n_freq = F2n / F1n

    # --- BOUNDED HYBRID CONSTRAINT ---
    # Frequency is trusted ONLY inside amplitude-decoded region

    lower = n_hat - 0.5
    upper = n_hat + 0.5

    n_freq_bounded = np.clip(n_freq, lower, upper)

    # --- Final decision ---
    n_final = np.round(n_freq_bounded)
    n_final = np.clip(n_final, SYMBOL_SET.min(), SYMBOL_SET.max())

    return n_final


# =====================================================
# FSK BASELINE TRANSMITTER
# =====================================================

def fsk_transmit(symbols):
    return symbols.astype(float)


# =====================================================
# FSK BASELINE RECEIVER
# =====================================================

def fsk_decode(rx):
    rx_hat = np.round(rx)
    rx_hat = np.clip(rx_hat, SYMBOL_SET.min(), SYMBOL_SET.max())
    return rx_hat


# =====================================================
# MAIN SIMULATION LOOP
# =====================================================

hybrid_SER = []
fsk_SER = []

for snr in SNR_DB:

    # ---------------------------
    # Generate random data
    # ---------------------------
    tx_symbols = np.random.choice(SYMBOL_SET, NUM_SYMBOLS)

    # ===========================
    # HYBRID SYSTEM
    # ===========================

    A2, F2 = hybrid_transmit(tx_symbols)

    A1_signal = A1 * np.ones(NUM_SYMBOLS)
    F1_signal = F1 * np.ones(NUM_SYMBOLS)

    # Add AWGN
    A1n = add_awgn(A1_signal, snr)
    A2n = add_awgn(A2, snr)
    F1n = add_awgn(F1_signal, snr)
    F2n = add_awgn(F2, snr)

    rx_hybrid = hybrid_decode(A1n, A2n, F1n, F2n)

    ser_h = np.mean(rx_hybrid != tx_symbols)
    hybrid_SER.append(ser_h)

    # ===========================
    # FSK BASELINE
    # ===========================

    tx_fsk = fsk_transmit(tx_symbols)

    rx_fsk_noisy = add_awgn(tx_fsk, snr)

    rx_fsk = fsk_decode(rx_fsk_noisy)

    ser_f = np.mean(rx_fsk != tx_symbols)
    fsk_SER.append(ser_f)

    print(f"SNR {snr:2d} dB | Hybrid SER = {ser_h:.6f} | FSK SER = {ser_f:.6f}")


# =====================================================
# PLOT RESULTS
# =====================================================

plt.figure(figsize=(8,6))
plt.semilogy(SNR_DB, fsk_SER, 'o-', linewidth=2, label="FSK Baseline")
plt.semilogy(SNR_DB, hybrid_SER, 's-', linewidth=2, label="Hybrid Ratio Scheme")
plt.xlabel("SNR (dB)")
plt.ylabel("Symbol Error Rate (SER)")
plt.title("Noise Robustness Comparison (Monte Carlo)")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()
