# ============================================================
# ALFRED - setup_ssh_windows.ps1
# Configure OpenSSH sur Windows pour ConnectBot
# UTILISATION (PowerShell en Admin) :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .\tools\connectbot\setup_ssh_windows.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$PROJET_PATH = "D:\PROJET_ALFRED\ALFRED_PC"
$PROFILE_PATH = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

Write-Host ""
Write-Host "=== ALFRED - Configuration SSH pour ConnectBot ===" -ForegroundColor Cyan
Write-Host ""

# 1. Verifier que OpenSSH Server est installe
$sshFeature = Get-WindowsCapability -Online | Where-Object Name -like "OpenSSH.Server*"
if ($sshFeature.State -ne "Installed") {
    Write-Host "[1/4] Installation de OpenSSH Server..." -ForegroundColor Yellow
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
} else {
    Write-Host "[1/4] OpenSSH Server : deja installe" -ForegroundColor Green
}

# 2. Demarrer et activer le service SSH
Write-Host "[2/4] Activation du service sshd..." -ForegroundColor Yellow
Start-Service sshd -ErrorAction SilentlyContinue
Set-Service -Name sshd -StartupType Automatic
Write-Host "      Service sshd actif et demarrage automatique" -ForegroundColor Green

# 3. Configurer le repertoire de demarrage SSH via le profil PowerShell
Write-Host "[3/4] Configuration du dossier de demarrage SSH..." -ForegroundColor Yellow

$profileDir = Split-Path $PROFILE_PATH
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$line1 = "# ALFRED - Dossier de travail automatique pour SSH/ConnectBot"
$line2 = 'if ($env:SSH_CLIENT -or $env:SSH_TTY) {'
$line3 = "    Set-Location `"$PROJET_PATH`""
$line4 = '    Write-Host "[ALFRED] Projet : ' + $PROJET_PATH + '" -ForegroundColor Cyan'
$line5 = "}"
$profileContent = "$line1`n$line2`n$line3`n$line4`n$line5"

if (Test-Path $PROFILE_PATH) {
    $existing = Get-Content $PROFILE_PATH -Raw -ErrorAction SilentlyContinue
    if ($existing -and $existing.Contains("ALFRED")) {
        Write-Host "      Profil deja configure" -ForegroundColor Green
    } else {
        Add-Content -Path $PROFILE_PATH -Value "`n$profileContent"
        Write-Host "      Profil mis a jour : $PROFILE_PATH" -ForegroundColor Green
    }
} else {
    Set-Content -Path $PROFILE_PATH -Value $profileContent -Encoding UTF8
    Write-Host "      Profil cree : $PROFILE_PATH" -ForegroundColor Green
}

# 4. Autoriser le port 22 dans le pare-feu Windows
Write-Host "[4/4] Verification du pare-feu Windows..." -ForegroundColor Yellow
$rule = Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue
if (-not $rule) {
    New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" `
        -DisplayName "OpenSSH Server (sshd)" `
        -Enabled True -Direction Inbound -Protocol TCP `
        -Action Allow -LocalPort 22 | Out-Null
    Write-Host "      Regle pare-feu ajoutee (port 22)" -ForegroundColor Green
} else {
    Write-Host "      Pare-feu deja configure" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Configuration terminee ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dans ConnectBot :" -ForegroundColor White
Write-Host "  Host     : votre IP locale (tapez ipconfig)" -ForegroundColor Gray
Write-Host "  Port     : 22" -ForegroundColor Gray
Write-Host "  Username : $env:USERNAME" -ForegroundColor Gray
Write-Host "  Auth     : mot de passe Windows" -ForegroundColor Gray
Write-Host ""
Write-Host "A la connexion, vous arriverez dans :" -ForegroundColor White
Write-Host "  $PROJET_PATH" -ForegroundColor Cyan
Write-Host ""
