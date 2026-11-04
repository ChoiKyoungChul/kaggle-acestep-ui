@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-FullPackage.ps1"
set "INSTALL_EXIT=%ERRORLEVEL%"
pause >nul
exit /b %INSTALL_EXIT%
