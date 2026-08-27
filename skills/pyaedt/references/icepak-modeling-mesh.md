# Icepak modeling and mesh priority

Use this reference for every Icepak package thermal task. Modeling quality and mesh quality are gates before solver tuning, DOE, compact-model extraction, or system-level reuse.

## Recommended order

1. Define the question and scale: package hotspot, junction-to-case resistance, board temperature, airflow, pressure drop, or system thermal limit.
2. Select fidelity before opening AEDT:
   - Basic package or board study: detailed solids only where the thermal path or heat source matters.
   - Package-to-board study: use a detailed package model for the package and compact representations for non-critical neighbors.
   - 2.5D or 3DIC: retain die, interposer, lid, TIM, cold plate, and layer-wise thermal paths; use compact models for repeated or distant structures.
   - OCP or server study: preserve the reference fixture, airflow path, and boundary conditions; simplify only non-critical hardware.
3. Import or create geometry, then simplify it before assigning mesh.
4. Assign materials, power, thermal interfaces, fluid region, boundaries, and monitors.
5. Set a global mesh, add local refinements, and use non-conformal mesh when separate assembly refinement is beneficial.
6. Run a baseline and check mesh quality, convergence, heat balance, and monitor stability.
7. Freeze the validated baseline geometry and mesh policy before DOE. Do not let DOE silently change mesh settings.

## Geometry modeling gate

Keep these features because they affect the thermal answer:

- heat-generating dies, heaters, resistors, and power maps;
- die attach, TIM, solder, lid, spreader, heat sink, cold plate, and thermal vias;
- contact interfaces and material transitions in the dominant heat path;
- fluid channels, vents, fan faces, and enough air volume to develop the intended flow;
- package layers or CTM blocks needed by the question being answered.

Simplify these features unless they are part of the question:

- tiny holes, cosmetic cuts, fasteners, text, logos, fillets, chamfers, and small rounds;
- repeated small features that do not change the thermal path;
- distant components that only contribute an aggregate heat load.

Use Icepak Simplify or an equivalent CAD cleanup flow with Bounding Box, Primitive Fit, or Polygon Fit. Check the result visually and numerically. Simplification must not remove a thermal interface, split a heat source, close a fluid opening, or change the package dimensions used for validation.

Before meshing, verify:

- units and overall dimensions are correct;
- solids do not overlap unexpectedly and intended contacts are present;
- every heat source and solid/fluid body has a material or explicit assignment;
- the thermal path from source to sink is continuous;
- fluid regions and openings are valid and not accidentally sealed;
- power applied to the model is accounted for in the expected sinks;
- imported object names are stable enough for PyAEDT automation.

## Mesh strategy

Start with a documented global mesh. Then refine only the physics-critical regions:

- die, heater, and hotspot;
- thin TIM or die-attach interfaces when modeled explicitly;
- solder bumps or balls when their individual path is required;
- lid, spreader, heat sink base, cold plate, and contact interfaces;
- narrow channels, vents, fan faces, and recirculation or wake regions;
- 2.5D/3DIC die-to-interposer, interposer-to-package, and package-to-cold-plate interfaces.

For current PyAEDT releases, prefer the Icepak mesh objects and inspect the installed signature before coding:

    global_mesh = ipk.mesh.global_mesh_region
    global_mesh.manual_settings = True
    global_mesh.settings["MaxElementSizeX"] = "2 mm"
    global_mesh.settings["MaxElementSizeY"] = "2 mm"
    global_mesh.settings["MaxElementSizeZ"] = "2 mm"
    global_mesh.update()

    die_mesh = ipk.mesh.assign_mesh_region(
        assignment=["Die"], level=4, name="DieMesh"
    )
    die_mesh.update()

Use `assign_mesh_region` for object-based local refinement and `assign_mesh_level` when a level-based refinement is more appropriate. A mesh-size region is useful for a non-model box around a hotspot or wake; keep it axis-aligned and ensure multi-level mesh is enabled. If only part of a box encloses the intended geometry, only that enclosed portion is refined.

For AEDT 2024 R1 and later, the mesh-region paradigm changed toward mesh-region objects. Older releases may require the explicit region box in the legacy call signature. Route by the installed AEDT version, not only the PyAEDT package version.

