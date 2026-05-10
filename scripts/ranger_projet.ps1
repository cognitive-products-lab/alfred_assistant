# ============================================================
# ALFRED — scripts/ranger_projet.ps1
# Objectif : ranger tous les fichiers mal placés à la racine
#            et corriger les anomalies src/ en une seule passe.
#
# Lancer depuis la racine du projet :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .\scripts\ranger_projet.ps1
#
# OU depuis n'importe où :
#   & "D:\PROJET_ALFRED\ALFRED_PC\scripts\ranger_projet.ps1"
# ============================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$ROOT = "D:\PROJET_ALFRED\ALFRED_PC"

$moved   = 0
$created = 0
$deleted = 0
$skipped = 0
$errors  = 0

function Write-Ok($msg)    { Write-Host "  ✅ $msg" -ForegroundColor Green  }
function Write-Skip($msg)  { Write-Host "  ⏭  $msg" -ForegroundColor Cyan   }
function Write-Warn($msg)  { Write-Host "  ⚠️  $msg" -ForegroundColor Yellow }
function Write-Title($msg) { Write-Host "`n$msg"     -ForegroundColor White  }

function Ensure-Dir($rel) {
    $full = Join-Path $ROOT $rel
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        Write-Ok "Dossier créé : $rel"
        $script:created++
    }
}

function Move-Safe($src_rel, $dst_rel) {
    $src = Join-Path $ROOT $src_rel
    $dst = Join-Path $ROOT $dst_rel
    if (-not (Test-Path $src)) {
        Write-Skip "Absent : $src_rel"
        $script:skipped++
        return
    }
    $dst_dir = Split-Path $dst -Parent
    if (-not (Test-Path $dst_dir)) {
        New-Item -ItemType Directory -Path $dst_dir -Force | Out-Null
        $script:created++
    }
    if (Test-Path $dst) {
        Write-Skip "Destination existe déjà : $dst_rel"
        $script:skipped++
        return
    }
    try {
        Move-Item -Path $src -Destination $dst -Force
        Write-Ok "$src_rel  →  $dst_rel"
        $script:moved++
    } catch {
        Write-Warn "ERREUR move $src_rel : $_"
        $script:errors++
    }
}

function Remove-Safe($rel) {
    $full = Join-Path $ROOT $rel
    if (Test-Path $full) {
        try {
            Remove-Item -Path $full -Force
            Write-Ok "Supprimé : $rel"
            $script:deleted++
        } catch {
            Write-Warn "ERREUR suppression $rel : $_"
            $script:errors++
        }
    } else {
        Write-Skip "Absent : $rel"
        $script:skipped++
    }
}

# ============================================================
# ÉTAPE 1 — Créer tous les dossiers manquants
# ============================================================
Write-Title "═══ ÉTAPE 1 — Création des dossiers ═══"

$new_dirs = @(
    "dashboard",
    "docs",
    "config\v1", "config\v2", "config\v3", "config\v4", "config\security",
    "data\v3", "data\v4", "data\v2\scenarios",
    "data\security", "data\memory\episodic",
    "data\profile", "data\actions", "data\context",
    "data\personality\instances", "data\personality\templates",
    "data\users\instances", "data\users\templates",
    "logs\security",
    "speech\tts\models\fr_FR",
    "src\rag",
    "src\conversation\input",
    "src\conversation\nlp",
    "src\conversation\output"
)
foreach ($d in $new_dirs) { Ensure-Dir $d }

# ============================================================
# ÉTAPE 2 — Racine → dashboard/
# ============================================================
Write-Title "═══ ÉTAPE 2 — Racine → dashboard/ ═══"

Move-Safe "ALFRED_DASHBOARD_DYNAMIC.html" "dashboard\ALFRED_DASHBOARD_DYNAMIC.html"
Move-Safe "dashboard_manifest.json"       "dashboard\dashboard_manifest.json"
Move-Safe "alfred_dashboard.html"         "dashboard\alfred_dashboard_legacy.html"

# dashboard_data.json : déplacer seulement si pas déjà dans dashboard/
$ddst = Join-Path $ROOT "dashboard\dashboard_data.json"
if (-not (Test-Path $ddst)) {
    Move-Safe "dashboard_data.json" "dashboard\dashboard_data.json"
} else {
    Remove-Safe "dashboard_data.json"
}

# ============================================================
# ÉTAPE 3 — Racine → docs/
# ============================================================
Write-Title "═══ ÉTAPE 3 — Racine → docs/ ═══"

