$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

if (-not (Test-Path ".githooks/pre-commit") -or -not (Test-Path ".githooks/pre-push")) {
    throw "Missing .githooks hook files."
}

git config core.hooksPath .githooks
Write-Output "Installed repo hooks via core.hooksPath=.githooks"
Write-Output "Active hooks:"
Write-Output " - .githooks/pre-commit"
Write-Output " - .githooks/pre-push"
