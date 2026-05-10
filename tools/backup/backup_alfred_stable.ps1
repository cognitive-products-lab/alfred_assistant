$projectRoot = "D:\PROJET_ALFRED\ALFRED_PC"
$backupRoot = Join-Path $projectRoot "_BACKUPS"

if (!(Test-Path $backupRoot)) {
    New-Item -ItemType Directory -Path $backupRoot | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupPath = Join-Path $backupRoot "ALFRED_STABLE_$timestamp"

New-Item -ItemType Directory -Path $backupPath | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " ALFRED - BACKUP VERSION STABLE" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$foldersToCopy = @(
    "src",
    "knowledges",
    "tests",
    "tools",
    "config",
    "assets"
)

foreach ($folder in $foldersToCopy) {
    $source = Join-Path $projectRoot $folder

    if (Test-Path $source) {
        $destination = Join-Path $backupPath $folder
        Write-Host "[COPY] $folder" -ForegroundColor Yellow
        Copy-Item -Path $source -Destination $destination -Recurse -Force
    }
}

$filesToCopy = @(
    "requirements.txt",
    "README.md",
    "dashboard_data.json",
    "manifest.json"
)

foreach ($file in $filesToCopy) {
    $source = Join-Path $projectRoot $file

    if (Test-Path $source) {
        Write-Host "[FILE] $file" -ForegroundColor Green
        Copy-Item -Path $source -Destination $backupPath -Force
    }
}

Write-Host "[TREE] Export structure..." -ForegroundColor Magenta
tree $projectRoot /F /A | Out-File (Join-Path $backupPath "project_tree.txt") -Encoding UTF8

$versionLines = @(
    "ALFRED Stable Backup",
    "====================",
    "",
    "Date : $(Get-Date)",
    "Projet : ALFRED_PC",
    "",
    "Contenu :",
    "- src",
    "- knowledges",
    "- tests",
    "- tools",
    "- config",
    "- assets",
    "",
    "Type :",
    "Backup manuel version stable"
)

$versionLines | Out-File (Join-Path $backupPath "backup_info.txt") -Encoding UTF8

Write-Host ""
Write-Host "Backup termine :" -ForegroundColor Cyan
Write-Host $backupPath -ForegroundColor White
Write-Host ""