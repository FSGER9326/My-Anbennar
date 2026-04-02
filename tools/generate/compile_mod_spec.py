#!/usr/bin/env python3
"""
compile_mod_spec.py
Reads a mod-spec.yaml file and validates it against the registry.
Emits a validated spec as JSON for the emit_*.py scripts to consume.
"""
import sys
import yaml
import json
from pathlib import Path

REQUIRED_META_FIELDS = ['mod_id', 'target_eu4', 'target_anbennar']
REQUIRED_REGISTRY_FIELDS = ['tag', 'event_namespace', 'country_tags_file']


def load_spec(spec_path: Path) -> dict:
    with open(spec_path) as f:
        raw = yaml.safe_load(f)
    return raw


def validate_meta(meta: dict) -> list:
    errors = []
    for field in REQUIRED_META_FIELDS:
        if field not in meta:
            errors.append(f"Missing required meta field: {field}")
    return errors


def validate_registries(registries: dict) -> list:
    errors = []
    for field in REQUIRED_REGISTRY_FIELDS:
        if field not in registries:
            errors.append(f"Missing required registry field: {field}")
    return errors


def validate_against_registry(spec: dict, registry_root: Path) -> list:
    errors = []

    # Check tag not already allocated
    tag = spec.get('registries', {}).get('tag')
    if tag:
        tags_yaml = registry_root / 'design' / 'registries' / 'tags.yaml'
        if tags_yaml.exists():
            import re
            txt = tags_yaml.read_text()
            if re.search(rf'^\s+{tag}\s*:', txt, re.MULTILINE):
                # Check if it's a submod reservation or just upstream
                if 'upstream: true' not in txt:
                    errors.append(f"Tag '{tag}' may already be registered — check design/registries/tags.yaml")

    # Check namespace not already allocated
    ns = spec.get('registries', {}).get('event_namespace')
    if ns:
        ns_yaml = registry_root / 'design' / 'registries' / 'namespaces.yaml'
        if ns_yaml.exists():
            import re
            txt = ns_yaml.read_text()
            if re.search(rf'^\s+{re.escape(ns)}\s*:', txt, re.MULTILINE):
                if 'upstream: true' not in txt:
                    errors.append(f"Namespace '{ns}' may already be registered — check design/registries/namespaces.yaml")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: compile_mod_spec.py <spec.yaml> [registry_root]")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    registry_root = Path(sys.argv[2]) if len(sys.argv) > 2 else spec_path.parent.parent

    spec = load_spec(spec_path)
    errors = []
    errors.extend(validate_meta(spec.get('meta', {})))
    errors.extend(validate_registries(spec.get('registries', {})))
    errors.extend(validate_against_registry(spec, registry_root))

    if errors:
        print("SPEC VALIDATION ERRORS:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)

    # Write validated JSON
    out_path = spec_path.with_suffix('.validated.json')
    with open(out_path, 'w') as f:
        json.dump(spec, f, indent=2)
    print(f"compile_mod_spec: OK — validated spec written to {out_path}")
    sys.exit(0)


if __name__ == '__main__':
    main()
