# PyAEDT workflows and validation

## End-to-end build pattern

1. Create a dedicated working directory and copy/archive source inputs.
2. Start or attach to AEDT with an explicit version and lifecycle policy.
3. Select the intended project/design and print the active names and design type.
4. Set units and variables before geometry. Use expressions with units rather than bare floats where the API accepts them.
5. Create or load geometry/EDB, then verify object count, names, materials, coordinate system, and bounding box.
6. Add excitations, boundaries, sources, and monitors. Verify each assignment references existing objects.
7. Configure global and local mesh operations. For Icepak, inspect global mesh region and local region assignments separately.
8. Create or edit a named setup and sweeps. Confirm the setup is active and its properties reflect the request.
9. Run the solver. Capture logs and wait for completion; do not export results while a solution is still running.
10. Postprocess with explicit expressions/variations and export artifacts to a known output directory.
11. Reopen/read key outputs when possible, check non-empty data and expected dimensions, save the project, and release AEDT.

## Geometry and assignments

Use explicit named arguments and stable names:

```python
component = hfss.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["10mm", "8mm", "1mm"],
    name="Component",
    material="copper",
)
assert hfss.modeler["Component"].material_name
```

For edits, retrieve existing objects by name and change their properties. Before boolean operations, verify both operands exist and are not already consumed by an earlier operation. Do not rely on GUI selection state.

## Mesh and setup checks

Generic mesh operations expose collections that can be read and edited. For object-style operations, update the `props` dictionary and call `.update()`. Icepak uses mesh regions and settings; HFSS 3D Layout uses net/layer-specific mesh APIs. AEDT 2024 R1 introduced a mesh-region paradigm change, so check the target release before using older region signatures.

For setups:

```python
setup = next((s for s in app.setups if s.name == "Setup1"), None)
if setup is None:
    setup = app.create_setup("Setup1")
setup.props["MaximumPasses"] = 10
setup.update()
assert any(s.name == "Setup1" for s in app.setups)
```

Use application-specific property names from the API or a recorded design; do not assume a Maxwell property is valid for HFSS or Icepak.

## Parametric studies and Optimetrics

Use design variables for dimensions, frequency, loads, and other intended sweep inputs. Distinguish project variables (`$name`) from design variables (`name`). Before adding a parametric/optimization setup, inspect existing Optimetrics objects to avoid duplicate names. Validate the generated variations and record the objective/constraint definitions with the result.

## Postprocessing

For report data, validate all of the following before interpreting results:

- the setup/solution name is solved;
- the expression exists for that design type;
- the requested variation/intrinsic values are available;
- the returned arrays are non-empty and have matching lengths;
- units and dB/linear/complex conventions are explicit;
- the exported file is present and readable.

Use AEDT reports when the artifact must remain editable in AEDT. Use solution data with Matplotlib/PyVista for external plots, field maps, animations, or automated reports. Never infer a pass/fail threshold from a plot without stating the frequency, variation, interpolation, and tolerance.

## PyEDB and HFSS 3D Layout

Use EDB/PyEDB for PCB/package/IC database edits such as stackup, layers, nets, components, padstacks, and layout geometry. Use `Hfss3dLayout` when the operation belongs to the AEDT design and solver. Keep EDB paths separate from `.aedt` project paths, save a copy before mutation, and check the target AEDT version before enabling `settings.pyedb_use_grpc` (supported for AEDT 2025 R2+ and enabled by default from 2026 R1 according to the versioned docs).

## Remote and secure gRPC

For local AEDT, use the secure local defaults. For client-server:

- confirm AEDT and PyAEDT are installed on both sides;
- use the same Python version where required;
- verify server host, port, process, firewall, and license;
- use mTLS and a controlled `ANSYS_GRPC_CERTIFICATES` directory for secure network connections;
- check the service-pack matrix before using WNUA/UDS/mTLS;
- use `PYAEDT_USE_PRE_GRPC_ARGS=True` only for older service-pack startup compatibility;
- constrain file upload/download destinations and audit remote service-manager access.

An insecure connection can expose project data and commands. Treat it as a tightly controlled diagnostic exception, never as a default fix.

## Extensions

Extensions can run from AEDT's Automation ribbon, command line, or Python. When connecting to an existing session, use `PYAEDT_DESKTOP_PORT` and `PYAEDT_DESKTOP_VERSION` or the current extension helper pattern. Keep extension input parsing strict, use `is_test`/headless paths where supported, and do not let an extension execute arbitrary user-provided code or paths.

## Troubleshooting matrix

| Symptom | First checks |
| --- | --- |
| Cannot import `ansys.aedt.core` | Active interpreter, installed package, venv, Python version, package namespace |
| AEDT starts then exits | license, version/service pack, port collision, secure transport mode, Student-version limitations |
| Cannot attach | process/port, `new_desktop`, machine name, firewall, gRPC/COM setting |
| Method/keyword missing | installed version, application class, API reference, renamed `pyaedt` vs `ansys.aedt.core` API |
| Object not found | active project/design, spelling/case, design type, object created in another modeler/EDB context |
| Solve fails | setup validity, assignments, mesh, license, solver messages, lock files, disk space |
| Empty report | wrong setup/solution, invalid expression, missing variation, solve incomplete, report category mismatch |
| Remote file error | server-side path, permissions, file manager, path normalization, transfer completion |
| Headless plot hangs | plotting backend, `block_figure_plot`, display requirements, exporting without GUI |

When a failure is version-sensitive, capture the smallest reproducible script and exact environment rather than recommending a broad reinstall.
