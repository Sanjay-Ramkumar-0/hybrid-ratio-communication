# 📡 Hybrid Ratio-Based Low Power & Low-Latency Communication System

This repository presents a novel physical-layer (PHY) communication architecture based on **self-referenced amplitude and frequency ratios** for ultra-low power and low-latency signaling.

Unlike conventional digital communication systems that rely on high-resolution ADCs, heavy DSP processing, and packet-based decoding, the proposed method directly encodes information in **analog signal relationships**, enabling:

• drastically reduced power consumption
• near-instant decoding latency
• hardware-friendly receiver design

The system is especially suitable for:

IoT devices, safety-critical signaling, embedded systems, and energy-constrained communication.

---

# 🔍 Core Concept

Traditional communication systems transmit data using:

• absolute amplitude levels
• discrete frequency tones
• phase modulation
• heavy digital processing

These approaches require precise calibration and large computational effort.

---

## ✅ Proposed Approach: Self-Referenced Ratio Encoding

Two signals are transmitted simultaneously:

Signal 1 → reference
Signal 2 → scaled version

### Information is encoded as:

Amplitude Ratio:

```
A2 / A1 = n
```

Frequency Ratio:

```
f2 / f1 = n + δ
```

Where:

n = coarse symbol value
δ = fine refinement

Because the receiver decodes **ratios instead of absolute values**, the system becomes:

✔ robust to gain drift
✔ immune to absolute voltage scaling
✔ simpler to implement in hardware

---

# 🎯 Design Goals

This work does NOT aim to outperform modern digital systems in raw noise robustness.

Instead it targets:

✅ Ultra-low power consumption
✅ Ultra-low decoding latency
✅ Favorable noise–energy tradeoff
✅ Hardware simplicity

---

# 📁 Repository Structure

```
simulations/
    noise_robustness.py
    power_efficiency.py
    cmos_scaling.py
    latency.py
    noise_power_tradeoff.py

results/
    (generated plots)

README.md
requirements.txt
```

---

# 📊 Simulation Overview & What Each File Proves

---

## 📡 1. noise_robustness.py

### Symbol Error Rate vs SNR

This simulation compares:

• Conventional FSK-style digital demodulation
• Proposed hybrid ratio decoding

Under AWGN noise conditions.

### What it proves:

• Digital systems achieve higher raw noise robustness
• Hybrid ratio scheme is moderately less robust

This is expected and honest.

It establishes the **tradeoff foundation** for power and latency gains.

---

## 🔋 2. power_efficiency.py

### Energy per Decoded Symbol

This simulation models block-level energy consumption of:

• High-resolution ADC + DSP digital receiver
• Low-complexity hybrid ratio receiver

### What it proves:

• Hybrid receiver consumes orders of magnitude less energy
• Energy remains nearly constant across reliability levels
• Digital systems burn rapidly increasing power to improve accuracy

This is the primary strength of the proposed architecture.

---

## ⚡ 3. cmos_scaling.py

### CMOS Dynamic Power Model

Uses the realistic CMOS relationship:

```
P ∝ C · V² · f
```

Where switching capacitance and operating frequency represent hardware complexity.

### What it proves:

• DSP-based digital receivers scale very poorly with speed
• Hybrid ratio receiver scales gently
• Hardware-friendly design is inherently power efficient

This connects the work to real silicon behavior.

---

## ⏱ 4. latency.py

### Decoding Delay Comparison

Models:

• Packet/frame-based digital decoding
• Single-symbol hybrid decoding

Including retry effects under noise.

### What it proves:

• Digital systems require tens to hundreds of symbol durations
• Hybrid system decodes in ~1–2 symbol times

This enables real-time and safety-critical communication.

---

## ⚖️ 5. noise_power_tradeoff.py

### Energy vs Reliability

Combines:

Noise performance + power consumption

into a single system-level efficiency curve.

### What it proves:

• Digital systems achieve reliability only by burning massive energy
• Hybrid system achieves useful reliability at minimal energy

This demonstrates superior **noise–energy efficiency**.

---

# 📈 Key Results Summary

| Metric                        | Digital System | Hybrid Ratio System      |
| ----------------------------- | -------------- | ------------------------ |
| Noise Robustness              | High           | Moderate                 |
| Power Consumption             | Very High      | Very Low                 |
| Latency                       | High           | Extremely Low            |
| Hardware Complexity           | Heavy DSP      | Simple Analog + Counters |
| Energy–Reliability Efficiency | Poor           | Excellent                |

---

# 🚀 Why This Matters

Modern communication increasingly prioritizes:

• energy efficiency
• real-time response
• hardware simplicity

over pure data rate.

Applications include:

✔ IoT sensors
✔ automotive safety systems
✔ embedded control networks
✔ low-power ASIC communication

This work introduces a **new physical-layer primitive** optimized for these domains.

---

# ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

# ▶️ Running Simulations

Example:

```bash
python simulations/noise_robustness.py
```

Each script generates its corresponding plot in `results/`.

---

# 📜 Research Perspective

This project demonstrates:

• a new ratio-based signaling architecture
• quantitative system-level evaluation
• realistic power modeling
• latency-aware communication design

The results emphasize **engineering tradeoffs**, not unrealistic superiority.

---

# 📌 Future Extensions

Optional improvements include:

• fading channel models
• hardware prototype
• multi-symbol payload encoding
• ASIC area modeling

---

# ✍️ Author

Sanjay Ramkumar
Electronics & Communication Engineering

---

# 🧠 Final Note

This work explores an alternative communication paradigm where **meaning is encoded directly in physical signal relationships**, enabling ultra-low-power and low-latency operation — a key direction for next-generation embedded and semantic communication systems.
