# Microstrip Transmission Line — Dielectric Loss Analysis

[Back to the portfolio](../README.md)

**Ansys HFSS · 2.45 GHz comparison · 2–3 GHz sweep · Simulation only**

## Overview

This project investigates signal transmission and reflection in a 40 mm microstrip line on an FR4 substrate. The line uses a 3 mm-wide copper trace above a finite copper ground plane, with a nominal 50 Ω design target.

Two HFSS models are compared. The baseline uses a dielectric loss tangent of 0.02; the second model sets this value to zero. Geometry, real relative permittivity, copper conductors, port definitions, and analysis settings are retained.

At **2.45 GHz**, the comparison gives:

- **Insertion loss:** 0.3392 dB → 0.0383 dB.
- **Transmitted incident power:** approximately 92.487% → 99.122%.
- **Reflected incident power:** approximately 0.309% → 0.248%.

These results support a substantial contribution from substrate dielectric loss in the baseline model. They do not constitute a measured loss budget or independently establish an exact 50 Ω characteristic impedance.

## Objective

Investigate how substrate dielectric loss influences the terminal S-parameters of a PCB transmission line, while developing a traceable simulation workflow covering geometry, material assignment, ports, boundaries, adaptive convergence, and result interpretation.

The structure represents a PCB interconnect between RF circuit elements. It is a transmission-line study, not an antenna-performance study.

## Geometry and Materials

![Microstrip transmission-line geometry](figures/geometry.png)

All dimensions and coordinates below are in **mm**, in the global coordinate system. The line extends along X, its width is along Y, and the stack-up is along Z.

| Object | Material / role | Origin (X, Y, Z) | Dimensions |
| --- | --- | --- | --- |
| Substrate | FR4 dielectric | (0, 0, 0) | 40 × 20 × 1.6 |
| Ground | Copper ground plane | (0, 0, −0.035) | 40 × 20 × 0.035 |
| Trace | Copper signal conductor | (0, 8.5, 1.6) | 40 × 3 × 0.035 |
| Port1Sheet | Terminal lumped-port sheet | (0, 8.5, 0) | Y: 3; Z: 1.6; normal along X |
| Port2Sheet | Terminal lumped-port sheet | (40, 8.5, 0) | Y: 3; Z: 1.6; normal along X |

The trace is centered across the substrate width. Both copper layers have a thickness of **35 µm**. No solder-mask or physical connector geometry is included.

### Controlled Material Comparison

| Substrate property | Baseline | Zero-dielectric-loss case |
| --- | --- | --- |
| Material definition | `FR4_epoxy` | Cloned FR4 definition (`FR4_epoxy - Copy`) |
| Relative permittivity, εr | 4.4 | 4.4 |
| Relative permeability, μr | 1 | 1 |
| Bulk conductivity | 0 S/m | 0 S/m |
| Dielectric loss tangent, tanδ | 0.02 | 0 |

The second material is an **idealized diagnostic model**, not a claim that real FR4 can be lossless. Copper remains a finite-conductivity material in both cases. The substrate has **Solve Inside enabled**; the copper trace and ground use **Solve Inside disabled**. Disabling Solve Inside for these copper objects does not make them perfect electric conductors.

The 3 mm trace width is an initial nominal-50 Ω choice, not the result of a completed impedance-optimization study. Setting the port reference impedance to 50 Ω does not force the physical line's characteristic impedance to that value.

## Simulation Setup

**Software:** Ansys Electronics Desktop Student 2025 R2.4 / HFSS.

**Design:** `HFSSDesign2`, Terminal Network.

| Setting | Configuration |
| --- | --- |
| Ports | Two terminal lumped ports |
| Signal conductor | Trace |
| Reference conductor | Ground |
| Port/reference impedance | 50 Ω at both ports |
| Port post-processing | Terminal renormalization enabled; lumped-port deembedding enabled |
| Open region | Created at 2.45 GHz with a Radiation boundary |
| Infinite ground | Disabled; the finite copper ground is modeled explicitly |
| Adaptive solution | Single frequency: 2.45 GHz |
| Maximum adaptive passes | 15 |
| Maximum Delta S target | 0.01 |
| Minimum adaptive passes | 2 |
| Required consecutive converged passes | 2 |
| Frequency sweep | Discrete, 2–3 GHz, 21 linearly spaced points |
| Frequency spacing | 50 MHz |
| Field storage | Adaptive-solution fields enabled; fields at all sweep frequencies not saved |

