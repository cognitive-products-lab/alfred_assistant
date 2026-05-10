# ============================================================
# ALFRED — setup_knowledges.ps1
# Rôle :
#   1. Créer tous les dossiers knowledges/ manquants
#   2. Y déposer les __init__.py vides requis
#   3. Copier les JSON depuis "script a verifier et classer\knowledges"
#      vers leurs chemins cibles dans knowledges/cpl/
#   4. Traiter le doublon knowledge_registry (v1.1 → actif, v1.0 → docs)
#   5. Déplacer les .docx dans docs/
#   6. Afficher un rapport final
# ============================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Chemins racines ──────────────────────────────────────────
$ROOT   = "D:\PROJET_ALFRED\ALFRED_PC"
$SOURCE = "D:\PROJET_ALFRED\script a verifier et classer\knowledges"
$DOCS   = "$ROOT\docs"

# ── Couleurs console ─────────────────────────────────────────
function Write-Ok($msg)   { Write-Host "  ✅ $msg" -ForegroundColor Green  }
function Write-Skip($msg) { Write-Host "  ⏭  $msg" -ForegroundColor Cyan   }
function Write-Warn($msg) { Write-Host "  ⚠️  $msg" -ForegroundColor Yellow }
function Write-Title($msg){ Write-Host "`n$msg" -ForegroundColor White      }

# ── Compteurs ────────────────────────────────────────────────
$created_dirs  = 0
$created_inits = 0
$copied_files  = 0
$skipped_files = 0
$errors        = 0

# ============================================================
# 1. LISTE COMPLÈTE DES DOSSIERS À CRÉER
#    (tous les sous-dossiers knowledges/ attendus par le manifest)
# ============================================================
Write-Title "═══ ÉTAPE 1 — Création des dossiers manquants ═══"

$knowledges_dirs = @(
    # Racine
    "knowledges",
    "knowledges\index",

    # CPL
    "knowledges\cpl",
    "knowledges\cpl\business_piloting",
    "knowledges\cpl\ethics_governance",
    "knowledges\cpl\execution",
    "knowledges\cpl\human_communication",
    "knowledges\cpl\human_organization",
    "knowledges\cpl\product_ia",
    "knowledges\cpl\strategy",

    # Core
    "knowledges\core",

    # Culture
    "knowledges\culture",
    "knowledges\culture\universes",
    "knowledges\culture\universes\dc",
    "knowledges\culture\universes\marvel",

    # Human
    "knowledges\human",
    "knowledges\human\cognition",
    "knowledges\human\emotional_intelligence",
    "knowledges\human\psychology",
    "knowledges\human\self_alignment",
    "knowledges\human\self_alignment\habits",
    "knowledges\human\self_alignment\routines",
    "knowledges\human\skills",
    "knowledges\human\skills\softskills",

    # Lifestyle
    "knowledges\lifestyle",
    "knowledges\lifestyle\daily_life",
    "knowledges\lifestyle\health",

    # Professional
    "knowledges\professional",
    "knowledges\professional\decision",
    "knowledges\professional\engineering",
    "knowledges\professional\engineering\ai",
    "knowledges\professional\engineering\cybersecurite",
    "knowledges\professional\engineering\systeme_design",
    "knowledges\professional\leadership",
    "knowledges\professional\product_management",
    "knowledges\professional\strategy",
    "knowledges\professional\strategy\product_strategy",

    # System
    "knowledges\system",
    "knowledges\system\ethics",
    "knowledges\system\memory",

    # Docs (pour archivage)
    "docs"
)

foreach ($rel in $knowledges_dirs) {
    $full = Join-Path $ROOT $rel
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        Write-Ok "Créé : $rel"
        $created_dirs++
    } else {
        Write-Skip "Existe : $rel"
    }
}

# ============================================================
# 2. CRÉATION DES __init__.py DANS LES DOSSIERS CPL
#    (pour que Python puisse importer les loaders de knowledge)
# ============================================================
Write-Title "═══ ÉTAPE 2 — Création des __init__.py ═══"

