# Peace Treaty Layer (Base EU4 vs Anbennar)

## Quick verdict

Anbennar uses an extensive peace-treaty extension layer with many custom peace options for regional, racial, religious, and narrative systems.

## Core anchors

- `common/peace_treaties/*.txt`

Representative custom files:

- `common/peace_treaties/anb_tributary.txt`
- `common/peace_treaties/anb_verne_faith.txt`
- `common/peace_treaties/anb_corinsfield_ban_mages.txt`
- `common/peace_treaties/anb_expand_raj.txt`
- `common/peace_treaties/anb_remove_evil_ruler.txt`

## Delta from vanilla-style baseline

- many additional peace options with custom triggers/effects
- broader system coupling (religion, race, regional mission arcs, narrative wars)
- special-case peace effects not represented in simple vanilla-only peace expectations

## Verne adaptation note

Prefer reusing existing custom peace patterns where possible; do not assume all goals should become mission rewards or events if a peace option already exists.

## Upstream risk

High risk in `common/peace_treaties` due broad shared usage.


## Object-ID appendix (first pass)

Representative peace option IDs/files to monitor:

- `anb_tributary.txt`
- `anb_verne_faith.txt`
- `anb_corinsfield_ban_mages.txt`
- `anb_expand_raj.txt`
- `anb_remove_evil_ruler.txt`
