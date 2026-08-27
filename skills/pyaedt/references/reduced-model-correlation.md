# DTM, compact, CTM, Delphi, and STM correlation

Use this reference when moving from a detailed Icepak package model to a fast model for 2.5D, 3DIC, OCP, board, or system DOE.

## Select the reduction target

- Detailed Thermal Model (DTM): reference geometry and physics for package characterization.
- Compact Package or CCM: fast representation when repetitive package features do not need explicit geometry.
- CTM: multi-die or 3DIC representation that preserves die-to-die and package-level thermal paths.
- Delphi network: boundary-condition-aware network extracted from multiple detailed trials.
- STM or Delphi-like surrogate: compact model trained and validated on steady-state or transient data.

The reduction target must preserve the responses needed by the consuming model. A model that matches maximum die temperature under one HTC is not automatically valid for a board, cold plate, or server airflow study.

## Training matrix

Build the training matrix from the intended use range:

- heat-source combinations and spatial power distributions;
- top, bottom, side, and package-to-board boundary conditions;
- flow or HTC levels when convection is part of the interface;
- ambient and inlet temperatures;
- material or interface uncertainty when the reduced model is expected to cover it;
- transient waveforms and time scales for RC/STM work.

Keep separate files or explicit labels for training, testing, and holdout cases. Do not select holdout cases after looking at the error.

## Required responses

Compare more than a single maximum temperature. At minimum include:

- each die or junction temperature;
- hotspot temperature and location;
- external node or reference-surface temperatures;
- heat flow through each declared external path;
- total heat balance;
- pressure or flow response when the compact model includes a fluid interface;
- transient rise and time constants when applicable.

Report absolute and relative error, worst case, mean error, bias, and error by operating condition. Define acceptance thresholds before fitting.

## BCI and extrapolation

Treat boundary-condition-independent behavior as a claim requiring evidence. Test new combinations of external boundary conditions and source distributions, not only new values along the training axes. Flag any query outside the stated factor range or with a new power-map topology.

For CTM/Delphi/STM extraction, archive node definitions, external face groups, internal node choices, optimizer settings, training data hash, test data hash, and exported model hash. If steady-state conductance is reused for transient fitting, verify that the network topology and node definitions are identical.

## Release gate

Release a reduced model only when:

1. the DTM nominal case passes model, mesh, solver, and heat-balance audits;
2. training and holdout data are independent;
3. all required temperature and heat-flow responses meet the predefined limits;
4. the valid factor range and unsupported conditions are stated;
5. the reduced model is compared against at least one new detailed case after export/import;
6. extrapolation and failed queries are flagged instead of silently returning a value.

## DOE integration

Freeze the DTM mesh policy before generating training data. If a factor changes geometry topology, dominant length scale, interface count, or fluid path, create a new mesh-qualified baseline or document a verified remeshing rule. Store mesh count, runtime, solver status, and model revision with every training and holdout record.

Official references:

- Icepak package hierarchy: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_chp_packages.html
- Delphi package characterization: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_delphi_pkg.html
- Delphi/STM toolkit: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Variables/ToolkitIcepakExtractDelphiNetwork.htm
- 3DIC CTM import: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/Icepak/3DIntegratedCircuitsinIcepak.htm
