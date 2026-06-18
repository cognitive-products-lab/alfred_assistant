@echo off
:: ============================================================
:: PROJECT  : ALFRED / Cognitive Products Lab
:: BLOCK    : B20 — Sécurité, Gouvernance & Conformité
:: SCRIPT   : complete_vlan.bat
:: TYPE     : Launcher script
:: VERSION  : V1.0
:: CREATED  : 2026-06-18
:: ============================================================
title ALFRED — VLAN Validation & Finalisation
cd /d "%~dp0\.."
echo.
echo ============================================================
echo   ALFRED — VLAN : Validation et finalisation ISO-20
echo   Cognitive Products Lab — B20 Securite
echo ============================================================
echo.
echo PREALABLE : Implémenter le VLAN physiquement
echo   1. SG108E — Configurer VLANs 10 / 20 / 30 (802.1Q)
echo   2. ER605  — Creer sous-interfaces VLAN + règles inter-VLAN
echo   3. PC Alfred — Brancher sur port VLAN10
echo   (Référence : docs/smsi/vlan_config.md)
echo.
pause
py -3 scripts\complete_vlan.py
pause
