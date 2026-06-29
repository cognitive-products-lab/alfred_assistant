import sys
sys.path.insert(0, "tools/dashboard_tools/dashboard_data")
from update_dashboard_data import evaluate_file, read_meta_status_from_json
import json

f = "knowledges/cpl/business_strategy/consulting_governance.json"
text = open(f, encoding="utf-8").read()
data = json.loads(text)

print("type  :", data.get("type"))
print("status:", data.get("status"))
print("_meta :", data.get("_meta"))
print()
print("read_meta_status_from_json ->", read_meta_status_from_json(text))
print()
info = evaluate_file(f)
print("evaluate_file ->", {k:v for k,v in info.items() if k != "content"})
