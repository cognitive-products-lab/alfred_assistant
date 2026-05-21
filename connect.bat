@echo off
:: ============================================================
:: ALFRED — connect.bat
:: Raccourci de navigation rapide vers le projet ALFRED_PC
:: Double-cliquer OU lancer depuis ConnectBot/SSH
:: ============================================================
cd /d D:\PROJET_ALFRED\ALFRED_PC
cmd /k "echo. && echo [ALFRED] Dossier projet : %CD% && echo [ALFRED] Pour lancer : python src\main.py && echo."
