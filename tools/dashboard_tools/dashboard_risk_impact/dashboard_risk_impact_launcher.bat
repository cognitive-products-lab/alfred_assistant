:: PROJECT  : ALFRED
:: BLOCK    : B20
:: FILE     : tools/dashboard_tools/dashboard_risk_impact/dashboard_risk_impact_launcher.bat
:: ROLE     : Lance update_risk_impact_data.py (regenere dashboard_risk_impact.json)
:: VERSION  : V1.0
:: STATUS   : STABLE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_risk_impact\dashboard_risk_impact_launcher.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard RISK IMPACT - Lancement
echo [ALFRED] ================================================
echo.

echo [ALFRED] Mise a jour de dashboard_risk_impact.json ...
python tools\dashboard_tools\dashboard_risk_impact\update_risk_impact_data.py
if errorlevel 1 (
    echo [ALFRED] ERREUR : update_risk_impact_data.py a echoue.
    pause
    exit /b 1
)

echo.
echo [ALFRED] Termine.
pause
