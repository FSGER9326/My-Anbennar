# Anbennar Upstream Sync Analyzer (PowerShell)
# Fetches recent upstream commits and categorizes changes

$REPORT = "C:\Users\User\.openclaw\workspace\docs\anbennar-upstream-report.md"
$API_BASE = "https://gitlab.com/api/v4/projects/Sando13%2Fanbennar-eu4-dev"

Write-Host "Fetching recent commits from Anbennar upstream..."

# Get last 30 commits
$commits = Invoke-RestMethod -Uri "$API_BASE/repository/commits?ref_name=new-master&per_page=30" -Method Get

$reportContent = @"
# Anbennar Upstream Sync Report
Generated: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')
Upstream: Sando13/anbennar-eu4-dev (new-master)
Your fork base: FSGER9326/My-Anbennar

## Recent Upstream Commits

"@

$categories = @{
    "GFX/UI" = @()
    "Bug Fixes" = @()
    "New Content" = @()
    "Country-Specific" = @()
    "Common/Shared" = @()
    "Verne-Touched" = @()
}

foreach ($commit in $commits) {
    $diff = Invoke-RestMethod -Uri "$API_BASE/repository/commits/$($commit.id)/diff?per_page=50" -Method Get
    $files = $diff | ForEach-Object { $_.new_path }
    
    $hasGfx = $files | Where-Object { $_ -match '(gfx/|\.dds|\.tga|\.png|interface/)' }
    $hasUI = $files | Where-Object { $_ -match '(custom_gui|\.gui)' }
    $hasLoc = $files | Where-Object { $_ -match '(localisation|\.yml)' }
    $hasVerne = $files | Where-Object { $_ -match '(verne|a33)' }
    $hasCommon = $files | Where-Object { $_ -match '^common/' }
    $hasEvents = $files | Where-Object { $_ -match '^events/' }
    $hasMissions = $files | Where-Object { $_ -match '^missions/' }
    
    $tag = ""
    if ($hasVerne) { $tag += "VERNE⚠️ " }
    if ($hasGfx -or $hasUI) { $tag += "GFX/UI " }
    if ($hasLoc) { $tag += "LOC " }
    if ($hasCommon) { $tag += "COMMON " }
    if ($hasEvents) { $tag += "EVENTS " }
    if ($hasMissions) { $tag += "MISSIONS " }
    if (-not $tag) { $tag = "other" }
    
    $fileList = $files -join ", "
    $reportContent += "- **[$($commit.short_id)]** $($commit.title) ($($commit.created_at.Substring(0,10)))`n"
    $reportContent += "  Tags: $tag`n"
    $reportContent += "  Files: $fileList`n"
    $reportContent += "  URL: $($commit.web_url)`n`n"
}

$reportContent += @"

## Safe to Cherry-Pick (non-Verne, shared systems)

These file patterns are safe to merge from upstream when they don't touch Verne content:

- common/ancestor_personalities/ - Anbennar personality system
- common/ruler_personalities/ - Ruler personality definitions
- common/event_modifiers/anb_misc_modifiers.txt - Generic modifiers
- common/scripted_functions/ - Shared scripted functions (review first)

## Always Review Before Merging

- common/scripted_effects/ — May affect Verne spell effects (4160→5690 province ID changes)
- common/custom_gui/magic_menu.txt — Province ID changes detected
- common/mercenary_companies/ — Check for Verne-specific mercs
- missions/ — Only merge if NOT touching A33_* slots
- events/ — Only merge if NOT touching verne namespace
- localisation/ — Verne loc files must not be overwritten

## Integration Commands

` `` `
cd C:\Users\User\Documents\GitHub\My-Anbennar
git fetch upstream new-master

# View what changed in a commit:
git show <hash> --stat

# Safe cherry-pick (after review):
git cherry-pick <hash>

# Or checkout specific files from upstream:
git checkout upstream/new-master -- common/ancestor_personalities/
` `` `

## Recent Verne-Relevant Changes

"@

# Find any commits touching Verne files
$verneCommits = @()
foreach ($c in $commits) {
    $diff = Invoke-RestMethod -Uri "$API_BASE/repository/commits/$($c.id)/diff?per_page=50" -Method Get
    $files = $diff | ForEach-Object { $_.new_path }
    $hasVerne = $files | Where-Object { $_ -match '(verne|a33|heartspier)' }
    if ($hasVerne) {
        $joined = [string]::Join(", ", $hasVerne)
        $verneCommits += "- [$($c.short_id)] $($c.title) - touches: $joined"
    }
}

if ($verneCommits) {
    $reportContent += ($verneCommits -join "`n")
} else {
    $reportContent += "No recent commits touch Verne-specific files."
}

$reportContent | Out-File -FilePath $REPORT -Encoding utf8
Write-Host "Report written to $REPORT"
