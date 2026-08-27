---
name: pyaedt
description: Version-aware automation of Ansys Electronics Desktop (AEDT) with PyAEDT for Icepak package thermal modeling, detailed and compact package models, CTM/Delphi/STM reduced models, DOE and Optimetrics, basic packages, OCP thermal models, 2.5D/3DIC chip-package-system flows, and coupled HFSS, HFSS 3D Layout/PyEDB, Maxwell, Q2D/Q3D, RedHawk-SC Electrothermal, Mechanical, and Fluent workflows. Use when Codex must write, explain, review, debug, or run Python/CLI workflows that control AEDT, Workbench, or manipulate AEDB/EDB/coupled thermal data, including Chinese-language requests about PyAEDT and package thermal simulation.
---

# PyAEDT automation

Skill profile: v1.4.0 - Icepak package thermal modeling, mesh, audit, coupled tool routing, reduced models, and reproducible DOE.

Use this skill to produce reliable, reproducible PyAEDT workflows. Treat AEDT and PyAEDT as a version-coupled engineering toolchain: first identify the installed AEDT/PyAEDT versions and interface, then use the matching official API reference and examples. Do not invent method names or silently mix legacy `pyaedt` imports with the modern `ansys.aedt.core` API.

## Workflow

1. Clarify the engineering target: AEDT application/design type, project/design inputs, geometry or EDB source, material/excitation/boundary requirements, solver setup, sweep/optimization, desired outputs, and whether the run is local, headless, or remote.
2. Inspect the environment before writing code when execution is requested:
   - `python -c "import ansys.aedt.core as a; print(a.__version__)"` (or inspect the installed package metadata).
   - `pyaedt version` and `pyaedt aedt-versions` when the CLI is available.
   - Confirm AEDT is installed, licensed, and the requested design type is available.
3. Choose the application class and interface from [api-map.md](references/api-map.md). Prefer the modern `ansys.aedt.core` namespace and gRPC for AEDT 2022 R2+. Use COM only when the installed AEDT/version requires it and the host is Windows.
4. Build the workflow in this order: session -> project/design -> variables/units -> geometry or EDB -> materials/assignments -> mesh -> setup/sweeps -> analyze -> postprocess/export -> cleanup.
5. Validate at every boundary: confirm object names, units, assignments, setup names, solve completion, available variations, expressions, and exported files. Report assumptions and version-sensitive parts.
6. Release sessions deterministically. Prefer `with Desktop(...)` or `with Hfss(...)` where appropriate; explicitly choose `close_on_exit`, `close_projects`, and `close_desktop` when attaching to an existing user session.

## Version routing

Always load [version-routing.md](references/version-routing.md) before choosing an interface or writing release-sensitive code. Then load exactly the closest version reference:

- AEDT 2021 R2-2022 R1: [version-legacy.md](references/version-legacy.md)
- AEDT 2022 R2-2024 R2: [version-grpc-transition.md](references/version-grpc-transition.md)
- AEDT 2025 R1-2025 R2: [version-modern-edb.md](references/version-modern-edb.md)
- AEDT 2026 R1 and later: [version-current.md](references/version-current.md)

If the installed PyAEDT major version is 0.x, also apply the migration notes in `version-routing.md`; for 1.x, prefer `ansys.aedt.core`, current argument names, and explicit exception handling. Do not treat a PyAEDT package version as interchangeable with an AEDT installation version.

For thermal work, also load [icepak-thermal.md](references/icepak-thermal.md). When the exact release is unknown, inspect it first and state which nearest version branch was selected.

For every Icepak task, load [icepak-modeling-mesh.md](references/icepak-modeling-mesh.md) before writing solver or DOE code. Treat geometry simplification, thermal-path continuity, mesh quality, and mesh independence as gates. Do not start DOE until one nominal case passes those gates.

For a production package workflow, also load [thermal-model-contract.md](references/thermal-model-contract.md) before creating case files, [icepak-physics-solver.md](references/icepak-physics-solver.md) when fluid, radiation, transient behavior, or characterization is important, and [reduced-model-correlation.md](references/reduced-model-correlation.md) when exporting or validating a compact, CTM, Delphi, or STM model.

When a task involves more than Icepak, load [coupled-tool-routing.md](references/coupled-tool-routing.md) first. It routes the eight prepared paths: Detailed Package, Package Definition/PyEDB, Rtheta/Delphi, RedHawk-SC Electrothermal, Q3D/Maxwell, HFSS, Mechanical, and Fluent/Icepak. Keep optional products dormant until installation, license, version, and data-transfer checks pass.

For package work, load [package-thermal-doe.md](references/package-thermal-doe.md). Use its model-fidelity ladder before building a large 2.5D/3DIC model: detailed thermal model -> mesh-qualified baseline -> DOE/parametric data -> compact/CTM/Delphi/STM model -> system-level reuse.

