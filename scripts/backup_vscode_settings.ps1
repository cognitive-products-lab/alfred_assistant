# ============================================================
# ALFRED / Cognitive Products Lab
# backup_vscode_settings.ps1
#
# Sauvegarde la configuration VS Code (settings, keybindings,
# snippets, liste des extensions) vers D:\ALFRED\vscode_backup
# (convention "ALFRED CORE"), pour pouvoir la restaurer facilement
# sur un autre poste (ex. futur Minisforum MS-S1 Max).
# ============================================================
# UTILISATION :
#   .\scripts\backup_vscode_settings.ps1
# ============================================================

$ErrorActionPreference = "Stop"

function Write-Step($title) {
    Write-Host ""
    Write-Host "==> $title" -ForegroundColor Cyan
}

$sourceDir = Join-Path $env:APPDATA "Code\User"
$targetDir = "D:\ALFRED\vscode_backup"
$stamp     = Get-Date -Format "yyyyMMdd_HHmmss"

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

# ------------------------------------------------------------
# 1. Copie settings / keybindings / snippets
# ------------------------------------------------------------
Write-Step "1/2 - Copie settings.json, keybindings.json, snippets"

if (-not (Test-Path $sourceDir)) {
    Write-Host "  [ECHEC] Dossier introuvable : $sourceDir - VS Code est-il installe ?" -ForegroundColor Red
    exit 1
}

$userBackupDir = Join-Path $targetDir "User"
New-Item -ItemType Directory -Force -Path $userBackupDir | Out-Null

foreach ($item in @("settings.json", "keybindings.json", "snippets")) {
    $src = Join-Path $sourceDir $item
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $userBackupDir -Recurse -Force
        Write-Host "  [OK] $item copie" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] $item absent" -ForegroundColor DarkGray
    }
}

# ------------------------------------------------------------
# 2. Liste des extensions installees
# ------------------------------------------------------------
Write-Step "2/2 - Liste des extensions installees"

if (Get-Command "code" -ErrorAction SilentlyContinue) {
    $extFile = Join-Path $targetDir "extensions.txt"
    code --list-extensions | Out-File -FilePath $extFile -Encoding UTF8
    Write-Host "  [OK] Extensions exportees : $extFile" -ForegroundColor Green
    Write-Host "       Restauration : Get-Content '$extFile' | ForEach-Object { code --install-extension `$_ }" -ForegroundColor DarkGray
} else {
    Write-Host "  [AVERT] Commande 'code' indisponible - extensions non exportees" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Sauvegarde terminee : $targetDir" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
