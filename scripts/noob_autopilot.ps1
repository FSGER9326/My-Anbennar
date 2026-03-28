$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Output "[0/2] Run noob doctor preflight"
& (Join-Path $scriptDir "noob_doctor.ps1")

Write-Output "[1/2] Run automation smoke checks"
& (Join-Path $scriptDir "verne_smoke_checks.ps1")
