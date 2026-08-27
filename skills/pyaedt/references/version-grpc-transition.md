# AEDT 2022 R2 to 2024 R2

## Use this branch when

The installed AEDT version is between 2022 R2 and 2024 R2.

## Interface rules

- Prefer gRPC for AEDT 2022 R2 and later.
- For 2022 R2 and older service packs, verify the gRPC service-pack requirements and use legacy startup arguments only when documented.
- Keep COM as a Windows fallback only for releases where the official compatibility matrix marks it supported.
- Treat EDB as a separate exception; general AEDT gRPC support does not imply PyEDB gRPC support.

## Session checks

Before remote or headless work, verify:

    AEDT process and port
    gRPC secure/insecure mode
    service pack
    host firewall
    license availability
    project path on the correct machine

For local work, use secure local defaults when the service pack supports them. For network work, do not use insecure transport as the normal solution.

## EDB rule

Do not set settings.pyedb_use_grpc = True in this branch unless the exact AEDT and PyEDB documentation explicitly supports it. Use the legacy EDB path or a release-matched PyEDB workflow.

Official references:

- https://aedt.docs.pyansys.com/version/stable/Getting_started/versioning.html
- https://aedt.docs.pyansys.com/version/stable/Getting_started/ClientServer.html
- https://aedt.docs.pyansys.com/version/stable/Getting_started/Troubleshooting.html
