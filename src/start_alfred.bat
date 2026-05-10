@echo off
title ALFRED Assistant
color 0D
mode con: cols=90 lines=30

echo.
echo ==================================================
echo              ALFRED - INITIALISATION
echo ==================================================
echo.

echo Lancement du systeme...
timeout /t 1 >nul

cd /d D:\PROJET_ALFRED\ALFRED_PC
python src\main.py

echo.
echo Alfred est ferme.
pause