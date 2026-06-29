import json
d = json.load(open("dashboard/dashboard_data/dashboard_data.json", encoding="utf-8"))
b18 = next(b for b in d["blocks"] if b["id"] == "b18")
sc = b18["status_counts"]
print("B18 status_counts:")
for k, v in sc.items():
    if v > 0:
        print(f"  {k:20s}: {v}")
validated = sc.get("validated", 0)
total = sum(sc.values())
print(f"\n  validated : {validated}/{total} = {100*validated//total}%")
