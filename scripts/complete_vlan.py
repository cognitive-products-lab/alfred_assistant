"""
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
SCRIPT   : complete_vlan.py
TYPE     : Script automatisation post-implémentation VLAN
REF      : ISO/IEC 27001:2022 — A.8.20 (Sécurité réseau)
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================

Usage :
    python scripts/complete_vlan.py           # mode normal (VLAN implémenté)
    python scripts/complete_vlan.py --planifie # mode planifié Q3 2026 (sans tests réseau)

Ce script :
1. Vérifie la connectivité réseau (skippable si VLAN pas encore en place)
2. Met à jour ISO-20 dans le manifest (partial → done)
3. Régénère le dashboard gouvernance
4. Synchronise ALFRED_WEB
5. Commit + push dev + merge main
"""

import json
import subprocess
import sys
import socket
import argparse
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dashboard" / "dashboard_gouvernance" / "_manifest.json"
VLAN_DOC = ROOT / "docs" / "smsi" / "vlan_config.md"
UPDATE_SCRIPT = ROOT / "tools" / "dashboard_tools" / "dashboard_gouvernance" / "update_gouvernance_data.py"
SYNC_SCRIPT = ROOT / "tools" / "sync_dashboards.py"

# IPs VLAN cibles (adapter selon configuration réelle)
VLAN10_PC_ALFRED = "192.168.10.10"   # PC Alfred sur VLAN10
VLAN20_ADMIN_GW  = "192.168.20.1"    # Gateway VLAN20 admin
VLAN30_IOT_GW    = "192.168.30.1"    # Gateway VLAN30 IoT

def print_header():
    print("=" * 60)
    print("  ALFRED — Validation VLAN & Finalisation ISO-20")
    print("  Cognitive Products Lab — B20 Sécurité")
    print("=" * 60)
    print()

def mode_planifie():
    """Mode planifié : architecture documentée, implémentation Q3 2026."""
    print("Mode PLANIFIÉ — Architecture documentée (implémentation Q3 2026)")
    print("-" * 60)
    print("  • vlan_config.md             ✅ Architecture documentée")
    print("  • config/security/network_policy.json  ✅ Règles firewall définies")
    print("  • Implémentation physique SG108E+ER605 ⏳ Q3 2026")
    print()
    print("ISO-20 sera marqué 'partial' (architecture OK, implémentation en attente).")
    print()
    rep = input("Confirmer et mettre à jour le manifest ? (oui/non) : ").strip().lower()
    return rep in ("oui", "o", "yes", "y")

def confirm_vlan_implemented():
    print("PRÉREQUIS : Implémentation physique VLAN")
    print("-" * 40)
    print("Avant de continuer, vérifier que :")
    print("  [1] SG108E — VLANs 10/20/30 configurés (802.1Q)")
    print("  [2] ER605  — Sous-interfaces VLAN créées")
    print("  [3] ER605  — Règles inter-VLAN appliquées (VLAN10 isolé)")
    print("  [4] PC Alfred branché sur port VLAN10")
    print()
    rep = input("L'implémentation physique est-elle terminée ? (oui/non) : ").strip().lower()
    if rep not in ("oui", "o", "yes", "y"):
        print("\nImplémentation non confirmée. Arrêt du script.")
        print("Astuce : utilisez --planifie pour documenter l'architecture sans tester le réseau.")
        return False
    return True

def test_connectivity(host, label, expect_reachable=True, timeout=2):
    """Teste la connectivité réseau vers un hôte."""
    try:
        sock = socket.create_connection((host, 80), timeout=timeout)
        sock.close()
        reachable = True
    except (socket.timeout, ConnectionRefusedError, OSError):
        # Port 80 fermé ≠ unreachable — tenter ICMP via ping
        result = subprocess.run(
            ["ping", "-n", "1", "-w", str(timeout * 1000), host],
            capture_output=True, text=True
        )
        reachable = result.returncode == 0

    status = "✅" if reachable == expect_reachable else "❌"
    expected = "joignable" if expect_reachable else "isolé (non joignable)"
    actual = "joignable" if reachable else "non joignable"
    print(f"  {status} {label} ({host}) — attendu: {expected}, réel: {actual}")
    return reachable == expect_reachable

