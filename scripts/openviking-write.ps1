# openviking-write.ps1 — Write facts, decisions, and session summaries to OpenViking
# Usage: powershell -ExecutionPolicy Bypass -File "C:\Users\User\.openclaw\workspace\scripts\openviking-write.ps1" -Action "decision" -Title "10-column" -Content "Falk adopted 10-column..."

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("decision", "task", "learning", "session_summary")]
    [string]$Action,
    
    [string]$Title = "",
    [string]$Content = "",
    [string]$Tags = "",
    [string]$SessionId = ""
)

$base = "http://127.0.0.1:1933"

# If no session exists, create one
if (-not $SessionId) {
    $existing = Invoke-RestMethod -Uri "$base/api/v1/sessions" -Method Get -TimeoutSec 5
    if ($existing.result.Count -gt 0) {
        $SessionId = $existing.result[0].session_id
    } else {
        $newSession = Invoke-RestMethod -Uri "$base/api/v1/sessions" -Method Post -Body (@{
            name = "Jordan-$(Get-Date -Format 'yyyy-MM-dd')"
            description = "Auto-managed session for Jordan agent"
        } | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 5
        $SessionId = $newSession.result.session_id
        Write-Host "Created session: $SessionId"
    }
}

# Build content based on type
$payload = @{
    type = $Action
    title = $Title
    content = $Content
    tags = ($Tags -split ',' | ForEach-Object { $_.Trim() })
    timestamp = (Get-Date).ToUniversalTime().ToString("o")
    source = "jordan-agent"
} | ConvertTo-Json -Depth 5

# Commit to session
$result = Invoke-RestMethod -Uri "$base/api/v1/sessions/$SessionId/commit" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 10

Write-Host "[$Action] $Title → $($result.result.status) (session: $SessionId)"
return $result
