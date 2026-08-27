"""Validate and summarize a PyAEDT/Icepak thermal case manifest.

This script does not launch AEDT. It provides a deterministic preflight gate
for case identity, model fidelity, physics, power, boundaries, mesh, solver,
responses, and provenance before an AEDT runner is invoked.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_GROUPS = (
    "identity",
    "model",
    "physics",
    "power",
    "boundaries",
    "mesh",
    "solver",
    "responses",
    "provenance",
)

REQUIRED_FIELDS = {
    "identity": ("case_id", "revision", "purpose"),
    "model": ("package_type", "fidelity", "units"),
    "physics": ("regime", "conduction", "convection", "radiation"),
    "power": ("definition", "total_power"),
    "boundaries": ("ambient_or_inlet", "reference_surfaces"),
    "mesh": ("global_policy", "quality_limits"),
    "solver": ("setup", "convergence"),
    "responses": ("required", "limits"),
    "provenance": ("geometry_source", "script_revision"),
}


def validate_manifest(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be a JSON object"]

    for group in REQUIRED_GROUPS:
        value = data.get(group)
        if not isinstance(value, dict):
            errors.append(f"missing object: {group}")
            continue
        for field in REQUIRED_FIELDS[group]:
            if field not in value or value[field] in (None, "", [], {}):
                errors.append(f"missing value: {group}.{field}")

    case_id = data.get("identity", {}).get("case_id")
    if isinstance(case_id, str) and ("/" in case_id or "\\" in case_id):
        errors.append("identity.case_id must not contain path separators")

    total_power = data.get("power", {}).get("total_power")
    if isinstance(total_power, (int, float)) and total_power < 0:
        errors.append("power.total_power must be non-negative")

    return errors


def summary(data: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    identity = data.get("identity", {})
    model = data.get("model", {})
    return {
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
        "case_id": identity.get("case_id"),
        "revision": identity.get("revision"),
        "package_type": model.get("package_type"),
        "fidelity": model.get("fidelity"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON case manifest")
    parser.add_argument("--output", type=Path, help="write JSON summary")
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_manifest(data)
    result = summary(data, errors)
    rendered = json.dumps(result, indent=2, ensure_ascii=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
