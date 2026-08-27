# Coupled package thermal tool routing

This reference prepares the eight package-thermal routes shown in the project planning image. It defines the preferred source solver, Icepak role, data exchanged, and readiness gate. A route being prepared does not mean that the licensed Ansys product is installed or that a solve has been executed.

## Route matrix

| Engineering question | Preferred route | Icepak role | Main exchange | Readiness state |
| --- | --- | --- | --- | --- |
| QFN, QFP, BGA, power package | Icepak Detailed Package | Reference package DTM and mesh | Power, package geometry, Tj and heat flow | Ready for AEDT validation |
| Package + PCB + enclosure | HFSS 3D Layout/PyEDB + Package Definition -> Icepak | PCB, package, air and enclosure thermal model | Stackup, traces, vias, components, package thermal data | Ready for EDB/AEDT validation |
| Rjc, Rjb, Rja and package characterization | Icepak characterization + Delphi/STM | Generate controlled boundary data and reduced model | Boundary temperatures/HTC, heat flow, junction temperature, network | Ready for DTM validation |
| FCBGA, chiplet, 2.5D, 3DIC | RedHawk-SC Electrothermal + Icepak | System cooling boundary and package thermal environment | Power maps, temperature, HTC, CTM, die/layer metadata | Workflow ready; product/license pending |
| Joule heating from current | Q3D or Maxwell -> Icepak | Consume volume/surface EM losses and solve temperature | Loss map, frequency/time, material temperature feedback | Ready for coupling smoke test |
| RF-loss package heating | HFSS -> Icepak | Consume surface/volume RF loss and solve temperature | Frequency, solution, loss map, thermal feedback | Ready for coupling smoke test |
| Package warpage, thermal stress, solder reliability | Icepak -> Mechanical | Provide non-uniform temperature field | Temperature field, mapped geometry, CTE/material/constraints | Prepared but dormant by current scope |
| Liquid cooling, cold plate, complex channel | Icepak or Fluent -> Icepak/system | Electronics thermal model or co-simulation target | Flow field, HTC, temperature, pressure drop, geometry | Ready for route selection |

## Route selection rules

### 1. Detailed package

Use a detailed Icepak package when the output depends on die attach, mold, substrate, exposed pad, solder, lid, heat spreader, or package-to-board heat spreading. Start with one mesh-qualified DTM before creating a compact model or DOE.

### 2. Package plus PCB and enclosure

Use HFSS 3D Layout or PyEDB for stackup, layer, net, padstack, component, via, and trace data. Use Package Definition for the component thermal representation, then link the PCB/package into Icepak. Keep EDB paths separate from `.aedt` paths, record the source design revision, and verify the package definition is intended for Icepak thermal analysis.

Do not replace a package definition with a generic cuboid when the result depends on die-to-board, exposed-pad, solderball, via, or copper-spreading paths.

### 3. Rtheta and Delphi/STM

Use controlled characterization boundaries for Rjc, Rjb, or Rja. Document the reference surface, source temperature, heat-flow path, ambient, and whether surfaces are adiabatic, fixed HTC, fixed temperature, or system-coupled. Use multiple boundary conditions for Delphi/STM extraction and reserve independent testing/holdout cases.

Do not compare a package Rtheta from one reference surface to a system result using another surface without a spreading and boundary-condition review.

### 4. RedHawk-SC Electrothermal and Icepak

Use Icepak for the package/system cooling environment and RedHawk-SC Electrothermal for high-resolution chip, metal-layer, bump, or multi-die electrothermal behavior. Define a data contract for power-map coordinates, layer order, die locations, temperature units, HTC or boundary files, CTM metadata, and feedback direction.

For 2.5D/3DIC, preserve die-to-die heat coupling, interposer/bridge paths, vertical layer order, underfill/TIM, package lid, and cold-plate interfaces. Do not flatten a CTM or power map without a documented reason and validation case.

### 5. Q3D/Maxwell and Icepak

