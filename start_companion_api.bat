:: FUNCTION : STARTUP
:: ROLE     : Batch launcher script — API compagnon locale (client Android PoC)

:: PROJECT : ALFRED
:: BLOCK   : Client compagnon Android (PoC)
:: FILE    : start_companion_api.bat
:: VERSION : V0.1 (PoC)
:: STATUS  : POC

@echo off
title ALFRED - API Compagnon
color 0B
mode con: cols=90 lines=30
chcp 65001 >nul

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo ==================================================
echo       ALFRED - API COMPAGNON (client Android)
echo ==================================================
echo.

cd /d D:\PROJET_ALFRED\ALFRED_PC
python interface\companion_api.py

echo.
echo ==================================================
echo       API COMPAGNON ARRETEE
echo ==================================================
pause
