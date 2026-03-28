param(
    [Parameter(Mandatory = $true)][string]$Slug,
    [Parameter(Mandatory = $true)][string]$Tag,
    [switch]$WithSyncHelper
)

$ErrorActionPreference = "Stop"

if ($Slug -notmatch '^[a-z0-9][a-z0-9_-]*$') {
    throw "Country slug must match ^[a-z0-9][a-z0-9_-]*$"
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$base = Join-Path $repoRoot ("docs/theorycrafting/" + $Slug)
$profileDir = Join-Path $repoRoot "automation/country_profiles"
$profilePath = Join-Path $profileDir ("$Slug.json")

$smokeShPath = Join-Path $repoRoot ("scripts/smoke_$Slug.sh")
$smokePs1Path = Join-Path $repoRoot ("scripts/smoke_$Slug.ps1")
$syncShPath = Join-Path $repoRoot ("scripts/sync_${Slug}_with_main.sh")
$syncPs1Path = Join-Path $repoRoot ("scripts/sync_${Slug}_with_main.ps1")

function Get-DisplayName {
    param([Parameter(Mandatory = $true)][string]$Value)
    $textInfo = (Get-Culture).TextInfo
    return $textInfo.ToTitleCase(($Value -replace '[-_]', ' '))
}

function Get-FileStem {
    param([Parameter(Mandatory = $true)][string]$Value)
    $parts = $Value -split '[-_]' | Where-Object { $_ -ne '' }
    return (($parts | ForEach-Object {
        if ($_.Length -eq 1) { $_.ToUpper() } else { $_.Substring(0, 1).ToUpper() + $_.Substring(1) }
    }) -join '')
}

$displayName = Get-DisplayName -Value $Slug
$fileStem = Get-FileStem -Value $Slug
New-Item -ItemType Directory -Force -Path $base | Out-Null
New-Item -ItemType Directory -Force -Path $profileDir | Out-Null

$planTemplate = Join-Path $repoRoot "docs/theorycrafting/_templates/country-overhaul-plan-template.md"
$dossierTemplate = Join-Path $repoRoot "docs/theorycrafting/_templates/country-dossier-template.md"
$manifestTemplate = Join-Path $repoRoot "docs/theorycrafting/_templates/country-checklist-status-manifest-template.json"

Copy-Item $planTemplate (Join-Path $base "country-overhaul-plan.md") -Force
Copy-Item $dossierTemplate (Join-Path $base "country-dossier.md") -Force
Copy-Item $manifestTemplate (Join-Path $base "checklist-status-manifest.json") -Force

$planPath = Join-Path $base "country-overhaul-plan.md"
$dossierPath = Join-Path $base "country-dossier.md"
$manifestPath = Join-Path $base "checklist-status-manifest.json"

$planText = Get-Content $planPath -Raw -Encoding UTF8
$planText = $planText.Replace("<Country Name>", $displayName)
[System.IO.File]::WriteAllText($planPath, $planText, [System.Text.UTF8Encoding]::new($false))

$dossierText = Get-Content $dossierPath -Raw -Encoding UTF8
$dossierText = $dossierText.Replace("<Country Name>", $displayName)
[System.IO.File]::WriteAllText($dossierPath, $dossierText, [System.Text.UTF8Encoding]::new($false))

$manifestText = Get-Content $manifestPath -Raw -Encoding UTF8
$manifestText = $manifestText.Replace("<country>", $Slug)
[System.IO.File]::WriteAllText($manifestPath, $manifestText, [System.Text.UTF8Encoding]::new($false))

$profileJson = @"
{
  "name": "$Slug",
  "require_patterns": [
    {
      "description": "country mission file exists with TODO mission placeholder",
      "pattern": "TODO_${Slug}_MISSION",
      "paths": ["missions/$fileStem`_Missions.txt"]
    },
    {
      "description": "country event file exists with TODO event placeholder",
      "pattern": "TODO_${Slug}_EVENT",
      "paths": ["events/Flavour_$fileStem.txt"]
    },
    {
      "description": "country localisation file exists with TODO loc placeholder",
      "pattern": "TODO_${Slug}_LOC",
      "paths": ["localisation/Flavour_${fileStem}_l_english.yml"]
    }
  ],
  "require_all_patterns": [
    {
      "description": "starter placeholders remain visible while scaffolding",
      "patterns": [
        "TODO_${Slug}_MISSION",
        "TODO_${Slug}_EVENT",
        "TODO_${Slug}_LOC"
      ],
      "paths": [
        "missions/$fileStem`_Missions.txt",
        "events/Flavour_$fileStem.txt",
        "localisation/Flavour_${fileStem}_l_english.yml"
      ]
    }
  ],
  "forbid_patterns": [
    {
      "description": "no unresolved merge markers in country files",
      "pattern": "<<<<<<<|=======|>>>>>>>",
      "paths": [
        "missions/$fileStem`_Missions.txt",
        "events/Flavour_$fileStem.txt",
        "localisation/Flavour_${fileStem}_l_english.yml"
      ]
    }
  ]
}
"@
[System.IO.File]::WriteAllText($profilePath, $profileJson, [System.Text.UTF8Encoding]::new($false))

$smokeSh = @"
#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="`${PYTHON_BIN:-python3}"

if ! command -v "`${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "Run $Slug smoke profile"
"`${PYTHON_BIN}" scripts/country_smoke_runner.py --profile automation/country_profiles/$Slug.json

echo "$displayName smoke checks passed."
"@
[System.IO.File]::WriteAllText($smokeShPath, $smokeSh, [System.Text.UTF8Encoding]::new($false))

$smokePs1 = @"
`$ErrorActionPreference = "Stop"

`$scriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path

Write-Output "Run $Slug smoke profile"
& (Join-Path `$scriptDir "country_smoke_runner.ps1") -Profile "automation/country_profiles/$Slug.json"

Write-Output "$displayName smoke checks passed."
"@
[System.IO.File]::WriteAllText($smokePs1Path, $smokePs1, [System.Text.UTF8Encoding]::new($false))

if ($WithSyncHelper.IsPresent) {
    $syncSh = @"
#!/usr/bin/env bash
set -euo pipefail

BASE_REF="`${1:-origin/main}"

bash scripts/auto_sync_pr_with_main.sh "`${BASE_REF}"
bash scripts/smoke_$Slug.sh
"@
    [System.IO.File]::WriteAllText($syncShPath, $syncSh, [System.Text.UTF8Encoding]::new($false))

    $syncPs1 = @"
param(
    [string]`$BaseRef = "origin/main"
)

`$ErrorActionPreference = "Stop"
`$scriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path

& (Join-Path `$scriptDir "auto_sync_pr_with_main.ps1") -BaseRef `$BaseRef
& (Join-Path `$scriptDir "smoke_$Slug.ps1")
"@
    [System.IO.File]::WriteAllText($syncPs1Path, $syncPs1, [System.Text.UTF8Encoding]::new($false))
}

