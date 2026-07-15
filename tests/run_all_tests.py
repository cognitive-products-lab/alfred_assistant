"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TOOLS
FILE         : tests/run_all_tests.py
ROLE         : Runner global — lance tous les tests ALFRED et met a jour dashboard_tests.json

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-07-09
VERSION      : V1.2
STATUS       : TESTED

DESCRIPTION :
Decouvre et execute tous les tests pytest de tests/, met a jour
dashboard/dashboard_tests/dashboard_tests.json et affiche un tableau de bord.

Usage :
    python tests/run_all_tests.py              # tous les tests
    python tests/run_all_tests.py --security   # security_tests/ uniquement
    python tests/run_all_tests.py --fast        # exclut tests lents (stt, tts, voice)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests"
DASHBOARD_JSON = ROOT / "dashboard" / "dashboard_tests" / "dashboard_tests.json"

# Groupes de tests — ordre d'exécution
TEST_GROUPS = {
    "security":    ["tests/security_tests"],
    "b15":         ["tests/b15_tests"],
    "b29":         ["tests/b29_tests"],
    "integration": ["tests/integration_tests"],
    "root":        [
        "tests/test_b01_speech.py",
        "tests/test_b02_b03.py",
        "tests/test_b18_knowledge.py",
        "tests/test_micro.py",
        "tests/test_pipeline.py",
    ],
    "speech":      [
        "tests/test_tts_engine.py",
        "tests/test_tts_piper.py",
        "tests/test_tts_piper_status.py",
        "tests/test_stt.py",
        "tests/test_voice_loop.py",
    ],
    "slow":        [
        "tests/test_pipeline_llm.py",
    ],
}

SLOW_GROUPS = {"speech", "slow"}


