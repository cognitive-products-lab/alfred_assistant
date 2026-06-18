"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TOOLS
FILE         : tools/apply_headers.py
ROLE         : Applique les en-tetes standard ALFRED sur les fichiers Python manquants

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V2.0
STATUS       : ACTIVE

DESCRIPTION :
Parcourt src/, tests/, tools/ et ajoute un header standard sur tout fichier
Python n'en ayant pas encore. Ne modifie pas les fichiers deja headeres.
Genere un rapport JSON + affichage console.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # D:\PROJET_ALFRED\ALFRED_PC
TODAY = datetime.now().strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# Répertoires à scanner et à exclure
# ---------------------------------------------------------------------------
SCAN_DIRS = ["src", "tests", "tools", "scripts", "dashboard"]

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", "dist", "build", "_BACKUPS", "backups", "backup",
    "reports", ".vs", ".claude", "worktrees", "site-packages",
}

# ---------------------------------------------------------------------------
# Détection de bloc selon le chemin ALFRED_PC
# ---------------------------------------------------------------------------
BLOCK_MAP = [
    # Security first (priorité haute)
    (("src/security",),                              "B20", "Cybersecurite Zero Trust"),
    # Conversation / Audio
    (("src/conversation/input",),                    "B01", "Interaction conversationnelle"),
    (("src/conversation/nlp",),                      "B01", "NLP & Traitement langage"),
    (("src/conversation/output",),                   "B07", "TTS & Synthese vocale"),
    (("src/conversation",),                          "B01", "Pipeline conversationnel"),
    # LLM
    (("src/llm",),                                   "B04", "LLM Router Ollama/OpenAI"),
    # Memory
    (("src/memory",),                                "B02", "Memoire & RAG"),
    # AI / Cognitive
    (("src/ai",),                                    "B11", "Intelligence cognitive"),
    # Avatar / UI
    (("src/ui", "src/avatar"),                       "B15", "Avatar & Interface visuelle"),
    # Core / Orchestration
    (("src/core",),                                  "B19", "Integration main.py"),
    # Commands / Modes
    (("src/commands",),                              "B09", "Commandes & modes"),
    # Wellbeing
    (("src/wellbeing",),                             "B10", "Wellbeing & regulation"),
    # Config / Security network
    (("src/network", "config/network"),              "B18", "Config reseau Zero Trust"),
    # Tests
    (("tests/security",),                            "B20", "Tests securite B20"),
    (("tests",),                                     "TESTS", "Suite de tests"),
    # Tools / Dashboard
    (("tools/dashboard_tools",),                     "B20", "Dashboard outils"),
    (("tools",),                                     "TOOLS", "Outils projet"),
    (("dashboard",),                                 "DASHBOARD", "Dashboard"),
    (("scripts",),                                   "SCRIPTS", "Scripts maintenance"),
]


def detect_block(path: Path) -> tuple[str, str]:
    """Retourne (block_id, block_label) selon le chemin."""
    rel = path.relative_to(ROOT).as_posix().lower()
    for patterns, block, label in BLOCK_MAP:
        if any(rel.startswith(p.lower()) for p in patterns):
            return block, label
    return "GLOBAL", "Module ALFRED"


# ---------------------------------------------------------------------------
# Détection d'un header existant (deux styles)
# ---------------------------------------------------------------------------
def already_has_header(content: str) -> bool:
    head = content[:1500]
    return (
        "PROJECT" in head          # style docstring : PROJECT      : ALFRED
        or "# ALFRED" in head      # style commentaire : # ALFRED — ...
        or "<!--" in head[:20]     # HTML
        or "PROJECT : ALFRED" in head
    )


# ---------------------------------------------------------------------------
# Construction du header Python
# ---------------------------------------------------------------------------
def build_py_header(path: Path) -> str:
    block, label = detect_block(path)
    rel = path.relative_to(ROOT).as_posix()
    return f'''"""
PROJECT      : ALFRED
BLOCK        : {block}
FUNCTION     : XX.XX
FILE         : {rel}
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : {TODAY}
UPDATED      : {TODAY}
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
{label} — description a completer.
"""

'''


