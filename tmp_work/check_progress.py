import json
from pathlib import Path
ROOT = Path("knowledges")
total = validated = 0
by_domain = {}
for f in ROOT.rglob("*.json"):
    if "index" in f.parts or f.name in ("taxonomy.json",): continue
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("type") != "knowledge_unit": continue
        total += 1
        dom = d.get("domain","?")
        by_domain[dom] = by_domain.get(dom, {"t":0,"v":0})
        by_domain[dom]["t"] += 1
        if d.get("status") == "validated":
            validated += 1
            by_domain[dom]["v"] += 1
    except: pass
print(f"Total: {total} | Validated: {validated} | Remaining: {total-validated}")
for dom, s in sorted(by_domain.items()):
    print(f"  {dom}: {s['v']}/{s['t']}")
