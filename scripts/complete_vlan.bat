@echo off
chcp 65001 >nul
:: ============================================================
:: PROJECT  : ALFRED / Cognitive Products Lab
:: BLOCK    : B20 - Securite, Gouvernance & Conformite
:: SCRIPT   : complete_vlan.bat
:: VERSION  : V1.2
:: CREATED  : 2026-06-18
:: ============================================================
title ALFRED - VLAN Validation ISO-20
cd /d "%~dp0\.."
echo.
echo ============================================================
echo   ALFRED - VLAN : Validation et finalisation ISO-20
echo   Cognitive Products Lab - B20 Securite
echo ============================================================
echo.
echo Choisir le mode :
echo   [1] PLANIFIE  - Architecture documentee, implementation Q3 2026
echo                   (pas de tests reseau - mode actuel)
echo   [2] VALIDE    - VLAN physiquement implemente, tests reseau actifs
echo.
set /p mode="Votre choix (1 ou 2) : "
echo.
if "%mode%"=="1" (
    py -3 scripts\complete_vlan.py --planifie
) else if "%mode%"=="2" (
    py -3 scripts\complete_vlan.py
) else (
    echo Choix invalide. Relancer le script.
)
pause
