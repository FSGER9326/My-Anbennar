# Verne Modding QA Watcher
# Monitors the Anbennar repo for file changes and triggers QA
# Run as a background process

$REPO_DIR = "C:\Users\User\Documents\GitHub\My-Anbennar"
$TRACKER = "C:\Users\User\.openclaw\workspace\docs\verne-standards-tracker.md"
$QA_PROTOCOL = "C:\Users\User\.openclaw\workspace\docs\modding-qa-protocol.md"
$WORKSPACE = "C:\Users\User\.openclaw\workspace"

Write-Host "[QA Watcher] Starting continuous monitor on $REPO_DIR"
Write-Host "[QA Watcher] Checking for Verne file changes every 300 seconds"

# Track last check time
$lastCheck = Get-Date

# Track known file hashes to detect changes
$knownHashes = @{}
function Get-FileHashes {
    $hashes = @{}
    $verneFiles = Get-ChildItem -Path $REPO_DIR -Recurse -Include "*.txt", "*.yml" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '(Verne|verne|A33|a33|heartspier)' }
    foreach ($file in $verneFiles) {
        $hashes[$file.FullName] = (Get-FileHash $file.FullName -Algorithm MD5).Hash
    }
    return $hashes
}

# Initial hash snapshot
$knownHashes = Get-FileHashes
Write-Host "[QA Watcher] Tracking $($knownHashes.Count) Verne files"

while ($true) {
    Start-Sleep -Seconds 300  # Check every 5 minutes

    $currentHashes = Get-FileHashes
    $changedFiles = @()

    foreach ($path in $currentHashes.Keys) {
        if (-not $knownHashes.ContainsKey($path) -or $knownHashes[$path] -ne $currentHashes[$path]) {
            $changedFiles += $path
        }
    }

    # Check for new files
    foreach ($path in $currentHashes.Keys) {
        if (-not $knownHashes.ContainsKey($path)) {
            $changedFiles += $path
        }
    }

    if ($changedFiles.Count -gt 0) {
        Write-Host "[QA Watcher] $(Get-Date -Format 'HH:mm:ss') — Detected $($changedFiles.Count) changed file(s):"
        foreach ($f in $changedFiles) { Write-Host "  - $(Split-Path $f -Leaf)" }

        # Write change report for the QA subagent to pick up
        $report = "[QA Watcher] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
        $report += "Changed files:`n"
        foreach ($f in $changedFiles) {
            $report += "  - $f`n"
        }
        $report | Out-File -FilePath "$WORKSPACE\docs\qa-watch-changelog.txt" -Encoding utf8

        Write-Host "[QA Watcher] Change report written. QA subagent will pick this up."
        $knownHashes = $currentHashes
    } else {
        Write-Host "[QA Watcher] $(Get-Date -Format 'HH:mm:ss') — No changes detected"
    }
}
