param(
    [string[]]$File
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$pythonBin = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { "python" }

$argsList = @((Join-Path $repoRoot "scripts/event_id_audit.py"))
foreach ($entry in @($File)) {
    if (-not [string]::IsNullOrWhiteSpace($entry)) {
        $argsList += @("--file", $entry)
    }
}

& $pythonBin @argsList
if ($LASTEXITCODE -ne 0) {
    throw "Event ID audit failed."
}