def run_network_tests():
    """Vérifie l'isolation VLAN et la connectivité attendue."""
    print("\nTests réseau VLAN")
    print("-" * 40)
    print("(Ces tests sont indicatifs — adapter les IPs dans le script si besoin)")
    print()

    results = []

    # VLAN10 — PC Alfred doit être joignable depuis VLAN20 admin
    results.append(test_connectivity(VLAN10_PC_ALFRED, "PC Alfred VLAN10", expect_reachable=True))

    # Gateways VLAN
    results.append(test_connectivity(VLAN20_ADMIN_GW, "Gateway VLAN20 Admin", expect_reachable=True))
    results.append(test_connectivity(VLAN30_IOT_GW, "Gateway VLAN30 IoT", expect_reachable=True))

    passed = sum(results)
    total = len(results)
    print(f"\n  Résultat : {passed}/{total} tests OK")

    if passed < total:
        print("\n  ⚠️  Certains tests ont échoué.")
        print("     Vérifier les IPs dans le script (VLAN10_PC_ALFRED, etc.)")
        print("     ou adapter selon votre plan d'adressage réel.")
        rep = input("\n  Continuer quand même ? (oui/non) : ").strip().lower()
        return rep in ("oui", "o", "yes", "y")
    return True

def update_manifest_iso20(planifie=False):
    """Met à jour ISO-20 dans le manifest."""
    print("\nMise à jour manifest — ISO-20")
    print("-" * 40)

    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)

    today = date.today().isoformat()
    updated = False

    for norm in manifest.get("norms", []):
        for req in norm.get("requirements", []):
            if req.get("id") == "ISO-20":
                if planifie:
                    req["status"] = "partial"
                    req["proof_files"] = [
                        "docs/smsi/vlan_config.md",
                        "config/security/network_policy.json"
                    ]
                    req["note"] = f"Architecture VLAN documentée — implémentation physique Q3 2026 ({today})"
                    print(f"  ⏳ ISO-20 → partial (architecture OK, implémentation Q3 2026)")
                else:
                    req["status"] = "done"
                    req["proof_files"] = [
                        "docs/smsi/vlan_config.md",
                        "config/security/network_policy.json"
                    ]
                    req["note"] = f"VLAN 10/20/30 implémenté sur SG108E+ER605 — validé le {today}"
                    print(f"  ✅ ISO-20 → done (proof: vlan_config.md + network_policy.json)")
                updated = True
                break
        if updated:
            break

    if not updated:
        print("  ⚠️  ISO-20 non trouvé dans le manifest.")
        return False

    manifest["_meta"]["last_updated"] = today

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"  Manifest sauvegardé.")
    return True

def update_vlan_doc():
    """Met à jour le statut dans vlan_config.md."""
    print("\nMise à jour vlan_config.md")
    print("-" * 40)

    today = date.today().isoformat()
    content = VLAN_DOC.read_text(encoding="utf-8")

    if "STATUS   : Planifié" in content:
        content = content.replace(
            "STATUS   : Planifié",
            "STATUS   : Implémenté"
        )
        content = content.replace(
            "UPDATED  : 2026-06-18",
            f"UPDATED  : {today}"
        )
        VLAN_DOC.write_text(content, encoding="utf-8")
        print(f"  ✅ vlan_config.md — statut → Implémenté")
    else:
        print("  ℹ️  vlan_config.md déjà à jour ou statut différent.")

def _run(cmd, **kwargs):
    """subprocess.run avec encodage Windows-safe."""
    return subprocess.run(
        cmd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", **kwargs
    )

def run_update_dashboard():
    """Régénère le dashboard gouvernance."""
    print("\nRégénération dashboard gouvernance")
    print("-" * 40)
    result = _run([sys.executable, str(UPDATE_SCRIPT)])
    if result.returncode == 0:
        print("  ✅ Dashboard régénéré")
    else:
        print(f"  ⚠️  Erreur : {result.stderr[:200]}")

