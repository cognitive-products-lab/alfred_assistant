from pathlib import Path
import json
from datetime import datetime

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DIR = ROOT / "dashboard"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

TARGET = DASHBOARD_DIR / "dashboard_manifest_target.json"
CURRENT = DASHBOARD_DIR / "dashboard_manifest.json"

OUTPUT_JSON = DASHBOARD_DIR / "dashboard_target_report.json"
OUTPUT_MD = DASHBOARD_DIR / "dashboard_target_report.md"


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def get_file_status(rel_path):
    path = ROOT / rel_path

    if not path.exists():
        return "absent"

    if path.is_file() and path.stat().st_size == 0:
        return "empty"

    if path.suffix.lower() == ".json":
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                json.load(f)
            return "coded"
        except Exception:
            return "partial"

    if path.suffix.lower() == ".py":
        content = path.read_text(encoding="utf-8-sig", errors="ignore").strip()

        if not content:
            return "empty"

        if "STATUS: VALIDATED" in content or "VERSION FINALE" in content:
            return "valid"

        if "def " in content or "class " in content:
            return "coded"

        return "partial"

    return "coded"


def business_status(status):
    if status in ["absent", "empty"]:
        return "À coder"

    if status in ["partial", "created", "coded"]:
        return "Codé mais partiel"

    if status == "tested":
        return "Testé"

    if status == "valid":
        return "Version finale"

    return "À vérifier"


def main():
    target = load_json(TARGET)
    current = load_json(CURRENT)

    target_blocks = target.get("blocks", {})
    current_blocks = current.get("blocks", {})

    current_files = set()
    for b in current_blocks.values():
        for f in b.get("expected_files", []):
            current_files.add(f.replace("\\", "/"))

    report = {
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "missing_files": [],
        "existing_not_tracked": [],
        "files": []
    }

    md = []
    md.append("# Rapport ALFRED — Manifest cible\n")

    for block_id, block in target_blocks.items():
        label = block.get("label", "")
        files = block.get("expected_files", [])

        md.append(f"## {block_id.upper()} — {label}\n")

        for f in files:
            f_clean = f.replace("\\", "/")
            exists = (ROOT / f_clean).exists()
            tracked = f_clean in current_files
            status = get_file_status(f_clean)
            biz_status = business_status(status)

            item = {
                "block": block_id,
                "label": label,
                "path": f_clean,
                "exists": exists,
                "tracked": tracked,
                "status": status,
                "business_status": biz_status
            }

            report["files"].append(item)

            if not exists:
                report["missing_files"].append(f_clean)
                md.append(f"- ❌ **{biz_status}** — `{f_clean}`")
            elif not tracked:
                report["existing_not_tracked"].append(f_clean)
                md.append(f"- ⚠ **{biz_status} / non tracké** — `{f_clean}`")
            else:
                md.append(f"- ✅ **{biz_status}** — `{f_clean}`")

        md.append("")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("✅ Rapport généré")
    print(f"📄 {OUTPUT_JSON}")
    print(f"📄 {OUTPUT_MD}")
    print(f"❌ Fichiers manquants : {len(report['missing_files'])}")
    print(f"⚠️ Fichiers existants non trackés : {len(report['existing_not_tracked'])}")


if __name__ == "__main__":
    main()

