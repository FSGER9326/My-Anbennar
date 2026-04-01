# health-lightweight.ps1 — Gateway-only health check (no CLI needed)
param(
    [Parameter(Mandatory=$false)]
    [int]$TimeoutSec = 5
)

$gateway = "http://127.0.0.1:18789"
$healthy = $true
$issues = @()

try {
    $r = Invoke-RestMethod -Uri "$gateway/health" -TimeoutSec $TimeoutSec
    if ($r.ok -ne $true -or $r.status -ne 'live') {
        $issues += "Gateway health: $($r | ConvertTo-Json -Compress)"
    }
} catch {
    $issues += "Gateway unreachable: $_"
    $healthy = $false
}

# Check if memory-lancedb is responsive (optional)
try {
    $dbPath = "$env:USERPROFILE\.openclaw\data\memory-lancedb"
    if (Test-Path $dbPath) {
        $files = Get-ChildItem $dbPath -File -ErrorAction SilentlyContinue
        Write-Host "memory-lancedb: $($files.Count) files in store"
    }
} catch {
    Write-Host "memory-lancedb: not accessible (expected on this system)"
}

if ($issues.Count -eq 0) {
    Write-Host "HEALTH_OK"
    exit 0
} else {
    Write-Host "ISSUES FOUND:"
    $issues | ForEach-Object { Write-Host "  - $_" }
    exit 1
}