$init_dirs = @(
    "knowledges\cpl",
    "knowledges\cpl\business_piloting",
    "knowledges\cpl\ethics_governance",
    "knowledges\cpl\execution",
    "knowledges\cpl\human_communication",
    "knowledges\cpl\human_organization",
    "knowledges\cpl\product_ia",
    "knowledges\cpl\strategy",
    "knowledges\core",
    "knowledges\human",
    "knowledges\human\cognition",
    "knowledges\human\emotional_intelligence",
    "knowledges\human\psychology",
    "knowledges\human\self_alignment",
    "knowledges\human\self_alignment\habits",
    "knowledges\human\self_alignment\routines",
    "knowledges\human\skills",
    "knowledges\human\skills\softskills",
    "knowledges\lifestyle",
    "knowledges\lifestyle\daily_life",
    "knowledges\lifestyle\health",
    "knowledges\professional",
    "knowledges\professional\decision",
    "knowledges\professional\engineering",
    "knowledges\professional\engineering\ai",
    "knowledges\professional\engineering\cybersecurite",
    "knowledges\professional\engineering\systeme_design",
    "knowledges\professional\leadership",
    "knowledges\professional\product_management",
    "knowledges\professional\strategy",
    "knowledges\professional\strategy\product_strategy",
    "knowledges\system",
    "knowledges\system\ethics",
    "knowledges\system\memory"
)

foreach ($rel in $init_dirs) {
    $init_path = Join-Path $ROOT "$rel\__init__.py"
    if (-not (Test-Path $init_path)) {
        Set-Content -Path $init_path -Value "" -Encoding UTF8
        Write-Ok "__init__.py → $rel"
        $created_inits++
    } else {
        Write-Skip "__init__.py existe : $rel"
    }
}

# ============================================================
# 3. COPIE DES KNOWLEDGES JSON VERS LEURS CHEMINS CIBLES
# ============================================================
Write-Title "═══ ÉTAPE 3 — Copie des knowledges JSON ═══"

# Table : nom_source → chemin_relatif_cible (depuis ROOT)
$copy_map = @{
    "accessibility_principles.json"    = "knowledges\cpl\ethics_governance\accessibility_principles.json"
    "business_model_design.json"       = "knowledges\cpl\strategy\business_model_design.json"
    "client_interaction.json"          = "knowledges\cpl\human_communication\client_interaction.json"
    "communication_principles.json"    = "knowledges\cpl\human_communication\communication_principles.json"
    "decision_making_framework.json"   = "knowledges\cpl\execution\decision_making_framework.json"
    "emotional_intelligence.json"      = "knowledges\cpl\human_communication\emotional_intelligence.json"
    "energy_management.json"           = "knowledges\cpl\human_organization\energy_management.json"
    "ethical_ai_framework.json"        = "knowledges\cpl\ethics_governance\ethical_ai_framework.json"
    "governance_model.json"            = "knowledges\cpl\ethics_governance\governance_model.json"
    "pricing_strategy.json"            = "knowledges\cpl\business_piloting\pricing_strategy.json"
    "product_design_methodology.json"  = "knowledges\cpl\product_ia\product_design_methodology.json"
    "profitability_analysis.json"      = "knowledges\cpl\business_piloting\profitability_analysis.json"
    "project_management_core.json"     = "knowledges\cpl\execution\project_management_core.json"
    "revenue_mix_strategy.json"        = "knowledges\cpl\business_piloting\revenue_mix_strategy.json"
    "risk_management.json"             = "knowledges\cpl\execution\risk_management.json"
    "strategy_fundamentals.json"       = "knowledges\cpl\strategy\strategy_fundamentals.json"
    "task_prioritization.json"         = "knowledges\cpl\execution\task_prioritization.json"
    "tech_tradeoff_framework.json"     = "knowledges\cpl\product_ia\tech_tradeoff_framework.json"
    "user_needs_analysis.json"         = "knowledges\cpl\product_ia\user_needs_analysis.json"
    "value_proposition_framework.json" = "knowledges\cpl\strategy\value_proposition_framework.json"
}

