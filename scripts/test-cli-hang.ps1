$errLog = [System.IO.Path]::GetTempFileName()
$proc = Start-Process -FilePath "node" -ArgumentList "C:\Users\User\AppData\Roaming\npm\node_modules\openclaw\openclaw.mjs","status" -NoNewWindow -PassThru -RedirectStandardError $errLog
Start-Sleep 3
$tcpConns = Get-NetTCPConnection -OwningProcess $proc.Id -ErrorAction SilentlyContinue | Where-Object { $_.State -ne 'TimeWait' }
if ($tcpConns) {
    $tcpConns | Format-Table LocalAddress,LocalPort,RemoteAddress,RemotePort,State -AutoSize
} else {
    Write-Host "No TCP connections from openclaw process"
}
$proc.Kill()
$errOut = Get-Content $errLog -ErrorAction SilentlyContinue | Select-Object -First 5
Write-Host "STDERR: $errOut"
