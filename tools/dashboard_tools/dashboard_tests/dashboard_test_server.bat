:: PROJECT  : ALFRED
:: BLOCK    : DASHBOARD
:: FILE     : tools/dashboard_tools/dashboard_tests/dashboard_test_server.bat
:: ROLE     : Lance dashboard_test.py --serve : tests + sauvegarde JSON + ouverture navigateur
:: VERSION  : V2.0
:: STATUS   : ACTIVE
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   tools\dashboard_tools\dashboard_tests\dashboard_test_server.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  Dashboard TESTS - Lancement V2
echo [ALFRED] ================================================
echo.

echo [ALFRED] Execution des tests + ouverture navigateur ...
python tools\dashboard_tools\dashboard_tests\dashboard_test.py --serve

echo.
pause
