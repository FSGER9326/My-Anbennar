param(
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repoRoot

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    $output = & git @Arguments 2>&1
    [pscustomobject]@{
        Code = $LASTEXITCODE
        Output = (@($output) -join "`n").Trim()
    }
}

function Write-Status {
    param(
        [Parameter(Mandatory = $true)][string]$Level,
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Message
    )
    Write-Output ("[{0}] {1}: {2}" -f $Level, $Label, $Message)
}

$warnings = 0
$errors = 0

Write-Output "Repo doctor report"
Write-Output "=================="

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Status -Level "OK" -Label "git" -Message "git is available"
} else {
    Write-Status -Level "ERR" -Label "git" -Message "git is not on PATH"
    $errors++
}

foreach ($tool in @("powershell", "python", "python3", "bash")) {
    $command = Get-Command $tool -ErrorAction SilentlyContinue
    if ($command) {
        Write-Status -Level "OK" -Label $tool -Message $command.Source
    } else {
        Write-Status -Level "WARN" -Label $tool -Message "not found on PATH"
        $warnings++
    }
}

$branchResult = Invoke-Git -Arguments @("branch", "--show-current")
$branch = $branchResult.Output
if ($branchResult.Code -eq 0 -and -not [string]::IsNullOrWhiteSpace($branch)) {
    Write-Status -Level "OK" -Label "branch" -Message $branch
} else {
    Write-Status -Level "ERR" -Label "branch" -Message "could not determine current branch"
    $errors++
}

$dirtyResult = Invoke-Git -Arguments @("status", "--porcelain")
if ($dirtyResult.Code -eq 0 -and [string]::IsNullOrWhiteSpace($dirtyResult.Output)) {
    Write-Status -Level "OK" -Label "working-tree" -Message "clean"
} elseif ($dirtyResult.Code -eq 0) {
    Write-Status -Level "WARN" -Label "working-tree" -Message "has uncommitted changes"
    $warnings++
} else {
    Write-Status -Level "ERR" -Label "working-tree" -Message "could not inspect working tree"
    $errors++
}

$upstreamResult = Invoke-Git -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
if ($upstreamResult.Code -eq 0 -and -not [string]::IsNullOrWhiteSpace($upstreamResult.Output)) {
    Write-Status -Level "OK" -Label "upstream" -Message $upstreamResult.Output
    $countResult = Invoke-Git -Arguments @("rev-list", "--left-right", "--count", "HEAD...$($upstreamResult.Output)")
    if ($countResult.Code -eq 0 -and -not [string]::IsNullOrWhiteSpace($countResult.Output)) {
        $parts = $countResult.Output -split "\s+"
        if ($parts.Length -ge 2) {
            $behind = [int]$parts[0]
            $ahead = [int]$parts[1]
            if ($ahead -eq 0 -and $behind -eq 0) {
                Write-Status -Level "OK" -Label "sync" -Message "local branch matches upstream"
            } else {
                Write-Status -Level "WARN" -Label "sync" -Message "ahead $ahead, behind $behind"
                $warnings++
            }
        }
    }
} else {
    Write-Status -Level "WARN" -Label "upstream" -Message "no upstream branch configured"
    $warnings++
}

$gitDir = Join-Path $repoRoot ".git"
if (Test-Path (Join-Path $gitDir "MERGE_HEAD")) {
    Write-Status -Level "WARN" -Label "merge-state" -Message "merge in progress"
    $warnings++
} else {
    Write-Status -Level "OK" -Label "merge-state" -Message "no merge in progress"
}

if ((Test-Path (Join-Path $gitDir "rebase-apply")) -or (Test-Path (Join-Path $gitDir "rebase-merge"))) {
    Write-Status -Level "WARN" -Label "rebase-state" -Message "rebase in progress"
    $warnings++
} else {
    Write-Status -Level "OK" -Label "rebase-state" -Message "no rebase in progress"
}

$hooksPathResult = Invoke-Git -Arguments @("config", "--get", "core.hooksPath")
if ($hooksPathResult.Code -eq 0 -and $hooksPathResult.Output -eq ".githooks") {
    Write-Status -Level "OK" -Label "hooks-path" -Message ".githooks installed"
} elseif ($hooksPathResult.Code -eq 0 -and -not [string]::IsNullOrWhiteSpace($hooksPathResult.Output)) {
    Write-Status -Level "WARN" -Label "hooks-path" -Message "custom hooksPath is '$($hooksPathResult.Output)'"
    $warnings++
} else {
    Write-Status -Level "WARN" -Label "hooks-path" -Message "hooks not installed (run install_git_hooks)"
    $warnings++
}

foreach ($rel in @(
    ".githooks/pre-commit",
    ".githooks/pre-push",
    "scripts/verne_smoke_checks.ps1",
    "scripts/smart_smoke_router.ps1",
    "scripts/repo_doctor.ps1"
)) {
    $path = Join-Path $repoRoot $rel
    if (Test-Path $path) {
        Write-Status -Level "OK" -Label $rel -Message "present"
    } else {
        Write-Status -Level "WARN" -Label $rel -Message "missing"
        $warnings++
    }
}

if ($warnings -gt 0 -or $errors -gt 0) {
    Write-Output ""
    Write-Output "Recommended next actions:"
    if ($branch -eq "main") {
        Write-Output "- Stay on small commits and run verne_smoke_checks before push."
    }
    Write-Output "- Install Git hooks if you want automatic checks before commit/push."
    Write-Output "- Run text_hygiene_guard if docs or localisation text starts looking strange."
}

if ($Strict -and ($warnings -gt 0 -or $errors -gt 0)) {
    exit 1
}
