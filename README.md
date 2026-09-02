# RF, Microwave & Antenna Engineering Portfolio

**Ayşe Sena Şahin · Electrical and Electronics Engineer**

A portfolio of design and analysis projects with a long-term focus on RF, microwave, and antenna engineering. Each project documents its objective, model, engineering decisions, results, and verification limits.

The current portfolio features an HFSS microstrip transmission-line study. Antenna, matching-network, and passive microwave component projects will be added as they are completed.

## Projects

### 01 · Microstrip Transmission Line — Dielectric Loss Analysis

[Read the project documentation](01-microstrip-transmission-line/README.md)

A 40 mm PCB microstrip line with a nominal 50 Ω design target, modeled in Ansys HFSS. A controlled comparison changes the substrate loss tangent from 0.02 to 0 while retaining the same geometry, real permittivity, copper conductors, and simulation settings.

- **Analysis:** Terminal S-parameters over 2–3 GHz; numerical comparison at 2.45 GHz.
- **Key result:** Simulated insertion loss decreases from **0.3392 dB to 0.0383 dB** when dielectric loss is disabled.
- **Evidence:** Two HFSS model archives, S-parameter plots, and baseline adaptive-convergence results.
- **Scope:** Simulation-based analysis; no fabrication or RF measurements.

## Portfolio Approach

- **Design decisions:** Record dimensions, materials, assumptions, and reference conditions.
- **Controlled comparisons:** Change a clearly identified parameter and interpret the resulting behavior.
- **Quantitative reporting:** Present results with units, frequency, and relevant limitations.
- **Verification:** Distinguish software validation, numerical convergence, and agreement with physical measurements.
- **Reproduction:** Provide model files, software-version information, and instructions for repeating the analysis.

## Tools and Current Technical Coverage

**Ansys Electronics Desktop Student 2025 R2.4 / HFSS**

Current work covers microstrip modeling, terminal lumped ports, radiation boundaries, adaptive meshing, discrete frequency sweeps, and S-parameter interpretation.

## Using the Project Files

Each project directory contains its own README, model files, and supporting figures. Follow that project's instructions for software requirements, model restoration, and simulation settings.

Simulation results are reported as simulations. A completed solver run is not, by itself, evidence of manufacturing readiness or measured performance.
