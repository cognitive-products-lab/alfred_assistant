@echo off
REM ============================================================
REM  ALFRED — Dashboard Gouvernance CPL
REM  Lance la mise à jour des données + serveur local + navigateur
REM  Usage : double-clic sur ce fichier depuis Windows
REM ============================================================

TITLE ALFRED - Dashboard Gouvernance

echo.
echo ============================================================
echo  ALFRED — Dashboard Gouvernance CPL
echo  Cognitive Products Lab
echo ============================================================
echo.

REM Aller à la racine du projet (2 niveaux au-dessus de tools/dashboard_tools/dashboard_gouvernance/)
cd /d "%~dp0..\..\..\"
echo [INFO] Dossier racine : %CD%

echo.
echo [1/3] Mise a jour des donnees de gouvernance...
python tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py
if errorlevel 1 (
    echo [ERREUR] Echec de la mise a jour des donnees.
    pause
    exit /b 1
)

echo.
echo [2/3] Verification du serveur local (port 8001)...
netstat -ano | findstr ":8001" >nul 2>&1
if %errorlevel% == 0 (
    echo [INFO] Serveur deja actif sur le port 8001.
) else (
    echo [INFO] Demarrage du serveur HTTP sur le port 8001...
    start "ALFRED Gouvernance Server" python -m http.server 8001
    timeout /t 2 /nobreak >nul
)

echo.
echo [3/3] Ouverture du dashboard dans le navigateur...
start "" "http://localhost:8001/dashboard/dashboard_gouvernance/dashboard_gouvernance.html"

echo.
echo ============================================================
echo  Dashboard accessible : http://localhost:8001/dashboard/dashboard_gouvernance/dashboard_gouvernance.html
echo  Appuyer sur une touche pour fermer cette fenetre...
echo ============================================================
pause >nul
