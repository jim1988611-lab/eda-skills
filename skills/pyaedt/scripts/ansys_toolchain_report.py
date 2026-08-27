"""Report optional Ansys package-thermal toolchain readiness.

This is a read-only discovery script. It does not launch AEDT, Fluent,
Workbench, RedHawk-SC, or any solver. It reports local Python modules,
commands, and common Windows installation paths plus manual checks for
products that do not have a stable public executable discovery convention.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
from pathlib import Path
from typing import Any


def module_status(name: str) -> dict[str, Any]:
    spec = importlib.util.find_spec(name)
    return {"status": "available" if spec else "not_found", "module": name}


def command_status(names: list[str]) -> dict[str, Any]:
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return {"status": "available", "command": name, "path": resolved}
    return {"status": "not_found", "commands": names}


def common_paths(relative_paths: list[str]) -> list[str]:
    roots = []
    for env_name in ("ProgramFiles", "ProgramW6432"):
        value = os.environ.get(env_name)
        if value:
            roots.append(Path(value))
    roots.append(Path("C:/Program Files"))
    matches: list[str] = []
    for root in roots:
        for pattern in relative_paths:
            for match in root.glob(pattern):
                if match.exists():
                    rendered = str(match)
                    if rendered not in matches:
                        matches.append(rendered)
    return matches


def build_report() -> dict[str, Any]:
    aedt_command = command_status(["ansysedt"])
    aedt_paths = common_paths(["ANSYS Inc/v*/Electronics/AnsysEM/ansysedt.exe"])
    workbench_paths = common_paths(["ANSYS Inc/v*/Framework/bin/Win64/RunWB2.exe"])
    fluent_paths = common_paths(["ANSYS Inc/v*/fluent/ntbin/win64/fluent.exe"])
    return {
        "read_only": True,
        "tools": {
            "pyaedt": module_status("ansys.aedt.core"),
            "pyedb": module_status("pyedb"),
            "pyaedt_cli": command_status(["pyaedt"]),
            "aedt": {
                "status": "available" if aedt_command["status"] == "available" or aedt_paths else "not_found",
                "command": aedt_command,
                "paths": aedt_paths,
            },
            "workbench_mechanical": {
                "status": "available" if workbench_paths else "manual_check",
                "paths": workbench_paths,
            },
            "fluent": {
                "status": "available" if fluent_paths else "manual_check",
                "paths": fluent_paths,
            },
            "redhawk_sc_electrothermal": {
                "status": "manual_check",
                "note": "Verify installation, license, version, and data-transfer interface with the project owner.",
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write JSON report")
    args = parser.parse_args()
    rendered = json.dumps(build_report(), indent=2, ensure_ascii=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
