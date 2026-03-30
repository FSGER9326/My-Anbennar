#!/usr/bin/env python3
"""Validate automation/conflict_hotspots.yaml structure and severity boundaries."""

from __future__ import annotations

from pathlib import Path
import sys

from pr_conflict_churn_plan import parse_simple_yaml_lists

REGISTRY_PATH = Path("automation/conflict_hotspots.yaml")
REQUIRED_KEYS = ("single_writer_files", "single_writer_prefixes", "advisory_hotspots")


def has_duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate_paths(values: list[str], *, key: str, errors: list[str]) -> None:
    for value in values:
        if not value:
            errors.append(f"{key}: empty entry is not allowed")
            continue
        if value.startswith("/"):
            errors.append(f"{key}: '{value}' must be repo-relative (no leading slash)")
        if "\\" in value:
            errors.append(f"{key}: '{value}' must use '/' separators")


def validate_prefixes(values: list[str], *, key: str, errors: list[str]) -> None:
    for value in values:
        if not value.endswith("/"):
            errors.append(f"{key}: '{value}' must end with '/' to denote a directory prefix")


def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"Conflict hotspot registry is missing: {REGISTRY_PATH}")
        return 1

    try:
        parsed = parse_simple_yaml_lists(REGISTRY_PATH)
    except RuntimeError as exc:
        print(f"Conflict hotspot registry parse failed: {exc}")
        return 1

    errors: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in parsed:
            errors.append(f"missing required key: {key}")

    unexpected = sorted(set(parsed) - set(REQUIRED_KEYS))
    for key in unexpected:
        errors.append(f"unexpected top-level key: {key}")

    single_writer_files = parsed.get("single_writer_files", [])
    single_writer_prefixes = parsed.get("single_writer_prefixes", [])
    advisory_hotspots = parsed.get("advisory_hotspots", [])

    validate_paths(single_writer_files, key="single_writer_files", errors=errors)
    validate_paths(single_writer_prefixes, key="single_writer_prefixes", errors=errors)
    validate_paths(advisory_hotspots, key="advisory_hotspots", errors=errors)

    validate_prefixes(single_writer_prefixes, key="single_writer_prefixes", errors=errors)

    advisory_prefixes = [value for value in advisory_hotspots if value.endswith("/")]
    duplicates = {
        "single_writer_files": has_duplicates(single_writer_files),
        "single_writer_prefixes": has_duplicates(single_writer_prefixes),
        "advisory_hotspots": has_duplicates(advisory_hotspots),
    }
    for key, dups in duplicates.items():
        for value in dups:
            errors.append(f"{key}: duplicate entry '{value}'")

    single_writer_file_set = set(single_writer_files)
    single_writer_prefix_set = set(single_writer_prefixes)
    advisory_hotspot_set = set(advisory_hotspots)
    advisory_prefix_set = set(advisory_prefixes)

    for value in sorted(single_writer_file_set & advisory_hotspot_set):
        errors.append(
            f"entry '{value}' appears in both single_writer_files and advisory_hotspots"
        )
    for value in sorted(single_writer_prefix_set & advisory_prefix_set):
        errors.append(
            f"entry '{value}' appears in both single_writer_prefixes and advisory_hotspots"
        )

    if errors:
        print("Conflict hotspot registry validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "Conflict hotspot registry validation passed: "
        f"{len(single_writer_files)} single-writer files, "
        f"{len(single_writer_prefixes)} single-writer prefixes, "
        f"{len(advisory_hotspots)} advisory hotspots."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
