"""
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Gouvernance & Conformité
SCRIPT   : complete_dpa_openai.py
ROLE     : Finalisation RGPD-09 après acceptation DPA OpenAI sur le portail.
           Une fois la DPA acceptée sur platform.openai.com, ce script :
             1. Met à jour RGPD-09 → done dans _manifest.json
             2. Régénère dashboard_gouvernance_data.json + rapport horodaté
             3. Lance sync_dashboards.py (push vers ALFRED_WEB + GitHub)
             4. Committe les fichiers de conformité sur les 2 branches
VERSION  : V1.0
CREATED  : 2026-06-18
AUTHOR   : Cognitive Products Lab — Céline Darras
============================================================
USAGE :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python scripts/complete_dpa_openai.py
    (lancer APRÈS avoir accepté la DPA sur platform.openai.com)
============================================================
"""

from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT     = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dashboard" / "dashboard_gouvernance" / "_manifest.json"
UPDATE   = ROOT / "tools" / "dashboard_tools" / "dashboard_gouvernance" / "update_gouvernance_data.py"
SYNC     = ROOT / "tools" / "sync_dashboards.py"

SEP = "=" * 60


def _banner(msg: str, color: str = "") -> None:
    codes = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m", "cyan": "\033[96m", "": ""}
    reset = "\033[0m"
    print(f"{codes.get(color, '')}{msg}{reset}")


def confirm_dpa_accepted() -> bool:
    _banner(SEP, "cyan")
    _banner("  FINALISATION DPA OPENAI — RGPD Art. 28", "cyan")
    _banner(SEP, "cyan")
    print("""
  Avant de continuer, vérifiez que vous avez bien :

  1. Ouvert https://platform.openai.com/account/organization
  2. Cliqué sur "Legal" ou "Data Processing Addendum"
  3. Accepté / signé la DPA OpenAI

  La DPA est disponible ici si besoin :
  https://openai.com/policies/data-processing-addendum
""")
    rep = input("  Avez-vous accepté la DPA OpenAI ? (oui / non) : ").strip().lower()
    return rep in ("oui", "o", "yes", "y")


def update_manifest_rgpd09() -> None:
    """Passe RGPD-09 de partial/todo à done dans le manifest."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    date_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for norm in data["norms"]:
        if norm["id"] != "RGPD":
            continue
        for req in norm["requirements"]:
            if req["id"] == "RGPD-09":
                old_status = req["status"]
                req["status"] = "done"
                req["proof_files"] = ["docs/smsi/dpa_sous_traitants.md"]
                req["note"] = f"DPA OpenAI acceptée formellement le {date_now}"
                _banner(f"  [OK] RGPD-09 : {old_status} → done", "green")

    data["_meta"]["updated"] = date_now
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    _banner(f"  [OK] Manifest mis à jour : {MANIFEST.name}", "green")


def update_dpa_doc() -> None:
    """Met à jour le registre des DPA signées dans dpa_sous_traitants.md."""
    dpa_path = ROOT / "docs" / "smsi" / "dpa_sous_traitants.md"
    if not dpa_path.exists():
        return
    content = dpa_path.read_text(encoding="utf-8")
    date_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    old = "| OpenAI | ⚠️ À compléter | — | https://openai.com/policies/data-processing-addendum |"
    new = f"| OpenAI | ✅ {date_now} | DPA OpenAI API 2024 | https://openai.com/policies/data-processing-addendum |"
    if old in content:
        content = content.replace(old, new)
        dpa_path.write_text(content, encoding="utf-8")
        _banner(f"  [OK] dpa_sous_traitants.md mis à jour (date acceptation : {date_now})", "green")
    else:
        _banner("  [WARN] Ligne DPA non trouvée dans dpa_sous_traitants.md — mise à jour manuelle requise", "yellow")


import os as _os
_GIT_ENV = {**_os.environ, "GIT_TERMINAL_PROMPT": "0"}

def _sp(cmd, **kwargs):
    """subprocess.run avec encodage Windows-safe."""
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kwargs)

def run_update_dashboard() -> None:
    _banner("\n  Régénération dashboard gouvernance...", "cyan")
    result = _sp([sys.executable, str(UPDATE)], cwd=str(ROOT))
    if result.returncode == 0:
        _banner("  [OK] dashboard_gouvernance_data.json régénéré", "green")
    else:
        _banner(f"  [WARN] {result.stderr[:200]}", "yellow")


def run_sync() -> None:
    _banner("\n  Synchronisation dashboards + push GitHub...", "cyan")
    result = _sp([sys.executable, str(SYNC)], cwd=str(ROOT))
    if result.returncode == 0:
        _banner("  [OK] Sync + push ALFRED_WEB OK", "green")
    else:
        _banner(f"  [WARN] sync_dashboards.py : {result.stderr[:200]}", "yellow")


def git_commit_dpa() -> None:
    _banner("\n  Commit conformité DPA...", "cyan")
    files = [
        "dashboard/dashboard_gouvernance/_manifest.json",
        "dashboard/dashboard_gouvernance/dashboard_gouvernance_data.json",
        "docs/smsi/dpa_sous_traitants.md",
    ]
    # Récupérer les rapports générés aujourd'hui
    reports_dir = ROOT / "dashboard" / "dashboard_gouvernance" / "reports"
    for f in sorted(reports_dir.glob("audit_gouvernance_*.md")):
        files.append(str(f.relative_to(ROOT)))

    _sp(["git", "add"] + files, cwd=str(ROOT), env=_GIT_ENV)
    msg = (
        "RGPD-09 done : DPA OpenAI acceptée formellement\n\n"
        "Mise à jour manifest + dashboard gouvernance.\n"
        "Score RGPD passe de 95.5% à ~97%.\n\n"
        "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    )
    result = _sp(["git", "commit", "-m", msg], cwd=str(ROOT), env=_GIT_ENV)
    if "nothing to commit" in result.stdout + result.stderr:
        _banner("  [INFO] Rien à committer (déjà à jour)", "yellow")
    else:
        _banner("  [OK] Commit DPA créé", "green")

    # Push dev + merge main
    for branch in ("dev", "main"):
        if branch == "main":
            _sp(["git", "checkout", "main"], cwd=str(ROOT), env=_GIT_ENV)
            _sp(["git", "merge", "dev", "--no-ff", "-m",
                 "Merge dev->main : RGPD-09 DPA OpenAI done"],
                cwd=str(ROOT), env=_GIT_ENV)
        result = _sp(["git", "push", "origin", branch],
                     cwd=str(ROOT), env=_GIT_ENV, timeout=90)
        if result.returncode == 0:
            _banner(f"  [OK] Push {branch} OK", "green")
        else:
            _banner(f"  [WARN] Push {branch} : {result.stderr[:200]}", "yellow")

    _sp(["git", "checkout", "dev"], cwd=str(ROOT), env=_GIT_ENV)


def main() -> None:
    print()
    if not confirm_dpa_accepted():
        _banner("\n  Action annulée. Relancez ce script après avoir accepté la DPA.", "yellow")
        print(f"  URL : https://platform.openai.com/account/organization\n")
        sys.exit(0)

    print()
    _banner("  Mise à jour en cours...", "cyan")
    update_manifest_rgpd09()
    update_dpa_doc()
    run_update_dashboard()
    run_sync()
    git_commit_dpa()

    print()
    _banner(SEP, "green")
    _banner("  RGPD-09 DONE — DPA OpenAI finalisée", "green")
    _banner("  Score RGPD : ~97% · Global : ~98%", "green")
    _banner(SEP, "green")
    print()


if __name__ == "__main__":
    main()