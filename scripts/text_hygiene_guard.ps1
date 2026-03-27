$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$suspiciousTokens = @{}
$suspiciousTokens[(([char]0x00E2).ToString() + ([char]0x20AC).ToString())] = "likely mojibake from smart quotes or dashes"
$suspiciousTokens[(([char]0x00C3).ToString())] = "likely mojibake from UTF-8 text decoded as Latin-1"
$suspiciousTokens[(([char]0x00EF).ToString() + ([char]0x00BB).ToString() + ([char]0x00BF).ToString())] = "literal UTF-8 BOM bytes in file text"
$suspiciousTokens[(([char]0xFFFD).ToString())] = "replacement character found"

function Get-RelativeRepoPath {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$FullPath
    )

    if ($FullPath.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullPath.Substring($Root.Length).TrimStart('\', '/').Replace('\', '/')
    }

    return $FullPath.Replace('\', '/')
}

function Normalize-Line {
    param([Parameter(Mandatory = $true)][string]$Line)

    $lowered = $Line.ToLowerInvariant()
    $lowered = $lowered.Replace([string][char]96, "")
    $lowered = [regex]::Replace($lowered, '[^a-z0-9]+', " ")
    return $lowered.Trim()
}

$files = @()
$files += Get-ChildItem (Join-Path $repoRoot "docs") -Recurse -File -Filter *.md

$githubRoot = Join-Path $repoRoot ".github"
if (Test-Path $githubRoot) {
    $files += Get-ChildItem $githubRoot -Recurse -File -Filter *.md
}

$locRoot = Join-Path $repoRoot "localisation"
if (Test-Path $locRoot) {
    $files += Get-ChildItem $locRoot -Recurse -File -Filter *.yml
}

$errors = New-Object System.Collections.Generic.List[string]

foreach ($file in $files) {
    $rel = Get-RelativeRepoPath -Root $repoRoot -FullPath $file.FullName
    $text = Get-Content $file.FullName -Raw -Encoding UTF8

    foreach ($pair in $suspiciousTokens.GetEnumerator()) {
        if ($text.Contains($pair.Key)) {
            $errors.Add("${rel}: contains suspicious text ($($pair.Value))")
        }
    }

    $previousLine = ""
    $previousNormalized = ""
    $previousNumber = 0
    $lineNumber = 0

    foreach ($line in ($text -split "`r?`n")) {
        $lineNumber += 1
        $stripped = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($stripped)) {
            continue
        }
        if ($stripped.StartsWith("#")) {
            continue
        }

        $normalized = Normalize-Line -Line $stripped
        if (
            -not [string]::IsNullOrWhiteSpace($normalized) -and
            -not [string]::IsNullOrWhiteSpace($previousNormalized) -and
            $normalized -eq $previousNormalized -and
            $normalized -ne "on" -and
            $normalized.Length -ge 12 -and
            $stripped -ne $previousLine
        ) {
            $errors.Add("${rel}:${previousNumber}-${lineNumber}: near-duplicate consecutive lines")
        }

        $previousLine = $stripped
        $previousNormalized = $normalized
        $previousNumber = $lineNumber
    }
}

if ($errors.Count -gt 0) {
    Write-Output "Text hygiene guard failed:"
    foreach ($issue in $errors) {
        Write-Output " - $issue"
    }
    throw "Text hygiene guard failed."
}

Write-Output "Text hygiene guard passed."
