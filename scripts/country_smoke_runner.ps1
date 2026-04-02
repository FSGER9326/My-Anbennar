param(
    [Parameter(Mandatory = $true)]
    [string]$Profile
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$profilePath = if ([System.IO.Path]::IsPathRooted($Profile)) { $Profile } else { Join-Path $repoRoot $Profile }

if (-not (Test-Path $profilePath)) {
    throw "Missing smoke profile: $Profile"
}

function Get-RelativePath {
    param([string]$From, [string]$To)
    $fromUri = New-Object System.Uri($From)
    $toUri = New-Object System.Uri($To)
    $relativeUri = $fromUri.MakeRelativeUri($toUri)
    $relativePath = [System.Uri]::UnescapeDataString($relativeUri.ToString())
    return $relativePath.Replace('/', '\')
}

function Read-Text {
    param([Parameter(Mandatory = $true)][string]$Path)
    return Get-Content $Path -Raw -Encoding UTF8
}

function Strip-Comment {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Line)
    $inQuote = $false
    $builder = New-Object System.Text.StringBuilder
    foreach ($ch in $Line.ToCharArray()) {
        if ($ch -eq '"') {
            $inQuote = -not $inQuote
            [void]$builder.Append($ch)
            continue
        }
        if (($ch -eq '#') -and (-not $inQuote)) {
            break
        }
        [void]$builder.Append($ch)
    }
    return $builder.ToString()
}

function Is-Dangerous-ForTopLevelDuplicates {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    if (-not $RelativePath.EndsWith(".txt")) {
        return $false
    }
    return @(
        "common/scripted_effects/",
        "common/scripted_triggers/",
        "common/decisions/",
        "common/modifiers/"
    ) | ForEach-Object { $RelativePath.Contains($_) } | Where-Object { $_ } | Select-Object -First 1
}

function Get-StructuralErrors {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$RelativePath
    )

    $lines = Get-Content $Path -Encoding UTF8
    $errors = New-Object System.Collections.Generic.List[string]
    $depth = 0
    $topLevelKeys = @{}
    $checkDuplicates = [bool](Is-Dangerous-ForTopLevelDuplicates -RelativePath $RelativePath)
    $lineNumber = 0

    foreach ($rawLine in $lines) {
        $lineNumber += 1
        if ($rawLine.StartsWith("<<<<<<<") -or $rawLine.StartsWith("=======") -or $rawLine.StartsWith(">>>>>>>")) {
            $errors.Add(
                ("In {0} around line {1}: found a git merge conflict marker (<<<<<<<, =======, or >>>>>>>). Please resolve the conflict and remove markers." -f $RelativePath, $lineNumber)
            )
        }

        $line = Strip-Comment -Line $rawLine
        $opens = ([regex]::Matches($line, "\{")).Count
        $closes = ([regex]::Matches($line, "\}")).Count

        if ($checkDuplicates -and $depth -eq 0) {
            $m = [regex]::Match($line, "^\s*([A-Za-z0-9_.:\-]+)\s*=\s*\{")
            if ($m.Success) {
                $key = $m.Groups[1].Value
                if (-not $topLevelKeys.ContainsKey($key)) {
                    $topLevelKeys[$key] = $lineNumber
                } else {
                    $firstSeen = $topLevelKeys[$key]
                    $errors.Add(
                        ("In {0} around line {1}: duplicate top-level key '$key'. It was first defined around line {2}. This can silently overwrite logic in scripted files." -f $RelativePath, $lineNumber, $firstSeen)
                    )
                }
            }
        }

        $depth += ($opens - $closes)
        if ($depth -lt 0) {
            $errors.Add(("In {0} around line {1}: found '}}' without matching '{{' earlier in the file." -f $RelativePath, $lineNumber))
            $depth = 0
        }
    }

    if ($depth -ne 0) {
        $errors.Add(("In {0}: braces look unbalanced (net open braces: {1}). Check for a missing '{{' or '}}' near the end of the file." -f $RelativePath, $depth))
    }

    return $errors
}

$data = Get-Content $profilePath -Raw -Encoding UTF8 | ConvertFrom-Json
$name = if ($data.name) { [string]$data.name } else { [System.IO.Path]::GetFileNameWithoutExtension($profilePath) }

Write-Output "Running smoke profile: $name"
$errors = New-Object System.Collections.Generic.List[string]
$step = 0

foreach ($item in @($data.require_patterns)) {
    $step += 1
    $desc = [string]$item.description
    $regex = New-Object System.Text.RegularExpressions.Regex($item.pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $matched = $false

    Write-Output "[$step] require: $desc"
    foreach ($pathRel in @($item.paths)) {
        $path = Join-Path $repoRoot ([string]$pathRel)
        if (-not (Test-Path $path)) {
            $errors.Add("require '$desc': missing file $pathRel")
            continue
        }

        if ($regex.IsMatch((Read-Text -Path $path))) {
            $matched = $true
        }
    }

    if (-not $matched) {
        $errors.Add("require '$desc': pattern not found in any listed file")
    }
}

foreach ($item in @($data.require_all_patterns)) {
    $step += 1
    $desc = [string]$item.description
    $patterns = @($item.patterns)
    $existingPaths = New-Object System.Collections.Generic.List[string]

    Write-Output "[$step] require_all: $desc"
    foreach ($pathRel in @($item.paths)) {
        $path = Join-Path $repoRoot ([string]$pathRel)
        if (-not (Test-Path $path)) {
            $errors.Add("require_all '$desc': missing file $pathRel")
            continue
        }
        $existingPaths.Add($path)
    }

    $subIdx = 0
    foreach ($patternRaw in $patterns) {
        $subIdx += 1
        $regex = New-Object System.Text.RegularExpressions.Regex([string]$patternRaw, [System.Text.RegularExpressions.RegexOptions]::Multiline)
        $matched = $false

        foreach ($path in $existingPaths) {
            if ($regex.IsMatch((Read-Text -Path $path))) {
                $matched = $true
                break
            }
        }

        if (-not $matched) {
            $errors.Add("require_all '$desc': subpattern #$subIdx not found in any listed file; pattern='$patternRaw'")
        }
    }
}

foreach ($item in @($data.forbid_patterns)) {
    $step += 1
    $desc = [string]$item.description
    $regex = New-Object System.Text.RegularExpressions.Regex($item.pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)

    Write-Output "[$step] forbid: $desc"
    foreach ($pathRel in @($item.paths)) {
        $path = Join-Path $repoRoot ([string]$pathRel)
        if (-not (Test-Path $path)) {
            $errors.Add("forbid '$desc': missing file $pathRel")
            continue
        }

        if ($regex.IsMatch((Read-Text -Path $path))) {
            $errors.Add("forbid '$desc': forbidden pattern found in $pathRel")
        }
    }
}

if (@($data.structural_checks).Count -gt 0) {
    $step += 1
    Write-Output "[$step] structural: lightweight scripted-file checks"
    foreach ($pathRel in @($data.structural_checks)) {
        $path = Join-Path $repoRoot ([string]$pathRel)
        if (-not (Test-Path $path)) {
            $errors.Add("structural check: missing file $pathRel")
            continue
        }
$relativePath = Get-RelativePath -From $repoRoot -To $path
        if (-not $relativePath) { continue }
        foreach ($structuralError in @(Get-StructuralErrors -Path $path -RelativePath $relativePath)) {
            $errors.Add($structuralError)
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "Smoke profile failed:"
    foreach ($error in $errors) {
        Write-Output " - $error"
    }
    throw "Smoke profile failed."
}

Write-Output "Smoke profile passed."
