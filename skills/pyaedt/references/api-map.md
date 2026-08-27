# PyAEDT API map

## Namespace and application classes

Prefer imports from `ansys.aedt.core` in current releases. The following mapping is a starting point; inspect the installed API for exact constructor parameters and application-specific methods.

| AEDT capability | Typical class | Notes |
| --- | --- | --- |
| High-frequency 3D | `Hfss` | Driven/modal, eigenmode, transient, S-parameters, fields |
| High-frequency 3D Layout | `Hfss3dLayout` | PCB/package layout, nets/layers, EDB integration |
| Low-frequency magnetic | `Maxwell2d`, `Maxwell3d` | AC/DC/transient, magnetic forces, circuits |
| Thermal/fluid | `Icepak` | Thermal, flow, mesh regions, electrothermal coupling |
| Parasitic extraction | `Q2d`, `Q3d` | 2D/3D capacitance and inductance extraction |
| Circuit/system | `Circuit`, `TwinBuilder` | Nexxim circuit and system simulation |
| Mechanical in AEDT | `Mechanical` | AEDT Mechanical workflows when supported by installation |
| EMI/EMC | `Emit` | EMIT modeler and analysis |
| Motor design | `Rmxprt` | Rotating machine preprocessing |
| Maxwell circuit | `MaxwellCircuit` | Maxwell circuit design |
| Layout database | `Edb` / `pyedb.Edb` | PCB/package/IC database; not an AEDT design object |
| Coupled source/target | Icepak plus HFSS, HFSS 3D Layout, Maxwell, Q2D/Q3D, Mechanical, or external Fluent/RedHawk-SC data | Use an explicit exchange contract; do not assume the source solver shares the Icepak mesh or units |
| Application/session | `Desktop` | Launch, attach, release, version and process control |

## Session templates

```python
from ansys.aedt.core import Desktop

with Desktop(
    version="2026.1",
    non_graphical=True,
    new_desktop=True,
    close_on_exit=True,
) as desktop:
    print(desktop.aedt_version_id)
```

Attach to an existing local session only when intended:

```python
from ansys.aedt.core import Hfss

hfss = Hfss(
    project="input.aedt",
    design="HFSSDesign1",
    version="2026.1",
    new_desktop=False,
    close_on_exit=False,
)
try:
    # Work with the active/selected design.
    pass
finally:
    hfss.release_desktop(close_projects=False, close_desktop=False)
```

For remote gRPC, set the documented settings and provide the remote machine/port only when the server is already configured:

```python
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

settings.use_grpc_api = True
hfss = Hfss(machine="fullmachinename", port=50051, non_graphical=True)
```

Use secure defaults. Do not switch to insecure transport merely to bypass an unexplained error; first check the AEDT service pack, certificates, host firewall, and whether the server uses the expected startup arguments.

## Core object model

```python
# Variables: design variable vs project variable.
hfss["width"] = "1 mm"
hfss["$substrate_thickness"] = "0.8 mm"

# Modeler: create, retrieve, inspect, edit.
box = hfss.modeler.create_box(
    origin=[0, 0, 0],
    sizes=[10, 10, 1],
    name="Substrate",
    material="FR4_epoxy",
)
box.material_name = "FR4_epoxy"
box.transparency = 0.4
same_box = hfss.modeler["Substrate"]

# Setup: read/edit/create with explicit names.
for setup in hfss.setups:
    print(setup.name, setup.props)
setup = hfss.create_setup("Setup1")
setup.props["MaximumPasses"] = 10
setup.update()

# Solve and report.
hfss.analyze(setup.name)
hfss.post.create_report(["db(S(1,1))"])
```

The exact keyword names can differ by application and AEDT release. Confirm against the API reference or `inspect.signature()` before executing a generated call.

## Application-specific distinctions

- **HFSS:** validate solution type, boundaries, ports, radiation/open regions, adaptive setup, frequency sweep, and S-parameter expressions.
- **Maxwell:** validate design type (2D/3D), solution type, motion/force/torque setup, material B-H data, circuit coupling, and transient time steps.
- **Icepak:** validate fluid/solid materials, thermal sources, boundaries, global/local mesh regions, convergence monitors, and electrothermal links.
- **Q2D/Q3D:** validate nets, terminals, conductor/dielectric definitions, extraction setup, frequency range, and matrix/report outputs.
- **Hfss3dLayout/PyEDB:** validate stackup, layers, nets, padstacks, components, ports, and whether an operation belongs in EDB or AEDT.
- **Coupled thermal:** validate source/target design revisions, coordinate systems, units, selected solution/intrinsics, mapped power or temperature totals, mesh/scaling diagnostics, and one-way versus two-way feedback.
- **Circuit/TwinBuilder/EMIT/Mechanical/RMxprt:** use the application's own setup, schematic/modeler, and report APIs; do not assume HFSS method names transfer.

## CLI map

The current CLI exposes commands such as:

```text
pyaedt version
pyaedt aedt-versions
pyaedt session start --non-graphical --port 50051
pyaedt session list
pyaedt session attach --port 50051
pyaedt project list --port 50051
pyaedt project open my_project.aedt --port 50051
pyaedt project create --port 50051 --project DemoProject --design Filter1 --type Hfss
pyaedt run my_script.py --port 50051
pyaedt export screenshot --port 50051 --project DemoProject --design Filter1
pyaedt export config --port 50051 --project DemoProject --design Filter1 --output design.json
pyaedt doc user-guide
```

Run `pyaedt --help` and the command-specific `--help` before relying on a release-sensitive option. Use `--json` when a script needs machine-readable output.
