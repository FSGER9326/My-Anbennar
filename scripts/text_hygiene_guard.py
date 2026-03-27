#!/usr/bin/env python3
"""Catch common text-hygiene problems in docs and localization files."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

TARGET_GLOBS = [
    "docs/**/*.md",
    ".github/**/*.md",
    "localisation/**/*.yml",
]

SUSPICIOUS_TOKENS = {
    "\u00e2\u20ac": "likely mojibake from smart quotes or dashes",
    "\u00c3": "likely mojibake from UTF-8 text decoded as Latin-1",
    "\u00ef\u00bb\u00bf": "literal UTF-8 BOM bytes in file text",
    "\ufffd": "replacement character found",
}


def iter_files() -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in TARGET_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file():
                seen[path] = None
    return sorted(seen)


def normalize_line(line: str) -> str:
    lowered = line.lower()
    lowered = lowered.replace("`", "")
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return lowered.strip()


def main() -> int:
    errors: list[str] = []

    for path in iter_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")

        for token, reason in SUSPICIOUS_TOKENS.items():
            if token in text:
                errors.append(f"{rel}: contains suspicious text ({reason})")

        lines = text.splitlines()
        previous_line = ""
        previous_normalized = ""
        previous_number = 0

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue

            normalized = normalize_line(stripped)
            if (
                normalized
                and previous_normalized
                and normalized == previous_normalized
                and normalized != "on"
                and len(normalized) >= 12
                and stripped != previous_line
            ):
                errors.append(
                    f"{rel}:{previous_number}-{idx}: near-duplicate consecutive lines"
                )

            previous_line = stripped
            previous_normalized = normalized
            previous_number = idx

    if errors:
        print("Text hygiene guard failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("Text hygiene guard passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