def _run_pytest(target: str) -> dict:
    """Lance pytest sur une cible et retourne les stats via -v (comptage ligne par ligne)."""
    import re
    import xml.etree.ElementTree as ET
    safe = Path(target).name.replace("/", "_").replace("\\", "_")
    xml_file  = ROOT / f"_pytest_result_{safe}.xml"
    tmp_dir   = ROOT / ".pytest_tmp"
    tmp_dir.mkdir(exist_ok=True)
    cmd = [
        sys.executable, "-m", "pytest", target,
        "--tb=no", "-q", "--no-header", "--color=no",
        f"--junit-xml={xml_file}",
        f"--basetemp={tmp_dir}",
    ]
    t0 = time.monotonic()
    try:
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        subprocess.run(cmd, cwd=str(ROOT), env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        duration = round(time.monotonic() - t0, 2)

        passed = failed = error = skipped = 0
        if xml_file.exists():
            try:
                tree = ET.parse(xml_file)
                root_el = tree.getroot()
                suite = root_el if root_el.tag == "testsuite" else root_el.find("testsuite")
                if suite is not None:
                    t = int(suite.get("tests", 0))
                    f = int(suite.get("failures", 0))
                    e = int(suite.get("errors", 0))
                    s = int(suite.get("skipped", 0))
                    passed = t - f - e - s
                    failed = f; error = e; skipped = s
            except Exception:
                pass
            xml_file.unlink(missing_ok=True)

        total = passed + failed + error + skipped
        rate = round(passed / total * 100, 1) if total > 0 else 0.0
        name = Path(target).name.replace(".py", "")

        return {
            "name": name,
            "passed": passed, "failed": failed,
            "error": error, "skipped": skipped,
            "total": total, "rate": rate,
            "duration_s": duration,
            "ok": failed == 0 and error == 0,
            "failures": [],
        }
    except Exception as exc:
        return {
            "name": Path(target).name,
            "passed": 0, "failed": 0, "error": 1, "skipped": 0,
            "total": 1, "rate": 0.0,
            "duration_s": round(time.monotonic() - t0, 2),
            "ok": False,
            "failures": [str(exc)],
        }


def _grade(rate: float) -> str:
    if rate >= 95: return "A"
    if rate >= 80: return "B"
    if rate >= 65: return "C"
    if rate >= 50: return "D"
    return "F"


def _collect_targets(args: argparse.Namespace) -> list[str]:
    targets = []
    groups = ["security"] if args.security else list(TEST_GROUPS.keys())
    if args.fast:
        groups = [g for g in groups if g not in SLOW_GROUPS]
    for g in groups:
        for t in TEST_GROUPS[g]:
            p = ROOT / t
            if p.exists():
                targets.append(t)
    return targets


def _print_table(modules: list[dict]) -> None:
    sep = "-" * 70
    print(f"\n{'=' * 70}")
    print(f"  ALFRED -- TABLEAU DE BORD TESTS   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"{'=' * 70}")
    print(f"  {'Module':<40} {'P':>5} {'F':>5} {'E':>5} {'Total':>6} {'Taux':>6}  {'Durée':>7}")
    print(f"  {sep}")
    for m in modules:
        tag = "[OK]" if m["ok"] else "[KO]"
        print(
            f"  {tag} {m['name']:<38} {m['passed']:>5} {m['failed']:>5} {m['error']:>5} "
            f"{m['total']:>6} {m['rate']:>5.1f}%  {m['duration_s']:>5.2f}s"
        )
    total_p = sum(m["passed"] for m in modules)
    total_f = sum(m["failed"] for m in modules)
    total_e = sum(m["error"] for m in modules)
    total_t = sum(m["total"] for m in modules)
    total_d = sum(m["duration_s"] for m in modules)
    rate = round(total_p / total_t * 100, 1) if total_t > 0 else 0.0
    print(f"  {sep}")
    print(
        f"  {'TOTAL':<40} {total_p:>5} {total_f:>5} {total_e:>5} "
        f"{total_t:>6} {rate:>5.1f}%  {total_d:>5.2f}s"
    )
    ok_count = sum(1 for m in modules if m["ok"])
    ko_count = len(modules) - ok_count
    print(f"\n  GRADE : {_grade(rate)}   ({total_p}/{total_t})  |  OK: {ok_count}  KO: {ko_count}")
    print(f"{'=' * 70}\n")


def _save_dashboard(modules: list[dict]) -> None:
    total_p = sum(m["passed"] for m in modules)
    total_f = sum(m["failed"] for m in modules)
    total_e = sum(m["error"] for m in modules)
    total_s = sum(m["skipped"] for m in modules)
    total_t = sum(m["total"] for m in modules)
    total_d = round(sum(m["duration_s"] for m in modules), 2)
    rate = round(total_p / total_t * 100, 1) if total_t > 0 else 0.0
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    data = {
        "_meta": {
            "project": "ALFRED",
            "block": "GLOBAL - Tous les tests",
            "file": "dashboard/dashboard_tests/dashboard_tests.json",
            "version": "V1.1",
            "status": "ACTIVE",
            "description": "Résultats globaux — générés par tests/run_all_tests.py",
            "generated_at": now,
        },
        "generated_at": now,
        "grade": _grade(rate),
        "global_rate": rate,
        "total_tests": total_t,
        "total_passed": total_p,
        "total_failed": total_f,
        "total_error": total_e,
        "total_skipped": total_s,
        "total_duration_s": total_d,
        "modules": modules,
    }
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    DASHBOARD_JSON.write_text(json_str, encoding="utf-8")
    # Copie aussi vers dashboard_test.json (lu par le HTML via fetch)
    (DASHBOARD_JSON.parent / "dashboard_test.json").write_text(json_str, encoding="utf-8")
    print(f"  JSON sauvegardé : {DASHBOARD_JSON}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Runner global tests ALFRED")
    parser.add_argument("--security", action="store_true", help="security_tests/ uniquement")
    parser.add_argument("--fast", action="store_true", help="Exclure tests lents (stt/tts/voice)")
    args = parser.parse_args()

    targets = _collect_targets(args)
    if not targets:
        print("Aucun test trouvé.")
        sys.exit(1)

    print(f"\nLancement de {len(targets)} cible(s) de test...\n")
    modules = []
    for t in targets:
        print(f"  -> {t} ...", end=" ", flush=True)
        result = _run_pytest(t)
        tag = "[OK]" if result["ok"] else "[KO]"
        print(f"{tag}  {result['passed']}P {result['failed']}F {result['error']}E  ({result['duration_s']}s)")
        modules.append(result)

    _print_table(modules)
    _save_dashboard(modules)


if __name__ == "__main__":
    main()
