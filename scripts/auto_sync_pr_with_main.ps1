param(
    [string]$BaseRef = "origin/main"
)
# Flow parity contract: bash/python/powershell sync scripts share resolver order and exit modes (ok|needs_manual_conflict|guard_failed|smoke_failed).

$EXIT_OK = 0
$EXIT_NEEDS_MANUAL_CONFLICT = 20
$EXIT_GUARD_FAILED = 21
$EXIT_SMOKE_FAILED = 22

$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

function Invoke-GitCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & git @Arguments 2>&1
        $code = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }

    [pscustomobject]@{
        Code = $code
        Output = @($output) -join "`n"
    }
}

function Test-MergeHead {
    $result = Invoke-GitCommand -Arguments @("rev-parse", "-q", "--verify", "MERGE_HEAD")
    return ($result.Code -eq 0)
}

$statusCheck = Invoke-GitCommand -Arguments @("status", "--porcelain")
$unresolvedCheck = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
if (-not [string]::IsNullOrWhiteSpace($unresolvedCheck.Output)) {
    $statusLines = $statusCheck.Output -split "`n" | ForEach-Object { $_.TrimEnd() } | Where-Object { $_ }
    $validUnmerged = @("UU", "AA", "DD", "AU", "UA", "DU", "UD")
    foreach ($line in $statusLines) {
        if ($line.Length -lt 2 -or ($line.Substring(0, 2) -notin $validUnmerged)) {
            Write-Output "ERROR: Working tree has non-conflict changes. Commit or stash first."
            exit 1
        }
    }
    Write-Output "ERROR: Existing unresolved merge conflicts detected."
    Write-Output "EXIT_MODE=needs_manual_conflict"
    exit $EXIT_NEEDS_MANUAL_CONFLICT
}
if (-not [string]::IsNullOrWhiteSpace($statusCheck.Output)) {
    Write-Output "ERROR: Working tree is not clean. Commit or stash first."
    exit 1
}

$branchCheck = Invoke-GitCommand -Arguments @("branch", "--show-current")
$branch = $branchCheck.Output.Trim()
if ($branch -eq "main") {
    Write-Output "ERROR: Current branch is 'main'."
    Write-Output "This sync helper is for feature/PR branches only."
    Write-Output "If you are already on main, run a normal pull/check flow instead."
    exit 1
}

Write-Output "Fetching latest refs..."
$fetch = Invoke-GitCommand -Arguments @("fetch", "origin")
if ($fetch.Code -ne 0) {
    if (-not [string]::IsNullOrWhiteSpace($fetch.Output)) { Write-Output $fetch.Output }
    exit $fetch.Code
}

Write-Output "Merging $BaseRef into current branch (no auto-commit)..."
$merge = Invoke-GitCommand -Arguments @("merge", "--no-commit", "--no-ff", $BaseRef)
$mergeExit = $merge.Code
if (-not [string]::IsNullOrWhiteSpace($merge.Output)) { Write-Output $merge.Output }

if ($mergeExit -ne 0) {
    Write-Output "Merge reported conflicts. Attempting docs hotspot auto-resolution..."
    & (Join-Path $PSScriptRoot "resolve_docs_conflicts.ps1")
    & python (Join-Path $PSScriptRoot "resolve_content_conflicts.py") --union-docs-only
}

$remainingCheck = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
$remaining = $remainingCheck.Output
if (-not [string]::IsNullOrWhiteSpace($remaining)) {
    Write-Output "ERROR: Some conflicts remain. Resolve manually, then run:"
    Write-Output "  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1"
    Write-Output "  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1"
    Write-Output "EXIT_MODE=needs_manual_conflict"
    exit $EXIT_NEEDS_MANUAL_CONFLICT
}

if ($mergeExit -ne 0 -and -not (Test-MergeHead)) {
    Write-Output "ERROR: Merge failed before creating a merge state. Check base ref and rerun."
    exit 1
}

Write-Output "Running conflict guard and smoke checks..."
& (Join-Path $PSScriptRoot "docs_conflict_guard.ps1")
if ($LASTEXITCODE -ne 0) {
    Write-Output "EXIT_MODE=guard_failed"
    exit $EXIT_GUARD_FAILED
}
& (Join-Path $PSScriptRoot "verne_smoke_checks.ps1")
if ($LASTEXITCODE -ne 0) {
    Write-Output "EXIT_MODE=smoke_failed"
    exit $EXIT_SMOKE_FAILED
}

if (-not (Test-MergeHead)) {
    Write-Output "Already up to date. No merge commit needed."
    Write-Output "EXIT_MODE=ok"
    exit $EXIT_OK
}

Write-Output "Creating merge commit..."
$commit = Invoke-GitCommand -Arguments @("commit", "-m", "Merge $BaseRef into $branch with docs guard automation")
if (-not [string]::IsNullOrWhiteSpace($commit.Output)) { Write-Output $commit.Output }
if ($commit.Code -ne 0) { exit $commit.Code }

Write-Output "Done. Push your branch to update the existing PR."
Write-Output "EXIT_MODE=ok"