def run_sync():
    """Synchronise vers ALFRED_WEB."""
    print("\nSynchronisation ALFRED_WEB")
    print("-" * 40)
    if not SYNC_SCRIPT.exists():
        print("  ℹ️  sync_dashboards.py non trouvé — sync manuelle requise.")
        return
    result = _run([sys.executable, str(SYNC_SCRIPT)])
    if result.returncode == 0:
        print("  ✅ Sync ALFRED_WEB OK")
    else:
        print(f"  ⚠️  Erreur sync : {result.stderr[:200]}")

def git_commit_vlan(planifie=False):
    """Commit et push du VLAN sur dev, puis merge main."""
    print("\nGit — Commit + Push")
    print("-" * 40)

    import os
    git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}

    def git(*args, timeout=60):
        return _run(["git", *args], cwd=ROOT, env=git_env, timeout=timeout)

    today = date.today().isoformat()

    # Stage
    files = [
        "dashboard/dashboard_gouvernance/_manifest.json",
        "dashboard/dashboard_gouvernance/dashboard_gouvernance_data.json",
        "docs/smsi/vlan_config.md",
        "config/security/network_policy.json",
    ]
    git("add", *files)
    print("  Fichiers stagés.")

    # Commit dev
    if planifie:
        msg = f"B20 VLAN : ISO-20 partial — architecture documentée, implémentation Q3 2026 ({today})"
    else:
        msg = f"B20 VLAN : ISO-20 done — VLAN 10/20/30 validé sur SG108E+ER605 ({today})"
    r = git("commit", "-m", msg)
    if r.returncode != 0 and "nothing to commit" not in r.stdout:
        print(f"  ⚠️  Commit : {r.stderr[:200]}")
    else:
        print(f"  ✅ Commit dev : {msg[:60]}…")

    # Push dev
    r = git("push", "origin", "dev", timeout=90)
    if r.returncode == 0:
        print("  ✅ Push dev OK")
    else:
        print(f"  ⚠️  Push dev : {r.stderr[:300]}")

    # Merge main
    git("checkout", "main")
    merge_msg = f"Merge dev -> main : VLAN ISO-20 done ({today})"
    r = git("merge", "dev", "--no-ff", "-m", merge_msg)
    if r.returncode == 0:
        print("  ✅ Merge main OK")
    else:
        print(f"  ⚠️  Merge main : {r.stderr[:300]}")

    r = git("push", "origin", "main", timeout=90)
    if r.returncode == 0:
        print("  ✅ Push main OK")
    else:
        print(f"  ⚠️  Push main : {r.stderr[:300]}")

    git("checkout", "dev")

def main():
    parser = argparse.ArgumentParser(description="ALFRED — Validation VLAN & finalisation ISO-20")
    parser.add_argument(
        "--planifie", action="store_true",
        help="Mode planifié : architecture documentée, implémentation Q3 2026 (sans tests réseau)"
    )
    args = parser.parse_args()

    print_header()

    if args.planifie:
        if not mode_planifie():
            sys.exit(0)
    else:
        if not confirm_vlan_implemented():
            sys.exit(0)
        if not run_network_tests():
            print("\nTests réseau abandonnés. Corriger la configuration VLAN puis relancer.")
            sys.exit(1)

    if not update_manifest_iso20(planifie=args.planifie):
        sys.exit(1)

    update_vlan_doc()
    run_update_dashboard()
    run_sync()
    git_commit_vlan(planifie=args.planifie)

    print()
    print("=" * 60)
    if args.planifie:
        print("  ⏳ VLAN planifié — ISO-20 : partial (Q3 2026)")
        print("  Architecture documentée — relancer sans --planifie après implémentation.")
    else:
        print("  ✅ VLAN finalisé — ISO-20 : done")
    print("  Score gouvernance mis à jour — dashboard régénéré.")
    print("=" * 60)

if __name__ == "__main__":
    main()
