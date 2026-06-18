:: PROJECT  : ALFRED
:: BLOCK    : DASHBOARD
:: FILE     : tools/dashboard_tools/dashboard_tests/dashboard_test_server.bat
:: ROLE     : Lance run_all_tests.py (tous les tests) puis met a jour le dashboard et ouvre le navigateur
:: VERSION  : V3.0
:: UPDATED  : 2026-06-05
:: STATUS   : ACTIVE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_tests\dashboard_test_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Run All Tests + Dashboard - V3.0
echo [ALFRED] ================================================
echo.

echo [ALFRED] Etape 1/2 - Execution de tous les tests ALFRED...
echo.
python tests\run_all_tests.py
if errorlevel 1 (
    echo.
    echo [ALFRED] AVERT : Certains tests ont echoue - dashboard mis a jour quand meme.
)

echo.
echo [ALFRED] Etape 2/2 - Ouverture du dashboard HTML...
echo.
python tools\dashboard_tools\dashboard_tests\dashboard_test.py --serve-only

echo.
pause
