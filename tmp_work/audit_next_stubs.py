import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
domains = [
    "professional/decision",
    "professional/frameworks",
    "professional/product_management",
]

for domain in domains:
    d = ROOT / domain
    if not d.exists():
        print(f"  ABSENT: {domain}")
        continue
    files = sorted(d.rglob("*.json"))
    print(f"\n{domain} ({len(files)} fichiers)")
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            ku_type = data.get("type", "ABSENT")
            status = data.get("status", "?")
            title = data.get("title", f.stem)
            print(f"  [{ku_type}][{status}] {f.relative_to(ROOT / domain)} — {title}")
        except Exception as e:
            print(f"  ERR {f.name}: {e}")
