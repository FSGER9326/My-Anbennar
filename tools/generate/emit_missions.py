#!/usr/bin/env python3
"""
emit_missions.py
Generates Anbennar-shaped mission files from a validated mod-spec JSON.
Reads: mod_spec.validated.json
Outputs: mission files in the correct path, with correct slot/naming patterns.

Real Anbennar pattern:
  mytag_1 = {
      slot = 1
      generic = no
      ai = yes
      has_country_shield = yes
      potential = { tag = TAG }
      mytag_mission_1 = {
          name = "key_name_title"
          desc = "key_name_desc"
          ...
      }
  }
"""
import sys
import json
from pathlib import Path

MISSION_TEMPLATE = """{tree_key} = {{
    slot = {slot}
    generic = no
    ai = yes
    has_country_shield = yes
    potential = {{
        tag = {tag}
    }}
    {mission_id} = {{
        name = "{loc_prefix}{mission_id}_title"
        desc = "{loc_prefix}{mission_id}_desc"
        trigger = {{
            {trigger}
        }}
        effect = {{
            {effect}
        }}
        ai_will_do = {{
            factor = 1
        }}
    }}
}}
"""


def emit_mission_file(spec: dict, output_path: Path):
    missions = spec.get('content', {}).get('missions', [])
    tag = spec['registries']['tag']

    lines = [f"# Auto-generated from mod-spec — do not edit directly\n"]

    for m in missions:
        slot = m.get('slot', 1)
        tree_key = m.get('tree_key', f"{tag.lower()}_{slot}")
        mission_id = m.get('id', f"{tag.lower()}_mission_{slot}")
        trigger = m.get('trigger', 'always = yes')
        effect = m.get('effect', 'set_country_flag = done')
        loc_prefix = spec['registries'].get('loc_prefix', f"{tag.lower()}_")

        block = MISSION_TEMPLATE.format(
            tree_key=tree_key,
            slot=slot,
            tag=tag,
            mission_id=mission_id,
            loc_prefix=loc_prefix,
            trigger=trigger,
            effect=effect
        )
        lines.append(block)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"emit_missions: wrote {len(missions)} missions to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: emit_missions.py <spec.validated.json> [output_path]")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())

    tag = spec['registries']['tag']
    default_output = Path(f"missions/{tag}_Missions.txt")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_output

    emit_mission_file(spec, output_path)


if __name__ == '__main__':
    main()
