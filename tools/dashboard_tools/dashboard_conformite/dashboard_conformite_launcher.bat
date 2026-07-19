:: PROJECT  : ALFRED
:: BLOCK    : B20
:: FILE     : tools/dashboard_tools/dashboard_conformite/dashboard_conformite_launcher.bat
:: ROLE     : Lance update_conformite_data.py (regenere dashboard_conformite.json)
:: VERSION  : V1.0
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_conformite\dashboard_conformite_launcher.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard CONFORMITE - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Mise a jour de dashboard_conformite.json ...
python tools\dashboard_tools\dashboard_conformite\update_conformite_data.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : update_conformite_data.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Termine.
pause
