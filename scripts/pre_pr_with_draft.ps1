$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

$validationReport = if ($env:VALIDATION_REPORT) { $env:VALIDATION_REPORT } else { "automation/reports/validation_report.json" }
$prDraftOutput = if ($env:PR_DRAFT_OUTPUT) { $env:PR_DRAFT_OUTPUT } else { "automation/pr/PR_DRAFT.md" }
New-Item -ItemType Directory -Path (Split-Path -Parent $validationReport) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $prDraftOutput) -Force | Out-Null

$pythonCmd = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { throw "Neither 'py' nor 'python' is available on PATH." }
$pythonArgs = if ($pythonCmd -eq "py") { @("-3") } else { @() }

Write-Output "[1/3] Run pre-PR gate"
& (Join-Path $repoRoot "scripts/pre_pr_gate.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[2/3] Write machine-readable validation report"
& $pythonCmd @pythonArgs "scripts/write_validation_report.py" `
    --output $validationReport `
    --overall-status pass `
    --check "docs_conflict_guard|python scripts/docs_conflict_guard.py|pass|high" `
    --check "checklist_link_audit|python scripts/checklist_link_audit.py|pass|high" `
    --check "verne_checklist_audit|python scripts/verne_checklist_audit.py|pass|high" `
    --check "country_smoke_runner|python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json|pass|high" `
    --artifact "validation-report|$validationReport" `
    --artifact "pr-draft|$prDraftOutput"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[3/3] Generate PR draft"
& $pythonCmd @pythonArgs "scripts/pr_prep.py" --validation-report $validationReport --output $prDraftOutput
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "Pre-PR + draft flow passed."
Write-Output "- Validation report: $validationReport"
Write-Output "- PR draft: $prDraftOutput"
