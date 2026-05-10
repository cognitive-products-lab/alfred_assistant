# ============================================================
# ALFRED — ranger_fichiers_blocs.ps1
# Classe automatiquement les fichiers B20/B01/B02/B03
# depuis : D:\PROJET_ALFRED\script a verifier et classer\
# vers   : D:\PROJET_ALFRED\ALFRED_PC\
#
# Utilisation :
#   cd D:\PROJET_ALFRED
#   .\ranger_fichiers_blocs.ps1
#
# Le script :
#   1. Vérifie que les dossiers cibles existent (sinon les crée)
#   2. Copie chaque fichier au bon endroit
#   3. Affiche un rapport complet
#   4. Ne supprime RIEN de la source (copie, pas déplacement)
# ============================================================

$ErrorActionPreference = "Stop"

# ── Chemins ───────────────────────────────────────────────
$SOURCE = "D:\PROJET_ALFRED\script a verifier et classer"
$TARGET = "D:\PROJET_ALFRED\ALFRED_PC"

# Couleurs console
function Write-OK   { param($msg) Write-Host "  ✅ $msg" -ForegroundColor Green }
function Write-SKIP { param($msg) Write-Host "  ⏭  $msg" -ForegroundColor Yellow }
function Write-ERR  { param($msg) Write-Host "  ❌ $msg" -ForegroundColor Red }
function Write-HEAD { param($msg) Write-Host "`n$msg" -ForegroundColor Cyan }
function Write-SUB  { param($msg) Write-Host "  $msg" -ForegroundColor DarkCyan }

$copied  = 0
$skipped = 0
$errors  = 0

# ─────────────────────────────────────────────────────────
# Fonction utilitaire : créer dossier + copier fichier
# ─────────────────────────────────────────────────────────
function Copy-ToTarget {
    param(
        [string]$FileName,      # Nom du fichier source (ex: security_config.py)
        [string]$TargetSubPath  # Chemin relatif cible (ex: src\security)
    )

    $src  = Join-Path $SOURCE $FileName
    $dest = Join-Path $TARGET $TargetSubPath
    $full = Join-Path $dest $FileName

    # Vérifier existence source
    if (-not (Test-Path $src)) {
        Write-SKIP "ABSENT dans source : $FileName"
        $script:skipped++
        return
    }

    # Créer dossier cible si nécessaire
    if (-not (Test-Path $dest)) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
        Write-SUB "Dossier créé : $TargetSubPath"
    }

    # Copier
    try {
        Copy-Item -Path $src -Destination $full -Force
        Write-OK "$FileName  →  $TargetSubPath\"
        $script:copied++
    } catch {
        Write-ERR "Erreur copie $FileName : $_"
        $script:errors++
    }
}

# ─────────────────────────────────────────────────────────
# Vérifications préalables
# ─────────────────────────────────────────────────────────
Write-Head "═══════════════════════════════════════════════"
Write-Head "  ALFRED — Classement fichiers B20/B01/B02/B03"
Write-Head "═══════════════════════════════════════════════"

if (-not (Test-Path $SOURCE)) {
    Write-ERR "Dossier source introuvable : $SOURCE"
    exit 1
}
if (-not (Test-Path $TARGET)) {
    Write-ERR "Dossier cible introuvable : $TARGET"
    Write-ERR "Vérifie que ALFRED_PC existe sur le disque externe."
    exit 1
}

Write-Host "`n  Source : $SOURCE" -ForegroundColor White
Write-Host "  Cible  : $TARGET`n" -ForegroundColor White

# ═══════════════════════════════════════════════════════
# BLOC 20 — Cybersécurité Zero Trust (25 fichiers)
# ═══════════════════════════════════════════════════════
Write-Head "[ BLOC 20 ] Cybersécurité Zero Trust → src\security\"