Use Q3D for conductive DC/AC loss and parasitic-driven heating; use Maxwell for electromagnetic, magnetic, eddy-current, DC conduction, or transient losses. Link surface or volume loss to Icepak using the application-specific EM Loss interface.

Check the selected solution, frequency or time, loss type, source-to-target object mapping, and whether one-way or two-way temperature feedback is intended. Multiple selected frequencies are additive in the thermal solve; solve one excitation at a time when that is not the physical condition. Compare source and target mesh scaling information and investigate a scaling factor that is not close to one.

### 6. HFSS and Icepak

Use HFSS for RF surface or volume loss, then map the selected loss solution into Icepak. Record Driven Modal, Driven Terminal, or Eigenmode solution type, frequency, surface/volume loss, thermal object mapping, and feedback iterations. Do not mix loss from multiple frequencies unless simultaneous excitation is intended.

### 7. Icepak and Mechanical

Keep this route outside the primary thermal-only flow until thermal results pass geometry, mesh, solver, heat-balance, and correlation gates. When enabled, map the non-uniform Icepak temperature field into Mechanical and document geometry correspondence, CTE, material, contacts, supports, solder representation, and one-way versus iterative coupling.

Thermal stress, warpage, CTE mismatch, and solder fatigue are downstream analyses, not substitutes for thermal validation.

### 8. Icepak versus Fluent

Prefer Icepak for electronics package, PCB, enclosure, compact package, fan, heat sink, and system thermal workflows that benefit from AEDT package and EM coupling. Prefer Fluent when the problem is dominated by general CFD complexity such as multiphase flow, conjugate flow in complex channels, detailed turbulence, pumps, manifolds, or a broader fluid domain.

If Fluent supplies a flow or HTC field to Icepak, record interpolation surfaces, coordinate transforms, units, mapping error, and whether the imported field is one-way or part of an iterative loop. Do not combine an imported HTC with a resolved fluid domain on the same interface without an explicit anti-double-counting decision.

## Coupling acceptance gate

Every coupled route must pass these checks before DOE:

1. source and target geometry identifiers match the intended objects;
2. coordinate system, units, layer order, and orientation are documented;
3. total source power equals the mapped power within the declared tolerance;
4. selected frequency, time, solution, and intrinsic variation are explicit;
5. source-to-target mapping and mesh/scaling diagnostics are recorded;
6. one-way or two-way feedback is declared and converges if enabled;
7. coupled results are compared with a standalone source or reference case;
8. the coupled data file, source revision, target revision, and mapping log are archived.

## Environment status

The current local environment has PyAEDT/PyEDB available but no registered AEDT installation. RedHawk-SC Electrothermal, Fluent, and Mechanical should remain documented as optional routes until their installations, licenses, versions, and data-transfer interfaces are verified. Do not infer availability from the existence of a Python package.

## Official references

- Icepak EM Loss from HFSS, Maxwell, or Q3D: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Icepak/AssigningEMLossProperties.htm
- Icepak two-way coupling: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/Icepak/AddingTwoWayCouplingtoanIcepakDesign.htm
- Icepak PCB links and stackup data: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v242/en/Subsystems/Icepak/Content/Icepak/PCBsinIcepak.htm
- Package Definition for Icepak thermal analysis: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/HFSS3DLayout/Content/3DLayout/CreatingOrEditingPackageDefinitionsForComponents.htm
- Icepak to Mechanical transfer: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Mechanical/Content/Mechanical/SetupLink_ThermalCondition.htm
- Icepak getting-started coupling guides: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/GettingStarted/IcepakGettingStartedGuides.htm
- RedHawk-SC Electrothermal and Icepak training: https://learninghub.ansys.com/learn/course/external/view/elearning/857/ansys-redhawk-sc-electrothermal-shi-yong-jing-que-deicepak-xi-tong-re-bian-jie-tiao-jian-jin-xing-gao-jing-du3dic-re-fang-zhen
