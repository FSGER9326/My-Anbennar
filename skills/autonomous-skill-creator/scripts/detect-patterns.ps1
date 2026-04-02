# detect-patterns.ps1
# Scans trial logs, learnings, and background worker history for skill-creation candidates
# Outputs JSON array of pattern candidates to stdout

$ErrorActionPreference = "SilentlyContinue"

$WORKSPACE = "C:\Users\User\.openclaw\workspace"
$SUBAGENT_PATTERNS = "$WORKSPACE\docs\subagent-patterns.md"
$LEARNINGS = "$WORKSPACE\.learnings\LEARNINGS.md"
$ERRORS = "$WORKSPACE\.learnings\ERRORS.md"
$BG_WORKER = "$WORKSPACE\docs\background-worker.md"
$LEDGER = "$WORKSPACE\skills\self-improving-agent\ledger.md"

$candidates = @()

# 1. Scan trial log for high-reusability repeated tasks
$trialSection = Select-String -Path $SUBAGENT_PATTERNS -Pattern "Trial \d+" -Context 0,20 | Select-Object -Last 20
foreach ($trial in $trialSection) {
    $context = $trial.Context.PostContext -join "`n"
    if ($context -match "Reusability|Score[:\s]+(\d+)/5") {
        $score = if ($Matches) { [int]$Matches[1] } else { 0 }
        $occurrences = ($trialSection | Where-Object { $_.Line -match $trial.Line.Substring(0, [Math]::Min(30, $trial.Line.Length)) }).Count
        if ($score -ge 4 -and $occurrences -ge 2) {
            $taskType = if ($trial.Line -match "— (.+?)(?:\n|$)") { $Matches[1].Trim() } else { "unknown" }
            $candidates += @{
                pattern_key = ($taskType -replace "[^a-z0-9]+", "_").ToLower()
                category = "repeated_action"
                occurrences = $occurrences
                reusability_score = $score
                description = "Subagent task repeated: $taskType"
                source = "trial_log"
            }
        }
    }
}

# 2. Scan learnings for repeated patterns (3+ occurrences)
@($LEARNINGS, $ERRORS) | ForEach-Object {
    $file = $_
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        # Find Pattern-Key entries with Recurrence-Count >= 3
        $patternBlocks = [regex]::Matches($content, '(?sm)## \[.+?\].*?(?=^## |\z)') | ForEach-Object { $_.Value }
        foreach ($block in $patternBlocks) {
            if ($block -match 'Recurrence-Count[:\s]+(\d+)' -and [int]$Matches[1] -ge 3) {
                $key = if ($block -match 'Pattern-Key[:\s]+(.+)') { $Matches[1].Trim() } else { "unnamed" }
                $summary = if ($block -match 'Summary\s*\n+(.+?)(?=###|$)') { $Matches[1].Trim() } else { $key }
                $candidates += @{
                    pattern_key = $key
                    category = "repeated_action"
                    occurrences = [int]$Matches[1]
                    reusability_score = 8
                    description = $summary
                    source = "learnings"
                }
            }
        }
    }
}

# 3. Scan background worker completed tasks for repetition
if (Test-Path $BG_WORKER) {
    $bgContent = Get-Content $BG_WORKER -Raw
    # Extract completed task names
    $completed = [regex]::Matches($bgContent, '(?<=-\s\[x\]\s~~).+?(?=~~)') | ForEach-Object { $_.Value.Trim() }
    $completed += [regex]::Matches($bgContent, '(?<=✅\s).+?(?=\s)') | ForEach-Object { $_.Value.Trim() }
    $completed = $completed | Where-Object { $_ -ne "" } | Group-Object | Where-Object { $_.Count -ge 3 }
    foreach ($group in $completed) {
        $candidates += @{
            pattern_key = ($group.Name -replace "[^a-z0-9]+", "_").ToLower()
            category = "repeated_action"
            occurrences = $group.Count
            reusability_score = 7
            description = "Background worker repeated task: $($group.Name)"
            source = "background_worker"
        }
    }
}

# 4. Scan ledger for skills already created (skip these)
$createdSkills = @()
if (Test-Path $LEDGER) {
    $ledgerContent = Get-Content $LEDGER -Raw
    $createdSkills = [regex]::Matches($ledgerContent, '(?<=Skill Created:\s)[^\s]+') | ForEach-Object { $_.Value.ToLower() }
}

# Deduplicate and filter
$seen = @{}
$results = @()
foreach ($c in $candidates) {
    if ($createdSkills -contains $c.pattern_key) { continue }
    if (-not $seen.ContainsKey($c.pattern_key)) {
        $seen[$c.pattern_key] = $c
        $results += $c
    } else {
        # Merge: take max score and max occurrences
        $existing = $seen[$c.pattern_key]
        $existing.occurrences = [Math]::Max($existing.occurrences, $c.occurrences)
        $existing.reusability_score = [Math]::Max($existing.reusability_score, $c.reusability_score)
    }
}

# Sort by score descending
$results = $results | Sort-Object { $_.reusability_score * 10 + $_.occurrences } -Descending

# Output
if ($results.Count -gt 0) {
    Write-Output ($results | ConvertTo-Json -Depth 3)
} else {
    Write-Output "[]"
}
