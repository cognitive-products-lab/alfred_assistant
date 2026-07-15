:: PROJECT  : ALFRED
:: BLOCK    : B24
:: FUNCTION : 24.02 — Intégration API compagnon
:: FILE     : start_companion_api.bat
:: ROLE     : Lance l'API compagnon locale (interface/companion_api.py) pour
::            le PoC ALFRED_ANDROID — écoute sur 0.0.0.0:8420.
:: VERSION  : V1.0
:: STATUS   : ACTIVE
::
:: ⚠️ Réseau local uniquement — pas de HTTPS, jeton statique (COMPANION_API_TOKEN
::    dans .env). Ne jamais exposer ce port au-delà du réseau domestique.
::
:: Usage : double-clic ou depuis PowerShell
::   cd D:\PROJET_ALFRED\ALFRED_PC
::   start_companion_api.bat

@echo off
cd /d D:\PROJET_ALFRED\ALFRED_PC

echo.
echo [ALFRED] ================================================
echo [ALFRED]  API Compagnon (Bloc 24) - Lancement
echo [ALFRED] ================================================
echo.

if not exist ".env" (
    echo [ALFRED] ERREUR : .env introuvable. Copier .env.example en .env et
    echo [ALFRED] renseigner COMPANION_API_TOKEN avant de relancer.
    pause
    exit /b 1
)

echo [ALFRED] Demarrage sur http://0.0.0.0:8420 ...
echo [ALFRED] Emulateur Android : http://10.0.2.2:8420
echo [ALFRED] Telephone physique (meme Wi-Fi) : http://^<IP locale du PC^>:8420
echo.
python interface\companion_api.py

pause
