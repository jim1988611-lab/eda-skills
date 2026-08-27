# AEDT 2026 R1 and later

## Use this branch when

The installed AEDT version is 2026 R1, 2026 R2, 2027 R1, or a later release covered by the current official documentation.

## Default choices

- Prefer imports from ansys.aedt.core.
- Prefer gRPC with secure local defaults.
- PyEDB gRPC is enabled by default from AEDT 2026 R1; still record the effective setting and verify the package version.
- Use the current CLI for session, project, script, export, and documentation tasks.
- Recheck the changelog for release-specific API additions and removals.

## 2026 R2 service-pack note

Starting with AEDT 2026 R2 service pack 2, PyAEDT is bundled with AEDT. The bundled package contains runtime dependencies only. Install a separate virtual-environment package when optional extras, newer PyAEDT, or reproducible dependency pinning are required.

## Current code style

    from ansys.aedt.core import Desktop, Icepak

    with Desktop(
        version="2026.1",
        non_graphical=True,
        new_desktop=True,
        close_on_exit=True,
    ):
        app = Icepak(new_desktop=False)
        # Use current typed APIs and application-specific setup/mesh objects.

Replace the example version with one reported by pyaedt aedt-versions; do not hard-code 2026.1 in a portable tool.

## Current-feature checks

For current releases, verify the installed version before using:

- typed Fields Calculator builders;
- current CLI plugin commands;
- PyEDB gRPC;
- current Icepak mesh-region APIs;
- new setup/report arguments.

Official references:

- https://aedt.docs.pyansys.com/version/stable/Getting_started/Installation.html
- https://aedt.docs.pyansys.com/version/stable/Getting_started/versioning.html
- https://aedt.docs.pyansys.com/version/stable/Getting_started/cli.html
- https://aedt.docs.pyansys.com/version/stable/changelog.html
