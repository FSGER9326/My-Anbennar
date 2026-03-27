$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$auditScript = Join-Path $scriptDir "checklist_manifest_audit.ps1"

& $auditScript
