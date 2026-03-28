$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

function Write-PostFailSummary {
    Write-Output "Quick triage summary (priority order):"

    $mergeConflicts = (& git diff --name-only --diff-filter=U 2>$null) -join "`n"
    if (-not [string]::IsNullOrWhiteSpace($mergeConflicts)) {
        Write-Output "1) merge conflicts -> git diff --name-only --diff-filter=U ; Why first: unresolved merges can invalidate every later check."
    }

    & python "scripts/docs_conflict_guard.py" *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Output "2) conflict markers -> python scripts/docs_conflict_guard.py ; Why first: marker leftovers break parsing and hide real logic errors."
    }

    & powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\verne_smoke_checks.ps1" *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Output "3) syntax/structure checks -> powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1 ; Why first: structural failures must clear before deeper content audits."
    }

    & python "scripts/localisation_audit.py" *> $null
    $locExit = $LASTEXITCODE
    & python "scripts/event_id_audit.py" *> $null
    $eventExit = $LASTEXITCODE
    if ($locExit -ne 0) {
        Write-Output "4) localisation/event ID checks -> python scripts/localisation_audit.py ; Why first: broken localisation keys block text integrity checks before ID cleanup."
    }
    elseif ($eventExit -ne 0) {
        Write-Output "4) localisation/event ID checks -> python scripts/event_id_audit.py ; Why first: duplicate/missing event IDs can break runtime event flow even after syntax passes."
    }
}

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
        Write-PostFailSummary
        Write-Output ("Next command: {0} {1}" -f $Command, ($Arguments -join " "))
        Write-Output "Fix the issue shown above, then re-run: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1"
        exit 1
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Output ""
        Write-Output "Pre-PR gate failed."
        Write-PostFailSummary
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
