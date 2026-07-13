# ============================================================
# ALFRED — paths.py
# Gestion centralisée de tous les chemins du projet
# ============================================================
# POURQUOI CE FICHIER EST CRITIQUE :
# Tous les guides V1→V4 utilisent open("config/v3/...") etc.
# Ces chemins relatifs cassent selon le dossier d'exécution.
# Ce fichier résout le problème une fois pour toutes.
#
# UTILISATION dans n'importe quel module :
#   from paths import PATHS
#   with open(PATHS.config_v2 / "signal_weights.json") as f:
#       ...
#
# STATUS : VALIDATED
# ============================================================

from pathlib import Path


# ── Racine du projet ─────────────────────────────────────
# Ce fichier est à la racine de ALFRED_PC/
# Tous les chemins sont calculés relativement à lui.
BASE_DIR = Path(__file__).resolve().parent


# ── Source code ──────────────────────────────────────────
SRC_DIR         = BASE_DIR / "src"
SRC_SECURITY    = SRC_DIR / "security"
SRC_V1          = SRC_DIR / "v1"
SRC_V2          = SRC_DIR / "v2"
SRC_V2PP        = SRC_DIR / "v2pp"
SRC_V3          = SRC_DIR / "v3"
SRC_V4          = SRC_DIR / "v4"
SRC_REGULATION  = SRC_DIR / "regulation"
SRC_HEALTH      = SRC_DIR / "health"


# ── Configuration ─────────────────────────────────────────
CONFIG_DIR           = BASE_DIR / "config"
CONFIG_SECURITY      = CONFIG_DIR / "security"
CONFIG_V1            = CONFIG_DIR / "v1"
CONFIG_V2            = CONFIG_DIR / "v2"
CONFIG_V2PP          = CONFIG_DIR / "v2pp"
CONFIG_V3            = CONFIG_DIR / "v3"
CONFIG_V4            = CONFIG_DIR / "v4"
CONFIG_REGULATION    = CONFIG_DIR / "regulation"
CONFIG_HEALTH        = CONFIG_DIR / "health"
CONFIG_QUESTIONNAIRE = CONFIG_DIR / "questionnaire"


# ── Données ───────────────────────────────────────────────
DATA_DIR        = BASE_DIR / "data"
DATA_SECURITY   = DATA_DIR / "security"
DATA_MEMORY     = DATA_DIR / "memory"
DATA_PROFILE    = DATA_DIR / "profile"
DATA_ACTIONS    = DATA_DIR / "actions"
DATA_CONTEXT    = DATA_DIR / "context"
DATA_V1         = DATA_DIR / "v1"
DATA_V2         = DATA_DIR / "v2"
DATA_V2PP       = DATA_DIR / "v2pp"
DATA_V3         = DATA_DIR / "v3"
DATA_V4         = DATA_DIR / "v4"
DATA_HEALTH     = DATA_DIR / "health"


# ── Knowledges ────────────────────────────────────────────
KNOWLEDGE_DIR           = BASE_DIR / "knowledges"
KNOWLEDGE_HUMAN         = KNOWLEDGE_DIR / "human"
KNOWLEDGE_PROFESSIONAL  = KNOWLEDGE_DIR / "professional"
KNOWLEDGE_LIFESTYLE     = KNOWLEDGE_DIR / "lifestyle"


# ── Logs ─────────────────────────────────────────────────
LOGS_DIR        = BASE_DIR / "logs"


# ── Assets ───────────────────────────────────────────────
ASSETS_DIR      = BASE_DIR / "assets"
ASSETS_AVATAR   = ASSETS_DIR / "avatar"
ASSETS_AUDIO    = ASSETS_DIR / "audio"


# ── Auth ─────────────────────────────────────────────────
AUTH_DIR        = BASE_DIR / "auth"


# ── Speech ───────────────────────────────────────────────
SPEECH_DIR      = BASE_DIR / "speech"


# ── Tests ─────────────────────────────────────────────────
TESTS_DIR       = BASE_DIR / "tests"


# ── Dashboard ─────────────────────────────────────────────
# NB : dashboard_manifest/dashboard_data/dashboard_html ne sont utilisés
# nulle part ailleurs dans le code (vérifié le 13/07/2026, point C4-D du plan
# d'action) — uniquement affichés par le print() de vérification ci-dessous.
# Redirigés vers les vrais fichiers actifs de dashboard/dashboard_data/ suite
# à l'archivage des 3 duplicatas obsolètes (dashboard/_archive/).
DASHBOARD_DIR         = BASE_DIR / "dashboard"
DASHBOARD_DATA_DIR    = DASHBOARD_DIR / "dashboard_data"
DASHBOARD_MANIFEST    = DASHBOARD_DATA_DIR / "dashboard_data_manifest.json"
DASHBOARD_DATA        = DASHBOARD_DATA_DIR / "dashboard_data.json"
DASHBOARD_HTML        = DASHBOARD_DATA_DIR / "ALFRED_DASHBOARD_DYNAMIC.html"


# ── Tools ─────────────────────────────────────────────────
TOOLS_DIR             = BASE_DIR / "tools"
MANIFEST_TARGET       = TOOLS_DIR / "dashboard_manifest_target.json"
TARGET_REPORT_JSON    = TOOLS_DIR / "dashboard_target_report.json"


# ── Docs ─────────────────────────────────────────────────
DOCS_DIR              = BASE_DIR / "docs"
TARGET_REPORT_MD      = DOCS_DIR / "dashboard_target_report.md"


# ── Fichiers clés ─────────────────────────────────────────
ENV_FILE        = BASE_DIR / ".env"
ENV_EXAMPLE     = BASE_DIR / ".env.example"


