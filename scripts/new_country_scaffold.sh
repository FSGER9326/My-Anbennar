#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 <country-slug> <TAG> [--with-sync-helper]

Creates:
  - docs/theorycrafting/<country-slug>/...
  - automation/country_profiles/<country-slug>.json
  - scripts/smoke_<country-slug>.sh
  - scripts/smoke_<country-slug>.ps1

Optional:
  --with-sync-helper   also create scripts/sync_<country-slug>_with_main.sh/.ps1
USAGE
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

slug="$1"
tag="$2"
with_sync_helper="false"
file_stem="$(echo "$slug" | sed -E 's/(^|[-_])([a-z0-9])/\U\2/g')"

if [[ $# -ge 3 ]]; then
  case "$3" in
    --with-sync-helper) with_sync_helper="true" ;;
    *)
      echo "Unknown option: $3"
      usage
      exit 1
      ;;
  esac
fi

if [[ ! "$slug" =~ ^[a-z0-9][a-z0-9_-]*$ ]]; then
  echo "Error: country-slug must match ^[a-z0-9][a-z0-9_-]*$"
  exit 1
fi

base="docs/theorycrafting/${slug}"
profile_dir="automation/country_profiles"
profile_path="${profile_dir}/${slug}.json"
smoke_sh="scripts/smoke_${slug}.sh"
smoke_ps1="scripts/smoke_${slug}.ps1"
sync_sh="scripts/sync_${slug}_with_main.sh"
sync_ps1="scripts/sync_${slug}_with_main.ps1"

mkdir -p "$base" "$profile_dir"

cp docs/theorycrafting/_templates/country-overhaul-plan-template.md "$base/country-overhaul-plan.md"
cp docs/theorycrafting/_templates/country-checklist-status-manifest-template.json "$base/checklist-status-manifest.json"

# lightweight placeholder replacement
sed -i "s/<Country Name>/${slug^}/g" "$base/country-overhaul-plan.md"
sed -i "s/<country>/${slug}/g" "$base/checklist-status-manifest.json"

cat > "$profile_path" <<EOT
{
  "name": "${slug}",
  "require_patterns": [
    {
      "description": "country mission file exists with TODO mission placeholder",
      "pattern": "TODO_${slug}_MISSION",
      "paths": ["missions/${file_stem}_Missions.txt"]
    },
    {
      "description": "country event file exists with TODO event placeholder",
      "pattern": "TODO_${slug}_EVENT",
      "paths": ["events/Flavour_${file_stem}.txt"]
    },
    {
      "description": "country localisation file exists with TODO loc placeholder",
      "pattern": "TODO_${slug}_LOC",
      "paths": ["localisation/Flavour_${file_stem}_l_english.yml"]
    }
  ],
  "require_all_patterns": [
    {
      "description": "starter placeholders remain visible while scaffolding",
      "patterns": [
        "TODO_${slug}_MISSION",
        "TODO_${slug}_EVENT",
        "TODO_${slug}_LOC"
      ],
      "paths": [
        "missions/${file_stem}_Missions.txt",
        "events/Flavour_${file_stem}.txt",
        "localisation/Flavour_${file_stem}_l_english.yml"
      ]
    }
  ],
  "forbid_patterns": [
    {
      "description": "no unresolved merge markers in country files",
      "pattern": "<<<<<<<|=======|>>>>>>>",
      "paths": [
        "missions/${file_stem}_Missions.txt",
        "events/Flavour_${file_stem}.txt",
        "localisation/Flavour_${file_stem}_l_english.yml"
      ]
    }
  ]
}
EOT

cat > "$smoke_sh" <<EOT
#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="\${PYTHON_BIN:-python3}"

if ! command -v "\${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "Run ${slug} smoke profile"
"\${PYTHON_BIN}" scripts/country_smoke_runner.py --profile automation/country_profiles/${slug}.json

echo "${slug^} smoke checks passed."
EOT

cat > "$smoke_ps1" <<EOT
\$ErrorActionPreference = "Stop"

\$scriptDir = Split-Path -Parent \$MyInvocation.MyCommand.Path

Write-Output "Run ${slug} smoke profile"
& (Join-Path \$scriptDir "country_smoke_runner.ps1") -Profile "automation/country_profiles/${slug}.json"

Write-Output "${slug^} smoke checks passed."
EOT

chmod +x "$smoke_sh"

if [[ "$with_sync_helper" == "true" ]]; then
  cat > "$sync_sh" <<EOT
#!/usr/bin/env bash
set -euo pipefail

BASE_REF="\${1:-origin/main}"

bash scripts/auto_sync_pr_with_main.sh "\${BASE_REF}"
bash scripts/smoke_${slug}.sh
EOT

  cat > "$sync_ps1" <<EOT
param(
    [string]\$BaseRef = "origin/main"
)

\$ErrorActionPreference = "Stop"
\$scriptDir = Split-Path -Parent \$MyInvocation.MyCommand.Path

& (Join-Path \$scriptDir "auto_sync_pr_with_main.ps1") -BaseRef \$BaseRef
& (Join-Path \$scriptDir "smoke_${slug}.ps1")
EOT

  chmod +x "$sync_sh"
fi

cat > "$base/README.md" <<EOT
# ${slug^} Theorycrafting

Tag: ${tag}

Start here:
- country-overhaul-plan.md
- checklist-status-manifest.json
- ../../../automation/country_profiles/${slug}.json

## One command to validate this country

- Bash: \`bash scripts/smoke_${slug}.sh\`
- PowerShell: \`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\smoke_${slug}.ps1\`

Run generic audit once repo-map files exist:
- Python: \`python scripts/checklist_manifest_audit.py --manifest $base/checklist-status-manifest.json\`
- Python 3 fallback: \`python3 scripts/checklist_manifest_audit.py --manifest $base/checklist-status-manifest.json\`
- Python override example: \`python scripts/checklist_manifest_audit.py --manifest $base/checklist-status-manifest.json --index-file docs/repo-maps/README.md\`
EOT

if [[ "$with_sync_helper" == "true" ]]; then
  cat >> "$base/README.md" <<EOT

## Optional sync helper alias

Use the country-scoped sync helper to merge \`origin/main\` into your branch and immediately rerun the ${slug} smoke profile:

- Bash: \`bash scripts/sync_${slug}_with_main.sh\`
- PowerShell: \`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync_${slug}_with_main.ps1\`
EOT
fi

echo "Created scaffold at $base"
echo "Created smoke profile at $profile_path"
echo "Created smoke wrappers: $smoke_sh, $smoke_ps1"
if [[ "$with_sync_helper" == "true" ]]; then
  echo "Created sync helpers: $sync_sh, $sync_ps1"
fi
