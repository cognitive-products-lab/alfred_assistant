@echo off
chcp 65001 >nul
title ALFRED — Dashboard Sécurité

REM ============================================================
REM ALFRED — Dashboard sécurité (lanceur rapide Windows)
REM Double-clic ou appel depuis l'explorateur
REM ============================================================

cd /d "%~dp0\.."

echo.
echo ============================================================
echo   ALFRED — Dashboard de Securite
echo ============================================================
echo.

REM -- Détection environnement virtuel
if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activation venv...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activation venv...
    call venv\Scripts\activate.bat
) else (
    echo [WARN] Aucun venv detecte — Python systeme utilise
)

echo.
echo [1/3] Rapport terminal...
echo ============================================================
python src\security\security_dashboard.py
echo.

echo [2/3] Generation rapport HTML...
echo ============================================================
python -c "import sys; sys.path.insert(0,'%CD%'); from dotenv import load_dotenv; load_dotenv('.env'); from src.security.html_report import generate_html_report; from pathlib import Path; p=generate_html_report(Path('demo/alfred_security_report.html')); print('[OK] Rapport HTML:', p)"

echo.
echo [3/3] Ouverture dans le navigateur...
if exist "demo\alfred_security_report.html" (
    start "" "demo\alfred_security_report.html"
    echo [OK] Navigateur ouvert
) else (
    echo [WARN] Fichier HTML non trouve
)

echo.
echo ============================================================
echo   ALFRED — Local-First ^| Zero Trust ^| Security by Design
echo ============================================================
echo.
pause
