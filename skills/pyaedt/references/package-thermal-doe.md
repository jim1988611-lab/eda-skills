# Package thermal modeling and DOE

## Scope

Use this workflow for basic IC packages, BGA/QFN/QFP/FCBGA, OCP NIC or accelerator thermal models, 2.5D interposer systems, chiplets, and 3DIC assemblies. Keep thermal stress and deformation out of the primary flow until the thermal model is validated.

## Recommended model-fidelity ladder

| Level | Model | Use |
| --- | --- | --- |
| 0 | Thermal resistance / energy-balance spreadsheet or Python check | Sanity check power, boundary temperature, and expected Tj |
| 1 | Icepak Detailed Thermal Model (DTM) | Reference model for a single package, characterization, and calibration |
| 2 | Icepak Compact Package, CCM, Delphi network, or STM | Fast board/system sweeps and repeated DOE |
| 3 | CTM-based package or multi-die model | 2.5D/3DIC chip-package-system analysis |
| 4 | OCP or system-level thermal assembly | Standardized enclosure/card/module studies using reusable Icepak/STEP models |

Do not start with a compact model before a detailed reference model exists. Do not use a detailed 3D package for every DOE point when a validated reduced model can answer the question.

## Tool routing

### Basic packages

Use Icepak Detailed Package when package-level temperatures, heat paths, and junction-to-case or junction-to-board behavior are needed. Use Compact Package or a Delphi/STM model when the package is embedded in a board, card, chassis, or system and repeated evaluations are required.

### OCP

If OCP means Open Compute Project NIC, accelerator, storage, or module work, first check whether the OCP workstream provides an Icepak model and STEP geometry. Preserve the OCP thermal test fixture, airflow, power, and boundary assumptions when comparing results. Do not replace an OCP reference model with an arbitrary enclosure model and call the results equivalent.

### 2.5D and 3DIC

Use RedHawk-SC Electrothermal or the chip power-flow owner to generate temperature-dependent chip power maps and CTM data. Import the packaged 3DIC/CTM data into Icepak for package and system thermal analysis. Verify die locations, layer stack, material properties, power-map units, temperature points, and interface names before solving.

### Electrical-to-thermal coupling

Use Q3D or Maxwell for conductive and electromagnetic losses, HFSS for RF loss, and link the loss data into Icepak. For SIwave DCIR, export power dissipation to Icepak and, where appropriate, feed the temperature map back to the electrical solve.

## Fast-model workflow

1. Build a small DTM for one package type and verify geometry, materials, power, and thermal boundaries.
2. Parameterize only factors that are physically controllable or uncertain.
3. Run mesh and energy-balance checks on the baseline before DOE.
4. Run a screening DOE with a limited number of factors. Add interaction or response-surface points only after identifying dominant factors.
5. Export all design variables, monitor outputs, setup/mesh metadata, and solver status. Keep a unique case ID for every variation.
6. Use the parametric data to train a compact model, Delphi network, or STM when the response is smooth enough.
7. Reserve a holdout set of DOE points. Compare DTM and reduced-model results for Tj, hotspot temperature, boundary heat flow, and any required thermal resistance.
8. Reuse the validated reduced model in large 2.5D/3DIC/OCP system sweeps.

For a production run, define the case contract and audit gates in [thermal-model-contract.md](thermal-model-contract.md). For model extraction and correlation, use [reduced-model-correlation.md](reduced-model-correlation.md); do not release a compact model from a single boundary condition or a single maximum-temperature comparison.

## DOE factor library

Select factors from the actual package and cooling problem:

- die power and spatial power-map distribution;
- die location, die size, die thickness, and die-to-die spacing;
- silicon, mold compound, substrate, lid, heat spreader, solder, bump, and TIM conductivity;
- TIM thickness and contact resistance;
- lid/spreader thickness, material, and interface condition;
- package-to-board and package-to-heatsink contact;
- board temperature, ambient temperature, flow rate, inlet temperature, and convection coefficient;
- heat-sink geometry, fan operating point, and airflow direction;
- number of dies, active dies, power mode, and transient power profile.

Keep the factor table with units, nominal value, lower/upper bounds, source, and whether the factor is design-controlled or uncertainty-driven.

## DOE response library

Record at minimum:

- maximum die/junction temperature;
- temperature at each die and thermal interface;
- hotspot coordinates and layer;
- total heat flow through case, board, lid, and side paths;
- junction-to-case, junction-to-board, or other defined thermal resistance;
- temperature uniformity across dies;
- airflow, pressure drop, or flow rate when fluid is modeled;
- solver convergence, mesh count, runtime, and failed-case reason.

For 3DIC, also record per-die power, CTM profile, inter-die temperature difference, and package-level thermal bottlenecks.

## PyAEDT implementation rules

Use Icepak application variables and Optimetrics for AEDT-native parametric studies. Use explicit monitor names and export the parametric results rather than scraping images. The Icepak API exposes parametrics, optimizations, export_parametric_results, export_summary, export_profile, and export_results; inspect the installed API signature before generating calls.

Use external Python DOE only for orchestration, sampling, surrogate fitting, or cross-project comparison. Keep AEDT case generation and result export inside version-controlled scripts. Do not mix an external surrogate prediction with solver results without labeling the model type and validation error.

## Acceptance criteria

Accept a fast thermal model only when:

- the DTM baseline passes energy balance and mesh sensitivity checks;
- training and holdout points are separate;
- temperature and heat-flow errors are reported by response and operating condition;
- the reduced model remains valid over a stated factor range;
- units, power normalization, ambient conditions, and reference surfaces are documented;
- a failed or extrapolated DOE point is flagged instead of silently accepted.
- every case has a stable case ID, mesh metadata, solver status, input provenance, and result artifact path;
- any geometry-topology, dominant-length-scale, power-map-topology, or boundary-class change triggers a new mesh-qualified baseline.

## Deliberately excluded for now

Do not add thermal stress, warpage, CTE mismatch, solder fatigue, or Mechanical coupling to the primary package workflow until the thermal-only model and DOE acceptance criteria are stable. Add those as a separate downstream branch later.

## Official references

- Icepak package objects: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_chp_packages.html
- Delphi package characterization: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_delphi_pkg.html
- Delphi/STM optimization with parametric training data: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Variables/ToolkitIcepakExtractDelphiNetwork.htm
- 3DIC CTM import to Icepak: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/Icepak/3DIntegratedCircuitsinIcepak.htm
- Icepak PyAEDT API: https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.icepak.Icepak.html
- OCP NIC thermal models: https://www.opencompute.org/wiki/Server/NIC
- OCP thermal methodology: https://www.opencompute.org/wiki/Storage/Thermal_Sim_Methodology
