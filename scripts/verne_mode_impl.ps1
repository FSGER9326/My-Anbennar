$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Output "When to use this mode: implementation slices (script/event/loc edits) before commit/push."

Write-Output "[1/4] Run country smoke profile"
& (Join-Path $scriptDir "country_smoke_runner.ps1") -Profile "automation/country_profiles/verne.json"

Write-Output "[2/4] Run localisation audit"
& (Join-Path $scriptDir "localisation_audit.ps1") -File "localisation/Flavour_Verne_A33_l_english.yml"

Write-Output "[3/4] Run event ID audit"
& (Join-Path $scriptDir "event_id_audit.ps1") -File "events/Flavour_Verne_A33.txt"

Write-Output "[4/4] Run conflict guard"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")

Write-Output "Verne implementation mode checks passed."
