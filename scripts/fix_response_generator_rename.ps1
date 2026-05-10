# ============================================================
# ALFRED — fix_response_generator_rename.ps1
# Remplace toutes les references a response_generator_v2
# par response_generator dans les fichiers config et Python
# ============================================================
# UTILISATION :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .\scripts\fix_response_generator_rename.ps1
# ============================================================

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  ALFRED - Renommage response_generator_v2  " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$baseDir = "D:\PROJET_ALFRED\ALFRED_PC"
$oldName = "response_generator_v2.py"
$newName = "response_generator.py"
$oldString = "response_generator_v2"
$newString = "response_generator"

$filesToPatch = @(
    "$baseDir\config\knowledge_settings.json",
    "$baseDir\config\rag_settings.json",
    "$baseDir\config\quality_thresholds.json",
    "$baseDir\config\routing_rules.json",
    "$baseDir\config\self_alignment_rules.json",
    "$baseDir\config\response_patterns.json",
    "$baseDir\knowledges\core\alfred_core_identity.json"
)

Write-Host "[1/3] Renommage du fichier Python..." -ForegroundColor Yellow

$oldFile = "$baseDir\src\core\$oldName"
$newFile = "$baseDir\src\core\$newName"

if (Test-Path $oldFile) {
    Rename-Item -Path $oldFile -NewName $newName
    Write-Host "  OK : $oldName => $newName" -ForegroundColor Green
} elseif (Test-Path $newFile) {
    Write-Host "  INFO : $newName existe deja." -ForegroundColor DarkGray
} else {
    Write-Host "  ATTENTION : Fichier introuvable : $oldFile" -ForegroundColor Red
}

Write-Host ""
Write-Host "[2/3] Mise a jour des references dans les fichiers config..." -ForegroundColor Yellow

$patchCount = 0

foreach ($file in $filesToPatch) {
    if (-not (Test-Path $file)) {
        Write-Host "  IGNORE (introuvable) : $file" -ForegroundColor DarkYellow
        continue
    }

    $content = Get-Content $file -Raw -Encoding UTF8

    if ($content -match [regex]::Escape($oldString)) {
        $updated = $content -replace [regex]::Escape($oldString), $newString
        Set-Content -Path $file -Value $updated -Encoding UTF8 -NoNewline
        Write-Host "  OK patche : $(Split-Path $file -Leaf)" -ForegroundColor Green
        $patchCount++
    } else {
        Write-Host "  INFO : aucune reference dans $(Split-Path $file -Leaf)" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "[3/3] Scan de securite..." -ForegroundColor Yellow

$allFiles = Get-ChildItem -Path $baseDir -Recurse -Include "*.json","*.py","*.txt","*.md" -ErrorAction SilentlyContinue

$residual = @()
foreach ($f in $allFiles) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($content -match [regex]::Escape($oldString)) {
        $residual += $f.FullName
    }
}

if ($residual.Count -eq 0) {
    Write-Host "  OK : Aucune reference residuelle." -ForegroundColor Green
} else {
    Write-Host "  ATTENTION : References residuelles dans :" -ForegroundColor Red
    foreach ($r in $residual) {
        Write-Host "    => $r" -ForegroundColor Red
    }
    Write-Host "  Remplace manuellement $oldString par $newString dans ces fichiers." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Termine - $patchCount fichier(s) patche(s)" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""