#!/usr/bin/env python3
"""Aggregate validation JSON outputs into report artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"

SEVERITY_WEIGHT = {"critical": 0, "error": 1, "warning": 2, "info": 3}
AUTOFIX_SAFE_CODES = {
    "MERGE_CONFLICT_MARKER",
    "HEADING_SINGLETON_VIOLATION",
    "MISSING_UTF8_BOM",
}


def _fixability_rank(issue: dict[str, object]) -> int:
    cmd = str(issue.get("suggested_fix_command") or "").strip()
    code = str(issue.get("code") or "")
    if code in AUTOFIX_SAFE_CODES and cmd:
        return 0
    if cmd:
        return 1
    return 2


def aggregate(inputs: list[Path]) -> dict[str, object]:
    checks: list[dict[str, object]] = []
    issues: list[dict[str, object]] = []

    for p in inputs:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            data = {
                "check": p.stem,
                "status": "failed",
                "issues": [
                    {
                        "check": p.stem,
                        "severity": "error",
                        "file": str(p),
                        "line": None,
                        "code": "INVALID_AUDIT_JSON",
                        "message": f"unable to parse audit JSON: {exc}",
                        "suggested_fix_command": "Re-run the failing audit with --format json and fix its runtime error",
                    }
                ],
            }
        try:
            source = p.relative_to(ROOT).as_posix()
        except ValueError:
            source = str(p)
        checks.append({"check": data.get("check", p.stem), "status": data.get("status", "unknown"), "source": source})
        issues.extend(data.get("issues", []))

    issues.sort(key=lambda i: (SEVERITY_WEIGHT.get(str(i.get("severity", "warning")).lower(), 99), _fixability_rank(i), str(i.get("check", "")), str(i.get("file", "")), int(i.get("line") or 0)))

    return {
        "status": "failed" if issues else "passed",
        "summary": {
            "checks_total": len(checks),
            "checks_failed": sum(1 for c in checks if c.get("status") == "failed"),
            "issues_total": len(issues),
        },
        "checks": checks,
        "issues": issues,
    }


def to_markdown(report: dict[str, object]) -> str:
    checks = report["checks"]
    issues = report["issues"]
    lines = [
        "# Validation Report",
        "",
        f"**Status:** {report['status']}",
        f"**Checks:** {report['summary']['checks_total']} total, {report['summary']['checks_failed']} failed",
        f"**Issues:** {report['summary']['issues_total']}",
        "",
        "## Checks",
        "",
        "| Check | Status | Source |",
        "|---|---|---|",
    ]
    for c in checks:
        lines.append(f"| `{c['check']}` | {c['status']} | `{c['source']}` |")

    lines.extend(["", "## Issues (sorted by impact and fixability)", ""])
    if not issues:
        lines.append("No issues found. ✅")
        return "\n".join(lines) + "\n"

    lines.extend([
        "| Severity | Check | Location | Code | Message | Suggested fix |",
        "|---|---|---|---|---|---|",
    ])
    for i in issues:
        loc = str(i.get("file", ""))
        if i.get("line"):
            loc = f"{loc}:{i['line']}"
        msg = str(i.get('message', '')).replace('|', '\\|')
        lines.append(
            f"| {i.get('severity','')} | `{i.get('check','')}` | `{loc}` | `{i.get('code','')}` | {msg} | `{i.get('suggested_fix_command','')}` |"
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", action="append", required=True, help="Input JSON file from individual audit (repeatable)")
    ap.add_argument("--out-json", default="artifacts/validation_report.json")
    ap.add_argument("--out-md", default="artifacts/validation_report.md")
    args = ap.parse_args()

    inputs = [ROOT / p for p in args.input]
    report = aggregate(inputs)

    out_json = ROOT / args.out_json
    out_md = ROOT / args.out_md
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(to_markdown(report), encoding="utf-8")

    def _disp(path: Path) -> str:
        try:
            return path.relative_to(ROOT).as_posix()
        except ValueError:
            return str(path)

    print(f"Wrote {_disp(out_json)} and {_disp(out_md)}")
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
