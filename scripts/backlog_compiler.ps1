param(
    [switch]$Plan,
    [string]$Output = "docs/wiki/current-work-queue.md",
    [ValidateSet("missing-target-files", "todo-placeholders", "missing-sentinels", "ledger-drift")]
    [string]$Focus,
    [switch]$StrictMissingTargets,
    [switch]$StrictTodo,
    [switch]$StrictSentinels,
    [switch]$StrictLedger
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

$py = "python"
if (-not (Get-Command $py -ErrorAction SilentlyContinue)) {
    $py = "py"
}

$args = @("scripts/backlog_compiler.py")
if ($Plan) { $args += "--plan" }
if ($Output) { $args += @("--output", $Output) }
if ($Focus) { $args += @("--focus", $Focus) }
if ($StrictMissingTargets) { $args += "--strict-missing-targets" }
if ($StrictTodo) { $args += "--strict-todo" }
if ($StrictSentinels) { $args += "--strict-sentinels" }
if ($StrictLedger) { $args += "--strict-ledger" }

if ($py -eq "py") {
    & py -3 @args
}
else {
    & python @args
}