Move-Safe "LISTE GLOBALE KNOWLEDGES.docx"                         "docs\LISTE_GLOBALE_KNOWLEDGES.docx"
Move-Safe "competence_connaissances.docx"                         "docs\competence_connaissances.docx"
Move-Safe "knowledge_registry_v1_0_archive.json"                  "docs\knowledge_registry_v1_0_archive.json"
Move-Safe "dashboard_manifest_adapte_tree_02_05_fin_session.json" "docs\dashboard_manifest_adapte_tree_02_05_fin_session.json"
Move-Safe "dashboard_target_report.md"                            "docs\dashboard_target_report.md"
Move-Safe "tree_fin_session_02_05.txt"                            "docs\tree_fin_session_02_05.txt"
Move-Safe "tree_debut_session_2026-05-03_11-24.txt"               "docs\tree_debut_session_2026-05-03_11-24.txt"
Move-Safe "tree_debut_session_2026-05-03_11-32.txt"               "docs\tree_debut_session_2026-05-03_11-32.txt"
Move-Safe "knowledges_tree.txt"                                   "docs\knowledges_tree.txt"

# ============================================================
# ÉTAPE 4 — Racine → scripts/
# ============================================================
Write-Title "═══ ÉTAPE 4 — Racine → scripts/ ═══"

Move-Safe "check_tools.ps1"                   "scripts\check_tools.ps1"
Move-Safe "clean_project.ps1"                 "scripts\clean_project.ps1"
Move-Safe "deploy_knowledges.ps1"             "scripts\deploy_knowledges.ps1"
Move-Safe "fix_response_generator_rename.ps1" "scripts\fix_response_generator_rename.ps1"
Move-Safe "ranger_fichiers_blocs.ps1"         "scripts\ranger_fichiers_blocs.ps1"
Move-Safe "setup_knowledges.ps1"              "scripts\setup_knowledges.ps1"
Move-Safe "update_knowledge_registry.ps1"     "scripts\update_knowledge_registry.ps1"

# ============================================================
# ÉTAPE 5 — Racine → tests/
# ============================================================
Write-Title "═══ ÉTAPE 5 — Racine → tests/ ═══"

Move-Safe "test_b01_speech.py"   "tests\test_b01_speech.py"
Move-Safe "test_b02_b03.py"      "tests\test_b02_b03.py"
Move-Safe "test_pipeline.py"     "tests\test_pipeline.py"
Move-Safe "test_pipeline_llm.py" "tests\test_pipeline_llm.py"

# ============================================================
# ÉTAPE 6 — Racine → config/v4/ (fichiers V4 égarés)
# ============================================================
Write-Title "═══ ÉTAPE 6 — Racine → config/v4/ ═══"

Move-Safe "action_rules.json"        "config\v4\action_rules.json"
Move-Safe "home_devices.json"        "config\v4\home_devices.json"
Move-Safe "orchestration_rules.json" "config\v4\orchestration_rules.json"
Move-Safe "scenario_rules.json"      "config\v4\scenario_rules.json"
Move-Safe "trigger_rules.json"       "config\v4\trigger_rules.json"

# ============================================================
# ÉTAPE 7 — Racine → data/v4/ (fichiers V4 égarés)
# ============================================================
Write-Title "═══ ÉTAPE 7 — Racine → data/v4/ ═══"

Move-Safe "action_log.json"     "data\v4\action_log.json"
Move-Safe "device_registry.json""data\v4\device_registry.json"
Move-Safe "home_state.json"     "data\v4\home_state.json"
Move-Safe "sensor_state.json"   "data\v4\sensor_state.json"
Move-Safe "trigger_log.json"    "data\v4\trigger_log.json"

# ============================================================
# ÉTAPE 8 — Racine → speech/tts/models/fr_FR/
# ============================================================
Write-Title "═══ ÉTAPE 8 — Racine → speech/ ═══"

Move-Safe "fr_FR-mls_1840-low.onnx"      "speech\tts\models\fr_FR\fr_FR-mls_1840-low.onnx"
Move-Safe "fr_FR-mls_1840-low.onnx.json" "speech\tts\models\fr_FR\fr_FR-mls_1840-low.onnx.json"
Move-Safe "ALIASES"                       "speech\tts\models\fr_FR\ALIASES"
Move-Safe "MODEL_CARD"                    "speech\tts\models\fr_FR\MODEL_CARD"

# fr_FR-upmc-medium déjà dans speech/ → supprimer doublons racine
foreach ($f in @("fr_FR-upmc-medium.onnx","fr_FR-upmc-medium.onnx.json")) {
    $src = Join-Path $ROOT $f
    $ref = Join-Path $ROOT "speech\tts\models\fr_FR\$f"
    if ((Test-Path $src) -and (Test-Path $ref)) {
        Remove-Safe $f
    } elseif (Test-Path $src) {
        Move-Safe $f "speech\tts\models\fr_FR\$f"
    }
}

