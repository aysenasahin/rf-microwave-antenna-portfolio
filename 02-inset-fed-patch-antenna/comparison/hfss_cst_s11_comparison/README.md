# HFSS–CST S11 comparison

Comparison of the one-port simulation results for a 2.45 GHz inset-fed microstrip patch antenna using Ansys HFSS and the CST time-domain solver. Both Touchstone exports use a **50 Ω reference impedance**.

![HFSS and CST S11 comparison](results/hfss_cst_s11_comparison.png)

## Results

The target-frequency values below are evaluated at the **exported 2.450 GHz sample in both files**.

| Metric | HFSS | CST time domain |
| --- | ---: | ---: |
| S11 at 2.450 GHz | −29.04 dB | −21.89 dB |
| VSWR at 2.450 GHz | 1.073 | 1.175 |
| Input impedance at 2.450 GHz | 50.60 + j3.50 Ω | 58.50 + j1.99 Ω |
| Frequency of sampled S11 minimum | 2.450 GHz | 2.441 GHz |
| Sampled minimum S11 | −29.04 dB | −36.68 dB |
| Estimated −10 dB lower band edge | 2.4111 GHz | 2.4020 GHz |
| Estimated −10 dB upper band edge | 2.4871 GHz | 2.4798 GHz |
| Estimated −10 dB bandwidth | 76.1 MHz | 77.8 MHz |
| Fractional bandwidth, referenced to 2.450 GHz | 3.11% | 3.17% |
| Reflected power fraction at 2.450 GHz | 0.125% | 0.647% |

The two results show similar −10 dB bandwidths. The CST sampled reflection minimum occurs **9 MHz below** the HFSS sampled minimum, equivalent to approximately **0.37% of 2.450 GHz**. At the target frequency, the HFSS model has the smaller reflection magnitude and VSWR. The deeper CST minimum at 2.441 GHz must be distinguished from its result at 2.450 GHz.

These observations describe the agreement between the two simulation results. A deeper S11 minimum alone does not establish which solver is more accurate. Port, boundary, material and mesh choices can contribute to differences; their individual contributions have not been isolated here.

## Data and calculation method

| Export property | HFSS | CST time domain |
| --- | --- | --- |
| Original export | `hfss_s11.s1p` | `cst_s11_3.s1p` |
| File in this package | [data/hfss_s11.s1p](data/hfss_s11.s1p) | [data/cst_s11.s1p](data/cst_s11.s1p) |
| Solver/project information from header | HFSS 2025.2.4; `Patch_Antenna_2p45GHz_Final`; `Setup1: Sweep` | CST; `InsetFed_PatchAntenna_2p45GHz_CST_TD.cst` |
| Touchstone representation | MA: magnitude and angle in degrees | RI: real and imaginary parts |
| Exported frequency range | 1.500–3.500 GHz | 2.000–3.000 GHz |
| Frequency sample spacing | 5 MHz | 1 MHz |
| Exported samples | 401 | 1001 |
| Reference impedance | 50 Ω | 50 Ω |

The original exports are included without changing their numerical contents. The CST file is renamed to `cst_s11.s1p` inside this package. The comparison plot uses the common **2.000–3.000 GHz** range, with a detail panel covering **2.380–2.520 GHz**. Lines connect the original exported samples; no smoothing or interpolation of the plotted curves is applied.

S11 minima are the minima of the **exported sample sets within the common range**. In particular, the HFSS 5 MHz export spacing is coarser than the CST 1 MHz spacing. These sampled minima do not locate continuous-curve minima with finer precision than the exports provide. Export sample spacing is separate from the solver's adaptive-mesh convergence criterion.

The −10 dB band edges are estimated by linear interpolation **in dB** between the two exported samples that bracket each crossing around the sampled minimum. Bandwidth is the difference between those two crossing frequencies. Fractional bandwidth is calculated relative to the common 2.450 GHz target frequency.

For complex reflection coefficient `Γ = S11`, the calculations are:

```text
S11_dB = 20 log10(|Γ|)
VSWR = (1 + |Γ|) / (1 − |Γ|)
Zin = 50 (1 + Γ) / (1 − Γ)
Reflected power (%) = 100 |Γ|²
Fractional bandwidth (%) = 100 (f_high − f_low) / 2.450 GHz
```

This package covers input reflection, matching and impedance. Radiation gain, efficiency and beamwidth require the corresponding far-field results.

## Reproduce

Install NumPy and Matplotlib, then run from this folder:

```bash
python -m pip install numpy matplotlib
python compare_s11.py
```

The script reads both one-port Touchstone representations, checks the shared 50 Ω reference and frequency ordering, calculates the target-frequency and band metrics, and produces:

- [Comparison PNG](results/hfss_cst_s11_comparison.png)
- [Comparison SVG](results/hfss_cst_s11_comparison.svg)
- [Full numerical metrics CSV](results/hfss_cst_s11_metrics.csv)

The figure and CSV are generated directly from the source files. They can be regenerated after exporting updated results by replacing the corresponding file in `data/`.

## Portfolio location

Suggested location in the existing portfolio:

`02-inset-fed-patch-antenna/comparison/`

Copy the **contents of this package folder** into that location, preserving `data/` and `results/`, so the relative links above continue to work. The antenna project's main README can link to `comparison/README.md` and display `comparison/results/hfss_cst_s11_comparison.png`.
