:: PROJECT  : ALFRED
:: BLOCK    : DASHBOARD
:: FILE     : tools/dashboard_tools/dashboard_data/dashboard_data_server.bat
:: ROLE     : Lance update_dashboard_data.py puis ouvre ALFRED_DASHBOARD_DYNAMIC.html
:: VERSION  : V1.1
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_data\dashboard_data_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard DATA - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Mise a jour de dashboard_data.json ...
python tools\dashboard_tools\dashboard_data\update_dashboard_data.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : update_dashboard_data.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Lancement du serveur HTTP sur le port 8000 ...
start "ALFRED HTTP Server" python -m http.server 8000

timeout /t 2 /nobreak >nul

echo [ALFRED] Ouverture du dashboard ...
start "" "http://localhost:8000/dashboard/dashboard_data/ALFRED_DASHBOARD_DYNAMIC.html"

echo.
echo [ALFRED] Dashboard pret :
echo [ALFRED] http://localhost:8000/dashboard/dashboard_data/ALFRED_DASHBOARD_DYNAMIC.html
echo.
echo [ALFRED] Ferme la fenetre serveur pour arreter.
pause
