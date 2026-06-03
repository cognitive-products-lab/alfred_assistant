"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TOOLS
FILE         : tools/dashboard_tools/dashboard_tests/dashboard_test.py
ROLE         : Tableau de bord des tests de securite (CLI)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Lance les tests de la suite security_tests/ via pytest,
collecte les résultats par module et affiche un tableau de bord
visuel (passed / failed / error / Duree).

Usage:
    python tools/dashboard_tools/dashboard_tests/dashboard_test.py
    python tools/dashboard_tools/dashboard_tests/dashboard_test.py --module test_access_control
    python tools/dashboard_tools/dashboard_tests/dashboard_test.py --json
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 sur les terminaux Windows (cp1252 par défaut)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─── Chemin racine ────────────────────────────────────────────────────────────

_ROOT = Path(__file__).resolve().parents[3]   # ALFRED_PC/
_TESTS_DIR = _ROOT / "tests" / "security_tests"

# ─── Couleurs ANSI (désactivées si pas de TTY) ────────────────────────────────

def _tty() -> bool:
    return sys.stdout.isatty()

_GREEN  = "\033[32m" if _tty() else ""
_RED    = "\033[31m" if _tty() else ""
_YELLOW = "\033[33m" if _tty() else ""
_CYAN   = "\033[36m" if _tty() else ""
_BOLD   = "\033[1m"  if _tty() else ""
_RESET  = "\033[0m"  if _tty() else ""

# ─── Structures de données ────────────────────────────────────────────────────

@dataclass
class ModuleResult:
    name: str
    passed: int = 0
    failed: int = 0
    error: int = 0
    skipped: int = 0
    duration_s: float = 0.0
    failures: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.error + self.skipped

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.error == 0

    @property
    def rate(self) -> float:
        return round(self.passed / self.total * 100, 1) if self.total else 0.0


@dataclass
class DashboardResult:
    modules: list[ModuleResult] = field(default_factory=list)
    total_passed: int = 0
    total_failed: int = 0
    total_error: int = 0
    total_skipped: int = 0
    total_duration_s: float = 0.0
    generated_at: str = ""

    @property
    def total_tests(self) -> int:
        return self.total_passed + self.total_failed + self.total_error + self.total_skipped

    @property
    def global_rate(self) -> float:
        return round(self.total_passed / self.total_tests * 100, 1) if self.total_tests else 0.0

    @property
    def grade(self) -> str:
        r = self.global_rate
        if r >= 98: return "A+"
        if r >= 95: return "A"
        if r >= 90: return "B"
        if r >= 80: return "C"
        if r >= 60: return "D"
        return "F"


# ─── Collecte des fichiers de test ────────────────────────────────────────────

def _discover_modules(filter_name: str | None = None) -> list[Path]:
    if not _TESTS_DIR.exists():
        sys.exit(f"[ERREUR] Dossier introuvable : {_TESTS_DIR}")
    modules = sorted(_TESTS_DIR.glob("test_*.py"))
    if filter_name:
        key = filter_name if filter_name.startswith("test_") else f"test_{filter_name}"
        key = key if key.endswith(".py") else f"{key}.py"
        modules = [m for m in modules if m.name == key]
        if not modules:
            sys.exit(f"[ERREUR] Module non trouvé : {key}")
    return modules


# ─── Exécution pytest par module ─────────────────────────────────────────────

def _run_module(path: Path) -> ModuleResult:
    result = ModuleResult(name=path.stem)
    t0 = time.perf_counter()

    proc = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(path),
            "--tb=line",
            "-q",
            "--no-header",
        ],
        capture_output=True,
        text=True,
        cwd=str(_ROOT),
    )
    result.duration_s = round(time.perf_counter() - t0, 2)

    # Lecture du résumé — pytest entoure la ligne de "==" :
    # "======== 12 passed, 1 warning in 0.28s ========"
    import re as _re
    _COUNT_RE = _re.compile(r"(\d+)\s+(passed|failed|errors?|skipped|warning)")

    output = proc.stdout + proc.stderr
    for line in reversed(output.splitlines()):
        line_clean = line.strip().strip("=").strip()
        if not line_clean:
            continue
        matches = _COUNT_RE.findall(line_clean)
        if not matches:
            continue
        for raw_n, label in matches:
            n = int(raw_n)
            label = label.rstrip("s")  # "errors" → "error", "warnings" → "warning"
            if label == "passed":    result.passed  = n
            elif label == "failed":  result.failed  = n
            elif label == "error":   result.error   = n
            elif label == "skipped": result.skipped = n
        # stop dès qu'on a au moins une métrique de test (hors warning)
        if result.passed + result.failed + result.error + result.skipped > 0:
            break
        # ligne avec seulement des warnings → continuer à chercher
        if any(lbl.rstrip("s") == "warning" for _, lbl in matches):
            continue
        break

    # Si pytest exit 0 mais rien parsé → 0 tests (fichier vide)
    # Récupère les lignes FAILED pour affichage
    result.failures = [
        ln.strip() for ln in output.splitlines()
        if ln.strip().startswith("FAILED")
    ]

    return result


# ─── Agrégation ───────────────────────────────────────────────────────────────

