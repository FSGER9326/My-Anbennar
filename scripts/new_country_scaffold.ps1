param(
    [Parameter(Mandatory = $true)][string]$Slug,
    [Parameter(Mandatory = $true)][string]$Tag
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$base = Join-Path $repoRoot ("docs/theorycrafting/" + $Slug)

function Get-DisplayName {
    param([Parameter(Mandatory = $true)][string]$Value)
    $textInfo = (Get-Culture).TextInfo
    return $textInfo.ToTitleCase(($Value -replace '[-_]', ' '))
}

$displayName = Get-DisplayName -Value $Slug
New-Item -ItemType Directory -Force -Path $base | Out-Null

$planTemplate = Join-Path $repoRoot "docs/theorycrafting/_templates/country-overhaul-plan-template.md"
$manifestTemplate = Join-Path $repoRoot "docs/theorycrafting/_templates/country-checklist-status-manifest-template.json"

Copy-Item $planTemplate (Join-Path $base "country-overhaul-plan.md") -Force
Copy-Item $manifestTemplate (Join-Path $base "checklist-status-manifest.json") -Force

$planPath = Join-Path $base "country-overhaul-plan.md"
$manifestPath = Join-Path $base "checklist-status-manifest.json"

$planText = Get-Content $planPath -Raw -Encoding UTF8
$planText = $planText.Replace("<Country Name>", $displayName)
[System.IO.File]::WriteAllText($planPath, $planText, [System.Text.UTF8Encoding]::new($false))

$manifestText = Get-Content $manifestPath -Raw -Encoding UTF8
$manifestText = $manifestText.Replace("<country>", $Slug)
[System.IO.File]::WriteAllText($manifestPath, $manifestText, [System.Text.UTF8Encoding]::new($false))

$readme = @(
    "# $displayName Theorycrafting",
    "",
    "Tag: $Tag",
    "",
    "Start here:",
    "- country-overhaul-plan.md",
    "- checklist-status-manifest.json",
    "",
    "Run generic audit once repo-map files exist:",
    "- PowerShell: ``powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\checklist_manifest_audit.ps1 -Manifest docs/theorycrafting/$Slug/checklist-status-manifest.json``",
    "- Python: ``python scripts/checklist_manifest_audit.py --manifest docs/theorycrafting/$Slug/checklist-status-manifest.json``",
    "- Python override example: ``python scripts/checklist_manifest_audit.py --manifest docs/theorycrafting/$Slug/checklist-status-manifest.json --index-file docs/repo-maps/README.md``",
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $base "README.md"), $readme, [System.Text.UTF8Encoding]::new($false))
Write-Output "Created scaffold at docs/theorycrafting/$Slug"
