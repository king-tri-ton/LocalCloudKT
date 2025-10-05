@echo off
call LCKT_stop.bat
timeout /t 2 >nul
call LCKT_start.bat
