"""
Fix dashboard B18 :
  1. Corrige read_meta_status_from_json() dans update_dashboard_data.py
     -> lit aussi "status" root-level pour type=knowledge_unit
  2. Ajoute tous les KU existants dans dashboard_data_manifest.json (b18 expected_files)
  3. Met à jour les compteurs b18 (expected_count, sub_targets.knowledge_files)
"""
import json
import re
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC")
KNOWLEDGES_ROOT = ROOT / "knowledges"
MANIFEST_PATH = ROOT / "dashboard/dashboard_data/dashboard_data_manifest.json"
SCRIPT_PATH = ROOT / "tools/dashboard_tools/dashboard_data/update_dashboard_data.py"

# ═══════════════════════════════════════════════════════════════════════════
# 1. CORRIGER update_dashboard_data.py — read_meta_status_from_json
# ═══════════════════════════════════════════════════════════════════════════

script_text = SCRIPT_PATH.read_text(encoding="utf-8")

OLD_FUNC = '''def read_meta_status_from_json(text: str) -> str | None:
    """
    Lit _meta.status directement depuis le JSON parsé.
    Retourne le statut en minuscules, ou None si absent.
    Mapping :
      VALIDATED / validated / validated_v2 -> "validated"
      STABLE                               -> "validated"
      TESTED                               -> "tested"
      ACTIVE / active / created            -> "coded"
      DRAFT / draft / coded                -> "coded"
    """
    try:
        data = json.loads(text)
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    meta = data.get("_meta")
    if not isinstance(meta, dict):
        return None

    raw = meta.get("status", "")
    if not isinstance(raw, str):
        return None

    s = raw.strip().upper()
    if s in ("VALIDATED", "VALIDATED_V2"):
        return "validated"
    if s == "STABLE":
        return "validated"
    if s in ("EN_LIGNE", "ONLINE", "DEPLOYED"):
        return "validated"
    if s == "TESTED":
        return "tested"
    if s in ("ACTIVE", "CREATED", "DRAFT", "CODED"):
        return "coded"
    if s == "ARCHIVE":
        return "archive"
    return None'''

NEW_FUNC = '''def read_meta_status_from_json(text: str) -> str | None:
    """
    Lit le statut depuis le JSON parsé.
    Priorité :
      1. _meta.status (fichiers de config ALFRED avec en-tête standard)
      2. status root-level pour type=knowledge_unit (KU de la knowledge base)
    Mapping :
      VALIDATED / validated / validated_v2 -> "validated"
      STABLE                               -> "validated"
      TESTED                               -> "tested"
      ACTIVE / active / created            -> "coded"
      DRAFT / draft / coded                -> "coded"
    """
    try:
        data = json.loads(text)
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    # Priorité 1 : _meta.status (fichiers de config standard ALFRED)
    meta = data.get("_meta")
    if isinstance(meta, dict):
        raw = meta.get("status", "")
        if isinstance(raw, str) and raw.strip():
            s = raw.strip().upper()
            if s in ("VALIDATED", "VALIDATED_V2"):
                return "validated"
            if s == "STABLE":
                return "validated"
            if s in ("EN_LIGNE", "ONLINE", "DEPLOYED"):
                return "validated"
            if s == "TESTED":
                return "tested"
            if s in ("ACTIVE", "CREATED", "DRAFT", "CODED"):
                return "coded"
            if s == "ARCHIVE":
                return "archive"

    # Priorité 2 : status root-level pour les knowledge_unit
    if data.get("type") == "knowledge_unit":
        raw = data.get("status", "")
        if isinstance(raw, str) and raw.strip():
            s = raw.strip().lower()
            if s in ("validated", "validated_v2"):
                return "validated"
            if s == "tested":
                return "tested"
            if s in ("draft", "coded", "partial"):
                return "coded"

    return None'''

if OLD_FUNC in script_text:
    script_text = script_text.replace(OLD_FUNC, NEW_FUNC)
    SCRIPT_PATH.write_text(script_text, encoding="utf-8")
    print("OK  update_dashboard_data.py — read_meta_status_from_json corrigée")
else:
    # Essayer de trouver la fonction par son nom et la remplacer
    # Regex pour trouver la fonction existante
    pattern = r'def read_meta_status_from_json\(text: str\) -> str \| None:.*?(?=\ndef |\Z)'
    match = re.search(pattern, script_text, re.DOTALL)
    if match:
        script_text = script_text[:match.start()] + NEW_FUNC + script_text[match.end():]
        SCRIPT_PATH.write_text(script_text, encoding="utf-8")
        print("OK  update_dashboard_data.py — fonction remplacée par regex")
    else:
        print("WARN  Fonction read_meta_status_from_json non trouvée — vérifier manuellement")

# ═══════════════════════════════════════════════════════════════════════════
# 2. MANIFEST — collecter tous les KU existants
# ═══════════════════════════════════════════════════════════════════════════

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
b18 = manifest["blocks"]["b18"]

# Collecter tous les KU paths (relatifs à ROOT)
all_ku_paths = []
for json_file in sorted(KNOWLEDGES_ROOT.rglob("*.json")):
    # Ignorer index, backup, non-KU
    if "index" in json_file.parts:
        continue
    if "backup" in json_file.name.lower():
        continue
    try:
        data = json.loads(json_file.read_text(encoding="utf-8"))
        if data.get("type") == "knowledge_unit":
            rel = str(json_file.relative_to(ROOT)).replace("\\", "/")
            all_ku_paths.append(rel)
    except Exception:
        pass

print(f"KU trouvés sur disque : {len(all_ku_paths)}")

# Fichiers déjà dans le manifest b18
existing_b18 = set(b18.get("expected_files", []))

# KU non encore dans le manifest
new_ku_to_add = [p for p in all_ku_paths if p not in existing_b18]
print(f"KU à ajouter au manifest b18 : {len(new_ku_to_add)}")

# Ajouter les nouveaux KU
if "expected_files" not in b18:
    b18["expected_files"] = []
for p in new_ku_to_add:
    b18["expected_files"].append(p)

# Mettre à jour les compteurs b18
total_expected = len(b18["expected_files"])
non_ku_count = total_expected - len(all_ku_paths)

# sub_targets
if "sub_targets" in b18:
    b18["sub_targets"]["knowledge_files"] = len(all_ku_paths)

# expected_count = nombre de fichiers listés
b18["expected_count"] = total_expected
# target_full_files_count (objectif long terme) = au moins les KU actuels
if b18.get("target_full_files_count", 0) < total_expected:
    b18["target_full_files_count"] = total_expected

print(f"Total expected b18 après mise à jour : {total_expected}")
print(f"  dont KU : {len(all_ku_paths)}")
print(f"  dont autre : {non_ku_count}")

MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nOK  dashboard_data_manifest.json mis à jour")
print(f"    {len(new_ku_to_add)} nouveaux KU ajoutés au bloc b18")
print("\nRelancer : python tools/dashboard_tools/dashboard_data/update_dashboard_data.py")
