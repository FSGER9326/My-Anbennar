#!/usr/bin/env python3
"""
scan_namespace_collisions.py
Scans event files for namespace declarations, then checks that event IDs
are unique within each namespace and that no two files declare the same
namespace.

Also checks that decision files do not reuse decision keys across files
in ways that could cause silent overwrites.
"""
import sys
import os
import re
from pathlib import Path
from collections import defaultdict

SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools', '.github'}


def extract_namespace(txt: str) -> str | None:
    m = re.search(r'^\s*namespace\s*=\s*(\S+)', txt, re.MULTILINE)
    return m.group(1) if m else None


def extract_event_ids(txt: str, namespace: str) -> list:
    ids = []
    # Match e.g. "namespace.1 = {" or just "1 = {"
    for m in re.finditer(r'^\s*' + re.escape(namespace) + r'\.(\d+)\s*=', txt, re.MULTILINE):
        ids.append(f"{namespace}.{m.group(1)}")
    return ids


def extract_decision_keys(txt: str) -> list:
    keys = []
    for m in re.finditer(r'^\s*(\w+)\s*=\s*\{', txt, re.MULTILINE):
        keys.append(m.group(1))
    return keys


def scan_events(root: Path):
    ns_map = defaultdict(list)  # namespace -> [(file, [ids])]
    for path in root.rglob('events/*.txt'):
        if any(d in path.parts for d in SKIPDirs):
            continue
        txt = path.read_text(encoding='utf-8', errors='replace')
        ns = extract_namespace(txt)
        if not ns:
            continue
        ids = extract_event_ids(txt, ns)
        ns_map[ns].append((str(path), ids))

    issues = []
    for ns, files in ns_map.items():
        if len(files) > 1:
            paths = [f[0] for f in files]
            issues.append(f"Namespace '{ns}' declared in multiple files: {paths}")

        all_ids = []
        for fp, ids in files:
            for eid in ids:
                if eid in all_ids:
                    issues.append(f"Duplicate event ID {eid} in: {fp}")
                all_ids.append(eid)

    return issues


def scan_decisions(root: Path):
    key_map = defaultdict(list)  # decision key -> [(file, line)]
    for path in root.rglob('decisions/*.txt'):
        if any(d in path.parts for d in SKIPDirs):
            continue
        txt = path.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'^\s*(\w+)\s*=\s*\{', txt, re.MULTILINE):
            key = m.group(1)
            key_map[key].append(str(path))

    issues = []
    for key, paths in key_map.items():
        if len(paths) > 1:
            issues.append(f"Decision key '{key}' appears in multiple files: {list(set(paths))}")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()

    all_issues = []
    all_issues.extend(scan_events(root))
    all_issues.extend(scan_decisions(root))

    if all_issues:
        print("NAMESPACE COLLISION ISSUES:")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("scan_namespace_collisions: PASS")
        sys.exit(0)


if __name__ == '__main__':
    main()
