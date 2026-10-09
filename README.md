# RF, Microwave & Antenna Engineering Portfolio

RF, microwave, and antenna simulation projects using **Ansys HFSS** and **CST Studio Suite**. The portfolio covers transmission-line modeling, dielectric loss, impedance matching, antenna optimization, field interpretation, mesh convergence, and comparison between electromagnetic simulation tools.

## Projects

### 01 · Microstrip Transmission Line — Dielectric Loss Analysis

[View project documentation](01-microstrip-transmission-line/README.md)

A **40 mm FR4 microstrip transmission line** with a nominal **50 Ω** design target, modeled in HFSS to investigate the effect of substrate dielectric loss.

- Modeled a two-port microstrip structure using terminal lumped ports and radiation boundaries.
- Compared identical structures with **tanδ = 0.02** and **tanδ = 0** over **2–3 GHz**.
- At **2.45 GHz**, simulated insertion loss decreased from **0.3392 dB to 0.0383 dB** when dielectric loss was disabled.
- Evaluated S11, S21, adaptive convergence, and power transmission/reflection behavior.

**Topics:** Microstrip Transmission Lines · S-Parameters · Dielectric Loss · HFSS · Electromagnetic Simulation

---

### 02 · Inset-Fed Microstrip Patch Antenna — HFSS Design & CST Comparison

[View project documentation](02-inset-fed-patch-antenna/README.md) · [Reproducible S11 comparison](02-inset-fed-patch-antenna/comparison/hfss_cst_s11_comparison/README.md)

A **2.45 GHz inset-fed rectangular patch antenna** designed and optimized in HFSS, then modeled in CST to compare input matching and radiation characteristics.

- Tuned the patch length from **28.83 mm to 28.54 mm** to move the HFSS reflection minimum toward the target frequency.
- At **2.45 GHz**, obtained **S11 = −29.04 dB in HFSS** and **−21.89 dB in CST**, with VSWR values of **1.073** and **1.175**, respectively.
- Obtained sampled S11 minima at **2.450 GHz in HFSS** and **2.441 GHz in CST**; estimated −10 dB bandwidths were **76.1 MHz** and **77.8 MHz**.
- Compared input impedance, Smith charts, broadside radiation patterns, realized gain, radiation efficiency, and −3 dB beamwidth.
- Recorded peak realized gains of approximately **3.53 dBi in HFSS** and **3.25 dBi in CST**, with approximately **51% radiation efficiency** in both models.
- Documented field distributions, surface currents, and adaptive mesh convergence.
- Included both model archives, result figures, numerical exports, and a Python script that reproduces the S11 comparison.

![HFSS–CST S11 comparison](02-inset-fed-patch-antenna/comparison/hfss_cst_s11_comparison/results/hfss_cst_s11_comparison.png)

**Topics:** Microstrip Patch Antennas · Inset Feeding · Impedance Matching · Far-Field Radiation · Mesh Convergence · HFSS · CST · Simulation Comparison

---

## Tools & Technical Areas

| Area | Tools and methods |
|---|---|
| Electromagnetic simulation | Ansys Electronics Desktop / HFSS; CST Studio Suite |
| Numerical modeling | Frequency-domain FEM; time-domain simulation; adaptive tetrahedral and hexahedral meshing |
| RF and microwave | Microstrip transmission lines, S-parameters, dielectric loss, and 50 Ω impedance matching |
| Antenna analysis | Patch antennas, inset feeding, realized gain, directivity, radiation efficiency, and half-power beamwidth |
| Field interpretation | Electric and magnetic fields, surface currents, and transmission/reflection behavior |
| Numerical comparison | Touchstone exports, Python, NumPy, and Matplotlib |
| Documentation | Markdown, Git, and GitHub |

The results presented in this portfolio are simulation based. Hardware fabrication and measurement are future extensions of the documented projects.
