$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Output "[1/4] Run Verne smoke profile"
& (Join-Path $scriptDir "country_smoke_runner.ps1") -Profile "automation/country_profiles/verne.json"

Write-Output "[2/4] Run checklist status audit"
& (Join-Path $scriptDir "verne_checklist_audit.ps1")

Write-Output "[3/4] Run checklist markdown link audit"
& (Join-Path $scriptDir "checklist_link_audit.ps1")

Write-Output "[4/4] Run docs + automation conflict guard"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")

Write-Output "All Verne smoke checks passed."
