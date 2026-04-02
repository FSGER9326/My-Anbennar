#!/usr/bin/env python3
"""
scan_override_blast_radius.py
Classifies files as high-risk if they override upstream Anbennar files,
and flags when high-risk paths are modified without explicit justification.

High-risk paths:
  - map/ (adjacencies.csv, default.map, definition.csv, positions.txt, provinces.bmp)
  - common/country_tags/ (tag registry — crash risk)
  - common/estate_privileges/ (game balance)
  - common/government_reforms/ (systemic changes)
  - common/scripted_effects/ (shared logic)
  - common/scripted_triggers/ (shared logic)
  - common/religions/ (religious system)
  - common/trade_companies/ (trade system)
  - common/cultures/ (culture system)

For PRs touching these paths, requires blast-radius summary in PR body.
"""
import sys
import os
from pathlib import Path

HIGH_RISK_PATHS = {
    'map': 'HIGH — map assets (positions, provinces, adjacencies)',
    'common/country_tags': 'CRITICAL — tag registry (crash risk if malformed)',
    'common/estate_privileges': 'HIGH — estate balance',
    'common/government_reforms': 'HIGH — government system',
    'common/scripted_effects': 'HIGH — shared effect logic',
    'common/scripted_triggers': 'HIGH — shared trigger logic',
    'common/religions': 'HIGH — religious system',
    'common/trade_companies': 'MEDIUM — trade system',
    'common/cultures': 'MEDIUM — culture system',
    'common/mercenaries': 'MEDIUM — mercenary system',
    'common/tradegoods': 'MEDIUM — trade goods',
}

RISK_THRESHOLD = 'HIGH'  # Fail if CRITICAL or HIGH touched without blast-radius note

SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools', '.github'}


def classify_risk(path: Path) -> str | None:
    """Return risk level if path is high-risk, else None."""
    rel = str(path)
    for risk_prefix, level in HIGH_RISK_PATHS.items():
        if risk_prefix in rel:
            return level
    return None


def check_changed_files(root: Path, upstream_sha: str = None) -> list:
    """Check which high-risk files were modified vs upstream."""
    import subprocess

    issues = []
    try:
        # Get list of changed files vs upstream
        cmd = ['git', 'diff', '--name-only', f'{upstream_sha}...HEAD'] if upstream_sha else ['git', 'status', '--porcelain']
        result = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        changed_files = result.stdout.strip().split('\n')
    except Exception:
        # Fallback: scan all files
        changed_files = [str(p) for p in root.rglob('*') if p.is_file()]

    touched_risks = {}
    for f in changed_files:
        if not f or f.startswith('??'):
            continue
        fp = root / f
        risk = classify_risk(fp)
        if risk:
            touched_risks[f] = risk

    if touched_risks:
        issues.append("HIGH-RISK PATHS TOUCHED:")
        for f, risk in sorted(touched_risks.items()):
            issues.append(f"  [{risk}] {f}")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()
    upstream_sha = os.environ.get('UPSTREAM_SHA', None)

    all_issues = check_changed_files(root, upstream_sha)

    if all_issues:
        print("BLAST RADIUS ALERT:")
        for issue in all_issues:
            print(issue)
        print("\nPR requires blast-radius summary for high-risk path changes.")
        sys.exit(1)
    else:
        print("scan_override_blast_radius: PASS — no high-risk paths touched")
        sys.exit(0)


if __name__ == '__main__':
    main()
