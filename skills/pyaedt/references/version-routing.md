# PyAEDT version routing

## Required discovery

Before generating release-sensitive code, collect:

    PyAEDT package version: python -m pip show pyaedt
    PyAEDT import version: python -c "import ansys.aedt.core as a; print(a.__version__)"
    AEDT installations: pyaedt aedt-versions
    Python runtime: python --version
    OS and architecture: platform.platform(), platform.machine()

If the CLI or import is unavailable, report that the environment is not ready and do not infer a version from a project filename.

## Compatibility matrix

| AEDT range | Interface choice | EDB/PyEDB | Primary guidance |
| --- | --- | --- | --- |
| 2021 R2 to 2022 R1 | COM on Windows | Legacy path | Use release-matched PyAEDT and avoid gRPC-only patterns. |
| 2022 R2 to 2024 R2 | Prefer gRPC; COM only where the matrix permits it | EDB is the exception to general gRPC support | Check service pack and transport mode before remote work. |
| 2025 R1 | gRPC | EDB gRPC not yet the default boundary | Use modern session code; do not assume PyEDB gRPC. |
| 2025 R2 | gRPC | PyEDB gRPC is supported and can be enabled | Use settings.pyedb_use_grpc = True only when the package and AEDT support it. |
| 2026 R1 and later | gRPC | PyEDB gRPC is enabled by default from 2026 R1 | Prefer current ansys.aedt.core and secure defaults. |

This matrix is a routing aid, not a substitute for the exact versioned compatibility table. Recheck the official versioning page for service-pack exceptions.

## PyAEDT major-version migration

For PyAEDT 0.x code:

    from pyaedt import Circuit
    circuit = Circuit(designname="Demo")

For PyAEDT 1.x code:

    from ansys.aedt.core import Circuit
    circuit = Circuit(design="Demo")

Migration rules:

- Replace imports from pyaedt with imports from ansys.aedt.core when the installed major version supports the new namespace.
- Replace deprecated argument names such as designname with design.
- Do not rely on a method returning False to indicate every error in 1.x; use try/except and inspect logs because the default error-handler behavior changed.
- Check release notes for renamed modules, removed deprecations, and behavior changes before upgrading a production script.
- Keep the PyAEDT package version and AEDT installation version pinned/documented together.

## Selection rule

1. Select the AEDT range from the installed AEDT version.
2. Select the API style from the installed PyAEDT major version.
3. Select EDB behavior separately; it does not follow the general AEDT gRPC boundary.
4. Select the Python runtime and wheelhouse for the target AEDT release.
5. Run an import and session smoke test before a solver run.

Official references:

- https://aedt.docs.pyansys.com/version/stable/Getting_started/versioning.html
- https://aedt.docs.pyansys.com/version/stable/release_1_0.html
- https://aedt.docs.pyansys.com/version/stable/Getting_started/Installation.html
- https://aedt.docs.pyansys.com/version/stable/changelog.html
