# Hybrid Ratio-Based Low-Power and Low-Latency Communication System

## Overview

This repository investigates a **ratio-based physical-layer communication architecture** designed to prioritize **receiver-side energy efficiency and low decoding latency** rather than spectral efficiency or Shannon-limit performance.

The proposed approach encodes information using **self-referenced amplitude and frequency ratios**, allowing decoding without reliance on absolute signal levels or carrier phase recovery. The system is evaluated at a **system and waveform level** and compared against a rigorously defined **non-coherent M-ary Frequency Shift Keying (M-FSK)** baseline.

The work is intended for **short-range, low-data-rate, energy-constrained communication scenarios**, such as IoT sensing, embedded control signaling, and low-power beacons.

---

## Motivation

Conventional digital communication systems achieve robustness through:

* High-resolution ADCs
* Continuous DSP processing
* Frame-based decoding and synchronization

While effective, these mechanisms impose **significant power and latency overhead**, which is undesirable in ultra-low-power or real-time systems.

This project explores an alternative design philosophy:

> **Shift complexity away from continuous digital processing and toward simple, self-referenced physical relationships.**

---

## Core Idea: Self-Referenced Ratio Encoding

### Transmitted Signals

Two signals are transmitted simultaneously:

* A **reference signal**
* A **scaled signal**

Information is encoded in the **ratio** between these signals.

### Amplitude Ratio (Coarse Information)

A₂ / A₁ = n

* Provides a coarse symbol estimate
* Does not require absolute gain calibration
* Sensitive to path mismatch (acknowledged)

### Frequency Ratio (Fine Information)

f₂ / f₁ = n + δ

* Refines the estimate within a bounded region
* Estimated non-coherently
* Requires finite observation time

### Hybrid Decoding Principle

The receiver first obtains a **coarse amplitude-based anchor**, then refines the estimate using a **bounded frequency ratio**, preventing large symbol jumps due to noise.

---

## Design Objectives (Explicit Scope)

This work **does not aim** to:

* Maximize spectral efficiency
* Approach Shannon capacity
* Compete with high-throughput digital standards

Instead, it targets:

* **Low receiver-side energy consumption**
* **Low end-to-end decoding latency**
* **Architectural simplicity**
* **Favorable noise–energy tradeoffs**

---

## Baseline System Definition: Non-Coherent M-FSK

To ensure a fair and defensible comparison, the baseline system is defined rigorously.

### Modulation

* **Non-coherent orthogonal M-FSK**
* Orthogonal spacing:
  [
  \Delta f = \frac{1}{T_s}
  ]

### Transmitted Signal

The transmitted waveform is:

`s_k(t) = sqrt(2·E_s / T_s) · cos(2π·f_k·t),   0 ≤ t < T_s`

with frequency mapping:

`f_k = f_c + k·Δf`

### Channel Model

[
r(t) = s_k(t) + n(t)
]

* Additive White Gaussian Noise (AWGN)
* No fading or interference

### Receiver

* Non-coherent energy detection
* M parallel correlators (I/Q)
* Full-symbol integration

This baseline reflects **practical low-power digital receivers** that avoid carrier phase recovery but still rely on high-rate sampling and DSP.

---

## Simulation Structure

```
simulations/
├── noise_robustness_fsk_waveform.py
├── power_efficiency.py
├── latency.py
├── noise_power_tradeoff.py
```

```
results/
├── noise_vs_snr.png
├── power_efficiency.png
├── latency.png
├── noise_power_tradeoff.png
```

---

## Simulation Descriptions and What They Prove

---

### 1. Noise Robustness (`noise_robustness_fsk_waveform.py`)

**Purpose:**
Compare symbol error rate (SER) under AWGN.

**Methodology:**

* FSK: waveform-level simulation with non-coherent energy detection
* Hybrid: system-level ratio decoding

**Result:**

* FSK achieves superior raw noise robustness
* Hybrid exhibits higher SER at low SNR

**Interpretation:**
This result is expected and establishes the **tradeoff foundation** for power and latency advantages.

---

### 2. Receiver Power Efficiency (`power_efficiency.py`)

**Purpose:**
Compare **receiver-side energy per decoded symbol**.

**Modeling Approach:**

* Block-level energy model
* Energy = Power × Active Time
* Explicit accounting for:

  * ADC activity
  * DSP correlators
  * Frequency counters
  * Observation windows

**Result:**

* M-FSK energy scales with:

  * Number of correlators
  * Symbol duration
* Hybrid energy remains significantly lower

**Claim Scope:**
Only **receiver-side baseband processing energy** is considered.

---

### 3. Latency Analysis (`latency.py`)

**Purpose:**
Compare decoding delay under realistic receiver assumptions.

**Latency Components:**

* Synchronization overhead (FSK)
* Symbol observation time
* Frequency estimation time (hybrid)
* Retransmission probability

**Key Result:**

* FSK latency dominated by framing and full-symbol integration
* Hybrid latency dominated by short observation windows

---

### 4. Noise–Power Tradeoff (`noise_power_tradeoff.py`)

**Purpose:**
Combine **measured SER** with **receiver energy models**.

**Important Note:**

* SER values are derived from simulations
* No assumed exponential error models

**Result:**

* To achieve a given reliability, the hybrid receiver consumes significantly less energy
* Demonstrates architectural efficiency rather than raw robustness

---

## Phase-2 Analytical Validation

To justify simulation assumptions, three analytical bounds are included.

---

### (a) Frequency Estimation Latency Bound

Frequency estimation requires observing multiple signal cycles:

Var(f̂) ≥ K / (T_obs² · SNR)

* N_cycles typically 8–20
* This bound is explicitly included in latency modeling

---

### (b) Frequency Estimation Accuracy Bound (CRLB Intuition)

For non-coherent frequency estimation in AWGN:

Var(f̂) ≥ K / (T_obs² · SNR)

This establishes an **accuracy–latency tradeoff**, justifying the chosen observation window.

---

### (c) Oscillator Stability Bound

Oscillator drift:

Δf = f · ppm · 10⁻⁶

Design requirement:

Δf · T_freq ≪ 1

This implies that **short-term stability**, not long-term accuracy, is sufficient.

---

## Simulation Scope and Limitations

The simulations are intended to evaluate **architectural tradeoffs**, not circuit-level performance.

**Limitations:**

* AWGN channel only
* No multipath fading or interference
* No Doppler modeling
* No PA non-linearity
* No ADC quantization modeling
* Transmitter energy not optimized
* Not intended to approach Shannon capacity

These assumptions allow isolation of **power and latency effects**.

---

## Key Takeaways

| Aspect           | FSK        | Hybrid Ratio |
| ---------------- | ---------- | ------------ |
| Noise robustness | High       | Moderate     |
| Receiver energy  | High       | Low          |
| Latency          | High       | Very low     |
| DSP complexity   | High       | Minimal      |
| Design goal      | Robustness | Efficiency   |

---

## Intended Use Cases

* Ultra-low-power IoT nodes
* Embedded control signaling
* Safety or event-triggered communication
* Short-range sensor networks

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running Simulations

```bash
python simulations/noise_robustness_fsk_waveform.py
python simulations/power_efficiency.py
python simulations/latency.py
python simulations/noise_power_tradeoff.py
```

---

## Author

**Sanjay Ramkumar**
Electronics and Communication Engineering

---

## Final Note

This repository explores a **receiver-centric communication architecture** where **energy efficiency and latency** are prioritized over spectral efficiency. The results demonstrate that meaningful communication is possible using simple physical relationships when system-level tradeoffs are explicitly acknowledged.
