# sync-to-obsidian.ps1
# Syncs OpenClaw memory files to the Obsidian vault
# Run after each session or via cron

$ErrorActionPreference = "Stop"

$openclawWorkspace = "C:\Users\User\.openclaw\workspace"
$obsidianVault = "C:\Users\User\Documents\Crab Memory"
$today = Get-Date -Format "yyyy-MM-dd"

# Ensure target directories exist
$dirs = @(
    "$obsidianVault\01-Daily",
    "$obsidianVault\05-Learnings",
    "$obsidianVault\04-Decisions"
)
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
}

$synced = @()

# Helper function to add frontmatter if missing
function Add-Frontmatter($content, $yaml) {
    if ($content.TrimStart() -match "^---") { return $content }
    return ($yaml + "`n`n" + $content)
}

# 1. Sync today's daily file
$srcDaily = "$openclawWorkspace\memory\$today.md"
if (Test-Path $srcDaily) {
    $content = Get-Content $srcDaily -Raw -Encoding UTF8
    $fm = @"
---
date: $today
tags: [daily, jordan, openclaw-sync]
type: daily-note
source: openclaw-memory
---
"@
    $content = Add-Frontmatter $content $fm
    $content | Set-Content -Path "$obsidianVault\01-Daily\$today.md" -Encoding UTF8 -NoNewline
    $synced += "01-Daily/$today.md"
}

# 2. Sync yesterday's daily file (in case it was updated late)
$yesterday = (Get-Date).AddDays(-1).ToString("yyyy-MM-dd")
$srcYesterday = "$openclawWorkspace\memory\$yesterday.md"
if (Test-Path $srcYesterday) {
    $existingObsidian = "$obsidianVault\01-Daily\$yesterday.md"
    $srcMod = (Get-Item $srcYesterday).LastWriteTime
    $dstMod = if (Test-Path $existingObsidian) { (Get-Item $existingObsidian).LastWriteTime } else { [datetime]::MinValue }
    if ($srcMod -gt $dstMod) {
        $content = Get-Content $srcYesterday -Raw -Encoding UTF8
        $fm = @"
---
date: $yesterday
tags: [daily, jordan, openclaw-sync]
type: daily-note
source: openclaw-memory
---
"@
        $content = Add-Frontmatter $content $fm
        $content | Set-Content -Path $existingObsidian -Encoding UTF8 -NoNewline
        $synced += "01-Daily/$yesterday.md"
    }
}

# 3. Sync MEMORY.md
$srcMemory = "$openclawWorkspace\MEMORY.md"
if (Test-Path $srcMemory) {
    $content = Get-Content $srcMemory -Raw -Encoding UTF8
    $fm = @"
---
title: Long-Term Memory
type: knowledge-base
tags: [memory, openclaw, config]
updated: $today
source: openclaw-memory
---
"@
    $content = Add-Frontmatter $content $fm
    $content | Set-Content -Path "$obsidianVault\03-Knowledge\Long-Term Memory.md" -Encoding UTF8 -NoNewline
    $synced += "03-Knowledge/Long-Term Memory.md"
}

# 4. Sync .learnings/ERRORS.md
$srcErrors = "$openclawWorkspace\.learnings\ERRORS.md"
if (Test-Path $srcErrors) {
    $content = Get-Content $srcErrors -Raw -Encoding UTF8
    $fm = @"
---
title: Error Log
type: learnings
tags: [errors, lessons, qa]
updated: $today
source: openclaw-learnings
---
"@
    $content = Add-Frontmatter $content $fm
    $content | Set-Content -Path "$obsidianVault\05-Learnings\ERRORS.md" -Encoding UTF8 -NoNewline
    $synced += "05-Learnings/ERRORS.md"
}

# 5. Sync .learnings/LEARNINGS.md
$srcLearnings = "$openclawWorkspace\.learnings\LEARNINGS.md"
if (Test-Path $srcLearnings) {
    $content = Get-Content $srcLearnings -Raw -Encoding UTF8
    $fm = @"
---
title: Learnings
type: learnings
tags: [learnings, insights, best-practices]
updated: $today
source: openclaw-learnings
---
"@
    $content = Add-Frontmatter $content $fm
    $content | Set-Content -Path "$obsidianVault\05-Learnings\LEARNINGS.md" -Encoding UTF8 -NoNewline
    $synced += "05-Learnings/LEARNINGS.md"
}

# 6. Sync .learnings/FEATURE_REQUESTS.md
$srcFeatures = "$openclawWorkspace\.learnings\FEATURE_REQUESTS.md"
if (Test-Path $srcFeatures) {
    $content = Get-Content $srcFeatures -Raw -Encoding UTF8
    $fm = @"
---
title: Feature Requests
type: learnings
tags: [features, requests]
updated: $today
source: openclaw-learnings
---
"@
    $content = Add-Frontmatter $content $fm
    $content | Set-Content -Path "$obsidianVault\05-Learnings\FEATURE_REQUESTS.md" -Encoding UTF8 -NoNewline
    $synced += "05-Learnings/FEATURE_REQUESTS.md"
}

# Summary
Write-Host "=== Obsidian Sync Complete ==="
Write-Host "Synced $($synced.Count) files:"
foreach ($f in $synced) {
    Write-Host "  + $f"
}
Write-Host "Vault: $obsidianVault"
Write-Host "Time: $(Get-Date -Format 'HH:mm:ss')"
