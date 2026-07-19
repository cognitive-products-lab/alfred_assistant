:: PROJECT  : ALFRED
:: BLOCK    : B20
:: FILE     : tools/dashboard_tools/run_all_dashboard_tools.bat
:: ROLE     : Lanceur MANUEL complet — regenere TOUS les dashboards
::            (dashboard_data, gouvernance, conformite, vulnerabilites,
::            risk_impact, security, tests, knowledge registry + dashboard,
::            quality data) puis synchronise ALFRED_PC -> ALFRED_WEB (git push).
:: VERSION  : V1.0
:: STATUS   : STABLE
::
:: ATTENTION : la derniere etape (sync_dashboards.py) pousse automatiquement
:: sur GitHub et declenche un deploiement Render. L'etape "Tests securite"
:: relance la suite pytest security_tests/ et peut prendre plusieurs minutes.
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\run_all_dashboard_tools.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ======================================================
echo [ALFRED]  Regeneration complete de TOUS les dashboards + sync
echo [ALFRED] ======================================================
echo.

python tools\dashboard_tools\run_all_dashboard_tools.py
if errorlevel 1 (
    echo [ALFRED] ATTENTION : une ou plusieurs etapes ont echoue. Voir details ci-dessus.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Termine.
pause
