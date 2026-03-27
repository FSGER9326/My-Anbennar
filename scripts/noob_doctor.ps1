$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python (Join-Path $PSScriptRoot "noob_doctor.py") @args
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 (Join-Path $PSScriptRoot "noob_doctor.py") @args
}
else {
    Write-Output "ERROR: Python is not installed or not on PATH."
    Write-Output "fix: Install Python 3 and ensure python/python3 is available on PATH."
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
