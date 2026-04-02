#!/usr/bin/env python3
"""
emit_events.py
Generates Anbennar-shaped event files from a validated mod-spec JSON.
Real Anbennar pattern:
  namespace = flavour_<slug>
  flavour_slug.1 = {
      title = "flavour_slug_1_title"
      desc = "flavour_slug_1_desc"
      picture = "event_picture_default"
      is_triggered_only = yes
      trigger = { tag = TAG }
      immediate = { ... }
      option = { name = "flavour_slug_1_opt_1" effect = { ... } }
      option = { name = "flavour_slug_1_opt_2" effect = { ... } }
  }
"""
import sys
import json
from pathlib import Path

EVENT_TEMPLATE = """namespace = {namespace}

{ns_prefix}.{id} = {{
    title = "{loc_prefix}{ns_prefix}_{id}_title"
    desc = "{loc_prefix}{ns_prefix}_{id}_desc"
    picture = "{picture}"
    is_triggered_only = {is_triggered_only}
    mean_time_to_happen = {{ months = {mttd_months} }}

    trigger = {{
        tag = {tag}
    }}

    immediate = {{
        {immediate}
    }}

    option = {{
        name = "{loc_prefix}{ns_prefix}_{id}_opt_1"
        effect = {{
            {effect}
        }}
    }}
}}
"""


def emit_event_file(spec: dict, output_path: Path):
    events = spec.get('content', {}).get('events', [])
    ns = spec['registries']['event_namespace']
    tag = spec['registries']['tag']
    loc_prefix = spec['registries'].get('loc_prefix', f"{tag.lower()}_")

    lines = [f"# Auto-generated from mod-spec — do not edit directly\n"]

    for e in events:
        eid = e.get('id', 1)
        picture = e.get('picture', 'event_art_storytelling')
        is_triggered_only = 'yes' if e.get('is_triggered_only', True) else 'no'
        mttd = e.get('mttd_months', 12)
        immediate = e.get('immediate', '')
        effect = e.get('effect', 'set_country_flag = done')

        block = EVENT_TEMPLATE.format(
            namespace=ns,
            ns_prefix=ns,
            id=eid,
            loc_prefix=loc_prefix,
            tag=tag,
            picture=picture,
            is_triggered_only=is_triggered_only,
            mttd_months=mttd,
            immediate=immediate,
            effect=effect
        )
        lines.append(block)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"emit_events: wrote {len(events)} events to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: emit_events.py <spec.validated.json> [output_path]")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())

    ns = spec['registries']['event_namespace']
    tag = spec['registries']['tag']
    default_output = Path(f"events/Flavour_{ns.title()}_{tag}.txt")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_output

    emit_event_file(spec, output_path)


if __name__ == '__main__':
    main()