# ---------------------------------------------------------------------------
# Traitement d'un fichier
# ---------------------------------------------------------------------------
def process_file(path: Path, apply: bool, backup_dir: Path) -> dict:
    rel = str(path.relative_to(ROOT))
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding="utf-8-sig")
        except Exception as e:
            return {"file": rel, "status": "ERROR_READ", "detail": str(e)}

    if already_has_header(content):
        return {"file": rel, "status": "ALREADY_OK"}

    if path.suffix.lower() != ".py":
        return {"file": rel, "status": "SKIPPED_NOT_PY"}

    header = build_py_header(path)

    if not apply:
        return {"file": rel, "status": "DRY_RUN_READY", "block": detect_block(path)[0]}

    # Sauvegarde
    backup_path = backup_dir / path.relative_to(ROOT)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)

    path.write_text(header + content, encoding="utf-8")
    return {"file": rel, "status": "APPLIED", "block": detect_block(path)[0]}


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------
def scan(apply: bool) -> list[dict]:
    results: list[dict] = []
    backup_dir = ROOT / "backups" / f"headers_{TODAY}"

    if apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Backup : {backup_dir}")

    for scan_subdir in SCAN_DIRS:
        base = ROOT / scan_subdir
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            # Exclure dossiers bannis
            if any(excl in path.parts for excl in EXCLUDED_DIRS):
                continue
            results.append(process_file(path, apply, backup_dir))

    return results


# ---------------------------------------------------------------------------
# Rapport
# ---------------------------------------------------------------------------
def report(results: list[dict], apply: bool) -> None:
    applied  = [r for r in results if r["status"] == "APPLIED"]
    dry_run  = [r for r in results if r["status"] == "DRY_RUN_READY"]
    already  = [r for r in results if r["status"] == "ALREADY_OK"]
    errors   = [r for r in results if r["status"].startswith("ERROR")]
    skipped  = [r for r in results if r["status"].startswith("SKIPPED")]

    print(f"\n{'='*60}")
    print(f"  ALFRED — Apply Headers  ({'APPLY' if apply else 'DRY RUN'})")
    print(f"{'='*60}")
    print(f"  Total scannes  : {len(results)}")
    print(f"  Deja OK        : {len(already)}")
    if apply:
        print(f"  Headers ajoutes: {len(applied)}")
        if applied:
            by_block: dict = {}
            for r in applied:
                b = r.get("block","?")
                by_block[b] = by_block.get(b, 0) + 1
            for b, c in sorted(by_block.items()):
                print(f"    {b:12}: {c}")
    else:
        print(f"  A traiter      : {len(dry_run)}")
        if dry_run:
            by_block: dict = {}
            for r in dry_run:
                b = r.get("block","?")
                by_block[b] = by_block.get(b, 0) + 1
            for b, c in sorted(by_block.items()):
                print(f"    {b:12}: {c}")
    print(f"  Ignores        : {len(skipped)}")
    print(f"  Erreurs        : {len(errors)}")
    for e in errors:
        print(f"    {e['file']} — {e.get('detail','')}")

    # Sauvegarde JSON
    rep_dir = ROOT / "reports" / "standardization"
    rep_dir.mkdir(parents=True, exist_ok=True)
    rep_file = rep_dir / "apply_headers_report.json"
    rep_file.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "APPLY" if apply else "DRY_RUN",
        "summary": {
            "total": len(results), "applied": len(applied),
            "already_ok": len(already), "dry_run_ready": len(dry_run),
            "errors": len(errors),
        },
        "applied_files": [r["file"] for r in applied],
        "dry_run_files": [r["file"] for r in dry_run],
        "errors": errors,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Rapport : {rep_file}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    apply = "--apply" in sys.argv

    print(f"\nALFRED — Apply Headers V2.0")
    print(f"Mode : {'APPLY' if apply else 'DRY RUN (ajouter --apply pour appliquer)'}")
    print(f"Root : {ROOT}")

    results = scan(apply)
    report(results, apply)
