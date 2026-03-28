$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

function Invoke-GateStep {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label,
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    Write-Output $Label
    try {
        & $Command @Arguments
    }
    catch {
        Write-Output ""
        Write-Output "Pre-PR gate failed."
        Write-Output ("Next command: {0} {1}" -f $Command, ($Arguments -join " "))
        Write-Output "Fix the issue shown above, then re-run: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1"
        exit 1
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Output ""
        Write-Output "Pre-PR gate failed."
        Write-Output ("Next command: {0} {1}" -f $Command, ($Arguments -join " "))
        Write-Output "Fix the issue shown above, then re-run: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1"
        exit 1
    }
}

Invoke-GateStep -Label "[1/4] Docs conflict guard" -Command "python" -Arguments @("scripts/docs_conflict_guard.py")
Invoke-GateStep -Label "[2/4] Checklist link audit" -Command "python" -Arguments @("scripts/checklist_link_audit.py")
Invoke-GateStep -Label "[3/4] Verne checklist audit" -Command "python" -Arguments @("scripts/verne_checklist_audit.py")
Invoke-GateStep -Label "[4/4] Verne country smoke runner" -Command "python" -Arguments @("scripts/country_smoke_runner.py", "--profile", "automation/country_profiles/verne.json")

Write-Output "Pre-PR gate passed. Safe to open a PR."
