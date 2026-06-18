:: PROJECT  : ALFRED
:: BLOCK    : B20
:: FILE     : tools/dashboard_tools/dashboard_gouvernance/dashboard_gouvernance_server.bat
:: ROLE     : Lance dashboard_gouvernance.py puis ouvre dashboard_gouvernance_dynamique.html
:: VERSION  : V1.0
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_gouvernance\dashboard_gouvernance_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard GOUVERNANCE 360° - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Mise a jour de dashboard_gouvernance.json ...
python tools\dashboard_tools\dashboard_gouvernance\dashboard_gouvernance.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : dashboard_gouvernance.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Lancement du serveur HTTP sur le port 8000 ...
start "ALFRED HTTP Server" python -m http.server 8000

timeout /t 2 /nobreak >nul

echo [ALFRED] Ouverture du dashboard ...
start "" "http://localhost:8000/dashboard/dashboard_gouvernance/dashboard_gouvernance_dynamique.html"

echo.
echo [ALFRED] Dashboard pret :
echo [ALFRED] http://localhost:8000/dashboard/dashboard_gouvernance/dashboard_gouvernance_dynamique.html
echo.
echo [ALFRED] Ferme la fenetre serveur pour arreter.
pause
