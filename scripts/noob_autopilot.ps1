param(
    [string]$BaseRef = "origin/main",
    [ValidateSet("manual", "prefer-main", "prefer-branch")]
    [string]$ResolutionStrategy = "manual"
)

$EXIT_NEEDS_MANUAL_CONFLICT = 20
$EXIT_GUARD_FAILED = 21
$EXIT_SMOKE_FAILED = 22

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

Write-Output "[STEP 1/7] Verify clean working tree"
$statusResult = Invoke-GitCommand -Arguments @("status", "--porcelain")
$unresolvedAtStart = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
if (-not [string]::IsNullOrWhiteSpace($statusResult.Output) -and [string]::IsNullOrWhiteSpace($unresolvedAtStart.Output)) {
    Fail-WithNextCommand -Message "Working tree is not clean." -NextCommand "git status --short"
}

Write-Output "[STEP 2/7] Fetch latest origin"
if ([string]::IsNullOrWhiteSpace($unresolvedAtStart.Output)) {
    $fetch = Invoke-GitCommand -Arguments @("fetch", "origin")
    if ($fetch.Code -ne 0) {
        if (-not [string]::IsNullOrWhiteSpace($fetch.Output)) { Write-Output $fetch.Output }
        Fail-WithNextCommand -Message "Could not fetch from origin." -NextCommand "git fetch origin"
    }
}

Write-Output "[STEP 3/7] Run auto_sync_pr_with_main (PowerShell)"
$syncScript = Join-Path $scriptDir "auto_sync_pr_with_main.ps1"
$syncLog = New-TemporaryFile
if (-not [string]::IsNullOrWhiteSpace($unresolvedAtStart.Output)) {
    @(
        "Existing unresolved merge conflicts detected; skipping merge step."
        "EXIT_MODE=needs_manual_conflict"
    ) | Set-Content -Path $syncLog.FullName
    $syncExit = $EXIT_NEEDS_MANUAL_CONFLICT
}
else {
    & $syncScript -BaseRef $BaseRef *> $syncLog.FullName
    $syncExit = $LASTEXITCODE
    if ($null -eq $syncExit) {
        $syncExit = 0
    }
}
Get-Content -Path $syncLog.FullName

Write-Output "[STEP 4/7] Handle sync result"
if ($syncExit -eq 0) {
    Write-Output "auto_sync_pr_with_main completed."
}
elseif ($syncExit -eq $EXIT_NEEDS_MANUAL_CONFLICT) {
    if ($ResolutionStrategy -eq "manual") {
        $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
        Fail-WithNextCommand -Message "Sync paused: unresolved conflicts need manual attention." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main"
    }
    Write-Output "Sync mode: needs_manual_conflict. Applying $ResolutionStrategy strategy..."
    $unresolvedAfter = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=U")
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
elseif ($syncExit -eq $EXIT_GUARD_FAILED) {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "Sync mode: guard_failed (docs conflict guard did not pass)." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1"
}
elseif ($syncExit -eq $EXIT_SMOKE_FAILED) {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "Sync mode: smoke_failed (smoke checks did not pass)." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1"
}
else {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "auto_sync_pr_with_main.ps1 failed unexpectedly (exit $syncExit)." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\auto_sync_pr_with_main.ps1 -BaseRef $BaseRef"
}

Write-Output "[STEP 5/7] Run docs_conflict_guard (post-sync confirmation)"
& (Join-Path $scriptDir "docs_conflict_guard.ps1")
$guardExit = $LASTEXITCODE
if ($null -eq $guardExit) {
    $guardExit = 0
}
if ($guardExit -ne 0) {
    $syncLog | Remove-Item -Force -ErrorAction SilentlyContinue
    Fail-WithNextCommand -Message "docs_conflict_guard failed." -NextCommand "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1"
}

Write-Output "[STEP 6/7] Run verne_smoke_checks (post-sync confirmation)"
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

Write-Output "[STEP 7/7] Done"
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
