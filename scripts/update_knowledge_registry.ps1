# ============================================================
# ALFRED — update_knowledge_registry.ps1
# Ajoute les 8 nouvelles fiches knowledge dans le registry
# ============================================================
# UTILISATION :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .\scripts\update_knowledge_registry.ps1
# ============================================================

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  ALFRED - Mise a jour Knowledge Registry   " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$registryPath = "D:\PROJET_ALFRED\ALFRED_PC\knowledges\index\knowledge_registry.json"

if (-not (Test-Path $registryPath)) {
    Write-Host "ERREUR : Registry introuvable : $registryPath" -ForegroundColor Red
    exit 1
}

# -- Charger le registry actuel -------------------------------
$registry = Get-Content $registryPath -Raw -Encoding UTF8 | ConvertFrom-Json

$before = $registry.knowledge_units.Count
Write-Host "  Fiches actuelles : $before" -ForegroundColor DarkGray
Write-Host ""

# -- Nouvelles fiches a ajouter -------------------------------
$newUnits = @(

    # HUMAN - Emotional Intelligence
    [PSCustomObject]@{
        id          = "knowledges.human.emotional_intelligence.emotional_support"
        title       = "Emotional Support"
        path        = "knowledges/human/emotional_intelligence/emotional_support.json"
        domain      = "human"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("emotion", "support", "stabilite", "empathy", "alfred")
    },
    [PSCustomObject]@{
        id          = "knowledges.human.emotional_intelligence.empathy"
        title       = "Empathy"
        path        = "knowledges/human/emotional_intelligence/empathy.json"
        domain      = "human"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("empathy", "emotion", "support", "human", "alfred")
    },
    [PSCustomObject]@{
        id          = "knowledges.human.emotional_intelligence.self_regulation"
        title       = "Self Regulation"
        path        = "knowledges/human/emotional_intelligence/self_regulation.json"
        domain      = "human"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("self_regulation", "emotion", "stabilite", "behavior", "alfred")
    },

    # HUMAN - Self Alignment
    [PSCustomObject]@{
        id          = "knowledges.human.self_alignment.habits.habit_building"
        title       = "Habit Building"
        path        = "knowledges/human/self_alignment/habits/habit_building.json"
        domain      = "human"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("habit_building", "self_alignment", "behavior", "routines", "alfred")
    },
    [PSCustomObject]@{
        id          = "knowledges.human.self_alignment.routines.daily_balance"
        title       = "Daily Balance"
        path        = "knowledges/human/self_alignment/routines/daily_balance.json"
        domain      = "human"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("daily_balance", "self_alignment", "routines", "energy_management", "alfred")
    },

    # PROFESSIONAL - Decision
    [PSCustomObject]@{
        id          = "knowledges.professional.decision.decision_making"
        title       = "Decision Making"
        path        = "knowledges/professional/decision/decision_making.json"
        domain      = "professional"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("decision_making", "professional", "methodology", "analysis", "alfred")
    },
    [PSCustomObject]@{
        id          = "knowledges.professional.decision.problem_solving"
        title       = "Problem Solving"
        path        = "knowledges/professional/decision/problem_solving.json"
        domain      = "professional"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("problem_solving", "professional", "methodology", "logic", "alfred")
    },
    [PSCustomObject]@{
        id          = "knowledges.professional.decision.prioritization"
        title       = "Prioritization"
        path        = "knowledges/professional/decision/prioritization.json"
        domain      = "professional"
        priority    = "high"
        load_policy = "on_demand"
        tags        = @("prioritization", "organization", "planning", "execution", "alfred")
    }
)

# -- Verifier les doublons et ajouter -------------------------
Write-Host "[1/3] Verification des doublons..." -ForegroundColor Yellow

$existingIds = $registry.knowledge_units | ForEach-Object { $_.id }
$added = 0
$skipped = 0

foreach ($unit in $newUnits) {
    if ($existingIds -contains $unit.id) {
        Write-Host "  IGNORE (deja present) : $($unit.id)" -ForegroundColor DarkGray
        $skipped++
    } else {
        $registry.knowledge_units += $unit
        Write-Host "  AJOUTE : $($unit.title)" -ForegroundColor Green
        $added++
    }
}

