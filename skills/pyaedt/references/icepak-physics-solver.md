# Icepak physics and solver validation

Use this reference with [icepak-modeling-mesh.md](icepak-modeling-mesh.md) when the result depends on fluid behavior, radiation, transient response, or a calibrated thermal resistance.

## Select the physical model

Classify the dominant transport before selecting solver settings:

- conduction-dominated package: resolve solid paths and interfaces; use a fluid only when convection or radiation is part of the question;
- forced convection: define inlet, outlet, fan curve, flow direction, pressure drop, and operating point;
- natural convection: define gravity orientation, enclosure size, openings, and buoyancy behavior;
- conjugate heat transfer: resolve the fluid-solid interface and verify that heat crosses it continuously;
- transient: define the power waveform, initial condition, time step, output interval, and thermal time scale;
- radiation-sensitive: define emissivity, participating surfaces, view-factor assumptions, and enclosure temperature.

Do not replace a resolved fan or fluid path with a guessed HTC without documenting the calibration target. Do not use a fixed temperature sink when the intended result is a flow-dependent thermal resistance.

## Physics checks before solve

Record the dimensionless or scale checks relevant to the case: characteristic length, velocity, fluid properties, Reynolds number for forced flow, and buoyancy scale such as Grashof or Rayleigh for natural convection. These checks guide laminar/turbulence and enclosure decisions; they are not universal pass/fail values.

For heat sinks and channels, check fin pitch, hydraulic diameter, boundary-layer development length, wake length, and whether the outlet is far enough from recirculation. For packages, check that the air region is not so small that the enclosure boundary controls the hotspot.

Use a solver-appropriate near-wall treatment and refine the wall-normal direction where wall heat transfer is a response. Do not claim wall resolution from total cell count alone. Record the selected turbulence, buoyancy, radiation, and initialization options with the case manifest.

## Thermal interfaces and materials

Use temperature-dependent properties when the operating range makes constant properties misleading. Record conductivity direction for anisotropic materials, density and heat capacity for transient work, and emissivity for radiating surfaces.

Represent TIM, solder, die attach, package contacts, and thermal plates with one of: resolved solid, conducting plate, resistance, network link, or compact block. Record the source of each resistance and avoid counting both a physical layer and its equivalent contact resistance.

Verify that the heat source is applied to the intended volume or face. For a power map, check coordinates, units, total power, spatial interpolation, inactive regions, and whether the map is steady or time-dependent.

## Solver and result gates

Do not accept a case because `analyze()` returned or residuals decreased. Require:

- no fatal or license errors;
- stable monitor trends and stated residual criteria;
- heat input and heat removal balance within the case tolerance;
- hotspot and reference-surface temperatures are available;
- flow rate, pressure drop, or boundary heat flow is available when relevant;
- results are insensitive to the stated initialization and reasonable solver settings;
- the coarse/base/fine comparison passes the predefined response thresholds.

For transient work, also compare energy storage and heat flow over time. The time step must resolve the source waveform and dominant thermal response; a smooth-looking curve is not proof of temporal resolution.

## Characterization choices

For Rjc/Rjb or controlled package characterization, isolate the intended path with adiabatic or controlled surfaces and state the reference temperature. For system use, prefer boundary-condition-independent compact or Delphi/STM models only after comparison against the detailed model under multiple boundary conditions.

For a package embedded in a board or server, do not transfer a characterization resistance into a different reference surface without checking heat spreading, contact area, and boundary-condition dependence.

## Official references

- Icepak thermal boundary conditions: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v242/en/Subsystems/Icepak/Content/Icepak/AssigningThermalBoundaryConditionsinIcepak.htm
- Junction-to-case characterization: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_mdlpkg_junction_case.html
- Finned heat sink setup: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v242/en/PDFs/Getting%20Started%20with%20Icepak%20-%20Finned%20Heat%20Sink.pdf
- Cold plate setup: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/PDFs/Getting%20Started%20with%20Icepak%20-%20Cold%20Plate%20Model.pdf
