# Version-aware Icepak thermal workflow

## Select the Icepak branch

Use Icepak for thermal/fluid designs. Load the AEDT version reference first because Icepak mesh-region and setup behavior changes across releases.

## Core workflow

1. Load [icepak-modeling-mesh.md](icepak-modeling-mesh.md) and define the required model fidelity.
2. Open or create an Icepak design and print aedt_version_id, project, design, and solution type.
3. Set model units and design variables before creating solids, fluid regions, and component geometry.
4. Simplify imported geometry while preserving heat sources, dominant thermal interfaces, fluid paths, and validation dimensions.
5. Assign solid/fluid materials and thermal sources; validate every assignment by object name and confirm heat-path continuity.
6. Configure openings, walls, fans, heat sinks, and monitor points using the Icepak-specific API.
7. Configure the global mesh region and local mesh regions. Use non-conformal mesh only after checking the interface and refinement purpose. Do not reuse HFSS mesh calls without checking the Icepak mesh class.
8. Run mesh validation and a coarse/base/fine sensitivity check before finalizing the setup or launching DOE.
9. Create or edit the Icepak setup with explicit convergence criteria and maximum iterations.
10. Solve and wait for completion. Capture solver messages and verify monitors before reading results.
11. Export maximum temperature, temperature distribution, pressure drop, flow rate, mesh statistics, and convergence data with units and design variation recorded.

## Mesh version split

For current Icepak releases, use the global mesh region and subregion objects:

    global_mesh = ipk.mesh.global_mesh_region
    global_mesh.manual_settings = True
    global_mesh.settings["MaxElementSizeX"] = "2 mm"
    global_mesh.settings["MaxElementSizeY"] = "2 mm"
    global_mesh.settings["MaxElementSizeZ"] = "2 mm"
    global_mesh.update()

For AEDT 2024 R1 and later, check the revised mesh-region paradigm and current assign_mesh_region signature. For older releases, define the region box explicitly when the legacy signature requires it.

## Setup version split

Icepak setup template keys may contain spaces in the documentation but use the documented no-space keyword form when passed to create_setup:

    setup = ipk.create_setup(MaxIterations=5)
    setup.update()

Inspect setup.props after creation and set only keys supported by the target release. Record the convergence criteria used for the run.

## Result acceptance checks

Do not call a thermal run successful only because analyze() returned. Require:

- solver completion without fatal messages;
- non-empty temperature and flow results;
- maximum temperature and hotspot object are identified;
- temperature and pressure units are explicit;
- mesh quality, cell count, and mesh sensitivity are recorded;
- monitor values meet the requested convergence/tolerance;
- exported result files exist and can be reopened;
- the project is saved to the intended output path.

Official references:

- https://aedt.docs.pyansys.com/version/stable/User_guide/mesh.html
- https://aedt.docs.pyansys.com/version/stable/API/SetupTemplatesIcepak.html
- https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.icepak.Icepak.html
