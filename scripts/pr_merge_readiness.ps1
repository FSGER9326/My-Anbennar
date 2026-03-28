param(
    [switch]$FullChecks
)

$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & git @Arguments 2>&1
        $code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousPreference
    }

    [pscustomobject]@{
        Code = $code
        Output = @($output) -join "`n"
    }
}

function Pass($Message) { Write-Output "✅ $Message" }
function Warn($Message) { Write-Output "⚠️  $Message" }
function Fail($Message, $NextCommand) {
    Write-Output "❌ $Message"
    Write-Output "Next command: $NextCommand"
    exit 1
}

$repoCheck = Invoke-Git -Arguments @("rev-parse", "--git-dir")
if ($repoCheck.Code -ne 0) {
    Fail "Not inside a git repository." "cd <repo-root>"
}

$branchResult = Invoke-Git -Arguments @("branch", "--show-current")
$branch = $branchResult.Output.Trim()
if ([string]::IsNullOrWhiteSpace($branch)) {
    Fail "Detached HEAD detected." "git switch <your-branch>"
}
Pass "Branch: $branch"

$status = Invoke-Git -Arguments @("status", "--porcelain")
if (-not [string]::IsNullOrWhiteSpace($status.Output)) {
    Fail "Working tree is not clean." "git status --short"
}
Pass "Working tree is clean"

Pass "Fetching origin"
$fetch = Invoke-Git -Arguments @("fetch", "origin")
if ($fetch.Code -ne 0) {
    if (-not [string]::IsNullOrWhiteSpace($fetch.Output)) { Write-Output $fetch.Output }
    Fail "Could not fetch from origin." "git remote -v"
}

$originMain = Invoke-Git -Arguments @("rev-parse", "--verify", "origin/main")
if ($originMain.Code -ne 0) {
    Fail "origin/main not found after fetch." "git remote -v"
}

$upstream = Invoke-Git -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
if ($upstream.Code -ne 0 -or [string]::IsNullOrWhiteSpace($upstream.Output)) {
    Warn "No upstream set for $branch"
    Write-Output "Next command: git push --set-upstream origin $branch"
    $upstreamRef = $null
} else {
    $upstreamRef = $upstream.Output.Trim()
    Pass "Upstream: $upstreamRef"
}

$includesMain = Invoke-Git -Arguments @("merge-base", "--is-ancestor", "origin/main", "HEAD")
if ($includesMain.Code -eq 0) {
    Pass "Branch already includes latest origin/main"
} else {
    Warn "Branch does not include latest origin/main"
    Write-Output "Next command: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main"
}

if ($upstreamRef) {
    $aheadBehind = Invoke-Git -Arguments @("rev-list", "--left-right", "--count", "$upstreamRef...HEAD")
    if ($aheadBehind.Code -eq 0) {
        $parts = $aheadBehind.Output.Trim().Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)
        if ($parts.Count -eq 2) {
            $behind = [int]$parts[0]
            $ahead = [int]$parts[1]
            if ($behind -gt 0) {
                Warn "Your branch is behind upstream by $behind commit(s)."
                Write-Output "Next command: git pull --rebase"
            } else {
                Pass "Not behind upstream"
            }

            if ($ahead -gt 0) {
                Pass "Ahead of upstream by $ahead commit(s)"
            } else {
                Warn "No local commits ahead of upstream."
            }
        }
    }
}

$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tempDir | Out-Null
try {
    $wtAdd = Invoke-Git -Arguments @("worktree", "add", "--detach", $tempDir, "HEAD")
    if ($wtAdd.Code -ne 0) {
        Fail "Could not create temporary worktree." "git worktree prune"
    }

    $prev = Get-Location
    Set-Location $tempDir
    try {
        $merge = Invoke-Git -Arguments @("merge", "--no-commit", "--no-ff", "origin/main")
        if ($merge.Code -eq 0) {
            Pass "Merge simulation with origin/main: no conflicts"
            [void](Invoke-Git -Arguments @("merge", "--abort"))
        } else {
            $unmerged = Invoke-Git -Arguments @("diff", "--name-only", "--diff-filter=U")
            if (-not [string]::IsNullOrWhiteSpace($unmerged.Output)) {
                Fail "Merge simulation found conflicts against origin/main." "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main"
            }
            Fail "Merge simulation failed for a non-conflict reason." "git status --short"
        }
    } finally {
        Set-Location $prev
    }
}
finally {
    [void](Invoke-Git -Arguments @("worktree", "remove", "--force", $tempDir))
    Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
}

if ($FullChecks) {
    Pass "Running pre-PR gate"
    & (Join-Path $scriptDir "pre_pr_gate.ps1")
    $gateExit = $LASTEXITCODE
    if ($null -eq $gateExit) { $gateExit = 0 }
    if ($gateExit -ne 0) {
        Fail "pre_pr_gate.ps1 failed." "powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1"
    }
} else {
    Warn "Skipped full checks (pass -FullChecks to run pre_pr_gate.ps1)."
    Write-Output "Next command: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pr_merge_readiness.ps1 -FullChecks"
}

Pass "PR merge readiness checks completed"
