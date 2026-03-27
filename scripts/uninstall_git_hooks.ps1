$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

$current = git config --get core.hooksPath 2>$null
if ($LASTEXITCODE -eq 0 -and $current -eq ".githooks") {
    git config --unset core.hooksPath
    Write-Output "Removed repo hooksPath (.githooks)."
    Write-Output "Manual fallback:"
    Write-Output " - powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\smart_smoke_router.ps1"
    Write-Output " - powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verne_smoke_checks.ps1"
    exit 0
}

Write-Output "No repo hooksPath override was set."
