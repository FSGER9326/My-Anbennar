# encoding-unicode-scan.ps1
# Validates EU4 mod file encodings and scans for hidden/malicious Unicode
# Part of openclaw-eu4-validator

param(
    [string]$Path = "."
)

$ErrorCount = 0
$WarningCount = 0

Write-Host "=== EU4 Encoding & Unicode Scanner ===" -ForegroundColor Cyan

# --- Part 1: Encoding validation ---

# Localisation files MUST have UTF-8 BOM
$locFiles = Get-ChildItem -Recurse -Include "*_l_english.yml" -Path $Path
foreach ($file in $locFiles) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $hasBom = $bytes.Count -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
    if (-not $hasBom) {
        Write-Host "[ENCODING ERROR] $($file.FullName) — Missing UTF-8 BOM (required for localisation)" -ForegroundColor Red
        $ErrorCount++
    }
}

# Script files should NOT have UTF-8 BOM
$scriptExts = @("*.txt", "*.gui")
$allFiles = Get-ChildItem -Recurse -Path $Path -Include $scriptExts | Where-Object { $_.FullName -notmatch "localisation" }
foreach ($file in $allFiles) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    if ($bytes.Count -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Host "[ENCODING ERROR] $($file.FullName) — UTF-8 BOM on script file (should be CP-1252, not UTF-8)" -ForegroundColor Red
        $ErrorCount++
    }
}

# --- Part 2: Hidden / bidirectional Unicode ---

# Characters that should never appear in EU4 files
$badRanges = @(
    @{ Name = "Bidi Override"; Pattern = "[\u200E\u200F\u202A-\u202E]" };     # LRM, RLM, bidi embeddings
    @{ Name = "Zero-Width chars"; Pattern = "[\u200B-\u200D\uFEFF]" };       # ZWSP, ZWNJ, ZWJ, BOM
    @{ Name = "Special spaces"; Pattern = "[\u00A0\u2028\u2029]" }            # NBSP, LS, PS
)

# Text files to scan
$textFiles = Get-ChildItem -Recurse -Path $Path -Include "*.txt","*.yml","*.gui","*.md" | Where-Object { $_.FullName -notmatch "node_modules" }

foreach ($file in $textFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    
    foreach ($range in $badRanges) {
        if ($content -match $range.Pattern) {
            Write-Host "[UNICODE WARNING] $($file.FullName) — Contains $($range.Name): $($matches.Value)" -ForegroundColor Yellow
            $WarningCount++
        }
    }
    
    # Smart quotes (wrong for EU4)
    if ($content -match "[\u2018-\u201F]") {
        Write-Host "[UNICODE WARNING] $($file.FullName) — Smart quotes detected (EU4 uses straight quotes)" -ForegroundColor Yellow
        $WarningCount++
    }
}

# --- Part 3: Line ending check ---
$crlfFiles = Get-ChildItem -Recurse -Path $Path -Include "*.txt","*.yml" | Where-Object { $_.FullName -notmatch "node_modules" }
foreach ($file in $crlfFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    if ($content -match "`r`n") {
        # CRLF is fine on Windows, just flag if it's mixed
        if ($content -match "[^`r]`n") {
            Write-Host "[LINE ENDING WARNING] $($file.FullName) — Mixed LF/CRLF line endings" -ForegroundColor Yellow
            $WarningCount++
        }
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Errors: $ErrorCount" -ForegroundColor $(if ($ErrorCount -gt 0) { "Red" } else { "Green" })
Write-Host "Warnings: $WarningCount" -ForegroundColor $(if ($WarningCount -gt 0) { "Yellow" } else { "Green" })

if ($ErrorCount -gt 0) { exit 1 }
if ($WarningCount -gt 0) { exit 0 }
exit 0
