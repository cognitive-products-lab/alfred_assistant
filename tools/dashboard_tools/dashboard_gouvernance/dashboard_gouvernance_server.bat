:: PROJECT  : ALFRED / Cognitive Products Lab
:: BLOCK    : B20
:: FILE     : tools/dashboard_tools/dashboard_gouvernance/dashboard_gouvernance_server.bat
:: ROLE     : Recalcule les scores · Lance http.server 8001 · Ouvre index.html
:: VERSION  : V2.0 (port 8001 · nouveau dashboard conformité réglementaire)
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_gouvernance\dashboard_gouvernance_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard CONFORMITE REGLEMENTAIRE - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Recalcul des scores de conformite...
python tools\dashboard_tools\dashboard_gouvernance\update_gouvernance_data.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : update_gouvernance_data.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Lancement du serveur HTTP sur le port 8001 ...
start "ALFRED HTTP Server 8001" python -m http.server 8001

timeout /t 2 /nobreak >nul

echo [ALFRED] Ouverture du dashboard conformite ...
start "" "http://localhost:8001/dashboard/dashboard_gouvernance/index.html"

echo.
echo [ALFRED] Dashboard pret :
echo [ALFRED] http://localhost:8001/dashboard/dashboard_gouvernance/index.html
echo.
echo [ALFRED] Ferme la fenetre serveur pour arreter.
pause
