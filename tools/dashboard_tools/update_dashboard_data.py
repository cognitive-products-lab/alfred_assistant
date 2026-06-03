from pathlib import Path
from datetime import datetime
import json
import ast

# ============================================================
# ALFRED â€” update_dashboard_data.py
# Objectif :
#   1. Lire dashboard_manifest.json
#   2. VÃ©rifier quels fichiers attendus existent vraiment
#   3. Ã‰valuer leur statut : absent / vide / codÃ© / testÃ© / validÃ©
#   4. GÃ©nÃ©rer dashboard_data.json pour ALFRED_DASHBOARD.html
# ============================================================

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DIR = ROOT / "dashboard"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_PATH = DASHBOARD_DIR / "dashboard_manifest.json"
VALIDATION_REGISTRY_PATH = DASHBOARD_DIR / "validation_registry.json"
OUTPUT_PATH = DASHBOARD_DIR / "dashboard_data.json"

# Dossiers oÃ¹ chercher les tests associÃ©s
TEST_DIRS = [
    ROOT / "tests",
    ROOT / "src" / "tests",
]

# Dossiers exclus du scan global
EXCLUDED_DIR_PARTS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def safe_relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIR_PARTS for part in path.parts)


def file_exists(relative_path: str) -> bool:
    return (ROOT / relative_path).exists()


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except Exception:
            return ""
    except Exception:
        return ""


