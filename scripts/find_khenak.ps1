$text = Get-Content "C:\Users\User\Documents\GitHub\My-Anbennar\missions\Verne_Missions.txt" -Raw -Encoding UTF8
$lines = $text.Split("`n")
$inMission = $false
$currentMission = ""
foreach($line in $lines) {
    if($line -match '^\s*(A33_\w+)\s*=\s*\{?\s*$') {
        $inMission = $true
        $currentMission = $Matches[1]
    }
    if($inMission -and ($line -like '*khenak*' -or $line -like '*Khenak*')) {
        Write-Host "$currentMission : $($line.Trim())"
    }
    if($inMission -and $line -match '^\s*\}\s*$') {
        $inMission = $false
    }
}
