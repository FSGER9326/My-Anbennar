$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot
$validationReport = if ($env:VALIDATION_REPORT) { $env:VALIDATION_REPORT } else { "automation/reports/validation_report.json" }
$prDraftOutput = if ($env:PR_DRAFT_OUTPUT) { $env:PR_DRAFT_OUTPUT } else { "automation/pr/PR_DRAFT.md" }
New-Item -ItemType Directory -Path (Split-Path -Parent $validationReport) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $prDraftOutput) -Force | Out-Null

$checkRecords = New-Object System.Collections.Generic.List[Object]

function Add-CheckRecord {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][string]$Status,
        [Parameter(Mandatory = $true)][string]$Severity
    )

    $checkRecords.Add([ordered]@{
        name = $Name
        command = $Command
        status = $Status
        severity = $Severity
    })
}

function Write-ValidationReport {
    param(
        [Parameter(Mandatory = $true)][string]$OverallStatus,
        [Parameter(Mandatory = $true)][object[]]$UnresolvedIssues
    )

    $payload = [ordered]@{
        generated_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        overall_status = $OverallStatus
        checks = $checkRecords
        unresolved_issues = $UnresolvedIssues
        artifacts = @(
            @{ name = "validation-report"; path = $validationReport },
            @{ name = "pr-draft"; path = $prDraftOutput }
        )
    }

    $payload | ConvertTo-Json -Depth 8 | Set-Content -Path $validationReport -Encoding UTF8
}

function Invoke-GateStep {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label,
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [string]$Severity = "high"
    )

    Write-Output $Label
    try {
        & $Command @Arguments
    }
    catch {
        Add-CheckRecord -Name $Name -Command ("{0} {1}" -f $Command, ($Arguments -join " ")).Trim() -Status "fail" -Severity $Severity
        Write-ValidationReport -OverallStatus "fail" -UnresolvedIssues @(@{
            title = "$Name failed"
            severity = $Severity
            resolved = $false
        })
        Write-Output ""
        Write-Output "Pre-PR gate failed."
        Write-Output ("Next command: {0} {1}" -f $Command, ($Arguments -join " "))
        Write-Output "Fix the issue shown above, then re-run: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1"
        exit 1
    }

    if ($LASTEXITCODE -ne 0) {
        Add-CheckRecord -Name $Name -Command ("{0} {1}" -f $Command, ($Arguments -join " ")).Trim() -Status "fail" -Severity $Severity
        Write-ValidationReport -OverallStatus "fail" -UnresolvedIssues @(@{
            title = "$Name failed"
            severity = $Severity
            resolved = $false
        })
        Write-Output ""
        Write-Output "Pre-PR gate failed."
        Write-Output ("Next command: {0} {1}" -f $Command, ($Arguments -join " "))
        Write-Output "Fix the issue shown above, then re-run: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1"
        exit 1
    }

    Add-CheckRecord -Name $Name -Command ("{0} {1}" -f $Command, ($Arguments -join " ")).Trim() -Status "pass" -Severity $Severity
}

Invoke-GateStep -Label "[1/5] Docs conflict guard" -Name "docs_conflict_guard" -Command "python" -Arguments @("scripts/docs_conflict_guard.py")
Invoke-GateStep -Label "[2/5] Checklist link audit" -Name "checklist_link_audit" -Command "python" -Arguments @("scripts/checklist_link_audit.py")
Invoke-GateStep -Label "[3/5] Verne checklist audit" -Name "verne_checklist_audit" -Command "python" -Arguments @("scripts/verne_checklist_audit.py")
Invoke-GateStep -Label "[4/5] Verne country smoke runner" -Name "country_smoke_runner" -Command "python" -Arguments @("scripts/country_smoke_runner.py", "--profile", "automation/country_profiles/verne.json")
Write-ValidationReport -OverallStatus "pass" -UnresolvedIssues @()
Invoke-GateStep -Label "[5/5] Generate PR draft" -Name "pr_prep" -Command "python" -Arguments @("scripts/pr_prep.py", "--validation-report", $validationReport, "--output", $prDraftOutput) -Severity "medium"
Write-ValidationReport -OverallStatus "pass" -UnresolvedIssues @()

Write-Output "Pre-PR gate passed. Safe to open a PR."
Write-Output "Generated artifacts:"
Write-Output "- Validation report: $validationReport"
Write-Output "- PR draft: $prDraftOutput"
