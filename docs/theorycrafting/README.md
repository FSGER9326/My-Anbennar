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

## New country in 5 minutes (noob workflow)

1. **Scaffold everything** (docs + smoke profile + one-command wrappers):
   - Bash: `./scripts/new_country_scaffold.sh mycountry MYC --with-sync-helper`
   - PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new_country_scaffold.ps1 -Slug mycountry -Tag MYC -WithSyncHelper`
2. **Open `docs/theorycrafting/mycountry/README.md`** and run the “One command to validate this country” command.
3. **Create placeholder files** the profile expects:
   - `missions/Mycountry_Missions.txt` with `TODO_mycountry_MISSION`
   - `events/Flavour_Mycountry.txt` with `TODO_mycountry_EVENT`
   - `localisation/Flavour_Mycountry_l_english.yml` with `TODO_mycountry_LOC`
4. **Run smoke checks** and confirm they pass:
   - Bash: `bash scripts/smoke_mycountry.sh`
   - PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\smoke_mycountry.ps1`
5. **Start replacing TODO markers with real content** as you implement missions/events/localisation.
