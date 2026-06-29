import json
from pathlib import Path

tax = json.loads(Path("knowledges/taxonomy.json").read_text(encoding="utf-8"))
links = json.loads(Path("knowledges/domain_links.json").read_text(encoding="utf-8"))

print("=== TAXONOMY ===")
print(f"  version: {tax['version']}")
print(f"  total_subdomains: {tax['total_subdomains']}")
print(f"  domaines: {list(tax['domains'].keys())}")

print("\n=== CUISINE ===")
cuisine = tax["domains"]["cuisine"]
for sub, data in cuisine["subdomains"].items():
    ku = data.get("linked_knowledge", [])
    intents = data.get("intents", [])
    print(f"  {sub}: {len(ku)} KU, {len(intents)} intents")

print("\n=== CULTURE/MANGA ===")
manga = tax["domains"]["culture"]["subdomains"]["manga"]
print(f"  {len(manga['linked_knowledge'])} KU, {len(manga['intents'])} intents")

print("\n=== INTENT ROUTING RULES ===")
for rule in tax["intent_routing_rules"]:
    print(f"  {rule}")

print("\n=== OPTIONAL DOMAINS ===")
print(f"  {tax['loading_policy']['optional_domains']}")

print("\n=== DOMAIN LINKS ===")
print(f"  total: {len(links['links'])} liens, version: {links['version']}")