$readmeLines = @(
    "# $displayName Theorycrafting",
    "",
    "Tag: $Tag",
    "",
    "Start here:",
    "- country-overhaul-plan.md",
    "- country-dossier.md",
    "- checklist-status-manifest.json",
    "- ../../../automation/country_profiles/$Slug.json",
    "",
    "## One command to validate this country",
    "",
    "- Bash: ``bash scripts/smoke_$Slug.sh``",
    "- PowerShell: ``powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\smoke_$Slug.ps1``",
    "",
    "Run generic audit once repo-map files exist:",
    "- PowerShell: ``powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\checklist_manifest_audit.ps1 -Manifest docs/theorycrafting/$Slug/checklist-status-manifest.json``",
    "- Python: ``python scripts/checklist_manifest_audit.py --manifest docs/theorycrafting/$Slug/checklist-status-manifest.json``",
    "- Python override example: ``python scripts/checklist_manifest_audit.py --manifest docs/theorycrafting/$Slug/checklist-status-manifest.json --index-file docs/repo-maps/README.md``"
)

if ($WithSyncHelper.IsPresent) {
    $readmeLines += @(
        "",
        "## Optional sync helper alias",
        "",
        "Use the country-scoped sync helper to merge ``origin/main`` into your branch and immediately rerun the $Slug smoke profile:",
        "",
        "- Bash: ``bash scripts/sync_${Slug}_with_main.sh``",
        "- PowerShell: ``powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync_${Slug}_with_main.ps1``"
    )
}

[System.IO.File]::WriteAllText((Join-Path $base "README.md"), ($readmeLines -join "`n"), [System.Text.UTF8Encoding]::new($false))

Write-Output "Created scaffold at docs/theorycrafting/$Slug"
Write-Output "Created smoke profile at automation/country_profiles/$Slug.json"
Write-Output "Created smoke wrappers: scripts/smoke_$Slug.sh, scripts/smoke_$Slug.ps1"
if ($WithSyncHelper.IsPresent) {
    Write-Output "Created sync helpers: scripts/sync_${Slug}_with_main.sh, scripts/sync_${Slug}_with_main.ps1"
}
