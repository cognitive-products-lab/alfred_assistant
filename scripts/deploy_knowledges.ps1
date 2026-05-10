# ============================================================
# ALFRED — deploy_knowledges.ps1
# Déploie et classe tous les fichiers JSON depuis le dossier
# de travail vers l'arborescence knowledges\ d'ALFRED_PC
#
# UTILISATION :
#   1. Ouvre PowerShell 7
#   2. cd D:\PROJET_ALFRED\ALFRED_PC
#   3. .\scripts\deploy_knowledges.ps1
# ============================================================

param(
    [string]$SourceDir  = "D:\PROJET_ALFRED\script a verifier et classer\knowledges",
    [string]$TargetBase = "D:\PROJET_ALFRED\ALFRED_PC\knowledges"
)

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      ALFRED — Déploiement des Knowledges             ║" -ForegroundColor Cyan
Write-Host "║      Source  → ALFRED_PC\knowledges\                 ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Vérifications préalables ─────────────────────────────────
if (-not (Test-Path $SourceDir)) {
    Write-Host "❌ Dossier source introuvable : $SourceDir" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $TargetBase)) {
    Write-Host "📁 Création du dossier cible : $TargetBase" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $TargetBase -Force | Out-Null
}

# ── Fonction utilitaire ──────────────────────────────────────
function Deploy-File($src, $destDir, $label) {
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    $dest = Join-Path $destDir (Split-Path $src -Leaf)
    if (Test-Path $dest) {
        Write-Host "  ⟳  [MAJ]  $label" -ForegroundColor DarkYellow
    } else {
        Write-Host "  ✅ [COPY] $label" -ForegroundColor Green
    }
    Copy-Item $src $dest -Force
}

# ══════════════════════════════════════════════════════════════
# TABLE DE CLASSEMENT
# Clé = nom de fichier (sans extension)
# Valeur = sous-dossier cible dans knowledges\
# ══════════════════════════════════════════════════════════════
$routing = @{

    # ── STRATE 1 — CORE ──────────────────────────────────────
    "alfred_core_identity"              = "core"
    "behavioral_modes"                  = "core"
    "system_rules"                      = "core"
    "ethical_framework"                 = "core"
    "personality_core_template_public"  = "core"

    # ── STRATE 1 — USER ──────────────────────────────────────
    "user_profile_template_public"      = "user"
    "user_adaptation"                   = "user"
    "personalization_engine"            = "user"
    "context_awareness"                 = "user"
    "feedback_loop"                     = "user"

    # ── STRATE 1 — SOFTSKILLS ────────────────────────────────
    "behavior_rules_softskills"         = "softskills"
    "emotional_management"              = "softskills"
    "problem_solving"                   = "softskills"
    "critical_thinking"                 = "softskills"
    "communication_clarity"             = "softskills"
    "decision_support"                  = "softskills"
    "resilience"                        = "softskills"
    "adaptability"                      = "softskills"
    "organization"                      = "softskills"
    "assertiveness"                     = "softskills"
    "negotiation"                       = "softskills"
    "conflict_management"               = "softskills"
    "focus_management"                  = "softskills"
    "discipline"                        = "softskills"
    "creativity"                        = "softskills"
    "active_listening"                  = "softskills"
    "leadership_personal"               = "softskills"

    # ── STRATE 1 — REASONING ─────────────────────────────────
    "reasoning_engine"                  = "reasoning"
    "reasoning_advanced"                = "reasoning"
    "multi_step_reasoning"              = "reasoning"
    "uncertainty_management"            = "reasoning"
    "decision_models"                   = "reasoning"
    "tradeoff_analysis"                 = "reasoning"
    "root_cause_analysis"               = "reasoning"
    "argumentation_frameworks"          = "reasoning"

    # ── STRATE 1 — MEMORY ────────────────────────────────────
    "memory_system"                     = "memory"
    "episodic_memory"                   = "memory"
    "semantic_memory"                   = "memory"
    "memory_prioritization"             = "memory"
    "memory_decay_rules"                = "memory"
    "memory_context_linking"            = "memory"
    "memory_learning_rules"             = "memory"

    # ── STRATE 1 — PSYCHOLOGY ────────────────────────────────
    "cognitive_biases"                  = "psychology"
    "emotional_patterns"                = "psychology"
    "cognitive_load"                    = "psychology"
    "decision_fatigue"                  = "psychology"
    "burnout_prevention"                = "psychology"
    "motivation"                        = "psychology"
    "behavioral_patterns"               = "psychology"

    # ── CPL — ÉTHIQUE & GOUVERNANCE ──────────────────────────
    "ethical_ai_framework"              = "cpl\ethics_governance"
    "governance_model"                  = "cpl\ethics_governance"
    "accessibility_principles"          = "cpl\ethics_governance"

    # ── CPL — STRATÉGIE ──────────────────────────────────────
    "strategy_fundamentals"             = "cpl\strategy"
    "value_proposition_framework"       = "cpl\strategy"
    "business_model_design"             = "cpl\strategy"

    # ── CPL — COMMUNICATION & HUMAIN ─────────────────────────
    "communication_principles"          = "cpl\human_communication"
    "client_interaction"                = "cpl\human_communication"
    "emotional_intelligence"            = "cpl\human_communication"

    # ── CPL — ORGANISATION HUMAINE ───────────────────────────
    "energy_management"                 = "cpl\human_organization"

    # ── CPL — EXÉCUTION & DÉCISION ───────────────────────────
    "decision_making_framework"         = "cpl\execution"
    "project_management_core"           = "cpl\execution"
    "risk_management"                   = "cpl\execution"
    "task_prioritization"               = "cpl\execution"

    # ── CPL — BUSINESS & PILOTAGE ────────────────────────────
    "pricing_strategy"                  = "cpl\business_piloting"
    "profitability_analysis"            = "cpl\business_piloting"
    "revenue_mix_strategy"              = "cpl\business_piloting"

    # ── CPL — PRODUIT & IA ───────────────────────────────────
    "product_design_methodology"        = "cpl\product_ia"
    "user_needs_analysis"               = "cpl\product_ia"
    "tech_tradeoff_framework"           = "cpl\product_ia"

    # ── REGISTRE ─────────────────────────────────────────────
    "knowledge_registry"                = ""
}

