$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\PROJET_ALFRED\ALFRED_PC"
$SourceDir = $PSScriptRoot
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$DestinationJson = Join-Path $ProjectRoot "dashboard\dashboard_vulnerabilites\dashboard_vulnerabilites.json"
$DestinationScript = Join-Path $ProjectRoot "tools\dashboard_tools\dashboard_vulnerabilites\update_vulnerabilites_data.py"

$SourceJson = Join-Path $SourceDir "dashboard_vulnerabilites.json"
$SourceScript = Join-Path $SourceDir "update_vulnerabilites_data.py"

if (-not (Test-Path $ProjectRoot)) {
    throw "Projet ALFRED_PC introuvable : $ProjectRoot"
}
if (-not (Test-Path $SourceJson)) {
    throw "Fichier source introuvable : $SourceJson"
}
if (-not (Test-Path $SourceScript)) {
    throw "Fichier source introuvable : $SourceScript"
}

New-Item -ItemType Directory -Force -Path (Split-Path $DestinationJson) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $DestinationScript) | Out-Null

foreach ($Destination in @($DestinationJson, $DestinationScript)) {
    if (Test-Path $Destination) {
        $Backup = "$Destination.backup_$Timestamp"
        Copy-Item $Destination $Backup -Force
        Write-Host "Sauvegarde : $Backup" -ForegroundColor DarkGray
    }
}

Copy-Item $SourceJson $DestinationJson -Force
Copy-Item $SourceScript $DestinationScript -Force
Write-Host "Fichiers installés dans ALFRED_PC." -ForegroundColor Green

$PythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCommand) {
    throw "Commande Python introuvable dans le PATH."
}
$Python = $PythonCommand.Source
Write-Host "Python utilisé : $Python" -ForegroundColor Cyan

& $Python -m pip install --upgrade pip-audit
if ($LASTEXITCODE -ne 0) {
    throw "L'installation de pip-audit a échoué avec le code $LASTEXITCODE."
}

Push-Location $ProjectRoot
try {
    & $Python $DestinationScript
    if ($LASTEXITCODE -ne 0) {
        throw "La génération du dashboard a échoué avec le code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

$Data = Get-Content $DestinationJson -Raw -Encoding UTF8 | ConvertFrom-Json
Write-Host ""
Write-Host "Dashboard vulnérabilités généré" -ForegroundColor Green
Write-Host "Total catalogue : $($Data.summary.total)"
Write-Host "Actives         : $($Data.summary.active_total)"
Write-Host "Détectées scan  : $($Data.summary.detected_last_scan)"
Write-Host "Résolues        : $($Data.summary.resolved_total)"
Write-Host "Statut          : $($Data._meta.status)"
Write-Host "JSON            : $DestinationJson"
Write-Host ""
Write-Host "Étape suivante : exécuter la synchronisation ALFRED_PC -> ALFRED_WEB, puis contrôler la copie publiée." -ForegroundColor Yellow
