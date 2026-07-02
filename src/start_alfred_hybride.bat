:: FUNCTION : STARTUP
:: ROLE     : Batch launcher script — mode perso + bouton "Mode Pro" (2e fenetre parallele)

:: PROJECT : ALFRED
:: BLOCK   : Bloc 12 — Collaboration professionnelle (dashboard : B10)
:: FILE    : start_alfred_hybride.bat
:: VERSION : V1.0
:: STATUS  : STABLE

@echo off
title ALFRED Hybride (perso + pro)
color 0D
mode con: cols=90 lines=30
chcp 65001 >nul

:: Fix encodage Unicode Windows
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo ==================================================
echo         ALFRED HYBRIDE - INITIALISATION
echo   (mode perso + bouton "Mode Pro" pour ouvrir
echo    une seconde fenetre ALFRED CPL en parallele)
echo ==================================================
echo.

echo Lancement du systeme...
timeout /t 1 >nul

cd /d D:\PROJET_ALFRED\ALFRED_PC
python src\alfred_with_ui.py --mode perso --hybrid

echo.
echo ==================================================
echo              ALFRED EST FERME
echo ==================================================
pause
