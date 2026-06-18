# ============================================================
# ALFRED - setup_minisforum_ms_s1_max.ps1
# Setup initial du Minisforum MS-S1 Max (Ryzen AI Max+ 395, 64Go/2To)
# comme machine de dev / serveur LLM local ALFRED
# ============================================================
# UTILISATION (PowerShell en administrateur recommande) :
#   .\setup_minisforum_ms_s1_max.ps1
#
# Etapes :
#   0. Installer les outils de base CPL (Python, Git, VS Code, gh,
#      Ollama, ffmpeg, 7-Zip, Windows Terminal) via
#      install_cpl_workstation_tools.ps1
#   1. Verifier Python 3.11+, Git, VS Code
#   2. Verifier Ollama, configurer OLLAMA_MODELS=D:\ALFRED\ollama\models
#   3. Cloner le depot ALFRED_PC (dev)
#   4. Creer le venv + installer requirements.txt
#   5. Telecharger les modeles Ollama a tester (70B/120B)
#   6. Lancer check_tools.ps1 pour validation finale
# ============================================================

$ErrorActionPreference = "Stop"

function Write-Step($title) {
    Write-Host ""
    Write-Host "==> $title" -ForegroundColor Cyan
}

function Test-Command($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

# ------------------------------------------------------------
# 0. Outils de base CPL (Python, Git, VS Code, gh, Ollama, ffmpeg...)
# ------------------------------------------------------------
Write-Step "0/6 - Outils de base Cognitive Products Lab"

$baseTools = Join-Path $PSScriptRoot "install_cpl_workstation_tools.ps1"
if (Test-Path $baseTools) {
    & $baseTools
} else {
    Write-Host "  [AVERT] install_cpl_workstation_tools.ps1 introuvable - etape ignoree" -ForegroundColor Yellow
}

# ------------------------------------------------------------
# 1. Outils systeme
# ------------------------------------------------------------
Write-Step "1/6 - Verification Python / Git / VS Code"

if (Test-Command "python") {
    Write-Host "  [OK] Python : $(python --version)" -ForegroundColor Green
} else {
    Write-Host "  [MANQUANT] Python 3.11+ -> https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "             (cocher 'Add python.exe to PATH' a l'installation)" -ForegroundColor Yellow
}

if (Test-Command "git") {
    Write-Host "  [OK] Git : $(git --version)" -ForegroundColor Green
} else {
    Write-Host "  [MANQUANT] Git -> https://git-scm.com/download/win" -ForegroundColor Red
}

if (Test-Command "code") {
    Write-Host "  [OK] VS Code : $(code --version | Select-Object -First 1)" -ForegroundColor Green
} else {
    Write-Host "  [MANQUANT] VS Code -> https://code.visualstudio.com/" -ForegroundColor Yellow
}

# ------------------------------------------------------------
# 2. Ollama
# ------------------------------------------------------------
Write-Step "2/6 - Ollama"

if (Test-Command "ollama") {
    Write-Host "  [OK] Ollama deja installe : $(ollama --version)" -ForegroundColor Green
} else {
    Write-Host "  [MANQUANT] Ollama -> https://ollama.com/download/windows" -ForegroundColor Yellow
    Write-Host "             Installer puis relancer ce script." -ForegroundColor Yellow
}

# Stocker les modeles sur D:\ALFRED (ALFRED CORE) plutot que C: (modeles 70-120B = 150-300 Go)
$ollamaModelsDir = "D:\ALFRED\ollama\models"
New-Item -ItemType Directory -Force -Path $ollamaModelsDir | Out-Null

if ($env:OLLAMA_MODELS -ne $ollamaModelsDir) {
    [System.Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $ollamaModelsDir, "User")
    $env:OLLAMA_MODELS = $ollamaModelsDir
    Write-Host "  [OK] Variable OLLAMA_MODELS definie sur $ollamaModelsDir" -ForegroundColor Green
    Write-Host "       (redemarrer Ollama / la session si deja installe pour qu'il la prenne en compte)" -ForegroundColor Yellow
} else {
    Write-Host "  [OK] OLLAMA_MODELS deja sur $ollamaModelsDir" -ForegroundColor Green
}

# ------------------------------------------------------------
# 3. Clone du depot ALFRED_PC
# ------------------------------------------------------------
Write-Step "3/6 - Depot ALFRED_PC"

$repoPath = "D:\PROJET_ALFRED\ALFRED_PC"
if (Test-Path $repoPath) {
    Write-Host "  [OK] Depot deja present : $repoPath" -ForegroundColor Green
} else {
    Write-Host "  Clonage du depot dans $repoPath ..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "D:\PROJET_ALFRED" | Out-Null
    git clone -b dev https://github.com/cognitive-products-lab/alfred_assistant.git $repoPath
}

Set-Location $repoPath

# ------------------------------------------------------------
# 4. Environnement virtuel Python
# ------------------------------------------------------------
Write-Step "4/6 - Environnement virtuel Python (.venv)"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "  [OK] .venv cree" -ForegroundColor Green
} else {
    Write-Host "  [OK] .venv deja present" -ForegroundColor Green
}

& ".venv\Scripts\python.exe" -m pip install --upgrade pip
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
Write-Host "  [OK] requirements.txt installes" -ForegroundColor Green

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "  [AVERT] .env cree depuis .env.example -> a completer avec les cles" -ForegroundColor Yellow
    } else {
        Write-Host "  [AVERT] .env absent et .env.example introuvable -> a creer manuellement" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [OK] .env present" -ForegroundColor Green
}

# ------------------------------------------------------------
# 5. Modeles Ollama a tester (70B / 120B)
# ------------------------------------------------------------
Write-Step "5/6 - Telechargement des modeles Ollama (peut prendre du temps)"

$models = @(
    "llama3.2",            # leger, deja utilise sur le PC actuel (reference de comparaison)
    "llama3.3:70b",        # excellent francais, ~42 Go RAM en Q4
    "qwen2.5:72b",         # tres bon multilingue/francais, ~45 Go RAM en Q4
    "command-r-plus:104b", # fort en RAG/contexte long, ~60 Go RAM en Q4
    "gpt-oss:120b"         # ~32 tok/s mesure sur Ryzen AI Max+ 395, ~65 Go RAM en Q4
)

if (Test-Command "ollama") {
    # Redemarrer le service Ollama pour qu'il prenne en compte OLLAMA_MODELS=$ollamaModelsDir
    Get-Process "ollama*" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3

    foreach ($model in $models) {
        Write-Host "  ollama pull $model" -ForegroundColor DarkCyan
        ollama pull $model
    }
} else {
    Write-Host "  [SKIP] Ollama non installe - pull manuel apres installation :" -ForegroundColor Yellow
    foreach ($model in $models) {
        Write-Host "    ollama pull $model" -ForegroundColor DarkGray
    }
}

# ------------------------------------------------------------
# 6. Verification finale
# ------------------------------------------------------------
Write-Step "6/6 - Verification finale (check_tools.ps1)"

if (Test-Path ".\scripts\check_tools.ps1") {
    & ".\scripts\check_tools.ps1"
} else {
    Write-Host "  [AVERT] check_tools.ps1 introuvable" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Setup termine." -ForegroundColor Cyan
Write-Host "  Prochaine etape : benchmarker les modeles 70B/120B" -ForegroundColor Cyan
Write-Host "  (voir src/llm/llm_client_ollama.py - MODEL_PROFILES)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
