param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ArgsFromCaller
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$python = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { "python" }
& $python (Join-Path $scriptDir "verne_orchestrator.py") @ArgsFromCaller
exit $LASTEXITCODE