def run_dashboard(filter_name: str | None = None) -> DashboardResult:
    modules = _discover_modules(filter_name)
    dash = DashboardResult(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    for path in modules:
        mod = _run_module(path)
        dash.modules.append(mod)
        dash.total_passed   += mod.passed
        dash.total_failed   += mod.failed
        dash.total_error    += mod.error
        dash.total_skipped  += mod.skipped
        dash.total_duration_s = round(dash.total_duration_s + mod.duration_s, 2)

    return dash


# --- Affichage ----------------------------------------------------------------

_W = 70  # largeur totale


def _bar(rate: float, width: int = 30) -> str:
    filled = round(rate / 100 * width)
    empty  = width - filled
    color  = _GREEN if rate >= 95 else _YELLOW if rate >= 75 else _RED
    return f"{color}{'#' * filled}{'.' * empty}{_RESET}"


def _status_icon(ok: bool) -> str:
    return f"{_GREEN}[OK]{_RESET}" if ok else f"{_RED}[KO]{_RESET}"


def print_dashboard(dash: DashboardResult) -> None:
    sep = "=" * _W
    thin = "-" * _W

    print()
    print(f"{_BOLD}{sep}{_RESET}")
    print(f"{_BOLD}  ALFRED -- TABLEAU DE BORD TESTS SECURITE   {dash.generated_at}{_RESET}")
    print(f"{_BOLD}{sep}{_RESET}")
    print()

    # En-tête colonnes
    print(f"  {'Module':<35} {'P':>5} {'F':>5} {'E':>5} {'Total':>6}  {'Taux':>6}  {'Duree':>7}")
    print(f"  {thin}")

    for mod in dash.modules:
        icon    = _status_icon(mod.ok)
        p_col   = f"{_GREEN}{mod.passed:>5}{_RESET}"
        f_col   = f"{_RED}{mod.failed:>5}{_RESET}"   if mod.failed else f"{'0':>5}"
        e_col   = f"{_RED}{mod.error:>5}{_RESET}"    if mod.error  else f"{'0':>5}"
        rate_s  = f"{mod.rate:>5.1f}%"
        dur_s   = f"{mod.duration_s:>6.2f}s"
        color_r = _GREEN if mod.rate >= 95 else _YELLOW if mod.rate >= 75 else _RED
        print(
            f"  {icon} {mod.name:<33} {p_col} {f_col} {e_col} "
            f"{mod.total:>6}  {color_r}{rate_s}{_RESET}  {dur_s}"
        )

        for fail in mod.failures[:3]:
            print(f"      {_RED}> {fail}{_RESET}")

    print(f"  {thin}")

    # Totaux
    g_color = _GREEN if dash.global_rate >= 95 else _YELLOW if dash.global_rate >= 75 else _RED
    print(
        f"  {'TOTAL':<35} "
        f"{_GREEN}{dash.total_passed:>5}{_RESET} "
        f"{_RED if dash.total_failed else ''}{dash.total_failed:>5}{_RESET} "
        f"{_RED if dash.total_error  else ''}{dash.total_error:>5}{_RESET} "
        f"{dash.total_tests:>6}  "
        f"{g_color}{dash.global_rate:>5.1f}%{_RESET}  "
        f"{dash.total_duration_s:>6.2f}s"
    )

    print()
    print(f"  Progression :")
    print(f"  {_bar(dash.global_rate, 50)}  {dash.global_rate:.1f}%")
    print()

    # Score global
    grade_color = _GREEN if dash.grade.startswith("A") else _YELLOW if dash.grade == "B" else _RED
    modules_ok   = sum(1 for m in dash.modules if m.ok)
    modules_fail = len(dash.modules) - modules_ok

    print(f"{_BOLD}{sep}{_RESET}")
    print(f"  GRADE GLOBAL : {grade_color}{_BOLD}{dash.grade}{_RESET}   "
          f"({dash.total_passed}/{dash.total_tests} tests réussis)")
    print(f"  Modules OK : {_GREEN}{modules_ok}{_RESET}  |  "
          f"Modules KO : {_RED if modules_fail else ''}{modules_fail}{_RESET}  |  "
          f"Duree totale : {dash.total_duration_s:.2f}s")
    print(f"{_BOLD}{sep}{_RESET}")

    # Modules défaillants
    failing = [m for m in dash.modules if not m.ok]
    if failing:
        print()
        print(f"{_RED}  Modules a corriger :{_RESET}")
        for m in failing:
            print(f"    {_RED}[KO] {m.name}  "
                  f"({m.failed} failed, {m.error} error){_RESET}")

    print()


def print_json(dash: DashboardResult) -> None:
    data = {
        "_meta": {
            "project": "ALFRED",
            "block": "B20 - Tests Securite",
            "file": "dashboard/dashboard_tests/dashboard_test.json",
            "version": "V1.0",
            "status": "ACTIVE",
            "description": "Resultats de la suite security_tests/ — genere par dashboard_test.py",
            "generated_at": dash.generated_at,
        },
        "generated_at": dash.generated_at,
        "grade": dash.grade,
        "global_rate": dash.global_rate,
        "total_tests": dash.total_tests,
        "total_passed": dash.total_passed,
        "total_failed": dash.total_failed,
        "total_error": dash.total_error,
        "total_skipped": dash.total_skipped,
        "total_duration_s": dash.total_duration_s,
        "modules": [
            {
                "name": m.name,
                "passed": m.passed,
                "failed": m.failed,
                "error": m.error,
                "skipped": m.skipped,
                "total": m.total,
                "rate": m.rate,
                "duration_s": m.duration_s,
                "ok": m.ok,
                "failures": m.failures,
            }
            for m in dash.modules
        ],
    }
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tableau de bord des tests de sécurité ALFRED (B20).",
    )
    parser.add_argument(
        "--module", "-m",
        metavar="NOM",
        help="Filtre sur un seul module (ex: test_access_control ou access_control).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Sortie JSON brute (pour intégration CI/monitoring).",
    )
    args = parser.parse_args()

    dash = run_dashboard(filter_name=args.module)

    if args.json:
        print_json(dash)
    else:
        print_dashboard(dash)

    # Code de sortie non-zéro si des tests échouent
    if dash.total_failed > 0 or dash.total_error > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
