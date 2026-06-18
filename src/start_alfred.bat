:: FUNCTION : STARTUP
:: ROLE     : Batch launcher script

:: PROJECT : ALFRED
:: BLOCK   : GLOBAL
:: FILE    : start_alfred.bat
:: VERSION : V1.0
:: STATUS  : ACTIVE

@echo off
title ALFRED Assistant
color 0D
mode con: cols=90 lines=30
chcp 65001 >nul

:: Fix encodage Unicode Windows
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo ==================================================
echo              ALFRED - INITIALISATION
echo ==================================================
echo.

echo Lancement du systeme...
timeout /t 1 >nul

cd /d D:\PROJET_ALFRED\ALFRED_PC
python src\alfred_with_ui.py

echo.
echo ==================================================
echo              ALFRED EST FERME
echo ==================================================
pause