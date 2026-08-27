"""Report the local PyAEDT/AEDT environment without launching AEDT."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from typing import Any


def command_output(command: list[str]) -> str | None:
    """Run a read-only diagnostic command and return its output."""
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    output = (completed.stdout or completed.stderr).strip()
    return output or None


def package_version(name: str) -> str | None:
    """Return an installed package version, if available."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def core_import_available() -> bool:
    """Check the modern import path without importing AEDT."""
    try:
        return importlib.util.find_spec("ansys.aedt.core") is not None
    except (ImportError, ModuleNotFoundError):
        return False


def main() -> int:
    pyaedt_cli = shutil.which("pyaedt")
    report: dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "pyaedt_package": package_version("pyaedt"),
        "pyedb_package": package_version("pyedb"),
        "modern_core_import": core_import_available(),
        "pyaedt_cli": pyaedt_cli,
        "pyaedt_version_command": (
            command_output([pyaedt_cli, "version"]) if pyaedt_cli else None
        ),
        "aedt_versions_command": (
            command_output([pyaedt_cli, "aedt-versions"]) if pyaedt_cli else None
        ),
    }
    print(json.dumps(report, indent=2))
    return 0 if report["modern_core_import"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