# ============================================================
# ÉTAPE 9 — Racine → logs/security/
# ============================================================
Write-Title "═══ ÉTAPE 9 — Racine → logs/ ═══"

Move-Safe "security.log" "logs\security\security.log"

# ============================================================
# ÉTAPE 10 — Doublons memory à la racine
#            (déjà dans knowledges/system/memory/ → supprimer)
# ============================================================
Write-Title "═══ ÉTAPE 10 — Suppression doublons memory racine ═══"

foreach ($f in @(
    "memory_context_linking.json", "memory_decay_rules.json",
    "memory_learning_rules.json",  "memory_prioritization.json",
    "memory_system.json",          "episodic_memory.json"
)) {
    $src = Join-Path $ROOT $f
    $ref = Join-Path $ROOT "knowledges\system\memory\$f"
    if ((Test-Path $src) -and (Test-Path $ref)) {
        Remove-Safe $f   # doublon confirmé
    } elseif (Test-Path $src) {
        # Pas dans knowledges → déplacer là où il appartient
        if ($f -eq "episodic_memory.json") {
            Move-Safe $f "data\memory\episodic\episodic_memory.json"
        } else {
            Move-Safe $f "knowledges\system\memory\$f"
        }
    }
}

# ============================================================
# ÉTAPE 11 — Ranger config/ (tout est à plat → sous-dossiers)
# ============================================================
Write-Title "═══ ÉTAPE 11 — config/ : à plat → sous-dossiers ═══"

# Mapping fichier → sous-dossier cible
$config_map = @{
    # security
    "access_policies.json"        = "security"
    "audit_retention_policy.json" = "security"
    "roles_permissions.json"      = "security"
    "security_settings.json"      = "security"
    "trusted_devices.json"        = "security"
    "zero_trust_rules.json"       = "security"
    # v1
    "basic_pipeline_rules.json"   = "v1"
    # v2
    "confidence_rules.json"       = "v2"
    "decision_rules.json"         = "v2"
    "edge_cases.json"             = "v2"
    "emotion_profiles.json"       = "v2"
    "fallback_rules.json"         = "v2"
    "feature_matrix.json"         = "v2"
    "kpi_config.json"             = "v2"
    "learning_rules.json"         = "v2"
    "module_mapping.json"         = "v2"
    "naming_conventions.json"     = "v2"
    "proactivity_rules.json"      = "v2"
    "product_roadmap.json"        = "v2"
    "scenario_catalog.json"       = "v2"
    "signal_weights.json"         = "v2"
    # v3
    "conversation_rules.json"     = "v3"
    "emotion_rules.json"          = "v3"
    "fusion_rules.json"           = "v3"
    "memory_rules.json"           = "v3"
    "orchestrator_rules.json"     = "v3"
    "pattern_rules.json"          = "v3"
    "priority_rules.json"         = "v3"
    "proactive_rules.json"        = "v3"
    "relational_rules.json"       = "v3"
    "safety_rules.json"           = "v3"
    "tone_profiles.json"          = "v3"
    "trigger_rules.json"          = "v3"
    "workflow_rules.json"         = "v3"
}

foreach ($fname in $config_map.Keys) {
    $sub    = $config_map[$fname]
    $src_r  = "config\$fname"
    $dst_r  = "config\$sub\$fname"
    $src    = Join-Path $ROOT $src_r
    $dst    = Join-Path $ROOT $dst_r
    if ((Test-Path $src) -and (-not (Test-Path $dst))) {
        Move-Safe $src_r $dst_r
    } elseif ((Test-Path $src) -and (Test-Path $dst)) {
        Write-Skip "Déjà dans $sub : $fname"
        $script:skipped++
    }
}

# ============================================================
# ÉTAPE 12 — Ranger data/ (à plat → sous-dossiers)
# ============================================================
Write-Title "═══ ÉTAPE 12 — data/ : à plat → sous-dossiers ═══"

