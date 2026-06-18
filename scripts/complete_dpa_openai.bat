@echo off
:: ============================================================
:: PROJECT  : ALFRED / Cognitive Products Lab
:: BLOCK    : B20 — Sécurité, Gouvernance & Conformité
:: SCRIPT   : complete_dpa_openai.bat
:: TYPE     : Launcher script
:: VERSION  : V1.0
:: CREATED  : 2026-06-18
:: ============================================================
title ALFRED — DPA OpenAI Finalisation
cd /d "%~dp0\.."
echo.
echo ============================================================
echo   ALFRED — DPA OpenAI : Finalisation automatique
echo   Cognitive Products Lab — B20 Securite
echo ============================================================
echo.
echo PREALABLE : Accepter le DPA sur platform.openai.com
echo   1. Aller sur https://platform.openai.com/account/organization
echo   2. Section Legal / Data Processing Addendum
echo   3. Cliquer "Accept"
echo.
pause
py -3 scripts\complete_dpa_openai.py
pause
