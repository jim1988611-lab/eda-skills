# AEDT 2025 R1 to 2025 R2

## Use this branch when

The installed AEDT version is 2025 R1 or 2025 R2.

## Interface rules

- Use gRPC as the primary AEDT interface.
- Do not assume COM is available for 2024 R2 and newer releases; follow the official matrix.
- Use current application constructors and the ansys.aedt.core namespace when the installed PyAEDT major version is 1.x.
- Verify the service pack before enabling secure transport modes.

## EDB split

- AEDT 2025 R1: do not assume PyEDB gRPC.
- AEDT 2025 R2: PyEDB gRPC is supported. Enable it only after checking the installed PyEDB/PyAEDT versions:

    from ansys.aedt.core.generic.settings import settings
    settings.pyedb_use_grpc = True

If PyEDB is used before AEDT 2026 R1, check whether the installation needs the all-dotnet extra or equivalent .NET dependencies.

## Validation

Run an EDB-specific smoke test separately from an AEDT design smoke test. Confirm that:

- the .aedb path is valid;
- the database opens and closes;
- edits persist after save;
- the AEDT design can consume the resulting data when required.

Official references:

- https://aedt.docs.pyansys.com/version/stable/Getting_started/versioning.html
- https://aedt.docs.pyansys.com/version/stable/Getting_started/Installation.html
- https://edb.docs.pyansys.com/