$data_map = @{
    # security
    "access_decisions_history.json"  = "security"
    "incident_register.json"         = "security"
    "trusted_devices_runtime.json"   = "security"
    # v2/scenarios
    "career_transition.json"         = "v2\scenarios"
    "daily_organization.json"        = "v2\scenarios"
    "isolation_support.json"         = "v2\scenarios"
    "mental_overload.json"           = "v2\scenarios"
    # v3
    "behavior_state.json"            = "v3"
    "context_memories.json"          = "v3"
    "conversation_state.json"        = "v3"
    "emotion_state.json"             = "v3"
    "feedback_log_v3.json"           = "v3"
    "fusion_results.json"            = "v3"
    "fusion_state.json"              = "v3"
    "learning_state_v3.json"         = "v3"
    "memory_patterns.json"           = "v3"
    "orchestrator_state.json"        = "v3"
    "proactive_results.json"         = "v3"
    "proactive_state.json"           = "v3"
    "relational_state.json"          = "v3"
    "safety_state.json"              = "v3"
    "workflow_log.json"              = "v3"
    # v4 (déjà fait étape 7 — skip silencieux)
    "action_log.json"                = "v4"
    "device_registry.json"           = "v4"
    "home_state.json"                = "v4"
    "sensor_state.json"              = "v4"
    "trigger_log.json"               = "v4"
    # actions
    "tasks.json"                     = "actions"
    # context
    "user_context.json"              = "context"
    # profile
    "user_profile.json"              = "profile"
    # personality/instances
    "personality.json"               = "personality"
    "personality_core.json"          = "personality\templates"
    "personality_core_template_public.json" = "personality\templates"
    # users/templates
    "user_adaptation_profile.json"   = "users\templates"
    "user_profile_template_public.json" = "users\templates"
}

foreach ($fname in $data_map.Keys) {
    $sub   = $data_map[$fname]
    $src_r = "data\$fname"
    $dst_r = "data\$sub\$fname"
    $src   = Join-Path $ROOT $src_r
    $dst   = Join-Path $ROOT $dst_r
    if ((Test-Path $src) -and (-not (Test-Path $dst))) {
        Move-Safe $src_r $dst_r
    } elseif ((Test-Path $src) -and (Test-Path $dst)) {
        Write-Skip "Déjà dans $sub : $fname"
        $script:skipped++
    }
}

# ============================================================
# ÉTAPE 13 — Corriger src/ (fichiers mal placés)
# ============================================================
Write-Title "═══ ÉTAPE 13 — src/ : corrections ═══"

# rag_engine.py à la racine src/ → src/rag/
Move-Safe "src\rag_engine.py" "src\rag\rag_engine.py"

# audio_listener.py et intent_classifier.py dans conversation/ direct → sous-dossiers
Move-Safe "src\conversation\audio_listener.py"   "src\conversation\input\audio_listener.py"
Move-Safe "src\conversation\intent_classifier.py" "src\conversation\nlp\intent_classifier.py"

# ============================================================
# ÉTAPE 14 — Supprimer artefacts IDE / .pyc inutiles
# ============================================================
Write-Title "═══ ÉTAPE 14 — Suppression artefacts IDE ═══"

foreach ($f in @(
    "DocumentLayout.backup.json",
    "DocumentLayout.json",
    "misc.xml",
    "modules.xml",
    "script.iml",
    "workspace.xml",
    "bandit.1",
    "__init__.cpython-313.pyc"
)) {
    Remove-Safe $f
}

# ============================================================
# ÉTAPE 15 — Mettre à jour update_dashboard.bat
#            (déjà corrigé en session précédente — vérifier)
# ============================================================
Write-Title "═══ ÉTAPE 15 — Vérification update_dashboard.bat ═══"

$bat = Join-Path $ROOT "update_dashboard.bat"
if (Test-Path $bat) {
    $content = Get-Content $bat -Raw
    if ($content -match "dashboard\\\\ALFRED_DASHBOARD" -or $content -match "dashboard.ALFRED_DASHBOARD") {
        Write-Ok "update_dashboard.bat pointe déjà vers dashboard\ ✅"
    } else {
        # Corriger le chemin start
        $fixed = $content -replace "start ALFRED_DASHBOARD\.html", "start dashboard\ALFRED_DASHBOARD.html"
        $fixed = $fixed   -replace "start alfred_dashboard\.html",  "start dashboard\ALFRED_DASHBOARD.html"
        Set-Content -Path $bat -Value $fixed -Encoding UTF8
        Write-Ok "update_dashboard.bat corrigé → dashboard\ALFRED_DASHBOARD.html"
        $script:moved++
    }
}

# ============================================================
# RAPPORT FINAL
# ============================================================
Write-Title "═══ RAPPORT FINAL ═══"
Write-Host ""
Write-Host "  📁 Dossiers créés   : $created"  -ForegroundColor Cyan
Write-Host "  📦 Fichiers déplacés : $moved"   -ForegroundColor Green
Write-Host "  🗑  Fichiers supprimés: $deleted" -ForegroundColor Gray
Write-Host "  ⏭  Ignorés (ok/abs)  : $skipped" -ForegroundColor DarkCyan
if ($errors -gt 0) {
    Write-Host "  ❌ Erreurs           : $errors"  -ForegroundColor Red
} else {
    Write-Host "  ✅ Aucune erreur"               -ForegroundColor Green
}
Write-Host ""
Write-Host "  Prochaine étape : python tools\update_dashboard_data.py" -ForegroundColor Yellow
Write-Host ""