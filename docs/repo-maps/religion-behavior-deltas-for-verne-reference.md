# Religion Behavior Deltas for Verne (Base EU4 vs Anbennar)

## Quick verdict

Verne religion behavior is not just vanilla conversion logic; Anbennar religion files and Verne flavor events include custom flows for Corinite and related paths.

## Core anchors

- `common/religions/00_anb_religion.txt`
- `common/religions/00_religion.txt` (baseline comparison)
- `events/Flavour_Verne_A33.txt`

Representative Verne-relevant anchors:

- Corinite and Regent Court linkage in `00_anb_religion.txt`
- custom center-of-reformation handling for Corinite (`add_reform_center = corinite` branches)
- Verne event flow in `Flavour_Verne_A33.txt` using `change_religion = corinite` and reform-center setup

## Delta from vanilla-style baseline

- stronger custom religion scripting and branching
- non-trivial reform-center and conversion chain handling
- event-driven religion progression tied to nation content

## Verne adaptation note

For pressure/disaster/religion design, reuse existing Corinite/Regent Court flow where possible before inventing independent conversion frameworks.

## Upstream risk

High risk in religion/event interplay:

- religion object behavior in `00_anb_religion.txt`
- Verne event IDs and scripted religion conversion paths in `events/Flavour_Verne_A33.txt`


## Object-ID appendix (first pass)

Representative religion/event IDs to monitor:

- religion objects: `regent_court`, `corinite`
- reform-center actions: `add_reform_center = corinite`
- Verne flavor event file: `events/Flavour_Verne_A33.txt`
