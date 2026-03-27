# Anbennar Base vs Verne Change Ledger

Purpose: one wiki-style table to track what your mod changes, how it is implemented, and how risky each part is during upstream updates.

## Status key

- `PLANNED`: design exists, not yet implemented
- `IMPLEMENTED`: implemented and tested at least once
- `NEEDS_REVALIDATION`: likely impacted by upstream update
- `BROKEN`: known issue after update

## Change ledger template

| System | Base Anbennar behavior | Verne behavior (your mod) | Main files touched | Pattern used | Update risk | Status | Last checked | Notes |
|---|---|---|---|---|---|---|---|---|
| Example: Verne dynasty correction | In base, Verne dynasty/heir behavior from flavor events | Add stricter dynasty-preservation helpers and fallback correction | `events/Flavour_Verne_A33.txt`; `common/on_actions/00_on_actions.txt`; `events/verne_overhaul_dynasty_events.txt` | Mirror `define_heir` + `on_new_heir` pattern | High | PLANNED | 2026-03-27 | Replace this example row with real implementation row when coded |

## Per-change detail section (copy/paste for each real implementation)

### Change ID: `VERNE-XXXX`

- **System area:**
- **Why we changed it:**
- **Base anchors reviewed:**
- **Implementation files:**
- **Mechanic flow summary:**
- **Compatibility risks with upstream:**
- **How to test quickly:**
- **Rollback plan:**
- **Owner + date:**

---

## Minimum rule before merge

For any non-trivial mechanic commit, add or update at least one ledger row.
