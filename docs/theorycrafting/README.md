# Theorycrafting Workspace (Generalized)

This folder is the reusable planning layer for **any country**, not just Verne.

## Structure

- `_templates/`:
  - reusable plan/checklist templates
- `verne/`:
  - Verne-specific theorycrafting entrypoint (current active overhaul)
- `<country-slug>/`:
  - future country-specific planning folders (Lorent, etc.)

## Workflow (fast path)

1. Create country scaffold with `./scripts/new_country_scaffold.sh <country-slug> <TAG>`.
2. Fill `country-overhaul-plan.md` from template.
3. Fill `checklist-status-manifest.json` flags (`scanned/mapped/verified`).
4. Add repo-maps/checklists as needed.
5. Run automation checks before implementation.
