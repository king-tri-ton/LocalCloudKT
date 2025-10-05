@echo off
echo Остановка LocalCloudKT...
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'pythonw.exe' -and ($_.CommandLine -match 'app.py') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo LocalCloudKT остановлен.
pause
