@echo off
cd /d C:\Python\LocalCloud

REM Создаем папку для логов, если нет
if not exist logs mkdir logs

echo Запуск LocalCloudKT...
start "" pythonw.exe -u app.py > logs\server.log 2>&1
exit
