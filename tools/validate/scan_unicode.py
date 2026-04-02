#!/usr/bin/env python3
"""
scan_unicode.py — Hidden/bidirectional Unicode scanner
Detects: BOM (wrong location), Bidi overrides, Zero-width chars, Smart quotes
Fails hard if any found in script/localisation files.
"""
import sys
import os
from pathlib import Path

# Characters that should never appear in EU4 text files
BOM = b'\xef\xbb\xbf'

BIDIRANGES = [
    (0x200E, 0x200E, "LRM"),
    (0x200F, 0x200F, "RLM"),
    (0x202A, 0x202A, "Bidi Embedding"),
    (0x202B, 0x202B, "Bidi Embedding"),
    (0x202C, 0x202C, "Bidi Pop"),
    (0x202D, 0x202D, "Bidi Override"),
    (0x202E, 0x202E, "Bidi Override (RTL)"),
]

ZEROWIDTH = [0x200B, 0x200C, 0x200D, 0xFEFF, 0xFFFE, 0xFFFF]

SMART_QUOTES = [(0x2018, 0x201F)]  # ' ' " etc

SKIPDirs = {'.git', 'node_modules', '.github', '__pycache__', '.cwtools'}


def scan_file(path: Path) -> list:
    issues = []
    try:
        raw = path.read_bytes()
    except Exception:
        return issues

    # BOM check (should not be on .txt/.gui files)
    if path.suffix in ('.txt', '.gui') and raw.startswith(BOM):
        issues.append(f"BOM on script file (should be CP-1252, not UTF-8): {path}")

    # Text mode read for character checks
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return issues

    for ch in text:
        cp = ord(ch)

        # Zero-width chars
        if cp in ZEROWIDTH:
            issues.append(f"Zero-width char U+{cp:04X} in: {path}")
            break

        # Bidirectional overrides
        for lo, hi, name in BIDIRANGES:
            if lo <= cp <= hi:
                issues.append(f"Bidi char {name} U+{cp:04X} in: {path}")
                break

        # Smart quotes
        for lo, hi in SMART_QUOTES:
            if lo <= cp <= hi:
                issues.append(f"Smart quote U+{cp:04X} in: {path} (EU4 uses straight quotes)")
                break
        else:
            continue
        break

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()
    exts = {'.txt', '.gui', '.yml', '.md'}

    all_issues = []
    for path in root.rglob('*'):
        if path.is_dir():
            continue
        if any(d in path.parts for d in SKIPDirs):
            continue
        if path.suffix in exts:
            issues = scan_file(path)
            all_issues.extend(issues)

    if all_issues:
        print("UNICODE ISSUES FOUND:")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("scan_unicode: PASS — no hidden/bidi Unicode found")
        sys.exit(0)


if __name__ == '__main__':
    main()