def is_effectively_empty(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return True

    if path.stat().st_size == 0:
        return True

    text = read_text_safe(path).strip()

    if not text:
        return True

    # On ignore les fichiers qui ne contiennent que des commentaires simples
    meaningful_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("//"):
            continue
        meaningful_lines.append(stripped)

    return len(meaningful_lines) == 0


def analyze_python_file(path: Path) -> dict:
    """
    Analyse qualitative simple d'un fichier .py.
    Ne remplace pas des tests, mais donne un bon signal dashboard.
    """
    result = {
        "has_code": False,
        "has_class": False,
        "has_function": False,
        "has_docstring": False,
        "imports_count": 0,
        "classes_count": 0,
        "functions_count": 0,
        "syntax_ok": False,
        "syntax_error": None,
    }

    text = read_text_safe(path)
    if not text.strip():
        return result

    try:
        tree = ast.parse(text)
        result["syntax_ok"] = True
    except SyntaxError as exc:
        result["syntax_error"] = f"{exc.msg} ligne {exc.lineno}"
        # MÃªme si syntaxe KO, on regarde quelques signaux simples
        result["has_code"] = len(text.strip()) > 80
        result["has_class"] = "class " in text
        result["has_function"] = "def " in text
        return result

    module_docstring = ast.get_docstring(tree)
    result["has_docstring"] = bool(module_docstring)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            result["imports_count"] += 1

        if isinstance(node, ast.ClassDef):
            result["classes_count"] += 1
            result["has_class"] = True

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result["functions_count"] += 1
            result["has_function"] = True

    result["has_code"] = (
        result["imports_count"] > 0
        or result["classes_count"] > 0
        or result["functions_count"] > 0
        or len(text.strip()) > 120
    )

    return result


def find_test_for_file(relative_path: str) -> list[str]:
    """
    Cherche des tests probables.
    Exemple :
      src/security/encryption_service.py
    Tests possibles :
      tests/test_encryption_service.py
      tests/security/test_encryption_service.py
      src/tests/test_encryption_service.py
    """
    source_path = Path(relative_path)
    stem = source_path.stem

    candidates = []

    for test_dir in TEST_DIRS:
        if not test_dir.exists():
            continue

        patterns = [
            f"test_{stem}.py",
            f"{stem}_test.py",
        ]

        for pattern in patterns:
            for found in test_dir.rglob(pattern):
                if found.exists() and not is_excluded(found):
                    candidates.append(safe_relative(found))

    return sorted(set(candidates))


def find_validation_marker(relative_path: str, file_text: str) -> bool:
    """
    Validation lÃ©gÃ¨re :
    - soit commentaire explicite VALIDATED / VALIDÃ‰ / STATUS: VALIDATED
    - soit mÃ©tadonnÃ©e dans le contenu
    """
    markers = [
        "STATUS: VALIDATED",
        "STATUS: VALIDÃ‰",
        "VALIDATED",
        "VALIDÃ‰",
        "VERSION FINALE",
        "VERSION VALIDÃ‰E",
        "@validated",
    ]

    upper_text = file_text.upper()
    return any(marker in upper_text for marker in markers)


def evaluate_file(relative_path: str) -> dict:
    path = ROOT / relative_path

    info = {
        "path": relative_path.replace("\\", "/"),
        "exists": path.exists(),
        "status": "absent",
        "score": 0,
        "size_bytes": 0,
        "tests": [],
        "details": {},
    }

    if not path.exists():
        return info

    if path.is_dir():
        info["status"] = "created"
        info["score"] = 20
        return info

    info["size_bytes"] = path.stat().st_size

    # ✅ CORRECT : AVANT le test empty
    if path.name == "__init__.py":
        info["status"] = "structural"
        info["score"] = 100
        info["details"]["note"] = "__init__.py structurel valide même vide"
        return info

    if is_effectively_empty(path):
        info["status"] = "empty"
        info["score"] = 20
        return info

    text = read_text_safe(path)
    suffix = path.suffix.lower()

    tests = []
    if suffix == ".py":
        py_analysis = analyze_python_file(path)
        tests = find_test_for_file(relative_path)

        info["details"]["python"] = py_analysis
        info["tests"] = tests

        if not py_analysis["syntax_ok"]:
            info["status"] = "partial"
            info["score"] = 40
            return info

        if py_analysis["has_class"] or py_analysis["has_function"]:
            info["status"] = "coded"
            info["score"] = 60
        else:
            info["status"] = "partial"
            info["score"] = 40

        if tests:
            info["status"] = "tested"
            info["score"] = 80

        if find_validation_marker(relative_path, text):
            info["status"] = "validated"
            info["score"] = 100

        return info

    if suffix == ".json":
        try:
            json.loads(text)
            info["status"] = "coded"
            info["score"] = 60

            if find_validation_marker(relative_path, text):
                info["status"] = "validated"
                info["score"] = 100

        except json.JSONDecodeError as exc:
            info["status"] = "partial"
            info["score"] = 40
            info["details"]["json_error"] = f"{exc.msg} ligne {exc.lineno}"

        return info

    # Fichiers doc, md, txt, yaml, etc.
    if len(text.strip()) > 200:
        info["status"] = "coded"
        info["score"] = 60
    else:
        info["status"] = "partial"
        info["score"] = 40

    if find_validation_marker(relative_path, text):
        info["status"] = "validated"
        info["score"] = 100

    return info


def normalize_manifest(manifest: dict) -> dict:
    """
    Accepte deux formats :
    1)
    {
      "blocks": {
        "b01": {
          "label": "...",
          "target_full_files_count": "...",
          "target_full_label": "Cible complète V1/V2/V3"
          "expected_files": [...]
        }
      }
    }

    2)
    {
      "b01": {
        "label": "...",
        "target_full_files_count": "...",
        "target_full_label": "Cible complète V1/V2/V3"
        "expected_files": [...]
      }
    }
    """
    if "blocks" in manifest and isinstance(manifest["blocks"], dict):
        return manifest["blocks"]

    return manifest


def status_counts(files_info: list[dict]) -> dict:
    counts = {
        "structural": 0,
        "absent": 0,
        "empty": 0,
        "partial": 0,
        "created": 0,
        "coded": 0,
        "tested": 0,
        "validated": 0,
    }

    for item in files_info:
        status = item.get("status", "absent")
        counts[status] = counts.get(status, 0) + 1
    return counts


def compute_block_progress(files_info: list[dict]) -> float:
    if not files_info:
        return 0.0

    total = sum(item["score"] for item in files_info)
    return round(total / len(files_info), 1)


def build_dashboard_data() -> dict:
    manifest = load_json(MANIFEST_PATH)
    blocks_manifest = normalize_manifest(manifest)

    validation_registry = (
        load_json(VALIDATION_REGISTRY_PATH)
        if VALIDATION_REGISTRY_PATH.exists()
        else {"validated_files": []}
    )

    validated_files = validation_registry.get("validated_files", [])

    validation_map = {
        item["path"].replace("\\", "/"): item
        for item in validated_files
        if "path" in item
    }

    blocks = []

    for block_id in sorted(blocks_manifest.keys()):
        block = blocks_manifest[block_id]

        label = block.get("label", block_id.upper())
        expected_files = block.get("expected_files", [])
        target_full_files_count = block.get(
            "target_full_files_count",
            len(expected_files)
        )

        files_info = []

        for path in expected_files:
            info = evaluate_file(path)
            normalized_path = info["path"].replace("\\", "/")

            validation_data = validation_map.get(normalized_path)

            if validation_data:
                status = validation_data.get("status", info["status"])

                info["status"] = status
                info["validation"] = validation_data
                info["validated"] = status == "validated"
                info["tested"] = status in {"tested", "validated"}

                if status == "validated":
                    info["score"] = 100
                elif status == "tested":
                    info["score"] = max(info.get("score", 0), 80)

            files_info.append(info)

        progress = compute_block_progress(files_info)

        detected = [
            item["path"]
            for item in files_info
            if item["exists"]
        ]
        effective_completed = sum(
            item["score"] / 100
            for item in files_info
        )

        full_project_progress = round(
            (effective_completed / target_full_files_count) * 100,
            1
        )

        missing = [
            item["path"]
            for item in files_info
            if not item["exists"]
        ]

        counts = status_counts(files_info)

        blocks.append({
            "id": block_id.lower(),
            "label": label,
            "target_full_files_count": target_full_files_count,
            "full_project_progress": full_project_progress,
            "sub_targets": block.get("sub_targets", {}),
            "progress": progress,
            "expected_count": len(expected_files),
            "files_count": len(detected),
            "missing_count": len(missing),
            "status_counts": counts,
            "files_detected": detected,
            "files_missing": missing,
            "files": files_info,
        })

    global_progress = (
        round(sum(block["progress"] for block in blocks) / len(blocks), 1)
        if blocks else 0.0
    )

    total_expected = sum(block["expected_count"] for block in blocks)
    total_detected = sum(block["files_count"] for block in blocks)
    total_missing = sum(block["missing_count"] for block in blocks)

    global_counts = {
        "structural": 0,
        "absent": 0,
        "empty": 0,
        "partial": 0,
        "created": 0,
        "coded": 0,
        "tested": 0,
        "validated": 0,
    }
    

    total_target_full_files = sum(
        block.get("target_full_files_count", block["expected_count"])
        for block in blocks
    )

    total_effective_completed = sum(
        sum(item["score"] / 100 for item in block["files"])
        for block in blocks
    )

    global_full_project_progress = round(
        (total_effective_completed / total_target_full_files) * 100,
        1
        ) if total_target_full_files else 0.0


    for block in blocks:
        for status, count in block["status_counts"].items():
            global_counts[status] = global_counts.get(status, 0) + count
        
    # =========================
    # Comptage fichiers validés
    # =========================
    validated_count = sum(
        block["status_counts"].get("validated", 0)
            for block in blocks
    )
    
    weighted_global_progress = round(
        (
            sum(
                block["full_project_progress"]
                * block["target_full_files_count"]
                for block in blocks
            )
        ) / total_target_full_files,
        1
    )   if total_target_full_files else 0.0

    return {
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "source": "dashboard_manifest.json + validation_registry.json",
        "mode": "manifest_expected_vs_existing_with_validation_registry",
        "validated_files_count": validated_count,
        "global_progress": global_progress,
        "total_target_full_files": total_target_full_files,
        "global_full_project_progress": global_full_project_progress,
        "total_expected_files": total_expected,
        "total_files_detected": total_detected,
        "total_files_missing": total_missing,
        "global_status_counts": global_counts,
        "validation_registry_count": len(validated_files),
        "blocks": blocks,
        "weighted_global_progress": weighted_global_progress,
    }


def save_dashboard_data(data: dict) -> None:
    OUTPUT_PATH.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def print_summary(data: dict) -> None:
    print("OK - dashboard_data.json mis à jour depuis dashboard_manifest.json")
    print(f"Mise à jour : {data['last_update']}")
    print(f"Fichiers attendus : {data['total_expected_files']}")
    print(f"Fichiers détectés : {data['total_files_detected']}")
    print(f"Fichiers manquants : {data['total_files_missing']}")
    print(f"Avancement global : {data['global_progress']}%")
    print("Détail par bloc :")
    for block in data["blocks"]:
        print(
            f" - {block['id'].upper()} | "
            f"{block['label']} | "
            f"tech: {block['progress']}% | "
            f"full: {block['full_project_progress']}% | "
            f"{block['files_count']}/{block['target_full_files_count']} cible"
        )


def main() -> None:
    data = build_dashboard_data()
    save_dashboard_data(data)
    print_summary(data)


if __name__ == "__main__":
    main()


