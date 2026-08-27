# AEDT 2021 R2 to 2022 R1

## Use this branch when

The installed AEDT version is 2021 R2, 2022 R1, or an equivalent legacy release.

## Interface rules

- Use the Windows COM interface; gRPC is not available in this branch.
- Use a PyAEDT release that explicitly supports the installed AEDT version.
- Prefer the Python runtime shipped with AEDT when external Python compatibility is uncertain.
- Do not copy current secure gRPC, remote server, PyEDB gRPC, or 1.x-only examples into this branch.
- Test project open, design selection, save, and release before attempting a solve.

## Workflow constraints

Keep scripts conservative:

    from ansys.aedt.core.generic.settings import settings
    settings.use_grpc_api = False

Only use this setting when the installed package exposes the current settings API. If the release uses the older namespace, follow its matching documentation instead of forcing this import.

Validate:

- AEDT is running on Windows.
- COM can see the intended project/design.
- only one automation process owns the project lock;
- the script closes or releases the session deterministically.

Official compatibility source:

https://aedt.docs.pyansys.com/version/stable/Getting_started/versioning.html