# ══════════════════════════════════════════════════════════════
# DÉPLOIEMENT
# ══════════════════════════════════════════════════════════════
$files        = Get-ChildItem -Path $SourceDir -Filter "*.json" -File
$deployed     = 0
$skipped      = 0
$unclassified = @()

Write-Host "📂 Source : $SourceDir" -ForegroundColor Gray
Write-Host "📂 Cible  : $TargetBase" -ForegroundColor Gray
Write-Host "📦 Fichiers trouvés : $($files.Count)" -ForegroundColor Gray
Write-Host ""

foreach ($file in $files) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)

    if ($routing.ContainsKey($stem)) {
        $subdir = $routing[$stem]
        if ($subdir -eq "") {
            $destDir = $TargetBase
        } else {
            $destDir = Join-Path $TargetBase $subdir
        }
        Deploy-File $file.FullName $destDir "$($file.Name) → knowledges\$subdir"
        $deployed++
    } else {
        # Essai de détection automatique par préfixe / mots-clés
        $autoDir = "unknown"
        if ($stem -match "memory|episodic|semantic")          { $autoDir = "memory" }
        elseif ($stem -match "reason|argument|tradeoff")      { $autoDir = "reasoning" }
        elseif ($stem -match "soft|skill|emotion|resilience") { $autoDir = "softskills" }
        elseif ($stem -match "core|identity|ethical|system")  { $autoDir = "core" }
        elseif ($stem -match "user|profile|feedback|context") { $autoDir = "user" }
        elseif ($stem -match "psycho|burnout|motivation|bias"){ $autoDir = "psychology" }
        elseif ($stem -match "pricing|revenue|profit|business"){ $autoDir = "cpl\business_piloting" }
        elseif ($stem -match "product|mvp|roadmap|ux")        { $autoDir = "cpl\product_ia" }
        elseif ($stem -match "strategy|value|market|competi") { $autoDir = "cpl\strategy" }
        elseif ($stem -match "risk|project|task|agile|execut"){ $autoDir = "cpl\execution" }
        elseif ($stem -match "energy|health|fatigue|sleep")   { $autoDir = "cpl\human_organization" }
        elseif ($stem -match "ethical|governance|access")     { $autoDir = "cpl\ethics_governance" }
        elseif ($stem -match "communication|client|emotion_i"){ $autoDir = "cpl\human_communication" }

        if ($autoDir -ne "unknown") {
            $destDir = Join-Path $TargetBase $autoDir
            Deploy-File $file.FullName $destDir "$($file.Name) → knowledges\$autoDir [auto]"
            $deployed++
            Write-Host "     ↑ classé automatiquement" -ForegroundColor DarkCyan
        } else {
            Write-Host "  ❓ [?????] $($file.Name) — non classé" -ForegroundColor DarkYellow
            $unclassified += $file.Name
            $skipped++
        }
    }
}

# ══════════════════════════════════════════════════════════════
# RAPPORT FINAL
# ══════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " RAPPORT DE DÉPLOIEMENT" -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ Déployés     : $deployed" -ForegroundColor Green
Write-Host "  ❓ Non classés  : $skipped" -ForegroundColor Yellow

if ($unclassified.Count -gt 0) {
    Write-Host ""
    Write-Host "  Fichiers non classés (à traiter manuellement) :" -ForegroundColor Yellow
    foreach ($f in $unclassified) {
        Write-Host "    - $f" -ForegroundColor DarkYellow
    }
    Write-Host ""
    Write-Host "  👉 Ces fichiers ont été laissés dans le dossier source." -ForegroundColor Gray
    Write-Host "  👉 Ajoute-les dans la table `$routing en haut du script." -ForegroundColor Gray
}

# ── Arborescence finale ──────────────────────────────────────
Write-Host ""
Write-Host "  Structure knowledges\ créée :" -ForegroundColor Cyan
Get-ChildItem -Path $TargetBase -Directory -Recurse |
    Select-Object -ExpandProperty FullName |
    ForEach-Object { Write-Host "    📁 $($_.Replace($TargetBase,''))" -ForegroundColor DarkGreen }

Write-Host ""
Write-Host "✅ Déploiement terminé." -ForegroundColor Green
Write-Host ""