The open-region dimensions are stored in the model; a separate region-size sensitivity study has not yet been documented. The single-frequency adaptive criterion assesses convergence at 2.45 GHz, not independently at every sweep frequency.

For rectangular lumped ports, the deembedding used here addresses an approximate port-parasitic contribution; it is not a subtraction of the physical 40 mm line length. See the Ansys documentation on [lumped-port calibration/deembedding](https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/HFSS/Content/HFSS/WhenHFSSNeedsPortCalibrationdeembedding.htm).

## Method

1. Construct the substrate, copper trace, and finite ground plane.
2. Assign materials and define the surrounding open region.
3. Place port sheets between the trace and ground at both ends; assign terminal lumped ports.
4. Run HFSS Validation Check, solve the adaptive setup, and inspect convergence.
5. Solve the 21-point frequency sweep and plot terminal S11 and S21 in dB.
6. Record both values at 2.45 GHz.
7. Save a separate project, clone the FR4 material, and change only tanδ from 0.02 to 0.
8. Re-solve the modified model and compare results under the same reference conditions.

### Baseline Convergence

The baseline passed HFSS Validation Check and reached **CONVERGED** after **10 adaptive passes**, before the maximum of 15. The reported solved-element count increased from 909 to 7,807.

| Pass | Maximum magnitude of Delta S | Below 0.01? |
| --- | --- | --- |
| 8 | 0.010259 | No |
| 9 | 0.0057187 | Yes |
| 10 | 0.0048088 | Yes |

The final two consecutive passes met the specified criterion.

![Baseline adaptive-convergence record](figures/baseline_convergence.png)

This is evidence of baseline numerical convergence under the selected criterion, not a guarantee of 1% physical accuracy. The second model was re-solved, but its pass-by-pass convergence record is not included in this report. Check convergence for **both cases** when repeating or extending the comparison.

Ansys describes the distinction between adaptive stopping settings in its [adaptive-analysis documentation](https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/HFSS/Content/HFSS/SettingAdaptiveAnalysisParametersforHFSS.htm).

## Results

### Terminal S-Parameter Plots

**Baseline — tanδ = 0.02**

![Baseline S11 and S21 over 2–3 GHz, with markers at 2.45 GHz](figures/baseline_sparameters.png)

**Zero-dielectric-loss case — tanδ = 0**

![Zero-dielectric-loss S11 and S21 over 2–3 GHz, with markers at 2.45 GHz](figures/zero_dielectric_loss_sparameters.png)

The report uses:

- S11: `dB(St(Port1Sheet_T1,Port1Sheet_T1))`.
- S21: `dB(St(Port2Sheet_T1,Port1Sheet_T1))`.

### Comparison at 2.45 GHz

| Quantity | Baseline: tanδ = 0.02 | Zero dielectric loss: tanδ = 0 |
| --- | --- | --- |
| S11, dB | −25.1043 | −26.0617 |
| S21, dB | −0.3392 | −0.0383 |
| Return loss, dB | 25.1043 | 26.0617 |
| Insertion loss, dB | 0.3392 | 0.0383 |
| Reflected incident power | 0.309% | 0.248% |
| Transmitted incident power | 92.487% | 99.122% |
| Power-balance remainder at the two ports | 7.204% | 0.630% |

Values are taken from the 2.45 GHz plot markers. Power percentages are calculated from those rounded dB values.

### Power Interpretation

For real 50 Ω reference impedances, excitation at Port 1, and matched termination at Port 2:

$$
\frac{P_{\mathrm{reflected}}}{P_{\mathrm{incident}}}=|S_{11}|^2,
\qquad
\frac{P_{\mathrm{transmitted}}}{P_{\mathrm{incident}}}=|S_{21}|^2.
$$

Since the plotted magnitude is $S_{ij,\mathrm{dB}}=20\log_{10}|S_{ij}|$:

$$
\text{Power percentage}=100\times10^{S_{ij,\mathrm{dB}}/10}.
$$

The remaining fraction is:

$$
1-|S_{11}|^2-|S_{21}|^2.
$$

For an illustrative **100 mW incident power**, the zero-dielectric-loss model therefore corresponds to approximately **99.122 mW transmitted**, **0.248 mW reflected**, and a **0.630 mW remainder**. This is a scaling example, not a claim that a 100 mW source was configured in the simulation.

