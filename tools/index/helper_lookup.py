#!/usr/bin/env python3
"""
helper_lookup.py
Searches common/scripted_effects/ and common/scripted_triggers/ for existing helpers.
Before writing any new effect/trigger, call this script to find close matches.
Returns top 3–5 matches with file path and parameter info.
"""
import sys
import re
from pathlib import Path
from difflib import SequenceMatcher

MIN_SIMILARITY = 0.3


def search_effects(root: Path, query: str, limit: int = 5) -> list:
    """Search for scripted effects matching query."""
    results = []
    effects_dir = root / 'common' / 'scripted_effects'
    if not effects_dir.exists():
        return results

    for path in sorted(effects_dir.glob('*.txt')):
        txt = path.read_text(encoding='utf-8', errors='replace')
        # Extract effect names and params
        for m in re.finditer(r'^(\w+)\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', txt, re.MULTILINE | re.DOTALL):
            name = m.group(1)
            block = m.group(0)
            score = SequenceMatcher(None, query.lower(), name.lower()).ratio()
            if score >= MIN_SIMILARITY:
                # Extract params if present
                params = re.findall(r'(?:param_\w+|=\s*\$?\w+)', block[:200])
                results.append({
                    'name': name,
                    'file': str(path.relative_to(root)),
                    'score': round(score, 3),
                    'params': params[:5]
                })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]


def search_triggers(root: Path, query: str, limit: int = 5) -> list:
    """Search for scripted triggers matching query."""
    results = []
    triggers_dir = root / 'common' / 'scripted_triggers'
    if not triggers_dir.exists():
        return results

    for path in sorted(triggers_dir.glob('*.txt')):
        txt = path.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'^(\w+)\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', txt, re.MULTILINE | re.DOTALL):
            name = m.group(1)
            block = m.group(0)
            score = SequenceMatcher(None, query.lower(), name.lower()).ratio()
            if score >= MIN_SIMILARITY:
                params = re.findall(r'(?:param_\w+|=\s*\$?\w+)', block[:200])
                results.append({
                    'name': name,
                    'file': str(path.relative_to(root)),
                    'score': round(score, 3),
                    'params': params[:5]
                })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]


def main():
    if len(sys.argv) < 2:
        print("Usage: helper_lookup.py <query> [repo_root] [limit]")
        sys.exit(1)

    query = sys.argv[1]
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('.')
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    effects = search_effects(root, query, limit)
    triggers = search_triggers(root, query, limit)

    print(f"helper_lookup: query='{query}'")
    print(f"\nScripted Effects ({len(effects)} matches):")
    for e in effects:
        print(f"  [{e['score']}] {e['name']} ({e['file']})")
        if e['params']:
            print(f"    params: {', '.join(e['params'])}")

    print(f"\nScripted Triggers ({len(triggers)} matches):")
    for t in triggers:
        print(f"  [{t['score']}] {t['name']} ({t['file']})")
        if t['params']:
            print(f"    params: {', '.join(t['params'])}")

    if not effects and not triggers:
        print(f"\nNo close matches found for '{query}' — consider creating a new helper.")
        print("Remember: create a new helper only if reused 3+ times.")


if __name__ == '__main__':
    main()
