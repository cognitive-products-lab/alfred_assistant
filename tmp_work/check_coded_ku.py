import json

files = [
    "knowledges/cpl/business_strategy/consulting_governance.json",
    "knowledges/human/interaction/conversation_repair.json",
    "knowledges/professional/engineering/reasoning/contradiction_detection.json",
    "knowledges/human/wellbeing/fatigue_patterns.json",
]
for f in files:
    try:
        d = json.load(open(f, encoding="utf-8"))
        print(f)
        print("  type  :", d.get("type", "ABSENT"))
        print("  status:", d.get("status", "ABSENT"))
        meta = d.get("_meta", "ABSENT")
        print("  _meta :", meta if meta == "ABSENT" else meta.get("status", "ABSENT"))
        print()
    except Exception as e:
        print(f"ERR {f}: {e}")
