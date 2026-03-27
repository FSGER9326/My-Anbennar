#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <country-slug> <TAG>"
  exit 1
fi

slug="$1"
tag="$2"
base="docs/theorycrafting/${slug}"
profile="automation/country_profiles/${slug}.json"
profile_dir="automation/country_profiles"
mkdir -p "$base"
mkdir -p "$profile_dir"

cp docs/theorycrafting/_templates/country-overhaul-plan-template.md "$base/country-overhaul-plan.md"
cp docs/theorycrafting/_templates/country-checklist-status-manifest-template.json "$base/checklist-status-manifest.json"
cp automation/country_profiles/_templates/country-smoke-profile-template.json "$profile"

# lightweight placeholder replacement
sed -i "s/<Country Name>/${slug^}/g" "$base/country-overhaul-plan.md"
sed -i "s/<country>/${slug}/g" "$base/checklist-status-manifest.json"

country_plan_path="docs/theorycrafting/${slug}/country-overhaul-plan.md"
country_manifest_path="docs/theorycrafting/${slug}/checklist-status-manifest.json"
country_readme_path="docs/theorycrafting/${slug}/README.md"

escape_sed_replacement() {
  sed -e 's/[&|]/\\&/g' <<<"$1"
}

slug_escaped="$(escape_sed_replacement "$slug")"
tag_escaped="$(escape_sed_replacement "$tag")"
country_plan_path_escaped="$(escape_sed_replacement "$country_plan_path")"
country_manifest_path_escaped="$(escape_sed_replacement "$country_manifest_path")"
country_readme_path_escaped="$(escape_sed_replacement "$country_readme_path")"

sed -i "s|<country>|${slug_escaped}|g" "$profile"
sed -i "s|<TAG>|${tag_escaped}|g" "$profile"
sed -i "s|<country_plan_path>|${country_plan_path_escaped}|g" "$profile"
sed -i "s|<country_manifest_path>|${country_manifest_path_escaped}|g" "$profile"
sed -i "s|<country_readme_path>|${country_readme_path_escaped}|g" "$profile"

cat > "$base/README.md" <<EOT
# ${slug^} Theorycrafting

Tag: ${tag}

Start here:
- country-overhaul-plan.md
- checklist-status-manifest.json
- automation smoke profile: ${profile}

Run automation checks:
- python scripts/country_smoke_runner.py --profile automation/country_profiles/${slug}.json
- python scripts/checklist_manifest_audit.py --manifest docs/theorycrafting/${slug}/checklist-status-manifest.json ...
- Optional override example: python scripts/checklist_manifest_audit.py --manifest docs/theorycrafting/${slug}/checklist-status-manifest.json --index-file docs/repo-maps/README.md
EOT

echo "Created scaffold at $base"
echo "Created smoke profile at $profile"
