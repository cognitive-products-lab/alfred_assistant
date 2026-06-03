:: PROJECT  : ALFRED
:: BLOCK    : DASHBOARD
:: FILE     : tools/dashboard_tools/dashboard_tests/dashboard_test_server.bat
:: ROLE     : Lance dashboard_test.py puis ouvre dashboard_tests.html (dashboard_test.json)
:: VERSION  : V1.0
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_tests\dashboard_test_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard TESTS - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Generation de dashboard_tests.json ...
python tools\dashboard_tools\dashboard_tests\dashboard_test.py --json > dashboard\dashboard_tests\dashboard_test.json
if errorlevel 1 (
    echo [ALFRED] AVERTISSEMENT : certains tests ont echoue - JSON genere quand meme.
)

echo.
echo [ALFRED] Lancement du serveur HTTP sur le port 8000 ...
start "ALFRED HTTP Server" python -m http.server 8000

timeout /t 2 /nobreak >nul

echo [ALFRED] Ouverture du dashboard ...
start "" "http://localhost:8000/dashboard/dashboard_tests/dashboard_tests.html"

echo.
echo [ALFRED] Dashboard pret :
echo [ALFRED] http://localhost:8000/dashboard/dashboard_tests/dashboard_tests.html
echo.
echo [ALFRED] Ferme la fenetre serveur pour arreter.
pause
