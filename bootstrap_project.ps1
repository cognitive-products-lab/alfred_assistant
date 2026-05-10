# ============================================================
# ALFRED — bootstrap_project.ps1
# Script de création de l'arborescence complète du projet
# ============================================================
# UTILISATION :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .\scripts\bootstrap_project.ps1
#
# Ce script :
#   1. Crée toute l'arborescence V1->V4
#   2. Crée les fichiers __init__.py nécessaires
#   3. Crée les fichiers JSON vides de base
#   4. Configure l'environnement virtuel Python
#   5. Crée le .env.example
# ============================================================

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         ALFRED — Bootstrap du projet             ║" -ForegroundColor Cyan
Write-Host "║     Local-first | Security by Design             ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Vérifier qu'on est au bon endroit ────────────────────
$expectedDir = "ALFRED_PC"
$currentDir  = Split-Path -Leaf (Get-Location)

if ($currentDir -ne $expectedDir) {
    Write-Host "⚠️  ATTENTION : Lance ce script depuis D:\PROJET_ALFRED\ALFRED_PC\" -ForegroundColor Yellow
    Write-Host "   Dossier actuel : $currentDir" -ForegroundColor Yellow
    $confirm = Read-Host "Continuer quand même ? (o/n)"
    if ($confirm -ne "o") { exit }
}

# ══════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ══════════════════════════════════════════════════════════
function New-Dir($path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  📁 $path" -ForegroundColor Green
    }
}

function New-File($path, $content = "") {
    if (-not (Test-Path $path)) {
        Set-Content -Path $path -Value $content -Encoding UTF8
        Write-Host "  📄 $path" -ForegroundColor DarkGreen
    }
}

function New-JsonFile($path, $content = "{}") {
    New-File $path $content
}

function New-InitPy($folder) {
    New-File "$folder\__init__.py" "# ALFRED module"
}

# ══════════════════════════════════════════════════════════
# 1. DOSSIERS RACINE
# ══════════════════════════════════════════════════════════
Write-Host "`n[1/9] Dossiers racine..." -ForegroundColor Cyan

$rootDirs = @(
    "src", "config", "data", "logs", "assets",
    "knowledges", "tests", "docs", "scripts",
    "auth", "speech", "interface", "integration",
    "packaging", "policy", "build", "ci"
)
foreach ($d in $rootDirs) { New-Dir $d }

# ══════════════════════════════════════════════════════════
# 2. SRC — Structure complète
# ══════════════════════════════════════════════════════════
Write-Host "`n[2/9] Structure src/..." -ForegroundColor Cyan

$srcModules = @(
    "src\core", "src\input", "src\output", "src\dialogue",
    "src\memory", "src\knowledge", "src\assistant_actions",
    "src\conversation", "src\ui", "src\regulation", "src\auth"
)
foreach ($d in $srcModules) { New-Dir $d; New-InitPy $d }

New-Dir "src\security"
New-InitPy "src\security"

foreach ($v in @("v1", "v2", "v2pp", "v3", "v4")) {
    New-Dir "src\$v"
    New-InitPy "src\$v"
}

$v2Modules = @("governance", "fusion", "decision", "learning",
               "confidence", "fallback", "experience", "scenarios",
               "knowledge", "product")
foreach ($m in $v2Modules) {
    New-Dir "src\v2\$m"
    New-InitPy "src\v2\$m"
}

$v3Modules = @("reasoning", "memory", "fusion", "proactive",
               "emotion", "orchestrator", "conversation",
               "learning", "safety")
foreach ($m in $v3Modules) {
    New-Dir "src\v3\$m"
    New-InitPy "src\v3\$m"
}

$v4Modules = @("home_state", "triggers", "actions",
               "orchestrator", "security", "integration", "scenarios")
foreach ($m in $v4Modules) {
    New-Dir "src\v4\$m"
    New-InitPy "src\v4\$m"
}

