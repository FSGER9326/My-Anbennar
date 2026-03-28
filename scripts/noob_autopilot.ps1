param(
    [string]$BaseRef = "origin/main",
    [ValidateSet("strict", "fast")]
    [string]$Mode = "fast",
    [switch]$PreferMain,
    [switch]$PreferBranch,
    [ValidateSet("manual", "prefer-main", "prefer-branch")]
    [string]$ResolutionStrategy = "manual",
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

if ($PreferMain -and $PreferBranch) {
    throw "Use either -PreferMain or -PreferBranch, not both."
}

$python = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { "python" }
$forward = @("--base-ref", $BaseRef, "--mode", $Mode)

if ($PreferMain) {
    $forward += "--prefer-main"
} elseif ($PreferBranch) {
    $forward += "--prefer-branch"
} elseif ($ResolutionStrategy -eq "prefer-main") {
    $forward += "--prefer-main"
} elseif ($ResolutionStrategy -eq "prefer-branch") {
    $forward += "--prefer-branch"
}

if ($ExtraArgs) {
    $forward += $ExtraArgs
}

& $python (Join-Path $scriptDir "verne_orchestrator.py") @forward
exit $LASTEXITCODE
