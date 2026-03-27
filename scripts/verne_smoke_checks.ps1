$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Output "[1/6] Run Verne smoke profile"
& (Join-Path $scriptDir "country_smoke_runner.ps1") -Profile "automation/country_profiles/verne.json"

Write-Output "[2/6] Run checklist status audit"
& (Join-Path $scriptDir "verne_checklist_audit.ps1")

Write-Output "[3/6] Run checklist markdown link audit"
& (Join-Path $scriptDir "checklist_link_audit.ps1")

Write-Output "[4/6] Run docs + automation conflict guard"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")

Write-Output "[5/6] Run Verne localisation audit"
& (Join-Path $scriptDir "localisation_audit.ps1") -File "localisation/Flavour_Verne_A33_l_english.yml"

Write-Output "[6/6] Run Verne event ID audit"
& (Join-Path $scriptDir "event_id_audit.ps1") -File "events/Flavour_Verne_A33.txt"

Write-Output "All Verne smoke checks passed."