New-InitPy "src"
New-File "src\main.py" @"
# ============================================================
# ALFRED — main.py
# Point d'entrée principal
# ============================================================
from paths import PATHS, ensure_dirs

def main():
    ensure_dirs()
    print("🤖 ALFRED démarré")
    print(f"   Base : {PATHS.base}")

if __name__ == "__main__":
    main()
"@

# ══════════════════════════════════════════════════════════
# 3. CONFIG — Tous les JSON de configuration
# ══════════════════════════════════════════════════════════
Write-Host "`n[3/9] Structure config/..." -ForegroundColor Cyan

foreach ($v in @("v1", "v2", "v2pp", "v3", "v4", "security")) {
    New-Dir "config\$v"
}

New-JsonFile "config\settings.json" '{"app_env": "local", "api_host": "127.0.0.1", "session_timeout": 900}'
New-JsonFile "config\router_rules.json" '{"routes": {}}'
New-JsonFile "config\safety_rules.json" '{"principles": ["non_malfaisance", "transparence"]}'
New-JsonFile "config\ethics_rules.json" '{"rules": []}'

New-JsonFile "config\security\security_settings.json" '{"encryption": "fernet", "mfa_required": false}'
New-JsonFile "config\security\access_policies.json" '{"policies": []}'
New-JsonFile "config\security\roles_permissions.json" '{"roles": {}}'
New-JsonFile "config\security\zero_trust_rules.json" '{"rules": []}'
New-JsonFile "config\security\trusted_devices.json" '{"devices": []}'
New-JsonFile "config\security\audit_retention_policy.json" '{"retention_days": 90}'

New-JsonFile "config\v1\basic_pipeline_rules.json" '{"pipeline": ["input", "security", "memory", "response"]}'

$v2Configs = @(
    @("naming_conventions.json", '{"python_files": "snake_case.py"}'),
    @("module_mapping.json", '{}'),
    @("signal_weights.json", '{"emotion": 0.4, "memory": 0.3, "intent": 0.3}'),
    @("decision_rules.json", '{"decision_thresholds": {"high_confidence": 0.7, "medium_confidence": 0.4}}'),
    @("learning_rules.json", '{"positive_feedback_bonus": 1, "negative_feedback_penalty": -1}'),
    @("confidence_rules.json", '{"thresholds": {"high": 0.7, "medium": 0.4}}'),
    @("fallback_rules.json", '{"fallback_modes": {}}'),
    @("edge_cases.json", '{"patterns": []}'),
    @("emotion_profiles.json", '{"profiles": {}}'),
    @("proactivity_rules.json", '{"rules": {}}'),
    @("scenario_catalog.json", '{"scenarios": []}'),
    @("product_roadmap.json", '{"versions": {}}'),
    @("feature_matrix.json", '{"features": []}'),
    @("kpi_config.json", '{"kpis": []}')
)
foreach ($c in $v2Configs) { New-JsonFile "config\v2\$($c[0])" $c[1] }

$v3Configs = @(
    "memory_rules.json", "pattern_rules.json", "fusion_rules.json",
    "confidence_rules.json", "proactive_rules.json", "trigger_rules.json",
    "emotion_rules.json", "tone_profiles.json", "relational_rules.json",
    "conversation_rules.json", "learning_rules.json", "safety_rules.json",
    "orchestrator_rules.json", "priority_rules.json", "workflow_rules.json"
)
foreach ($c in $v3Configs) { New-JsonFile "config\v3\$c" '{}' }

$v4Configs = @("home_devices.json", "trigger_rules.json", "action_rules.json",
               "orchestration_rules.json", "scenario_rules.json")
foreach ($c in $v4Configs) { New-JsonFile "config\v4\$c" '{}' }

# ══════════════════════════════════════════════════════════
# 4. DATA — Tous les fichiers de données
# ══════════════════════════════════════════════════════════
Write-Host "`n[4/9] Structure data/..." -ForegroundColor Cyan

