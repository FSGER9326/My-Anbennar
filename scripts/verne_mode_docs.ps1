$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Output "When to use this mode: docs/checklist-only edits before commit/push."

Write-Output "[1/3] Run checklist manifest audit"
& (Join-Path $scriptDir "checklist_manifest_audit.ps1")

Write-Output "[2/3] Run markdown link audit"
& (Join-Path $scriptDir "checklist_link_audit.ps1")

Write-Output "[3/3] Run conflict guard"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")

Write-Output "Verne docs mode checks passed."