## Non-conformal mesh

Use non-conformal mesh when a package, heat sink, or detailed subassembly needs a fine mesh while the surrounding enclosure can remain coarse. Inspect the interface between separately meshed regions and set a slack region when needed to prevent mesh bleeding or to protect a wake. Record the element count and monitor values for the conformal and non-conformal variants when qualifying the method.

Do not use non-conformal mesh to hide a bad interface or an under-sized fluid domain. Check temperature, pressure, velocity, heat flow, and residual behavior after the interface is created.

## Mesh quality and convergence gate

For each baseline and DOE family, record:

- total element or cell count and the count by major region;
- global and local mesh settings, refinement levels, and reuse status;
- face alignment, skewness, and aspect-ratio information when available;
- minimum, maximum, and representative quality values;
- maximum temperature, hotspot temperature, pressure drop, flow rate, and heat balance;
- residual history and monitor convergence.

Use the Icepak validation check and mesh visualization. The official getting-started material uses face alignment above 0.05 and skewness above 0.02 as example quality targets; treat these as documentation guidance, not universal acceptance limits. Establish project-specific limits for the package type and solver version.

Perform at least a coarse/base/fine comparison for a new model or a changed dominant heat path. Define the acceptance thresholds before the run, for example temperature delta at the hotspot, heat-flow delta, and pressure-drop delta. A mesh is not accepted merely because the solver converged.

Interpret mesh quality with the physical regime. For forced flow, inspect wall-normal resolution, boundary-layer development, fan or inlet operating point, and wake. For natural convection, inspect gravity orientation, buoyancy region, enclosure size, and rising plume resolution. For radiation-sensitive models, inspect surface coverage and mesh near radiating interfaces. Load [icepak-physics-solver.md](icepak-physics-solver.md) for solver-side checks.

Thin layers require a modeling decision, not automatic extreme refinement. If the physical thickness is too small for a practical 3D mesh, use a validated effective resistance, compact package representation, or equivalent interface treatment. If the layer is modeled explicitly, refine the interface and verify that the result is not dominated by one poorly resolved cell.

## DOE controls

- Validate one nominal case before launching a sweep.
- Freeze geometry topology, material definitions, boundary names, and the baseline mesh policy.
- Vary only physically meaningful factors such as power, TIM conductivity, interface resistance, die size, heat sink resistance, flow rate, or package dimensions.
- Decide whether mesh reuse is valid for each factor. Geometry-changing factors usually require remeshing or a verified adaptive strategy.
- Store mesh statistics with every result so a temperature change is not mistaken for a physical effect caused by a mesh change.
- Re-run coarse/base/fine checks for the final selected design points when the DOE changes the dominant length scale or flow path.

## Package-specific emphasis

- Basic packages: use detailed solids for die, attach, mold, lead frame, exposed pad, and thermal sink when their paths matter; compact nearby parts that do not affect the result.
- 2.5D: refine die, interposer, bridge, substrate, TIM, and heat spreader interfaces; do not refine the whole board uniformly.
- 3DIC: retain vertical layer order and heat paths; refine active dies, TSV or equivalent thermal paths when represented, inter-die interfaces, lid, and cold plate. Use CTM or other validated compact blocks for repeated structures.
- OCP: preserve the specified airflow and test fixture; refine NIC or accelerator hotspots and nearby flow restrictions, then use compact representations for distant server hardware.

## Source links

- PyAEDT mesh user guide: https://aedt.docs.pyansys.com/version/dev/User_guide/mesh.html
- Icepak mesh API: https://aedt.docs.pyansys.com/version/stable/API/Mesh.html
- Icepak local mesh region API: https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.modules.mesh_icepak.IcepakMesh.assign_mesh_region.html
- Icepak Simplify command: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Modeler/SimplifyCommand.htm
- Icepak mesh-size region: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Mesh/CreatingaMeshSizeRegion.htm
- Non-conformal meshing: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_mesh_assy.html
- Icepak getting-started mesh quality example: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/PDFs/Getting%20Started%20with%20Icepak%20-%20Coil%20and%20Plate.pdf