$b20Files = @(
    "__init__.py",
    "security_config.py",
    "security_logger.py",
    "secret_manager.py",
    "encryption_service.py",
    "input_validator.py",
    "role_manager.py",
    "permission_manager.py",
    "access_control.py",
    "session_manager.py",
    "mfa_manager.py",
    "device_registry.py",
    "policy_engine.py",
    "policy_decision_point.py",
    "policy_enforcement_point.py",
    "threat_detector.py",
    "behavioral_detector.py",
    "audit_trail.py",
    "incident_manager.py",
    "quarantine_service.py",
    "output_filter.py",
    "prompt_guard.py",
    "compliance_manager.py",
    "backup_security.py",
    "zero_trust_orchestrator.py"
)

foreach ($f in $b20Files) {
    Copy-ToTarget $f "src\security"
}

# Test B20
Copy-ToTarget "test_security_orchestrator.py" "tests\security"

# ═══════════════════════════════════════════════════════
# BLOC 01 — Interaction conversationnelle (8 fichiers)
# ═══════════════════════════════════════════════════════
Write-Head "[ BLOC 01 ] Interaction → src\input\ + src\output\"

# src\input\
$b01InputFiles = @(
    "__init__.py",
    "text_input.py",
    "nlp_engine.py",
    "nlp_engine_v2.py",
    "context_builder.py",
    "audio_capture.py",
    "stt_whisper.py",
    "voice_profile.py",
    "speech_manager.py"
)

foreach ($f in $b01InputFiles) {
    Copy-ToTarget $f "src\input"
}

# src\output\
# Note : __init__.py sera renommé __init___output.py dans la source
# si tu as les 2 __init__.py séparément — sinon on copie le même
$b01OutputFiles = @(
    "tts_output.py",
    "tts_piper.py"
)

foreach ($f in $b01OutputFiles) {
    Copy-ToTarget $f "src\output"
}

# __init__.py output (peut être le même fichier renommé)
$initOutputSrc = Join-Path $SOURCE "__init___output.py"
$initOutputDst = Join-Path $TARGET "src\output\__init__.py"
if (Test-Path $initOutputSrc) {
    Copy-Item $initOutputSrc $initOutputDst -Force
    Write-OK "__init___output.py  →  src\output\__init__.py"
    $copied++
} else {
    # Créer un __init__.py minimal si absent
    $initContent = '"""ALFRED — src/output/__init__.py"""'
    $outDir = Join-Path $TARGET "src\output"
    if (-not (Test-Path $outDir)) { New-Item -ItemType Directory $outDir -Force | Out-Null }
    $initContent | Out-File (Join-Path $outDir "__init__.py") -Encoding utf8 -Force
    Write-OK "__init__.py créé (minimal)  →  src\output\"
    $copied++
}

# Tests B01
Copy-ToTarget "test_b01_speech.py" "tests"

# Config voix
Copy-ToTarget "voice_config.json" "config"

# Assets voix (modèles Piper — si présents dans source)
$piperFiles = @(
    "fr_FR-upmc-medium.onnx",
    "fr_FR-upmc-medium.onnx.json"
)
foreach ($f in $piperFiles) {
    $srcPiper = Join-Path $SOURCE $f
    if (Test-Path $srcPiper) {
        $assetDir = Join-Path $TARGET "assets\voices"
        if (-not (Test-Path $assetDir)) {
            New-Item -ItemType Directory $assetDir -Force | Out-Null
        }
        Copy-Item $srcPiper (Join-Path $assetDir $f) -Force
        Write-OK "$f  →  assets\voices\"
        $copied++
    } else {
        Write-SKIP "Modèle Piper absent (normal si déjà en place) : $f"
        $skipped++
    }
}

# ═══════════════════════════════════════════════════════
# BLOC 02 — Mémoire (6 fichiers)
# ═══════════════════════════════════════════════════════
Write-Head "[ BLOC 02 ] Mémoire → src\memory\"

$b02Files = @(
    "memory_manager.py",
    "long_term_memory.py",
    "episodic_memory.py",
    "memory_indexer.py",
    "rag_stub.py"
)

foreach ($f in $b02Files) {
    Copy-ToTarget $f "src\memory"
}