$dataDirs = @("security", "memory\episodic", "memory\semantic",
              "memory\profile", "memory\long_term",
              "profile", "actions", "context",
              "v1", "v2\scenarios", "v2pp", "v3", "v4")
foreach ($d in $dataDirs) { New-Dir "data\$d" }

New-JsonFile "data\user_memory.json" '{"memories": []}'
New-JsonFile "data\personality.json" '{"core": {}, "adaptation": {}}'
New-JsonFile "data\preferences_profile.json" '{"preferences": []}'
New-JsonFile "data\dialogue_history.json" '{"history": []}'

New-JsonFile "data\memory\episodic\dialogue_history.json" '{"entries": []}'
New-JsonFile "data\profile\user_profile.json" '{"name": "", "why_keywords": [], "softskills": [], "personality_traits": [], "preferences": []}'
New-JsonFile "data\actions\tasks.json" '{"tasks": []}'
New-JsonFile "data\context\user_context.json" '{"location": "home", "energy_level": "normal"}'

New-JsonFile "data\security\incident_register.json" '{"incidents": []}'
New-JsonFile "data\security\access_decisions_history.json" '{"decisions": []}'
New-JsonFile "data\security\trusted_devices_runtime.json" '{"devices": []}'

$v2Data = @(
    "feedback_log.json", "learning_state.json", "memory_samples.json",
    "scenario_results.json", "robustness_results.json",
    "experience_state.json", "product_state.json"
)
foreach ($f in $v2Data) { New-JsonFile "data\v2\$f" '{}' }

$v2Scenarios = @("mental_overload.json", "career_transition.json",
                 "isolation_support.json", "daily_organization.json")
foreach ($f in $v2Scenarios) { New-JsonFile "data\v2\scenarios\$f" '{}' }

$v3Data = @(
    "context_memories.json", "memory_patterns.json", "behavior_state.json",
    "fusion_state.json", "fusion_results.json", "proactive_state.json",
    "proactive_results.json", "emotion_state.json", "relational_state.json",
    "orchestrator_state.json", "workflow_log.json", "conversation_state.json",
    "learning_state_v3.json", "feedback_log_v3.json", "safety_state.json"
)
foreach ($f in $v3Data) { New-JsonFile "data\v3\$f" '{}' }

$v4Data = @(
    "home_state.json", "sensor_state.json", "device_registry.json",
    "action_log.json", "trigger_log.json"
)
foreach ($f in $v4Data) { New-JsonFile "data\v4\$f" '{}' }

# ══════════════════════════════════════════════════════════
# 5. KNOWLEDGES
# ══════════════════════════════════════════════════════════
Write-Host "`n[5/9] Structure knowledges/..." -ForegroundColor Cyan

$knowledgeDirs = @(
    "knowledges\human\relationships", "knowledges\human\cognition",
    "knowledges\human\self_alignment",
    "knowledges\professional\decision", "knowledges\professional\communication",
    "knowledges\professional\engineering", "knowledges\professional\business",
    "knowledges\lifestyle\productivity", "knowledges\lifestyle\life_path"
)
foreach ($d in $knowledgeDirs) { New-Dir $d }
New-JsonFile "knowledges\manifest.json" '{"domains": {"professional": [], "human": [], "lifestyle": []}}'
New-JsonFile "knowledges\taxonomy.json" '{"categories": {}}'

# ══════════════════════════════════════════════════════════
# 6. LOGS
# ══════════════════════════════════════════════════════════
Write-Host "`n[6/9] Structure logs/..." -ForegroundColor Cyan

New-Dir "logs\archived"
foreach ($log in @("app.log", "errors.log", "security.log", "interaction.log")) {
    New-File "logs\$log" ""
}

# ══════════════════════════════════════════════════════════
# 7. ASSETS — Avatar et audio
# ══════════════════════════════════════════════════════════
Write-Host "`n[7/9] Structure assets/..." -ForegroundColor Cyan

