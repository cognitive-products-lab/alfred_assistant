# ============================================================
# ALFRED / Cognitive Products Lab
# install_cpl_workstation_tools.ps1
#
# Installe les programmes de base necessaires pour travailler sur
# ALFRED et sur tout futur projet Cognitive Products Lab, via winget.
# Generique : utilisable sur n'importe quel nouveau poste Windows 11
# (Minisforum MS-S1 Max, PC portable, etc.)
# ============================================================
# UTILISATION (PowerShell, de preference en administrateur) :
#   .\scripts\install_cpl_workstation_tools.ps1
#
# Pour les outils specifiques au projet ALFRED (clone du depot,
# venv Python, modeles Ollama), utiliser ensuite :
#   .\scripts\setup_minisforum_ms_s1_max.ps1
# ============================================================

$ErrorActionPreference = "Continue"

function Write-Step($title) {
    Write-Host ""
    Write-Host "==> $title" -ForegroundColor Cyan
}

if (-not (Get-Command "winget" -ErrorAction SilentlyContinue)) {
    Write-Host "[ECHEC] winget introuvable - mettre a jour 'App Installer' depuis le Microsoft Store" -ForegroundColor Red
    exit 1
}

# ------------------------------------------------------------
# Liste des outils a installer
# ------------------------------------------------------------
# id            : identifiant winget
# name          : nom affiche
# checkCmd      : commande a tester pour savoir si deja installe
# usage         : pourquoi cet outil
$tools = @(
    @{ id = "Python.Python.3.12";        name = "Python 3.12";        checkCmd = "python";  usage = "Stack ALFRED_PC / ALFRED_WEB (venv, pytest)" }
    @{ id = "Git.Git";                    name = "Git";                checkCmd = "git";      usage = "Versioning, clone des depots CPL" }
    @{ id = "Microsoft.VisualStudioCode"; name = "VS Code";            checkCmd = "code";     usage = "IDE principal" }
    @{ id = "GitHub.cli";                 name = "GitHub CLI (gh)";    checkCmd = "gh";       usage = "Gestion PR/issues en ligne de commande" }
    @{ id = "Ollama.Ollama";              name = "Ollama";             checkCmd = "ollama";   usage = "LLM locaux (llama3.x, qwen, gpt-oss...)" }
    @{ id = "Gyan.FFmpeg";                name = "FFmpeg";             checkCmd = "ffmpeg";   usage = "Conversion/traitement audio-video (TTS/STT, contenus CPL)" }
    @{ id = "7zip.7zip";                  name = "7-Zip";              checkCmd = "7z";       usage = "Archives (backups, exports knowledges)" }
    @{ id = "Microsoft.WindowsTerminal";  name = "Windows Terminal";   checkCmd = "wt";       usage = "Terminal moderne (onglets, PowerShell 7)" }
)

# ------------------------------------------------------------
# Installation
# ------------------------------------------------------------
Write-Step "Installation des outils via winget"

foreach ($tool in $tools) {
    Write-Host ""
    Write-Host "  $($tool.name)" -ForegroundColor White
    Write-Host "    Usage : $($tool.usage)" -ForegroundColor DarkGray

    if (Get-Command $tool.checkCmd -ErrorAction SilentlyContinue) {
        Write-Host "    [OK] Deja installe" -ForegroundColor Green
        continue
    }

    Write-Host "    Installation ($($tool.id))..." -ForegroundColor DarkCyan
    winget install --id $tool.id -e --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [OK] Installe" -ForegroundColor Green
    } else {
        Write-Host "    [AVERT] Code retour winget : $LASTEXITCODE - verifier manuellement" -ForegroundColor Yellow
    }
}

# ------------------------------------------------------------
# Resume
# ------------------------------------------------------------
Write-Step "Resume"

Write-Host "  Outils prets pour ALFRED et les futurs projets Cognitive Products Lab." -ForegroundColor Cyan
Write-Host "  IMPORTANT : ouvrir une NOUVELLE session PowerShell pour rafraichir le PATH" -ForegroundColor Yellow
Write-Host "              (Python/Git/gh/Ollama/ffmpeg viennent d'etre ajoutes)." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Prochaine etape (specifique ALFRED) :" -ForegroundColor Cyan
Write-Host "    .\scripts\setup_minisforum_ms_s1_max.ps1" -ForegroundColor DarkGray
