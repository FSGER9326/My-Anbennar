$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot
$validationReport = if ($env:VALIDATION_REPORT) { $env:VALIDATION_REPORT } else { "automation/reports/validation_report.json" }
$prDraftOutput = if ($env:PR_DRAFT_OUTPUT) { $env:PR_DRAFT_OUTPUT } else { "automation/pr/PR_DRAFT.md" }
New-Item -ItemType Directory -Path (Split-Path -Parent $validationReport) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $prDraftOutput) -Force | Out-Null

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

Invoke-GateStep -Label "[1/5] Docs conflict guard" -Command "python" -Arguments @("scripts/docs_conflict_guard.py")
Invoke-GateStep -Label "[2/5] Checklist link audit" -Command "python" -Arguments @("scripts/checklist_link_audit.py")
Invoke-GateStep -Label "[3/5] Verne checklist audit" -Command "python" -Arguments @("scripts/verne_checklist_audit.py")
Invoke-GateStep -Label "[4/5] Verne country smoke runner" -Command "python" -Arguments @("scripts/country_smoke_runner.py", "--profile", "automation/country_profiles/verne.json")

$payload = [ordered]@{
    generated_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    overall_status = "pass"
    checks = @(
        @{ name = "docs_conflict_guard"; command = "python scripts/docs_conflict_guard.py"; status = "pass"; severity = "high" },
        @{ name = "checklist_link_audit"; command = "python scripts/checklist_link_audit.py"; status = "pass"; severity = "high" },
        @{ name = "verne_checklist_audit"; command = "python scripts/verne_checklist_audit.py"; status = "pass"; severity = "high" },
        @{ name = "country_smoke_runner"; command = "python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json"; status = "pass"; severity = "high" }
    )
    unresolved_issues = @()
    artifacts = @(
        @{ name = "validation-report"; path = $validationReport },
        @{ name = "pr-draft"; path = $prDraftOutput }
    )
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $validationReport -Encoding UTF8

Invoke-GateStep -Label "[5/5] Generate PR draft" -Command "python" -Arguments @("scripts/pr_prep.py", "--validation-report", $validationReport, "--output", $prDraftOutput)

Write-Output "Pre-PR gate passed. Safe to open a PR."
Write-Output "Generated artifacts:"
Write-Output "- Validation report: $validationReport"
Write-Output "- PR draft: $prDraftOutput"
