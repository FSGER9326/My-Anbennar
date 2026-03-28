param(
    [string]$BaseRef = "origin/main",
    [ValidateSet("manual", "prefer-main", "prefer-branch")]
    [string]$ResolutionStrategy = "manual"
)

$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
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

function Fail-WithNextCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [Parameter(Mandatory = $true)]
        [string]$NextCommand
    )

    Write-Output "ERROR: $Message"
    Write-Output "Next command:"
    Write-Output $NextCommand
    exit 1
}

$branchResult = Invoke-GitCommand -Arguments @("branch", "--show-current")
$branch = $branchResult.Output.Trim()

Write-Output "[STEP 1/8] Verify clean working tree"
$statusResult = Invoke-GitCommand -Arguments @("status", "--porcelain")
if (-not [string]::IsNullOrWhiteSpace($statusResult.Output)) {
    Fail-WithNextCommand -Message "Working tree is not clean." -NextCommand "git status --short"
}

Write-Output "[STEP 2/8] Fetch latest origin"
$fetch = Invoke-GitCommand -Arguments @("fetch", "origin")
if ($fetch.Code -ne 0) {
    if (-not [string]::IsNullOrWhiteSpace($fetch.Output)) { Write-Output $fetch.Output }
    Fail-WithNextCommand -Message "Could not fetch from origin." -NextCommand "git fetch origin"
}

Write-Output "[STEP 3/8] Compile backlog plan queue before coding sessions"
& (Join-Path $scriptDir "backlog_compiler.ps1") -Plan
$planExit = $LASTEXITCODE
if ($null -eq $planExit) { $planExit = 0 }
if ($planExit -ne 0) {
    Fail-WithNextCommand -Message "backlog_compiler plan failed." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\backlog_compiler.ps1 -Plan"
}

Write-Output "[STEP 4/8] Run auto_sync_pr_with_main (PowerShell)"
$syncScript = Join-Path $scriptDir "auto_sync_pr_with_main.ps1"
$syncLog = New-TemporaryFile
& $syncScript -BaseRef $BaseRef *> $syncLog.FullName
$syncExit = $LASTEXITCODE
if ($null -eq $syncExit) {
    $syncExit = 0
}
if ($syncExit -eq 0) {
    Write-Output "auto_sync_pr_with_main completed."
}

Write-Output "[STEP 5/8] Resolve unresolved merge conflicts (docs hotspots only, when needed)"
$unresolved = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
if (-not [string]::IsNullOrWhiteSpace($unresolved.Output)) {
    & (Join-Path $scriptDir "resolve_docs_conflicts.ps1")
    $resolveExit = $LASTEXITCODE
    if ($null -eq $resolveExit) {
        $resolveExit = 0
    }
    if ($resolveExit -ne 0) {
        $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "Automatic docs conflict resolution failed." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\resolve_docs_conflicts.ps1"
    }
}

$unresolvedAfter = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
if (-not [string]::IsNullOrWhiteSpace($unresolvedAfter.Output)) {
    if ($ResolutionStrategy -eq "manual") {
        $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
        Fail-WithNextCommand -Message "Unresolved merge conflicts remain." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main"
    }

    Write-Output "Applying $ResolutionStrategy strategy to unresolved files..."
    $remainingList = ($unresolvedAfter.Output -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    foreach ($file in $remainingList) {
        if ($ResolutionStrategy -eq "prefer-main") {
            & git checkout --theirs -- $file
        }
        else {
            & git checkout --ours -- $file
        }
        & git add -- $file
    }
}

if ($syncExit -ne 0) {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "auto_sync_pr_with_main.ps1 failed." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main"
}

Write-Output "[STEP 6/8] Run docs_conflict_guard"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")
$guardExit = $LASTEXITCODE
if ($null -eq $guardExit) {
    $guardExit = 0
}
if ($guardExit -ne 0) {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "docs_conflict_guard failed." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1"
}

Write-Output "[STEP 7/8] Run verne_smoke_checks"
& (Join-Path $scriptDir "verne_smoke_checks.ps1")
$smokeExit = $LASTEXITCODE
if ($null -eq $smokeExit) {
    $smokeExit = 0
}
if ($smokeExit -ne 0) {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "verne_smoke_checks failed." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1"
}

$syncLog | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Output "[STEP 8/8] Done"
Write-Output "Habit reminder: sync first, then push."
$upstream = Invoke-GitCommand -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
if ($upstream.Code -eq 0 -and -not [string]::IsNullOrWhiteSpace($upstream.Output)) {
    Write-Output "Success. Push with:"
    Write-Output "git push"
}
else {
    Write-Output "Success. Push with:"
    Write-Output "git push --set-upstream origin $branch"
}