The remainder is not automatically conductor loss. It can include conductor dissipation and radiation, with additional uncertainty from numerical approximations and port post-processing. Reflected power is accounted for separately and should not be described as power dissipated in the line.

## Interpretation

Disabling substrate dielectric loss increases the transmitted fraction by approximately **6.635 percentage points** and reduces insertion loss by **0.3009 dB** at 2.45 GHz.

The comparison supports the conclusion that dielectric loss is a major contributor to the baseline line's attenuation. It also illustrates that low reflection does not imply negligible transmission loss: the baseline already has low S11 while transmitting about 92.49% of the incident power.

The change in the two-port power remainder is **not** a direct measurement of baseline dielectric heating. Material loss can also affect the complex impedance, field distribution, reflection, and other power contributions. A quantitative separation of dielectric, conductor, and radiation losses would require further analysis.

## Verification Status and Limitations

- **Simulation only:** No PCB fabrication, connector implementation, VNA measurement, or measurement-to-simulation comparison has been performed.
- **Material model:** Generic FR4 properties are used; no laminate-specific, frequency-dependent material characterization is included.
- **Numerical verification:** Baseline convergence is documented. Tighter convergence, full-band mesh sensitivity, and region-size sensitivity have not yet been demonstrated.
- **Port model:** Terminal lumped ports are idealizations. Port-size and deembedding sensitivity, or a wave-port cross-check, remain to be assessed.
- **Impedance target:** Low S11 at the 50 Ω reference does not independently prove an exact 50 Ω characteristic impedance.
- **Loss separation:** The approximately 0.63% residual in the modified model is not assigned entirely to copper loss.
- **Practical effects:** Solder mask, connectors, manufacturing tolerances, and laminate variability are not evaluated.
- **Data coverage:** The reported comparison is based on magnitude plots and point markers. Full complex S-parameter exports and phase/group-delay analysis are not included here.
- **Archive verification:** A clean-environment restore-and-re-solve test has not yet been documented.

## Model Files and Reproduction

| Archive | Description |
| --- | --- |
| [Microstrip_50Ohm.aedtz](models/Microstrip_50Ohm.aedtz) | Baseline FR4 model, tanδ = 0.02 |
| [Microstrip_FR4_tand0.aedtz](models/Microstrip_FR4_tand0.aedtz) | Same nominal geometry with substrate tanδ = 0 |

The archives were prepared **without Results/Solution Files**. They contain the model definitions and settings, but a new solve is required to regenerate numerical results and field data. The images above preserve the reported outputs. Ansys software is not included.

To repeat the comparison:

1. Use a compatible Ansys Electronics Desktop / HFSS installation; the original version was **Student 2025 R2.4**.
2. Choose **File → Restore Archive** and restore each archive into a separate working directory. Avoid overwriting existing project files.
3. Check the active project and substrate assignment: εr = 4.4 in both cases; tanδ = 0.02 for the baseline and 0 for the comparator. Confirm copper conductors and the recorded port/post-processing settings.
4. Run **Validation Check**, then **Analyze** on `Setup1`, including `Sweep_2to3GHz`.
5. Inspect convergence for each model before interpreting results. Do not treat reaching the maximum number of passes as successful convergence.
6. Open `Terminal S Parameter Plot1`, or create a Terminal Solution Data Report using `Setup1 : Sweep_2to3GHz`, `Freq`, and the S11/S21 expressions above.
7. Read markers at **2.45 GHz** and compare both dB values and power fractions. Document any differences in software version, settings, or convergence.

See Ansys documentation for [archiving projects](https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/HFSS/Content/Variables/ArchivingProjects.htm) and [restoring an archive](https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/HFSS/Content/Variables/RestoreArchiveCommand.htm).

## Further Work

The following are proposed extensions, not completed results:

- Preserve convergence records for both models and test tighter numerical settings.
- Export full complex S-parameters in Touchstone format.
- Cross-check characteristic impedance and study trace-width sensitivity.
- Visualize fields and surface currents to connect the geometry with propagation and return-current behavior.
- Compare finite-conductivity copper with an ideal-conductor case, supported by direct power-loss evaluation.
- Investigate boundary and port sensitivity before drawing conclusions from small residual losses.
