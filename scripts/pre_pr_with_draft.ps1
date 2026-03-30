$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

$validationReport = if ($env:VALIDATION_REPORT) { $env:VALIDATION_REPORT } else { "automation/reports/validation_report.json" }
$prDraftOutput = if ($env:PR_DRAFT_OUTPUT) { $env:PR_DRAFT_OUTPUT } else { "automation/pr/PR_DRAFT.md" }
New-Item -ItemType Directory -Path (Split-Path -Parent $validationReport) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $prDraftOutput) -Force | Out-Null

Write-Output "[1/3] Run pre-PR gate"
& (Join-Path $repoRoot "scripts/pre_pr_gate.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[2/3] Write machine-readable validation report"
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

Write-Output "[3/3] Generate PR draft"
python scripts/pr_prep.py --validation-report $validationReport --output $prDraftOutput
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "Pre-PR + draft flow passed."
Write-Output "- Validation report: $validationReport"
Write-Output "- PR draft: $prDraftOutput"
