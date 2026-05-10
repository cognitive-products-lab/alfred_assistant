import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Lire le manifest principal
manifest_path = ROOT / "dashboard" / "dashboard_manifest.json"
with open(manifest_path, encoding="utf-8") as f:
    m = json.load(f)

blocks = m.get("blocks", m)

print("=== B01 et B02 actuels ===")
for bid in ["b01", "b02"]:
    bloc = blocks.get(bid, {})
    print(f"\n{bid}: {bloc.get('label', '')}")
    for fpath in bloc.get("expected_files", []):
        print(f"  {fpath}")

# Fichiers à ajouter
to_add = {
    "b01": [
        "src/conversation/input/audio_listener.py",
        "src/conversation/nlp/intent_classifier.py",
        "src/conversation/output/tts_engine.py",
    ],
    "b02": [
        "src/rag/rag_engine.py",
    ],
}

print("\n=== Patch ===")
changed = False
for bid, new_files in to_add.items():
    bloc = blocks.get(bid, {})
    existing = set(bloc.get("expected_files", []))
    for f in new_files:
        if f not in existing:
            bloc.setdefault("expected_files", []).append(f)
            print(f"  + {bid} <- {f}")
            changed = True
        else:
            print(f"  = {bid} deja present : {f}")

if changed:
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)
    print("\ndashboard/dashboard_manifest.json mis a jour.")
else:
    print("\nRien a modifier.")
