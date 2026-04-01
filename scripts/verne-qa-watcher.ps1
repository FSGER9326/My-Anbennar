$REPO_DIR = "C:\Users\User\Documents\GitHub\My-Anbennar"
$WORKSPACE = "C:\Users\User\.openclaw\workspace"
$CHANGELOG = "$WORKSPACE\docs\qa-watch-changelog.txt"

function Get-VerneHashes {
    $hashes = @{}
    $files = Get-ChildItem -Path $REPO_DIR -Recurse -Include "*.txt", "*.yml" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '(Verne|verne|A33|a33|heartspier)' }
    foreach ($f in $files) {
        $hashes[$f.FullName] = (Get-FileHash $f.FullName -Algorithm MD5).Hash
    }
    return $hashes
}

function Get-QAChecks($fileName) {
    $checks = @()
    $lower = $fileName.ToLower()
    
    if ($lower -match 'mission') {
        $checks += "Full QA: syntax, flags, modifiers, localisation, tooltips, lore, logic, connections"
    }
    if ($lower -match 'event') {
        $checks += "Event+Loc check: event syntax, localisation keys, option triggers"
    }
    if ($lower -match 'modifier') {
        $checks += "Modifier+Loc check: modifier syntax, localisation entries"
    }
    if ($lower -match '\.yml') {
        $checks += "Localisation check: key consistency, formatting, placeholder syntax"
    }
    if ($lower -match 'decision') {
        $checks += "Decision check: trigger syntax, effect chains, localisation"
    }
    if ($lower -match 'country|tag') {
        $checks += "Tag check: country file syntax, government, ideas references"
    }
    if ($lower -match 'province|history') {
        $checks += "Province check: ownership, cores, culture, religion consistency"
    }
    if ($lower -match 'idea|government') {
        $checks += "Idea check: modifier syntax, localisation, balance review"
    }
    if ($checks.Count -eq 0) {
        $checks += "General check: syntax validity, flag references, modifier existence"
    }
    return $checks
}

$known = Get-VerneHashes
Write-Host "QA Watcher started - watching $($known.Count) Verne files..."
Write-Host "Changelog: $CHANGELOG"
Write-Host "Polling every 300 seconds..."

while ($true) {
    Start-Sleep -Seconds 300
    $current = Get-VerneHashes
    $changed = @()
    $newFiles = @()
    foreach ($p in $current.Keys) {
        if (-not $known.ContainsKey($p)) {
            $newFiles += (Split-Path $p -Leaf)
        } elseif ($known[$p] -ne $current[$p]) {
            $changed += (Split-Path $p -Leaf)
        }
    }
    if ($changed.Count -gt 0 -or $newFiles.Count -gt 0) {
        $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $lines = @()
        $lines += "=" * 60
        $lines += "[$ts] Verne File Changes Detected"
        $lines += "=" * 60
        
        if ($newFiles.Count -gt 0) {
            $lines += ""
            $lines += "NEW FILES ($($newFiles.Count)):"
            foreach ($f in $newFiles) { $lines += "  + $f" }
        }
        if ($changed.Count -gt 0) {
            $lines += ""
            $lines += "MODIFIED FILES ($($changed.Count)):"
            foreach ($f in $changed) { $lines += "  ~ $f" }
        }
        
        $lines += ""
        $lines += "RECOMMENDED QA CHECKS:"
        $allFiles = $changed + $newFiles
        $allChecks = @{}
        foreach ($f in $allFiles) {
            $checks = Get-QAChecks $f
            foreach ($c in $checks) {
                if (-not $allChecks.ContainsKey($c)) { $allChecks[$c] = @() }
                $allChecks[$c] += $f
            }
        }
        foreach ($check in $allChecks.Keys) {
            $lines += "  [$check]"
            $lines += "    Affects: $($allChecks[$check] -join ', ')"
        }
        $lines += "=" * 60
        $lines += ""
        
        $report = $lines -join "`n"
        $report | Out-File -FilePath $CHANGELOG -Encoding utf8 -Append
        Write-Host "[$ts] Detected $($changed.Count) modified + $($newFiles.Count) new files - logged to changelog"
        $known = $current
    }
}
