param(
    [string]$BaseRef = "origin/main"
)

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

$statusCheck = Invoke-GitCommand -Arguments @("status", "--porcelain")
if (-not [string]::IsNullOrWhiteSpace($statusCheck.Output)) {
    Write-Output "ERROR: Working tree is not clean. Commit or stash first."
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
}

$remainingCheck = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
$remaining = $remainingCheck.Output
if (-not [string]::IsNullOrWhiteSpace($remaining)) {
    Write-Output "ERROR: Some conflicts remain. Resolve manually, then run:"
    Write-Output "  powershell -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1"
    Write-Output "  powershell -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1"
    exit 1
}

Write-Output "Running conflict guard and smoke checks..."
& (Join-Path $PSScriptRoot "docs_conflict_guard.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& (Join-Path $PSScriptRoot "verne_smoke_checks.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$branchCheck = Invoke-GitCommand -Arguments @("branch", "--show-current")
$branch = $branchCheck.Output.Trim()
Write-Output "Creating merge commit..."
$commit = Invoke-GitCommand -Arguments @("commit", "-m", "Merge $BaseRef into $branch with docs guard automation")
if (-not [string]::IsNullOrWhiteSpace($commit.Output)) { Write-Output $commit.Output }
if ($commit.Code -ne 0) { exit $commit.Code }

Write-Output "Done. Push your branch to update the existing PR."
