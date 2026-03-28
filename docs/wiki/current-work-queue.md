# Current Work Queue

Rule: no new task can enter **Now** until the current **Now** item is committed.

## Now (max 1 item)

| Task | Target files | Done condition | Validation command |
|---|---|---|---|
| Keep this queue and session entry docs aligned | `README.md`, `docs/README.md`, `docs/start-here.md`, `docs/wiki/current-work-queue.md` | All queue links resolve and start-here requires choosing from Now before coding | `python scripts/checklist_link_audit.py` |

## Next (max 3 items)

| Task | Target files | Done condition | Validation command |
|---|---|---|---|
| Add one tiny v0.1 gameplay slice from queue | `common/*`, `events/*`, `missions/*`, `localisation/*` | One small slice ships with matching localization and no ID/key breakage | `bash scripts/verne_smoke_checks.sh` |
| Update ledgers for the completed slice | `docs/wiki/anbennar-base-vs-verne-change-ledger.md`, `docs/wiki/verne-id-ledger.md` | New/changed IDs and behavior deltas are documented in both ledgers | `python scripts/verne_checklist_audit.py` |
| Run pre-PR safety checks and document outcomes | `scripts/*`, `docs/*` | Pre-PR gate runs clean (or failures are documented with follow-up task) | `bash scripts/pre_pr_gate.sh` |

## Parked

| Task | Target files | Done condition | Validation command |
|---|---|---|---|
| Expand long-horizon design ideas after core stabilization | `docs/design/*` | Design notes are converted into implementation constraints and moved to Next | `python scripts/checklist_link_audit.py` |
