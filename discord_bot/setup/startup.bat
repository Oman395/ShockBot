@echo off
setlocal EnableExtensions DisableDelayedExpansion

set "StartupFolder="
for /F "skip=1 tokens=1,2*" %%I in ('%SystemRoot%\System32\reg.exe QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Startup 2^>nul') do if /I "%%I" == "Startup" if not "%%~K" == "" if "%%J" == "REG_SZ" (set "StartupFolder=%%~K") else if "%%J" == "REG_EXPAND_SZ" call set "StartupFolder=%%~K"
if not defined StartupFolder for /F "skip=1 tokens=1,2*" %%I in ('%SystemRoot%\System32\reg.exe QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Startup 2^>nul') do if /I "%%I" == "Startup" if not "%%~K" == "" if "%%J" == "REG_SZ" (set "StartupFolder=%%~K") else if "%%J" == "REG_EXPAND_SZ" call set "StartupFolder=%%~K"
if not defined StartupFolder set "StartupFolder=\"
if "%StartupFolder:~-1%" == "\" set "StartupFolder=%StartupFolder:~0,-1%"
if not defined StartupFolder set "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

echo Startup folder of current user is:
echo "%StartupFolder%"

move "main_shortcut.lnk" "%StartupFolder%"

endlocal