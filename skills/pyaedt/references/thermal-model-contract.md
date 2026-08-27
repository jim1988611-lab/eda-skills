# Thermal model contract and audit

Use this contract before creating or changing an Icepak package model. Missing information must be recorded as an explicit assumption; never silently choose a boundary condition, power normalization, reference surface, or material value.

## Contents

- [Case identity](#case-identity)
- [Required contract](#required-contract)
- [Audit gates](#audit-gates)
- [Evidence and release](#evidence-and-release)

## Case identity

Every case needs a stable `case_id`, model revision, AEDT version, PyAEDT version, source geometry identifier, and a unique output directory. Keep source files read-only and write generated AEDT projects, logs, exports, and reports into the case directory.

Use a manifest with these top-level groups:

- `identity`: case ID, owner, date, revision, solver versions, and purpose;
- `model`: package type, fidelity, geometry source, units, coordinate convention, and simplification policy;
- `physics`: steady or transient, conduction/convection/radiation choices, gravity, fluid, and material source;
- `power`: total power, per-source values, spatial map or matrix, time dependence, and normalization;
- `boundaries`: ambient or inlet state, flow or fan data, fixed temperature/heat/HTC choices, and reference surfaces;
- `mesh`: global settings, local regions, non-conformal settings, quality limits, and independence cases;
- `solver`: setup, convergence criteria, initialization, and restart policy;
- `responses`: required monitors, heat-flow paths, resistance definitions, and pass/fail limits;
- `provenance`: source files, scripts, git revision, random seed, and operator notes.

## Required contract

### Model and thermal path

Name every body that carries meaningful heat: die, die attach, TIM, mold, substrate, lead frame, exposed pad, solder, lid, spreader, heat sink, cold plate, interposer, bridge, and board. Record whether each is detailed, homogenized, compact, or represented by an effective resistance.

For each interface, record contact area, thickness, conductivity or contact resistance, and whether the interface is resolved as a solid or a boundary. A thin layer must have one deliberate representation; do not create a numerically thin solid and then assume it is resolved.

### Power and reference surfaces

Define whether power is total, per die, per block, per unit area, or imported as a spatial matrix. Verify the sum of all sources against the intended electrical or operating-mode power. Record the coordinate system, map resolution, interpolation, and temperature feedback assumption.

Define Rjc, Rjb, Rja, or other resistance metrics by their source temperature, reference surface, ambient definition, and heat-flow path. A resistance value without these definitions is not comparable across cases.

### Boundary conditions

Classify the case as one of the following before setup:

- conjugate CFD with explicit fluid and solid domains;
- prescribed HTC or thermal resistance characterization;
- fixed-temperature or fixed-heat boundary used for a controlled characterization;
- network or compact package connected to a system model.

Do not mix a prescribed HTC with a resolved fluid interface on the same physical path unless the double-counting assumption is documented. Record whether radiation is enabled and provide emissivity or the reason for omitting it.

## Audit gates

Run the following gates before solving:

1. `A0 schema`: manifest is complete, units are present, paths are constrained, and case ID is unique.
2. `A1 geometry`: dimensions, bounding boxes, contacts, openings, material bodies, and simplified geometry agree with the source intent.
3. `A2 physics`: power sum, material assignment, thermal interfaces, gravity, fluid, radiation, and boundary classifications are valid.
4. `A3 mesh`: global/local operations are assigned to intended objects, mesh statistics are captured, and the mesh plan matches the smallest dominant length scale.
5. `A4 solve`: setup exists, convergence criteria are explicit, monitors are non-empty, and solver status is successful.
6. `A5 result`: heat balance, hotspot, reference temperatures, flow/pressure responses, and exports pass the stated limits.
7. `A6 release`: inputs, scripts, logs, mesh metadata, result files, and assumptions are archived together.

Fail closed. A missing material, source, contact, monitor, or reference surface is a review failure, not a default-to-zero case.

## Evidence and release

At minimum, release a manifest, solver log, mesh summary, result table, convergence history, and a short assumptions file. For a reduced model, also release the training/test split, holdout error table, valid factor range, and model file hash.

The nominal case is the reference for every DOE family. If geometry topology, dominant length scale, boundary class, power-map topology, or material model changes, create a new baseline and repeat the audit gates.