$assetDirs = @(
    "assets\avatar\sprites\head_base", "assets\avatar\sprites\mouth",
    "assets\avatar\sprites\eyes", "assets\avatar\sprites\eyebrows",
    "assets\avatar\sprites\hair", "assets\avatar\sprites\effects",
    "assets\avatar\sprites\animations\blink",
    "assets\avatar\sprites\animations\talking",
    "assets\avatar\sprites\animations\emotions",
    "assets\avatar\exports\png", "assets\avatar\exports\webp",
    "assets\audio\notifications", "assets\audio\tts_cache",
    "assets\icons\app", "assets\images\ui"
)
foreach ($d in $assetDirs) { New-Dir $d }

# ══════════════════════════════════════════════════════════
# 8. FICHIERS RACINE DU PROJET
# ══════════════════════════════════════════════════════════
Write-Host "`n[8/9] Fichiers racine..." -ForegroundColor Cyan

New-File ".env.example" @"
# ============================================================
# ALFRED — Variables d'environnement
# COPIER ce fichier en .env et remplir les valeurs
# NE JAMAIS committer .env dans Git
# ============================================================

APP_ENV=local
API_HOST=127.0.0.1
SESSION_TIMEOUT=900
MAX_LOGIN_ATTEMPTS=5

# Générer avec : python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
FERNET_KEY=CHANGE_ME_GENERATE_WITH_PYTHON

# Générer avec : python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=CHANGE_ME_GENERATE_WITH_PYTHON
PIN_SALT=CHANGE_ME_GENERATE_WITH_PYTHON
"@

New-File ".gitignore" @"
# Secrets
.env
config/ssl/

# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
*.egg-info/

# Données personnelles (ne jamais versionner)
data/memory/
data/profile/
data/v*/
logs/*.log

# Build
build/
dist/
*.spec

# IDE
.vscode/settings.json
.idea/
"@

New-File "README.md" @"
# ALFRED — Assistant Cognitif Adaptatif

## Principes fondamentaux
- **Local-first** : toutes les données restent en local
- **Security by Design** : sécurité intégrée dès la conception
- **Zero Trust** : aucune confiance implicite

## Démarrage rapide
\`\`\`powershell
# 1. Créer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les secrets
Copy-Item .env.example .env
# Éditer .env avec tes vraies valeurs

# 4. Lancer ALFRED
python -m src.main
\`\`\`

## Architecture
V1 -> Pipeline minimal fonctionnel
V2 -> Intelligence décisionnelle
V2++ -> Valeur métier
V3 -> Compagnon cognitif adaptatif
V4 -> Action sur l'environnement
"@

New-File "pyproject.toml" @"
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "alfred"
version = "1.0.0"
description = "Assistant Cognitif Adaptatif - Local First"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
"@

# ══════════════════════════════════════════════════════════
# 9. ENVIRONNEMENT VIRTUEL PYTHON
# ══════════════════════════════════════════════════════════
Write-Host "`n[9/9] Environnement Python..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "  Création du venv..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "  ✅ .venv créé" -ForegroundColor Green
} else {
    Write-Host "  ✅ .venv existe déjà" -ForegroundColor Green
}

Write-Host "`n  Pour activer le venv :" -ForegroundColor Yellow
Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor White

# ══════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║            ✅ Bootstrap terminé !                ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines étapes :" -ForegroundColor Yellow
Write-Host "  1. Copier paths.py à la racine du projet" -ForegroundColor White
Write-Host "  2. .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  3. pip install -r requirements.txt" -ForegroundColor White
Write-Host "  4. Copier .env.example -> .env et remplir les valeurs" -ForegroundColor White
Write-Host "  5. python paths.py  (vérification des chemins)" -ForegroundColor White
Write-Host "  6. python -m src.main  (premier lancement)" -ForegroundColor White
Write-Host ""