# __init__.py memory
$initMemSrc = Join-Path $SOURCE "__init___memory.py"
$initMemDst = Join-Path $TARGET "src\memory\__init__.py"
if (Test-Path $initMemSrc) {
    Copy-Item $initMemSrc $initMemDst -Force
    Write-OK "__init___memory.py  →  src\memory\__init__.py"
    $copied++
} else {
    $memDir = Join-Path $TARGET "src\memory"
    if (-not (Test-Path $memDir)) { New-Item -ItemType Directory $memDir -Force | Out-Null }
    '"""ALFRED — src/memory/__init__.py — Bloc 02"""' | Out-File (Join-Path $memDir "__init__.py") -Encoding utf8 -Force
    Write-OK "__init__.py créé (minimal)  →  src\memory\"
    $copied++
}

# ═══════════════════════════════════════════════════════
# BLOC 03 — Émotions & Régulation (5 fichiers)
# ═══════════════════════════════════════════════════════
Write-Head "[ BLOC 03 ] Émotions → src\regulation\"

$b03Files = @(
    "emotion_detector.py",
    "mode_manager.py",
    "protection_guard.py",
    "wellbeing_tracker.py"
)

foreach ($f in $b03Files) {
    Copy-ToTarget $f "src\regulation"
}

# __init__.py regulation
$initRegSrc = Join-Path $SOURCE "__init___regulation.py"
$initRegDst = Join-Path $TARGET "src\regulation\__init__.py"
if (Test-Path $initRegSrc) {
    Copy-Item $initRegSrc $initRegDst -Force
    Write-OK "__init___regulation.py  →  src\regulation\__init__.py"
    $copied++
} else {
    $regDir = Join-Path $TARGET "src\regulation"
    if (-not (Test-Path $regDir)) { New-Item -ItemType Directory $regDir -Force | Out-Null }
    '"""ALFRED — src/regulation/__init__.py — Bloc 03"""' | Out-File (Join-Path $regDir "__init__.py") -Encoding utf8 -Force
    Write-OK "__init__.py créé (minimal)  →  src\regulation\"
    $copied++
}

# Tests B02 + B03
Copy-ToTarget "test_b02_b03.py" "tests"

# READMEs (documentation)
$readmeFiles = @(
    "B01_README_placement.md",
    "B01_README_V1_V3.md",
    "B02_B03_README_weekend.md"
)
foreach ($f in $readmeFiles) {
    Copy-ToTarget $f "docs"
}

# ═══════════════════════════════════════════════════════
# VÉRIFICATION STRUCTURE FINALE
# ═══════════════════════════════════════════════════════
Write-Head "[ VÉRIFICATION ] Structure cible"

$expectedDirs = @(
    "src\security",
    "src\input",
    "src\output",
    "src\memory",
    "src\regulation",
    "tests",
    "tests\security",
    "config",
    "assets\voices",
    "docs"
)

foreach ($dir in $expectedDirs) {
    $full = Join-Path $TARGET $dir
    if (Test-Path $full) {
        $count = (Get-ChildItem $full -File).Count
        Write-OK "$dir\ ($count fichiers)"
    } else {
        Write-SKIP "$dir\ (vide ou absent)"
    }
}

# ═══════════════════════════════════════════════════════
# RAPPORT FINAL
# ═══════════════════════════════════════════════════════
Write-Head "═══════════════════════════════════════════════"
Write-Host "`n  RAPPORT DE CLASSEMENT" -ForegroundColor White
Write-Host "  ─────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  ✅ Fichiers copiés  : $copied" -ForegroundColor Green
Write-Host "  ⏭  Fichiers ignorés : $skipped" -ForegroundColor Yellow
Write-Host "  ❌ Erreurs          : $errors" -ForegroundColor Red
Write-Host ""

if ($errors -eq 0) {
    Write-Host "  🎯 Classement terminé sans erreur." -ForegroundColor Green
    Write-Host ""
    Write-Host "  PROCHAINE ÉTAPE :" -ForegroundColor Cyan
    Write-Host "  cd D:\PROJET_ALFRED\ALFRED_PC" -ForegroundColor White
    Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pytest tests\ -v --tb=short" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  ⚠️  $errors erreur(s) détectée(s) — vérifier les messages ci-dessus." -ForegroundColor Red
}

Write-Head "═══════════════════════════════════════════════"