foreach ($src_name in $copy_map.Keys | Sort-Object) {
    $src_path = Join-Path $SOURCE $src_name
    $dst_path = Join-Path $ROOT $copy_map[$src_name]

    if (-not (Test-Path $src_path)) {
        Write-Warn "SOURCE INTROUVABLE : $src_name"
        $errors++
        continue
    }

    if (Test-Path $dst_path) {
        # Vérifier si identique (taille)
        $src_size = (Get-Item $src_path).Length
        $dst_size = (Get-Item $dst_path).Length
        if ($src_size -eq $dst_size) {
            Write-Skip "Identique (même taille) : $src_name"
            $skipped_files++
            continue
        } else {
            Write-Warn "Écrasement (tailles diff src=$src_size dst=$dst_size) : $src_name"
        }
    }

    try {
        Copy-Item -Path $src_path -Destination $dst_path -Force
        Write-Ok "Copié : $src_name → $($copy_map[$src_name])"
        $copied_files++
    } catch {
        Write-Warn "ERREUR copie $src_name : $_"
        $errors++
    }
}

# ============================================================
# 4. DOUBLON knowledge_registry — v1.1 devient actif, v1.0 archivé
# ============================================================
Write-Title "═══ ÉTAPE 4 — Gestion du doublon knowledge_registry ═══"

$reg_v1   = Join-Path $SOURCE "knowledge_registry.json"
$reg_v11  = Join-Path $SOURCE "knowledge_registry_v1_1.json"
$reg_dst  = Join-Path $ROOT "knowledges\knowledge_registry.json"
$reg_arch = Join-Path $DOCS  "knowledge_registry_v1_0_archive.json"

# v1.1 → destination active
if (Test-Path $reg_v11) {
    Copy-Item -Path $reg_v11 -Destination $reg_dst -Force
    Write-Ok "knowledge_registry_v1_1.json → knowledges\knowledge_registry.json (actif)"
    $copied_files++
} elseif (Test-Path $reg_v1) {
    Copy-Item -Path $reg_v1 -Destination $reg_dst -Force
    Write-Ok "knowledge_registry.json → knowledges\knowledge_registry.json (seule version disponible)"
    $copied_files++
} else {
    Write-Warn "Aucun knowledge_registry trouvé dans la source"
    $errors++
}

# v1.0 → archive dans docs/
if (Test-Path $reg_v1) {
    Copy-Item -Path $reg_v1 -Destination $reg_arch -Force
    Write-Ok "knowledge_registry.json → docs\knowledge_registry_v1_0_archive.json"
}

# Copie aussi dans knowledges/index/ (référencé dans le manifest)
$reg_index = Join-Path $ROOT "knowledges\index\knowledge_registry.json"
if (Test-Path $reg_v11) {
    Copy-Item -Path $reg_v11 -Destination $reg_index -Force
    Write-Ok "knowledge_registry_v1_1.json → knowledges\index\knowledge_registry.json"
}

# ============================================================
# 5. DÉPLACEMENT DES .DOCX VERS docs/
# ============================================================
Write-Title "═══ ÉTAPE 5 — Archivage des .docx dans docs/ ═══"

$docx_files = @(
    "competence_connaissances.docx",
    "LISTE GLOBALE KNOWLEDGES.docx"
)

foreach ($docx in $docx_files) {
    $src = Join-Path $SOURCE $docx
    $dst = Join-Path $DOCS $docx
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $dst -Force
        Write-Ok "Archivé : $docx → docs\"
    } else {
        Write-Skip "Non trouvé (déjà déplacé ?) : $docx"
    }
}

# ============================================================
# 6. RAPPORT FINAL
# ============================================================
Write-Title "═══ RAPPORT FINAL ═══"
Write-Host ""
Write-Host "  📁 Dossiers créés     : $created_dirs"    -ForegroundColor Cyan
Write-Host "  🐍 __init__.py créés  : $created_inits"   -ForegroundColor Cyan
Write-Host "  📄 Fichiers copiés    : $copied_files"     -ForegroundColor Green
Write-Host "  ⏭  Fichiers ignorés   : $skipped_files"   -ForegroundColor Gray
if ($errors -gt 0) {
    Write-Host "  ❌ Erreurs            : $errors"        -ForegroundColor Red
} else {
    Write-Host "  ✅ Aucune erreur"                       -ForegroundColor Green
}
Write-Host ""
Write-Host "  Prochaine étape : python paths.py  (vérifie les chemins)"  -ForegroundColor Yellow
Write-Host "  Puis            : python tools\update_dashboard_data.py"    -ForegroundColor Yellow
Write-Host ""