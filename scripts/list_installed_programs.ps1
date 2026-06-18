# ============================================================
# ALFRED / Cognitive Products Lab
# list_installed_programs.ps1
#
# Liste les programmes installes sur C: :
#   1. Dossiers presents dans C:\Program Files et C:\Program Files (x86)
#   2. Programmes enregistres dans le registre Windows (vue complete,
#      inclut aussi les apps installees ailleurs/via le Store)
#
# Export optionnel en CSV avec -Export
# ============================================================
# UTILISATION :
#   .\scripts\list_installed_programs.ps1
#   .\scripts\list_installed_programs.ps1 -Export
# ============================================================

param(
    [switch]$Export
)

function Write-Step($title) {
    Write-Host ""
    Write-Host "==> $title" -ForegroundColor Cyan
}

# ------------------------------------------------------------
# 1. Dossiers Program Files / Program Files (x86)
# ------------------------------------------------------------
Write-Step "1/2 - Dossiers dans C:\Program Files et C:\Program Files (x86)"

$folderResults = @()

foreach ($base in @("C:\Program Files", "C:\Program Files (x86)")) {
    if (Test-Path $base) {
        Get-ChildItem -Path $base -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $folderResults += [PSCustomObject]@{
                Source = $base
                Nom    = $_.Name
                Chemin = $_.FullName
            }
        }
    }
}

$folderResults | Sort-Object Source, Nom | Format-Table -AutoSize

# ------------------------------------------------------------
# 2. Programmes installes (registre)
# ------------------------------------------------------------
Write-Step "2/2 - Programmes installes (registre Windows)"

$regPaths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

$regResults = Get-ItemProperty -Path $regPaths -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName } |
    Select-Object DisplayName, DisplayVersion, Publisher, InstallLocation, InstallDate |
    Sort-Object DisplayName -Unique

$regResults | Format-Table -AutoSize

# ------------------------------------------------------------
# Export CSV
# ------------------------------------------------------------
if ($Export) {
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $outDir = "D:\PROJET_ALFRED\ALFRED_PC\reports"
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null

    $folderCsv = Join-Path $outDir "installed_programs_folders_$stamp.csv"
    $regCsv    = Join-Path $outDir "installed_programs_registry_$stamp.csv"

    $folderResults | Export-Csv -Path $folderCsv -NoTypeInformation -Encoding UTF8
    $regResults    | Export-Csv -Path $regCsv    -NoTypeInformation -Encoding UTF8

    Write-Host ""
    Write-Host "[OK] Exporte :" -ForegroundColor Green
    Write-Host "  $folderCsv" -ForegroundColor DarkGray
    Write-Host "  $regCsv" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "Total dossiers Program Files(s) : $($folderResults.Count)" -ForegroundColor White
Write-Host "Total programmes (registre)     : $($regResults.Count)" -ForegroundColor White