## Icepak modeling and mesh priority

When the request is package thermal modeling, spend the design effort in this order:

1. Scope and fidelity: decide what the model must predict and select detailed, compact, CTM, 2.5D, 3DIC, or OCP representation accordingly.
2. Geometry: simplify imported CAD, preserve dominant heat paths and fluid paths, and verify dimensions, contacts, openings, and assignments.
3. Physics: assign temperature-aware materials, power, TIM/contact resistance, fluid region, boundaries, and monitors.
4. Mesh: establish a global mesh, add local refinement around sources/interfaces/wakes, and use non-conformal mesh when separate assembly refinement is justified.
5. Quality: inspect validation results, cell count, face alignment, skewness, residuals, monitor stability, heat balance, and coarse/base/fine sensitivity.
6. DOE: freeze the baseline mesh policy, record mesh statistics per case, and remesh when a geometry or dominant length-scale change invalidates reuse.

For repeatable engineering work, create a case manifest and run the bundled [thermal_case_manifest.py](scripts/thermal_case_manifest.py) before launching AEDT. Treat a failed manifest or audit gate as a stop condition. Archive the manifest, input hashes, solver log, mesh summary, convergence history, result table, and model revision together.

Thin TIM, die attach, solder bumps, package interfaces, die-to-interposer layers, heat sinks, and cold plates require explicit modeling decisions. Do not solve a geometry problem by blindly reducing the global element size. See [icepak-modeling-mesh.md](references/icepak-modeling-mesh.md) for the package-specific mesh checklist and version split.

## Minimal safe pattern

```python
from pathlib import Path
from ansys.aedt.core import Desktop, Hfss

project_path = Path("results") / "filter.aedt"
project_path.parent.mkdir(parents=True, exist_ok=True)

with Desktop(
    version="2026.1",       # replace with an installed AEDT version
    non_graphical=True,
    new_desktop=True,
    close_on_exit=True,
) as desktop:
    hfss = Hfss(project=str(project_path), design="Filter", new_desktop=False)
    hfss["trace_width"] = "1 mm"
    # Create or edit model, assignments, mesh, setup, and sweeps here.
    hfss.save_project()
    # Analyze only after validating setup and inputs.
```

For a one-off app session, `Hfss(...)` can launch or attach directly. For scripts that own the AEDT lifecycle, prefer a `Desktop` context manager. When attaching to a user's existing AEDT session, preserve it unless the user explicitly asks to close it.

## Decision rules

- Use `non_graphical=True` for CI/batch runs only after confirming every required operation supports headless mode.
- Use named arguments for PyAEDT calls, stable object names, `Path` for filesystem work, and temporary folders for examples or disposable projects.
- Keep engineering quantities as AEDT strings such as `"10 mm"`, `"2.4GHz"`, and `"5W"`; use design variables for parametric geometry and solver inputs. A leading `$` denotes a project variable.
- Prefer object-oriented modeler access (`app.modeler["Body"]`) and returned object handles over raw AEDT scripting. Use `.props` plus `.update()` for setup/mesh objects when the typed property is not exposed.
- Avoid destructive operations on user projects. Save to a new path or archive before bulk edits; never overwrite a source project without explicit instruction.
- Never pass untrusted paths, shell commands, serialized objects, environment variables, or user-controlled executable settings into launch/remote helpers. Validate and constrain paths before use.
- Do not claim a solve succeeded from a returned boolean alone: check solver messages/status, setup existence, solution data, and expected exported artifacts.
- When an API differs by release, consult the installed API signature and the versioned official docs rather than adding a compatibility guess.

## Common task recipes

