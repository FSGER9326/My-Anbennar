param(
    [ValidateSet("manual", "pre-commit", "pre-push")]
    [string]$Mode = "manual",
    [switch]$Staged,
    [string]$Against
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    $output = & git @Arguments 2>&1
    [pscustomobject]@{
        Code = $LASTEXITCODE
        Output = @($output) -join "`n"
    }
}

function Get-ChangedFiles {
    if ($Staged) {
        return @((Invoke-Git -Arguments @("diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB")).Output -split "`r?`n" | Where-Object { $_ })
    }

    if (-not [string]::IsNullOrWhiteSpace($Against)) {
        return @((Invoke-Git -Arguments @("diff", "--name-only", "$Against...HEAD")).Output -split "`r?`n" | Where-Object { $_ })
    }

    if ($Mode -eq "pre-push") {
        $upstream = Invoke-Git -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
        if ($upstream.Code -eq 0 -and -not [string]::IsNullOrWhiteSpace($upstream.Output)) {
            return @((Invoke-Git -Arguments @("diff", "--name-only", "$($upstream.Output)...HEAD")).Output -split "`r?`n" | Where-Object { $_ })
        }
    }

    return @((Invoke-Git -Arguments @("diff", "--name-only", "HEAD")).Output -split "`r?`n" | Where-Object { $_ })
}

$files = Get-ChangedFiles
if ($files.Count -eq 0) {
    Write-Output "No relevant changed files detected."
    exit 0
}

$hasDocs = $false
$hasRepoMapDocs = $false
$hasAutomation = $false
$needsFullSmoke = $false

foreach ($file in $files) {
    if ($file -like "docs/*" -or $file -eq ".gitattributes" -or $file -like ".github/*" -or $file -like ".githooks/*") {
        $hasDocs = $true
    }
    if ($file -like "docs/repo-maps/*" -or $file -like "docs/wiki/*" -or $file -like "docs/design/*" -or $file -eq "docs/implementation-crosswalk.md") {
        $hasRepoMapDocs = $true
    }
    if ($file -like "scripts/*" -or $file -like "automation/*" -or $file -like ".github/workflows/*" -or $file -like ".githooks/*") {
        $hasAutomation = $true
    }
    if (
        $file -like "common/*" -or
        $file -like "decisions/*" -or
        $file -like "events/*" -or
        $file -like "missions/*" -or
        $file -like "localisation/*" -or
        $file -eq "automation/country_profiles/verne.json" -or
        $file -like "scripts/verne_smoke_checks.*" -or
        $file -like "scripts/country_smoke_runner.*"
    ) {
        $needsFullSmoke = $true
    }
}

Write-Output "Smart smoke router mode: $Mode"
Write-Output "Changed files:"
foreach ($file in $files) {
    Write-Output " - $file"
}

& (Join-Path $scriptDir "repo_doctor.ps1")

if ($hasDocs -or $hasAutomation -or $needsFullSmoke) {
    & (Join-Path $scriptDir "text_hygiene_guard.ps1")
}

if ($hasDocs -or $hasAutomation) {
    & (Join-Path $scriptDir "docs_conflict_guard.ps1")
}

if ($hasDocs) {
    & (Join-Path $scriptDir "checklist_link_audit.ps1")
}

if ($hasRepoMapDocs -or $hasAutomation) {
    & (Join-Path $scriptDir "verne_checklist_audit.ps1")
}

if ($needsFullSmoke) {
    & (Join-Path $scriptDir "verne_smoke_checks.ps1")
}

Write-Output "Smart smoke router finished."
