# 2.45 GHz Inset-Fed Microstrip Patch Antenna

Design, optimization, and full-wave electromagnetic analysis of a 2.45 GHz inset-fed rectangular microstrip patch antenna using Ansys HFSS.

The project focuses on analytical antenna sizing, 50-ohm impedance matching, resonance tuning, far-field characterization, surface-current analysis, and adaptive mesh convergence.

![Antenna Geometry](hfss/results/geometry.png)

---

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

---

## Design and Optimization

The initial rectangular patch dimensions were calculated analytically and implemented in Ansys HFSS.

The first full-wave simulation produced a resonant frequency near **2.425 GHz**. Since the resonance was below the 2.45 GHz target, the patch length was reduced from **28.83 mm to 28.54 mm**.

After tuning, the antenna resonated at the target frequency of **2.450 GHz** while maintaining strong impedance matching.

The final design was evaluated using:

- S-parameters
- VSWR
- Input impedance
- Smith Chart
- Directivity and realized gain
- Radiation efficiency
- E-plane and H-plane radiation patterns
- Half-power beamwidth
- Surface-current distribution
- Adaptive mesh convergence

---

## Reflection Coefficient

The final antenna exhibits a deep resonance at **2.450 GHz** with:

**S11 = -29.04 dB**

![S11](hfss/results/s11.png)

The low reflection coefficient indicates that only a small fraction of the incident power is reflected at the design frequency.

---

## Input Impedance

At 2.45 GHz, the simulated input impedance is approximately:

**Zin = 50.60 + j3.50 ohm**

which is close to the target 50-ohm impedance.

![Input Impedance](hfss/results/input_impedance.png)

The Smith Chart marker at 2.45 GHz also lies close to the center of the chart, confirming good impedance matching.

![Smith Chart](hfss/results/smith_chart.png)

---

## Final HFSS Results

| Parameter | Result |
|---|---:|
| Resonant Frequency | 2.450 GHz |
| S11 | -29.04 dB |
| VSWR | ~1.07 |
| Input Impedance | 50.60 + j3.50 ohm |
| Peak Directivity | ~6.41 dBi |
| Peak Realized Gain | 3.53 dBi |
| Radiation Efficiency | ~51.5% |
| H-plane HPBW (Phi = 0 deg) | ~99.4 deg |
| E-plane HPBW (Phi = 90 deg) | ~89.8 deg |
| Main Beam Direction | +Z / Broadside |

---

## 3D Realized Gain

The antenna exhibits a broadside radiation characteristic, with the main beam directed approximately along the **+Z axis**.

The maximum realized gain is approximately:

**3.53 dBi**

![3D Realized Gain](hfss/results/realized_gain_3d.png)

---

## Half-Power Beamwidth

The -3 dB beamwidth was determined from the realized-gain radiation patterns at 2.45 GHz.

### H-plane — Phi = 0 deg

The -3 dB crossings occur at approximately:

- Theta = 48.64 deg
- Theta = 309.24 deg

giving:

**HPBW ≈ 99.4 deg**

![H-plane HPBW](hfss/results/h_plane_hpbw.png)

### E-plane — Phi = 90 deg

The -3 dB crossings occur at approximately:

- Theta = 45.04 deg
- Theta = 315.24 deg

giving:

**HPBW ≈ 89.8 deg**

![E-plane HPBW](hfss/results/e_plane_hpbw.png)

---

## Surface Current Distribution

Surface-current density was evaluated at the resonant frequency of 2.45 GHz.

The current distribution shows strong current concentration around the microstrip feed and inset region, followed by current spreading across the resonant patch.

![Surface Current](hfss/results/surface_current.png)

---

## Adaptive Mesh Convergence

The HFSS adaptive solution was configured with a convergence requirement of:

**Delta S < 0.02**

The solution converged after **13 adaptive passes**, reaching:

**Delta S = 0.011751**

![Mesh Convergence](hfss/results/convergence.png)

This convergence check was used to confirm that the reported electromagnetic results were obtained from a sufficiently refined adaptive solution.

---

## HFSS Model

The archived Ansys HFSS model is available in:

`hfss/Patch_Antenna_2p45GHz_Final.aedtz`

---

## Tools and Methods

- Ansys Electronics Desktop 2025 R2
- Ansys HFSS
- Finite Element Method (FEM)
- Adaptive tetrahedral meshing
- S-parameter analysis
- Smith Chart analysis
- Far-field radiation analysis
- Surface-current analysis

---

## Next Step — CST Cross-Validation

The same antenna geometry will be reproduced in **CST Studio Suite** using the same material properties and dimensions.

The HFSS and CST results will then be compared in terms of:

- Resonant frequency
- S11
- Input impedance
- Realized gain
- Radiation pattern
- Beamwidth

This will provide a cross-solver comparison of the same antenna design.