- Geometry/materials/boundaries: select the correct application, create or load objects, assign materials and excitations, then verify object names and assignments before solving.
- Mesh: use the application-specific mesh API. For Icepak, load [icepak-modeling-mesh.md](references/icepak-modeling-mesh.md) and qualify geometry simplification, global/local/non-conformal mesh, and mesh independence before setup or DOE. Icepak mesh regions and HFSS 3D Layout net/layer operations differ from generic 3D mesh operations; see [workflows.md](references/workflows.md).
- Setup/sweeps/optimization: read existing setups first, edit their properties, create only when absent, and verify frequency/time/angle ranges and convergence criteria.
- Package thermal and DOE: start with a validated detailed package model, parameterize only physically meaningful factors, run a screening DOE, export monitor/parametric data, train a compact model only after holdout validation, and reuse the reduced model for large 2.5D/3DIC/OCP system studies.
- Production thermal workflow: load [thermal-model-contract.md](references/thermal-model-contract.md) for case identity, boundary definitions, audit gates, and release evidence. Load [reduced-model-correlation.md](references/reduced-model-correlation.md) before fitting or exporting DTM-derived compact/CTM/Delphi/STM models.
- Coupled tools: use [coupled-tool-routing.md](references/coupled-tool-routing.md) to choose the source solver, loss/temperature/power transfer direction, one-way versus two-way coupling, and mapping acceptance checks. Do not assume RedHawk-SC, Fluent, Mechanical, or Workbench availability from PyAEDT installation alone.
- Results: create an AEDT report when needed, retrieve solution data, then export CSV/JSON/PNG/PDF with explicit output paths. For fields, validate the field quantity, sampling context, intrinsics, and variation.
- PyEDB: use `Edb`/PyEDB for PCB/package/layout data and distinguish `.aedb`/EDB manipulation from an AEDT design session. Check AEDT version before enabling PyEDB gRPC.
- Extensions/CLI: use the `pyaedt` CLI for session/project/script/export operations and follow the extension environment variables when connecting an extension to an existing session.
- Remote: prefer secure local gRPC defaults; for client-server use the documented mTLS/certificate configuration and verify host, port, service pack, and Python compatibility.
- Version-specific behavior: follow the selected version reference; do not copy a current gRPC, PyEDB, mesh-region, or error-handling pattern into an older AEDT installation without checking compatibility.

## Debugging order

1. Capture Python, PyAEDT, AEDT, OS, interface, graphical/headless mode, host/port, and exact traceback.
2. Verify version compatibility and that the requested AEDT process is listening on the expected port.
3. Reduce to session launch/attach, then project/design open, then the smallest failing API call.
4. Check names, units, active design, setup/sweep state, license availability, file locks, permissions, and temporary-folder paths.
5. Compare against the matching official example and API signature. For gRPC failures, inspect secure/insecure mode, required service pack, certificates, and `PYAEDT_USE_PRE_GRPC_ARGS` only when the version requires it.
6. Preserve logs and generated files needed to reproduce the failure; do not "fix" it by disabling security or closing unrelated AEDT sessions.

## References

Load only the reference needed for the task:

- [pyaedt_env_report.py](scripts/pyaedt_env_report.py): read-only environment and version diagnostic; run it before release-sensitive work.
- [thermal_case_manifest.py](scripts/thermal_case_manifest.py): deterministic preflight validation for case identity, model fidelity, physics, power, boundaries, mesh, solver, responses, and provenance.
- [ansys_toolchain_report.py](scripts/ansys_toolchain_report.py): read-only discovery of PyAEDT, PyEDB, AEDT, Workbench/Mechanical, Fluent, and manual RedHawk-SC readiness.
- [api-map.md](references/api-map.md): application mapping, imports, session choices, and core API patterns.
- [workflows.md](references/workflows.md): end-to-end recipes, validation checks, remote/CLI patterns, and failure modes.
- [version-routing.md](references/version-routing.md): version decision tree, PyAEDT 0.x/1.x migration, and compatibility matrix.
- [version-legacy.md](references/version-legacy.md): AEDT 2021 R2-2022 R1 COM-only guidance.
- [version-grpc-transition.md](references/version-grpc-transition.md): AEDT 2022 R2-2024 R2 gRPC transition guidance.
- [version-modern-edb.md](references/version-modern-edb.md): AEDT 2025 R1-2025 R2 and PyEDB gRPC boundary.
- [version-current.md](references/version-current.md): AEDT 2026 R1 and later current behavior.
- [icepak-thermal.md](references/icepak-thermal.md): version-sensitive Icepak thermal and mesh workflow.
- [icepak-modeling-mesh.md](references/icepak-modeling-mesh.md): Icepak geometry modeling, simplification, mesh strategy, quality, convergence, and package-specific mesh gates.
- [icepak-physics-solver.md](references/icepak-physics-solver.md): fluid/solid/radiation/transient model selection, physics checks, solver gates, and characterization guidance.
- [thermal-model-contract.md](references/thermal-model-contract.md): case manifest, boundary definitions, audit gates, release evidence, and fail-closed rules.
- [reduced-model-correlation.md](references/reduced-model-correlation.md): DTM to compact/CTM/Delphi/STM training, holdout validation, BCI, extrapolation, and DOE integration.
- [coupled-tool-routing.md](references/coupled-tool-routing.md): eight package thermal routes, coupled data contracts, selection rules, acceptance gates, and optional-product readiness.
- [package-thermal-doe.md](references/package-thermal-doe.md): package model hierarchy, 2.5D/3DIC/OCP routing, DOE, and fast reduced-order model workflow.
- [sources.md](references/sources.md): official documentation, API, examples, repository, release, and package links searched for this skill.

Use official, versioned sources first. The web sources were reviewed on 2026-08-13; re-check them for current release-specific behavior before relying on a version number.
