#!/usr/bin/env bash
set -euo pipefail

# Verne automation smoke checks
# Run from repo root: ./scripts/verne_smoke_checks.sh

echo "[1/9] Check helper definitions exist"
required_helpers=(
  "verne_overhaul_enable_adventure_network_tier_1"
  "verne_overhaul_apply_regatta_spire_swap"
  "verne_overhaul_laments_regatta_anchor_state_ready"
  "verne_overhaul_akasik_access_ready"
)
for helper in "${required_helpers[@]}"; do
  rg -n "$helper" \
    common/scripted_effects/verne_overhaul_effects.txt common/scripted_triggers/verne_overhaul_triggers.txt >/dev/null
done

echo "[2/9] Check live call sites use helpers"
rg -n "verne_overhaul_enable_adventure_network_tier_1" missions/Verne_Missions.txt >/dev/null
rg -n "verne_overhaul_apply_regatta_spire_swap" events/Flavour_Verne_A33.txt >/dev/null
rg -n "verne_overhaul_laments_regatta_anchor_state_ready" missions/Verne_Missions.txt >/dev/null
rg -n "verne_overhaul_akasik_access_ready" missions/Verne_Missions.txt >/dev/null

echo "[3/9] Check helper still sets Port-of-Adventure unlock flag"
rg -n "set_country_flag = verne_unlock_port_of_adventure_button" common/scripted_effects/verne_overhaul_effects.txt >/dev/null

echo "[4/9] Check monument anchor IDs still exist"
rg -n "^kazakesh\s*=|^aur_kes_akasik\s*=|^kazakesh_stingport\s*=" common/great_projects/*.txt >/dev/null

echo "[5/9] Ensure no stale inline duplicate logic remains in mission/event call sites"
if rg -n "destroy_great_project|add_great_project|set_country_flag = verne_unlock_port_of_adventure_button|name = \"verne_network_of_adventure_tier_1\"" missions/Verne_Missions.txt events/Flavour_Verne_A33.txt >/dev/null; then
  echo "ERROR: stale inline logic found in mission/event call sites (should be in helper files)."
  exit 1
fi

echo "[6/9] Ensure key Verne repo-map docs are indexed"
rg -n "verne-monument-object-id-parity-check-reference.md" docs/repo-maps/README.md docs/repo-maps/anbennar-systems-master-index.md docs/repo-maps/anbennar-systems-scan-roadmap.md >/dev/null
rg -n "verne-adventure-chain-mission-event-localization-parity-reference.md" docs/repo-maps/README.md docs/repo-maps/anbennar-systems-master-index.md docs/repo-maps/anbennar-systems-scan-roadmap.md >/dev/null
rg -n "verne-cross-nation-mission-interaction-watchlist.md" docs/repo-maps/README.md docs/repo-maps/anbennar-systems-master-index.md docs/repo-maps/anbennar-systems-scan-roadmap.md >/dev/null

echo "[7/9] Run checklist status audit"
./scripts/verne_checklist_audit.py

echo "[8/9] Run checklist markdown link audit"
./scripts/checklist_link_audit.py

echo "[9/9] Run docs conflict guard"
./scripts/docs_conflict_guard.py

echo "All Verne smoke checks passed."
