:: FUNCTION : STARTUP
:: ROLE     : Batch launcher script — mode pro uniquement (produit ALFRED CPL)

:: PROJECT : ALFRED
:: BLOCK   : Bloc 12 — Collaboration professionnelle (dashboard : B10)
:: FILE    : start_alfred_cpl.bat
:: VERSION : V1.0
:: STATUS  : STABLE

@echo off
title ALFRED CPL
color 0D
mode con: cols=90 lines=30
chcp 65001 >nul

:: Fix encodage Unicode Windows
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo ==================================================
echo            ALFRED CPL - INITIALISATION
echo        (collaborateur professionnel augmente
echo         - pour tester et valider le produit)
echo ==================================================
echo.

echo Lancement du systeme...
timeout /t 1 >nul

cd /d D:\PROJET_ALFRED\ALFRED_PC
python src\alfred_with_ui.py --mode pro

echo.
echo ==================================================
echo            ALFRED CPL EST FERME
echo ==================================================
pause
