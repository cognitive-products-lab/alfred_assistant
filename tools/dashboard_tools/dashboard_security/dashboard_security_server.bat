:: PROJECT  : ALFRED
:: BLOCK    : DASHBOARD
:: FILE     : tools/dashboard_tools/dashboard_security/dashboard_security_server.bat
:: ROLE     : Lance dashboard_security.py puis ouvre dashboard_security.html
:: VERSION  : V1.0
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_security\dashboard_security_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard SECURITY - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Mise a jour de dashboard_security.json ...
python tools\dashboard_tools\dashboard_security\dashboard_security.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : dashboard_security.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Lancement du serveur HTTP sur le port 8000 ...
start "ALFRED HTTP Server" python -m http.server 8000

timeout /t 2 /nobreak >nul

echo [ALFRED] Ouverture du dashboard ...
start "" "http://localhost:8000/dashboard/dashboard_security/dashboard_security.html"

echo.
echo [ALFRED] Dashboard pret :
echo [ALFRED] http://localhost:8000/dashboard/dashboard_security/dashboard_security.html
echo.
echo [ALFRED] Ferme la fenetre serveur pour arreter.
pause