# -- Ajouter les routing rules --------------------------------
Write-Host ""
Write-Host "[2/3] Ajout des routing rules..." -ForegroundColor Yellow

$newRoutes = @(
    [PSCustomObject]@{
        rule_id   = "route_emotional_support"
        condition = [PSCustomObject]@{
            keywords_any = @("soutien emotionnel", "j'ai besoin d'aide", "je me sens mal", "je souffre", "accompagne-moi")
        }
        load = @(
            "knowledges.human.emotional_intelligence.emotional_support",
            "knowledges.human.emotional_intelligence.empathy"
        )
    },
    [PSCustomObject]@{
        rule_id   = "route_decision"
        condition = [PSCustomObject]@{
            keywords_any = @("decision", "choisir", "arbitrage", "je ne sais pas quoi faire", "aide-moi a choisir")
        }
        load = @(
            "knowledges.professional.decision.decision_making",
            "knowledges.professional.decision.prioritization"
        )
    },
    [PSCustomObject]@{
        rule_id   = "route_problem_solving"
        condition = [PSCustomObject]@{
            keywords_any = @("probleme", "bloquer", "solution", "resoudre", "comment faire")
        }
        load = @(
            "knowledges.professional.decision.problem_solving",
            "knowledges.professional.decision.decision_making"
        )
    },
    [PSCustomObject]@{
        rule_id   = "route_habits"
        condition = [PSCustomObject]@{
            keywords_any = @("habitude", "routine", "regularite", "consistance", "maintenir")
        }
        load = @(
            "knowledges.human.self_alignment.habits.habit_building",
            "knowledges.human.self_alignment.routines.daily_balance"
        )
    }
)

$existingRouteIds = $registry.routing_rules | ForEach-Object { $_.rule_id }
$routesAdded = 0

foreach ($route in $newRoutes) {
    if ($existingRouteIds -contains $route.rule_id) {
        Write-Host "  IGNORE (deja presente) : $($route.rule_id)" -ForegroundColor DarkGray
    } else {
        $registry.routing_rules += $route
        Write-Host "  AJOUTE : $($route.rule_id)" -ForegroundColor Green
        $routesAdded++
    }
}

# -- Mettre a jour le mode_based_loading ----------------------
Write-Host ""
Write-Host "[3/3] Mise a jour mode_based_loading..." -ForegroundColor Yellow

$supportMode = $registry.mode_based_loading.support_mode
if (-not ($supportMode -contains "knowledges.human.emotional_intelligence.emotional_support")) {
    $registry.mode_based_loading.support_mode += "knowledges.human.emotional_intelligence.emotional_support"
    Write-Host "  AJOUTE support_mode : emotional_support" -ForegroundColor Green
}
if (-not ($supportMode -contains "knowledges.human.emotional_intelligence.empathy")) {
    $registry.mode_based_loading.support_mode += "knowledges.human.emotional_intelligence.empathy"
    Write-Host "  AJOUTE support_mode : empathy" -ForegroundColor Green
}

$executionMode = $registry.mode_based_loading.execution_mode
if (-not ($executionMode -contains "knowledges.professional.decision.prioritization")) {
    $registry.mode_based_loading.execution_mode += "knowledges.professional.decision.prioritization"
    Write-Host "  AJOUTE execution_mode : prioritization" -ForegroundColor Green
}

# -- Sauvegarder ----------------------------------------------
$registry | ConvertTo-Json -Depth 10 | Set-Content $registryPath -Encoding UTF8

$after = $registry.knowledge_units.Count

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Termine" -ForegroundColor Cyan
Write-Host "  Fiches avant  : $before" -ForegroundColor DarkGray
Write-Host "  Fiches apres  : $after" -ForegroundColor Green
Write-Host "  Ajoutees      : $added" -ForegroundColor Green
Write-Host "  Ignorees      : $skipped" -ForegroundColor DarkGray
Write-Host "  Routes ajout  : $routesAdded" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Lance ensuite pour verifier :" -ForegroundColor Yellow
Write-Host "  python src\knowledge\knowledge_loader.py" -ForegroundColor White
Write-Host ""