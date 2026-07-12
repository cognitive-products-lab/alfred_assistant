:: PROJECT  : ALFRED
:: BLOCK    : Bloc 11.05 — Gouvernance data
:: FILE     : tools/dashboard_tools/dashboard_quality_data/dashboard_quality_data_server.bat
:: ROLE     : Lance update_quality_data_dashboard.py puis ouvre dashboard_quality_data_dynamique.html
:: VERSION  : V1.0
:: STATUS   : ACTIVE
::
:: ⚠️ DASHBOARD INTERNE — ne servir que sur localhost, ne jamais exposer ce port publiquement.
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_quality_data\dashboard_quality_data_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard QUALITE DATA [INTERNE] - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Mise a jour de dashboard_quality_data.json ...
python tools\dashboard_tools\dashboard_quality_data\update_quality_data_dashboard.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : update_quality_data_dashboard.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Lancement du serveur HTTP local sur le port 8010 ...
start "ALFRED HTTP Server" python -m http.server 8010

timeout /t 2 /nobreak >nul

echo [ALFRED] Ouverture du dashboard (localhost uniquement) ...
start "" "http://localhost:8010/dashboard/dashboard_quality_data/dashboard_quality_data_dynamique.html"

echo.
echo [ALFRED] Dashboard pret (INTERNE - ne pas exposer) :
echo [ALFRED] http://localhost:8010/dashboard/dashboard_quality_data/dashboard_quality_data_dynamique.html
echo.
echo [ALFRED] Ferme la fenetre serveur pour arreter.
pause
