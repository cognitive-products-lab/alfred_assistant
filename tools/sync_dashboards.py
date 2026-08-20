"""
PROJECT  : ALFRED
BLOCK    : B23
FUNCTION : 23.02 — Orchestration & planification quotidienne
FILE     : tools/sync_dashboards.py
ROLE     : Copie quotidienne des JSON dashboards ALFRED_PC -> ALFRED_WEB/static/dashboard/
           puis git commit + push pour declencher le deploiement Render automatiquement.
USAGE    : python tools/sync_dashboards.py
SCHEDULE : Planificateur Windows - tache ALFRED_SyncDashboards - tous les jours a 07h00
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ALFRED_PC = Path(__file__).resolve().parents[1]
ROOT = ALFRED_PC.parent

SRC_DATA              = ALFRED_PC / "dashboard/dashboard_data/dashboard_data.json"
SRC_SECURITY          = ALFRED_PC / "dashboard/dashboard_security/dashboard_security.json"
SRC_TESTS             = ALFRED_PC / "dashboard/dashboard_tests/dashboard_tests.json"
SRC_GOUVERNANCE       = ALFRED_PC / "dashboard/dashboard_gouvernance/dashboard_gouvernance.json"
SRC_GOUVERNANCE_DATA  = ALFRED_PC / "dashboard/dashboard_gouvernance/dashboard_gouvernance_data.json"
SRC_KNOWLEDGE_DATA    = ALFRED_PC / "dashboard/dashboard_knowledges_tool/knowledge_dashboard_data.json"
SRC_CONFORMITE        = ALFRED_PC / "dashboard/dashboard_conformite/dashboard_conformite.json"
SRC_VULNERABILITES    = ALFRED_PC / "dashboard/dashboard_vulnerabilites/dashboard_vulnerabilites.json"
SRC_RISK_IMPACT       = ALFRED_PC / "dashboard/dashboard_risk_impact/dashboard_risk_impact.json"
SRC_SECURITY_REPORT   = ALFRED_PC / "dashboard/dashboard_security_report/dashboard_security_report.json"

WEB_ROOT = ROOT / "ALFRED_WEB"
DEST_DIR = WEB_ROOT / "static/dashboard"

DEST_DATA              = DEST_DIR / "dashboard_data.json"
DEST_SECURITY          = DEST_DIR / "dashboard_security.json"
DEST_TESTS             = DEST_DIR / "dashboard_test.json"
DEST_GOUVERNANCE       = DEST_DIR / "dashboard_gouvernance.json"
DEST_GOUVERNANCE_DATA  = DEST_DIR / "dashboard_gouvernance_data.json"
DEST_KNOWLEDGE_DATA    = DEST_DIR / "knowledge_dashboard_data.json"
DEST_CONFORMITE        = DEST_DIR / "dashboard_conformite.json"
DEST_VULNERABILITES    = DEST_DIR / "dashboard_vulnerabilites.json"
DEST_RISK_IMPACT       = DEST_DIR / "dashboard_risk_impact.json"
DEST_SECURITY_REPORT   = DEST_DIR / "dashboard_security_report.json"
LOG_FILE               = DEST_DIR / "sync_log.json"

UPDATE_GOUVERNANCE    = ALFRED_PC / "tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py"
UPDATE_CONFORMITE     = ALFRED_PC / "tools/dashboard_tools/dashboard_conformite/update_conformite_data.py"
UPDATE_VULNERABILITES = ALFRED_PC / "tools/dashboard_tools/dashboard_vulnerabilites/update_vulnerabilites_data.py"
UPDATE_RISK_IMPACT    = ALFRED_PC / "tools/dashboard_tools/dashboard_risk_impact/update_risk_impact_data.py"
GEN_KNOWLEDGE         = ALFRED_PC / "dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py"
GEN_SECURITY_REPORT   = ALFRED_PC / "src/security/html_report.py"

# Patterns sensibles a anonymiser avant publication web
_SENSITIVE_PATTERNS = {
    "local_pc": "device_001",
    "demo_device_live": "device_002",
    "zt_test_device_001": "device_003",
    "SECRET_KEY": "Clé principale",
    "FERNET_KEY": "Clé chiffrement",
    "PIN_SALT": "Sel authentification",
    "http://172.16.0.1/internal": "adresse réseau interne bloquée",
    "http://169.254.169.254/metadata": "métadonnées cloud bloquées",
    "http://localhost/admin": "chemin administratif bloqué",
    "http://local/config": "chemin de configuration bloqué",
    "http://metadata/latest": "chemin de métadonnées bloqué",
}


def _sanitize_security_json(data: dict) -> dict:
    import copy

    d = copy.deepcopy(data)
    text = json.dumps(d, ensure_ascii=False)
    for raw, clean in _SENSITIVE_PATTERNS.items():
        text = text.replace(raw, clean)
    d = json.loads(text)

    for dev in d.get("devices", {}).get("devices", []):
        dev.pop("owner", None)

    if "last_event" in d.get("audit", {}):
        ev = d["audit"]["last_event"]
        for field in ("user_id", "device_id", "request_id", "role"):
            ev.pop(field, None)
        if ev.get("timestamp"):
            ev["timestamp"] = ev["timestamp"][:10]

    return d


def sync_file(src: Path, dest: Path, label: str, sanitize: bool = False) -> dict:
    if not src.exists():
        return {"file": label, "status": "ERROR", "reason": f"Source introuvable : {src}"}

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    if sanitize:
        raw = json.loads(src.read_text(encoding="utf-8"))
        cleaned = _sanitize_security_json(raw)
        dest.write_text(json.dumps(cleaned, ensure_ascii=False, indent=4), encoding="utf-8")
    else:
        shutil.copy2(src, dest)

    size = dest.stat().st_size
    return {"file": label, "status": "OK" + (" [sanitisé]" if sanitize else ""), "bytes": size}


def git_push(ts: str) -> dict:
    def run(cmd: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, cwd=str(WEB_ROOT), capture_output=True, text=True)

    status = run(["git", "status", "--porcelain", "static/dashboard/"])
    if not status.stdout.strip():
        return {"status": "SKIP", "reason": "Aucun changement detecte dans static/dashboard/"}

    run([
        "git", "add",
        "static/dashboard/dashboard_data.json",
        "static/dashboard/dashboard_security.json",
        "static/dashboard/dashboard_test.json",
        "static/dashboard/dashboard_gouvernance.json",
        "static/dashboard/dashboard_gouvernance_data.json",
        "static/dashboard/knowledge_dashboard_data.json",
        "static/dashboard/dashboard_conformite.json",
        "static/dashboard/dashboard_vulnerabilites.json",
        "static/dashboard/dashboard_risk_impact.json",
        "static/dashboard/dashboard_security_report.json",
        "static/dashboard/sync_log.json",
    ])

    msg = f"chore(dashboard): sync JSON quotidien {ts[:10]}"
    commit = run(["git", "commit", "-m", msg])
    if commit.returncode != 0:
        return {"status": "ERROR", "reason": commit.stderr.strip()}

    push = run(["git", "push", "origin", "main"])
    if push.returncode != 0:
        return {"status": "ERROR", "reason": push.stderr.strip()}

    return {"status": "OK", "commit": msg}


def regenerate_knowledge_dashboard() -> dict:
    """Exécute generate_knowledge_dashboard.py pour recalculer le JSON knowledges."""
    if not GEN_KNOWLEDGE.exists():
        return {"status": "SKIP", "reason": "generate_knowledge_dashboard.py introuvable"}
    result = subprocess.run(
        ["python", str(GEN_KNOWLEDGE)],
        cwd=str(ALFRED_PC),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return {"status": "ERROR", "reason": result.stderr.strip()[:200]}
    return {"status": "OK"}


def _run_update_script(script: Path, label: str) -> dict:
    """Lance un script update_*.py et retourne le statut."""
    if not script.exists():
        return {"status": "SKIP", "reason": f"{script.name} introuvable"}
    result = subprocess.run(
        ["python", str(script)],
        cwd=str(ALFRED_PC),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return {"status": "ERROR", "reason": result.stderr.strip()[:200]}
    return {"status": "OK"}


def regenerate_gouvernance() -> dict:
    return _run_update_script(UPDATE_GOUVERNANCE, "Gouvernance")


def regenerate_conformite() -> dict:
    return _run_update_script(UPDATE_CONFORMITE, "Conformité")


def regenerate_vulnerabilites() -> dict:
    return _run_update_script(UPDATE_VULNERABILITES, "Vulnérabilités")


def regenerate_risk_impact() -> dict:
    return _run_update_script(UPDATE_RISK_IMPACT, "Risques & Impact")


def regenerate_security_report() -> dict:
    return _run_update_script(GEN_SECURITY_REPORT, "Rapport Sécurité")


def main() -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    print(f"\n=== Sync dashboards ALFRED - {ts} ===\n")

    print("  Régénération knowledge_dashboard_data.json...")
    regen_k = regenerate_knowledge_dashboard()
    print(f"  [{regen_k['status']}]  generate_knowledge_dashboard.py  {regen_k.get('reason', '')}\n")

    for label, fn in [
        ("dashboard_gouvernance_data.json", regenerate_gouvernance),
        ("dashboard_conformite.json",       regenerate_conformite),
        ("dashboard_vulnerabilites.json",   regenerate_vulnerabilites),
        ("dashboard_risk_impact.json",      regenerate_risk_impact),
        ("dashboard_security_report.json",  regenerate_security_report),
    ]:
        print(f"  Régénération {label}...")
        r = fn()
        print(f"  [{r['status']}]  {label}  {r.get('reason', '')}\n")

    results = [
        sync_file(SRC_DATA,             DEST_DATA,             "dashboard_data.json"),
        sync_file(SRC_SECURITY,         DEST_SECURITY,         "dashboard_security.json", sanitize=True),
        sync_file(SRC_TESTS,            DEST_TESTS,            "dashboard_test.json"),
        sync_file(SRC_GOUVERNANCE,      DEST_GOUVERNANCE,      "dashboard_gouvernance.json"),
        sync_file(SRC_GOUVERNANCE_DATA, DEST_GOUVERNANCE_DATA, "dashboard_gouvernance_data.json"),
        sync_file(SRC_KNOWLEDGE_DATA,   DEST_KNOWLEDGE_DATA,   "knowledge_dashboard_data.json"),
        sync_file(SRC_CONFORMITE,       DEST_CONFORMITE,       "dashboard_conformite.json"),
        sync_file(SRC_VULNERABILITES,   DEST_VULNERABILITES,   "dashboard_vulnerabilites.json"),
        sync_file(SRC_RISK_IMPACT,      DEST_RISK_IMPACT,      "dashboard_risk_impact.json"),
        sync_file(SRC_SECURITY_REPORT,  DEST_SECURITY_REPORT,  "dashboard_security_report.json"),
    ]

    all_ok = all(r["status"].startswith("OK") for r in results)

    for r in results:
        tag = "OK" if r["status"].startswith("OK") else "ERREUR"
        detail = r.get("bytes", r.get("reason", ""))
        print(f"  [{tag}]  {r['file']}  ({detail})")

    git_result = {"status": "SKIP", "reason": "Copie en erreur — push annulé"}
    if all_ok:
        print("\n  Git push vers GitHub (-> Render)...")
        git_result = git_push(ts)
        tag = git_result["status"]
        detail = git_result.get("commit", git_result.get("reason", ""))
        print(f"  [{tag}]  {detail}")

    log = {"synced_at": ts, "sync_results": results, "git": git_result}
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n  Log : {LOG_FILE}")
    print("==========================================")


if __name__ == "__main__":
    main()
