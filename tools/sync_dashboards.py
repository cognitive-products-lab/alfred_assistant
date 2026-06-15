"""
PROJECT  : ALFRED
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

SRC_DATA = ALFRED_PC / "dashboard/dashboard_data/dashboard_data.json"
SRC_SECURITY = ALFRED_PC / "dashboard/dashboard_security/dashboard_security.json"
SRC_TESTS = ALFRED_PC / "dashboard/dashboard_tests/dashboard_tests.json"

WEB_ROOT = ROOT / "ALFRED_WEB"
DEST_DIR = WEB_ROOT / "static/dashboard"

DEST_DATA = DEST_DIR / "dashboard_data.json"
DEST_SECURITY = DEST_DIR / "dashboard_security.json"
DEST_TESTS = DEST_DIR / "dashboard_test.json"
LOG_FILE = DEST_DIR / "sync_log.json"

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


def main() -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    print(f"\n=== Sync dashboards ALFRED - {ts} ===\n")

    results = [
        sync_file(SRC_DATA, DEST_DATA, "dashboard_data.json"),
        sync_file(SRC_SECURITY, DEST_SECURITY, "dashboard_security.json", sanitize=True),
        sync_file(SRC_TESTS, DEST_TESTS, "dashboard_test.json"),
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
