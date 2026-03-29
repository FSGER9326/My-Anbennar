# Start Here

> [!IMPORTANT]
> **One-command path (default):**
> `bash scripts/noob_autopilot.sh`

This page is intentionally minimal: run the default command, then escalate only if the command tells you to.

## What should we do right now? (Decision guide)

1. Run `bash scripts/noob_autopilot.sh`.
2. If it passes, proceed with your normal push/PR flow.
3. If it reports conflicts, overlap risk, or failing checks, use the escalation links below.

## Tiny glossary (modding terms, not GitHub terms)

- **Hotspot file:** a frequently edited file where parallel edits are likely to conflict.
- **Single-writer file:** a file designated to one lane/author at a time to prevent merge churn.
- **Smoke checks:** fast structural checks that catch broken links, keys, or references early.

## Escalation links only

- Command reference and operational index:
  [docs/wiki/checklist-automation-system.md](./wiki/checklist-automation-system.md)
- Conflict decisions and mitigation flow:
  [docs/wiki/merge-conflict-prevention-playbook.md](./wiki/merge-conflict-prevention-playbook.md)
- Verne canonical file ownership truth:
  [docs/wiki/verne-canonical-vs-legacy-file-registry.md](./wiki/verne-canonical-vs-legacy-file-registry.md)
- Parallel lane model for safe multi-tasking:
  [docs/wiki/parallelization-lanes-playbook.md](./wiki/parallelization-lanes-playbook.md)
- Full docs hub:
  [docs/README.md](./README.md)
