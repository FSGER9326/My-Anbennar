#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <country-slug> <TAG>"
  exit 1
fi

slug="$1"
tag="$2"
base="docs/theorycrafting/${slug}"
mkdir -p "$base"

cp docs/theorycrafting/_templates/country-overhaul-plan-template.md "$base/country-overhaul-plan.md"
cp docs/theorycrafting/_templates/country-checklist-status-manifest-template.json "$base/checklist-status-manifest.json"

# lightweight placeholder replacement
sed -i "s/<Country Name>/${slug^}/g" "$base/country-overhaul-plan.md"
sed -i "s/<country>/${slug}/g" "$base/checklist-status-manifest.json"

cat > "$base/README.md" <<EOT
# ${slug^} Theorycrafting

Tag: ${tag}

Start here:
- country-overhaul-plan.md
- checklist-status-manifest.json

Run generic audit once repo-map files exist:
- ./scripts/checklist_manifest_audit.py --manifest $base/checklist-status-manifest.json
- Optional override example: ./scripts/checklist_manifest_audit.py --manifest $base/checklist-status-manifest.json --index-file docs/repo-maps/README.md
EOT

echo "Created scaffold at $base"