# ─────────────────────────────────────────────────────────
# Classe de regroupement (accès style PATHS.config_v2)
# ─────────────────────────────────────────────────────────
class _Paths:
    # Base
    base            = BASE_DIR
    src             = SRC_DIR
    config          = CONFIG_DIR
    data            = DATA_DIR
    logs            = LOGS_DIR
    assets          = ASSETS_DIR
    knowledges      = KNOWLEDGE_DIR

    # Sécurité
    src_security    = SRC_SECURITY
    config_security = CONFIG_SECURITY
    data_security   = DATA_SECURITY

    # Versions source
    src_v1          = SRC_V1
    src_v2          = SRC_V2
    src_v2pp        = SRC_V2PP
    src_v3          = SRC_V3
    src_v4          = SRC_V4
    src_regulation  = SRC_REGULATION
    src_health      = SRC_HEALTH

    # Versions config
    config_v1            = CONFIG_V1
    config_v2            = CONFIG_V2
    config_v2pp          = CONFIG_V2PP
    config_v3            = CONFIG_V3
    config_v4            = CONFIG_V4
    config_regulation    = CONFIG_REGULATION
    config_health        = CONFIG_HEALTH
    config_questionnaire = CONFIG_QUESTIONNAIRE

    # Versions data
    data_v1         = DATA_V1
    data_v2         = DATA_V2
    data_v2pp       = DATA_V2PP
    data_v3         = DATA_V3
    data_v4         = DATA_V4
    data_health     = DATA_HEALTH

    # Mémoire
    data_memory     = DATA_MEMORY
    data_profile    = DATA_PROFILE
    data_actions    = DATA_ACTIONS
    data_context    = DATA_CONTEXT

    # Knowledges
    knowledge_human         = KNOWLEDGE_HUMAN
    knowledge_professional  = KNOWLEDGE_PROFESSIONAL
    knowledge_lifestyle     = KNOWLEDGE_LIFESTYLE
    # Sous-dossiers human
    knowledge_psychology    = KNOWLEDGE_HUMAN / "psychology"
    knowledge_softskills    = KNOWLEDGE_LIFESTYLE / "softskills"
    knowledge_memory        = KNOWLEDGE_HUMAN / "cognition"
    knowledge_reasoning     = KNOWLEDGE_HUMAN / "cognition"
    # Sous-dossiers cpl
    knowledge_cpl_human_com  = KNOWLEDGE_DIR / "cpl" / "human_communication"
    knowledge_cpl_human_org  = KNOWLEDGE_DIR / "cpl" / "human_organization"
    knowledge_cpl_business   = KNOWLEDGE_DIR / "cpl" / "business_piloting"
    knowledge_cpl_strategy   = KNOWLEDGE_DIR / "cpl" / "strategy"
    knowledge_cpl_execution  = KNOWLEDGE_DIR / "cpl" / "execution"
    knowledge_cpl_product    = KNOWLEDGE_DIR / "cpl" / "product_ia"
    knowledge_cpl_ethics     = KNOWLEDGE_DIR / "cpl" / "ethics_governance"

    # Dashboard
    dashboard           = DASHBOARD_DIR
    dashboard_manifest  = DASHBOARD_MANIFEST
    dashboard_data      = DASHBOARD_DATA
    dashboard_html      = DASHBOARD_HTML

    # Tools
    tools               = TOOLS_DIR
    manifest_target     = MANIFEST_TARGET
    target_report_json  = TARGET_REPORT_JSON

    # Docs
    docs                = DOCS_DIR
    target_report_md    = TARGET_REPORT_MD

    # Divers
    auth            = AUTH_DIR
    speech          = SPEECH_DIR
    tests           = TESTS_DIR
    env_file        = ENV_FILE


# Instance globale unique — importer cette variable partout
PATHS = _Paths()


# ─────────────────────────────────────────────────────────
# Utilitaire : créer tous les dossiers nécessaires
# ─────────────────────────────────────────────────────────
def ensure_dirs():
    """
    Crée tous les dossiers du projet s'ils n'existent pas.
    À appeler au démarrage de main.py.
    """
    dirs = [
        SRC_SECURITY,
        CONFIG_SECURITY, CONFIG_V1, CONFIG_V2, CONFIG_V2PP, CONFIG_V3, CONFIG_V4,
        CONFIG_REGULATION, CONFIG_HEALTH, CONFIG_QUESTIONNAIRE,
        DATA_SECURITY, DATA_MEMORY, DATA_PROFILE, DATA_ACTIONS, DATA_CONTEXT,
        DATA_V1, DATA_V2, DATA_V2PP, DATA_V3, DATA_V4, DATA_HEALTH,
        KNOWLEDGE_HUMAN, KNOWLEDGE_PROFESSIONAL, KNOWLEDGE_LIFESTYLE,
        LOGS_DIR, ASSETS_AVATAR, ASSETS_AUDIO,
        AUTH_DIR, SPEECH_DIR, TESTS_DIR,
        DASHBOARD_DIR, TOOLS_DIR, DOCS_DIR,
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────
# Test rapide (lancer directement : python paths.py)
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== ALFRED — Vérification des chemins ===")
    print(f"BASE_DIR          : {BASE_DIR}")
    print(f"CONFIG_V2         : {PATHS.config_v2}")
    print(f"DATA_V3           : {PATHS.data_v3}")
    print(f"SRC_SECURITY      : {PATHS.src_security}")
    print(f"DASHBOARD_DIR     : {PATHS.dashboard}")
    print(f"DASHBOARD_MANIFEST: {PATHS.dashboard_manifest}")
    print(f"MANIFEST_TARGET   : {PATHS.manifest_target}")
    print(f"TARGET_REPORT_MD  : {PATHS.target_report_md}")
    print()
    print("Création des dossiers...")
    ensure_dirs()
    print("✅ Tous les dossiers sont prêts.")