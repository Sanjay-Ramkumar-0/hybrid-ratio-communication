# Hybrid Ratio-Based Low-Power and Low-Latency Communication System

## Overview

This repository explores a **receiver-centric physical-layer communication architecture** designed for scenarios where:

* **Receiver energy consumption is critical**
* **Decoding latency must be very low**
* **Data rates are modest**
* **Channel conditions are controlled or short-range**

Instead of relying on continuous high-rate ADC sampling and heavy digital signal processing (DSP), the proposed approach encodes information using **self-referenced amplitude and frequency ratios**. This allows symbol decisions to be made using **simple analog and mixed-signal operations**, trading some noise robustness for substantial gains in **energy efficiency and latency**.

The system is evaluated using a combination of:

* **Waveform-level simulations** (for a digital baseline)
* **System-level modeling** (for the proposed architecture)

and compared against a rigorously defined **non-coherent M-ary FSK (M-FSK)** receiver.

---

## Design Philosophy

Conventional low-power digital receivers (including non-coherent ones) still rely on:

* High-rate ADCs
* Continuous DSP
* Frame-based decoding and synchronization

In ultra-low-power systems (e.g., wake-up radios, IoT beacons), this **receiver overhead can dominate total energy consumption**.

This project investigates a different design philosophy:

> *If moderate noise robustness is acceptable, can we drastically simplify the receiver by encoding information in physical signal relationships instead of absolute values?*

The answer explored here is **yes — within a clearly bounded scope**.

---

## Baseline System: Non-Coherent M-FSK

To ensure a fair and defensible comparison, the baseline system is **precisely defined and simulated at the waveform level**.

### Modulation

* Non-coherent M-ary Frequency Shift Keying
* Orthogonal spacing:
  **Δf = 1 / Tₛ**

### Transmitted Signal

For symbol `k ∈ {0, 1, …, M−1}`:

```
s_k(t) = sqrt(2·E_s / T_s) · cos(2π·f_k·t),   0 ≤ t < T_s
```

where:

```
f_k = f_c + k·Δf
```

### Channel Model

* Additive White Gaussian Noise (AWGN)
* Used as a clean reference case

### Receiver

* Non-coherent energy detection
* M parallel I/Q correlators
* Full-symbol integration

This baseline reflects **practical low-complexity digital receivers** that avoid carrier phase recovery but still incur significant ADC and DSP energy.

---

## Proposed Hybrid Ratio-Based Scheme

### Core Concept

Two signals are transmitted simultaneously:

* A **reference signal**
* A **scaled signal**

Information is encoded in **ratios**, not absolute values.

---

### Amplitude Ratio (Coarse Information)

```
A₂ / A₁ = n
```

* Provides a coarse symbol estimate
* Does not require absolute gain calibration
* Sensitive to channel variations (discussed below)

---

### Frequency Ratio (Fine Information)

```
f₂ / f₁ = n + δ
```

* Refines the estimate within a bounded region
* Estimated non-coherently
* Requires finite observation time

---

### Hybrid Decoding Logic

1. Decode a coarse symbol using the amplitude ratio
2. Use this estimate to bound the frequency ratio
3. Make a final symbol decision

This bounded approach prevents large symbol jumps due to noise.

---

## Practical Design Considerations and System Behavior

This section explains how the system behaves under realistic conditions and clarifies its applicability.

---

### Amplitude Ratio Sensitivity to Channel Variations

In real wireless channels, the reference and scaled signals may experience **independent fading**:

```
A₂_rx / A₁_rx = (|h₂| / |h₁|) · (A₂_tx / A₁_tx)
```

To study this effect:

* Independent Rayleigh fading is applied to the amplitude paths
* Symbol error rate (SER) is re-evaluated

**Observation:**

* The amplitude ratio becomes unreliable under independent fading
* Performance degrades rapidly compared to M-FSK

**Implication:**

