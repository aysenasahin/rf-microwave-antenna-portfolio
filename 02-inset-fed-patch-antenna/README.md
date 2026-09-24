# 2.45 GHz Inset-Fed Microstrip Patch Antenna

Design, optimization, and full-wave electromagnetic analysis of a 2.45 GHz inset-fed rectangular microstrip patch antenna using Ansys HFSS.

## Design Specifications

| Parameter | Value |
|---|---:|
| Target Frequency | 2.45 GHz |
| Substrate | FR4 |
| Relative Permittivity | 4.4 |
| Loss Tangent | 0.02 |
| Substrate Thickness | 1.6 mm |
| Copper Thickness | 0.035 mm |
| Patch Width | 37.26 mm |
| Initial Patch Length | 28.83 mm |
| Optimized Patch Length | 28.54 mm |
| Feed Width | 3.0 mm |
| Inset Depth | 8 mm |

## Design Process

The initial antenna dimensions were calculated analytically and implemented in Ansys HFSS.

The first full-wave simulation produced a resonance near 2.425 GHz. The patch length was reduced from 28.83 mm to 28.54 mm, shifting the resonance to the target frequency of 2.45 GHz.

Impedance matching and radiation performance were evaluated using S-parameters, VSWR, input impedance, Smith Chart, far-field radiation patterns, radiation efficiency, and surface current distribution.

## Final HFSS Results

| Parameter | Result |
|---|---:|
| Resonant Frequency | 2.450 GHz |
| S11 | -27.9 dB |
| VSWR | 1.08 |
| Input Impedance | 51.8 + j3.7 ohm |
| Peak Directivity | 6.41 dBi |
| Peak Realized Gain | 3.53 dBi |
| Radiation Efficiency | 51.5% |
| H-plane HPBW | 76.69 deg |
| E-plane HPBW | 45.04 deg |
| Main Beam Direction | +Z / Broadside |

## Mesh Convergence

The adaptive HFSS solution converged after 13 passes.

Final Delta-S:

0.011751 < 0.02

## Tools

- Ansys Electronics Desktop
- Ansys HFSS
- Full-wave FEM electromagnetic simulation
