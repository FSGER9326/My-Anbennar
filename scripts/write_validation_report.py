#!/usr/bin/env python3
"""Write a machine-readable validation report for pre-PR and CI flows."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_check(value: str) -> dict[str, str]:
    parts = value.split("|", 3)
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "--check entries must use 'name|command|status|severity' format"
        )
    name, command, status, severity = [part.strip() for part in parts]
    if not all((name, command, status, severity)):
        raise argparse.ArgumentTypeError("--check entries cannot contain empty fields")
    return {
        "name": name,
        "command": command,
        "status": status,
        "severity": severity,
    }


def parse_artifact(value: str) -> dict[str, str]:
    parts = value.split("|", 2)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            "--artifact entries must use 'name|path-or-url' format"
        )
    name, path = [part.strip() for part in parts]
    if not all((name, path)):
        raise argparse.ArgumentTypeError("--artifact entries cannot contain empty fields")
    payload = {"name": name}
    if path.startswith(("http://", "https://")):
        payload["url"] = path
    else:
        payload["path"] = path
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Write validation report JSON.")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument(
        "--overall-status",
        default="pass",
        help="Overall validation status (default: pass)",
    )
    parser.add_argument(
        "--check",
        action="append",
        default=[],
        type=parse_check,
        help="Check entry in 'name|command|status|severity' format (repeatable)",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        type=parse_artifact,
        help="Artifact entry in 'name|path-or-url' format (repeatable)",
    )
    parser.add_argument(
        "--issue",
        action="append",
        default=[],
        help="Optional unresolved issue title to include as high severity",
    )
    args = parser.parse_args()

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "overall_status": args.overall_status,
        "checks": args.check,
        "unresolved_issues": [
            {"title": issue, "severity": "high", "resolved": False} for issue in args.issue
        ],
        "artifacts": args.artifact,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Validation report written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