> The amplitude-based component is best suited for **short-range, line-of-sight, or controlled propagation environments** where channel gains are correlated or quasi-static.

This explicitly bounds the applicability of the scheme.

---

### Frequency Ratio Estimation and Observation-Time Tradeoff

Frequency estimation is performed using a **non-coherent zero-crossing method**, chosen for:

* Low complexity
* Hardware friendliness
* No carrier phase recovery

Monte-Carlo simulations show:

* Short observation windows → high estimation variance
* Longer observation windows → improved accuracy

This establishes a clear **latency–accuracy tradeoff**.

A fixed observation length of **12 cycles** is selected as a reasonable operating point and is used consistently in latency modeling.

---

### Receiver Energy Modeling Approach

Receiver energy is modeled at the **architectural block level**, focusing on relative scaling trends rather than absolute power values.

Key assumptions:

* High-rate ADCs dominate energy consumption
* Continuous DSP is costly
* Counters and envelope detectors are lightweight

This abstraction is appropriate for **system-level architectural comparison** and is consistent with trends reported in ADC and low-power receiver literature.

---

### Transmitter Assumptions and System Asymmetry

The proposed scheme transmits two signals simultaneously, which may increase transmitter complexity.

This work intentionally targets **asymmetric systems**, such as:

* Wake-up radios
* Beacons
* Infrastructure-powered transmitters

In these cases, **receiver energy dominates system cost**, and transmitter optimization is acknowledged as a tradeoff and left for future work.

---

### Synchronization and Timing Considerations

Although the hybrid receiver operates on a symbol basis, it still requires:

* Symbol timing
* Observation window alignment

A small synchronization overhead is explicitly included in latency modeling to ensure a fair comparison with the frame-based M-FSK receiver.

---

## Phase-2 Analytical Validation

Simulation assumptions are supported by simple analytical bounds.

### Frequency Estimation Latency

```
T_freq = N_cycles / f
```

Frequency estimation requires observing multiple cycles; this is explicitly included in the latency model.

---

### Frequency Estimation Accuracy (CRLB Intuition)

```
Var(f̂) ≥ K / (T_obs² · SNR)
```

This explains the observed latency–accuracy tradeoff.

---

### Oscillator Stability Requirement

```
Δf = f · ppm · 10⁻⁶
```

Design requirement:

```
Δf · T_freq ≪ 1
```

Only **short-term oscillator stability** is required, which is achievable with low-cost oscillators.

---

## Simulation Files

```
simulations/
├── noise_robustness_fsk_waveform.py   # AWGN + Rayleigh fading analysis
├── frequency_estimation.py            # Zero-crossing frequency estimator
├── power_efficiency.py                # Receiver energy modeling
├── latency.py                         # Latency with explicit observation times
├── noise_power_tradeoff.py            # Derived SER–energy tradeoff
```

---

## Simulation Scope and Limitations

* AWGN and Rayleigh fading only
* No multipath delay spread
* No Doppler modeling
* No PA non-linearity
* No ADC quantization modeling
* Receiver-side focus
* Not intended to approach Shannon capacity

These assumptions isolate **architectural tradeoffs**.

---

## Key Takeaways

| Aspect           | M-FSK              | Hybrid Ratio        |
| ---------------- | ------------------ | ------------------- |
| Noise robustness | High               | Moderate            |
| Receiver energy  | High               | Low                 |
| Latency          | High (frame-based) | Low (symbol-based)  |
| DSP complexity   | High               | Minimal             |
| Applicability    | General            | Controlled channels |

---

## Intended Use Cases

* Wake-up radios
* IoT beacons
* Event-triggered signaling
* Short-range control communication

---

## Author

**Sanjay Ramkumar**
Electronics and Communication Engineering

---

## Final Note

This work demonstrates that **carefully bounded physical-layer simplification** can yield meaningful gains in energy efficiency and latency. Rather than competing with digital modulation universally, the proposed architecture serves as a **specialized communication primitive** for constrained, low-power environments.
