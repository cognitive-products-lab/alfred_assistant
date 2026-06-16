"""
update_gouvernance_data.py — Générateur de données pour le Dashboard Gouvernance CPL

Rôle :
  1. Lire _manifest.json (exigences par norme)
  2. Vérifier l'existence des fichiers de preuve
  3. Calculer les scores de conformité par norme et globalement
  4. Générer dashboard_gouvernance_data.json pour le dashboard HTML

Usage :
  python tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "dashboard" / "dashboard_gouvernance" / "_manifest.json"
OUTPUT_PATH = ROOT / "dashboard" / "dashboard_gouvernance" / "dashboard_gouvernance_data.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Écrit : {path.relative_to(ROOT)}")


def check_file_exists(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    return (ROOT / relative_path).exists()


def statut_to_score(statut: str) -> int:
    """Convertit un statut de conformité en score numérique 0-100."""
    return {
        "conforme": 100,
        "partiel": 50,
        "non_conforme": 0,
        "na": 100,
        "planifie": 0,
    }.get(statut, 0)


def maturite_label(niveau: int) -> str:
    labels = {
        0: "Inexistant",
        1: "Initial",
        2: "Reproductible",
        3: "Défini",
        4: "Maîtrisé",
        5: "Optimisé",
    }
    return labels.get(niveau, "Inconnu")


def statut_badge(statut: str) -> str:
    badges = {
        "conforme": "✅",
        "partiel": "⚠️",
        "non_conforme": "❌",
        "na": "N/A",
        "planifie": "📋",
    }
    return badges.get(statut, "?")


# ---------------------------------------------------------------------------
# Calcul de conformité par norme
# ---------------------------------------------------------------------------

def process_rgpd(norme_data: dict) -> dict:
    exigences = norme_data.get("exigences", [])
    scores = []
    items = []

    for ex in exigences:
        preuve_existe = check_file_exists(ex.get("fichier_preuve"))
        score = statut_to_score(ex["statut"])
        scores.append(score)

        items.append({
            "id": ex["id"],
            "article": ex["article"],
            "label": ex["label"],
            "statut": ex["statut"],
            "badge": statut_badge(ex["statut"]),
            "maturite": ex.get("maturite", 0),
            "maturite_label": maturite_label(ex.get("maturite", 0)),
            "preuve_path": ex.get("fichier_preuve"),
            "preuve_existe": preuve_existe,
            "gap": ex.get("gap"),
            "action": ex.get("action"),
            "date_cible": ex.get("date_cible"),
            "produits": ex.get("produits", []),
            "score": score,
        })

    total = len(scores)
    conformes = sum(1 for s in scores if s == 100)
    partiels = sum(1 for s in scores if s == 50)
    non_conformes = sum(1 for s in scores if s == 0)
    score_global = round(sum(scores) / total, 1) if total > 0 else 0

    return {
        "score_global": score_global,
        "conformes": conformes,
        "partiels": partiels,
        "non_conformes": non_conformes,
        "total": total,
        "items": items,
    }


def process_iso27001(norme_data: dict) -> dict:
    domaines = norme_data.get("domaines", [])
    scores = []
    items = []

    for d in domaines:
        preuve_existe = check_file_exists(d.get("fichier_preuve") or d.get("fichier_audit"))
        score = statut_to_score(d["statut"])
        scores.append(score)

        items.append({
            "id": d["id"],
            "label": d["label"],
            "statut": d["statut"],
            "badge": statut_badge(d["statut"]),
            "maturite": d.get("maturite", 0),
            "maturite_label": maturite_label(d.get("maturite", 0)),
            "preuve_path": d.get("fichier_preuve") or d.get("fichier_audit"),
            "preuve_existe": preuve_existe,
            "gap": d.get("gap"),
            "score": score,
        })

    total = len(scores)
    conformes = sum(1 for s in scores if s == 100)
    partiels = sum(1 for s in scores if s == 50)
    non_conformes = sum(1 for s in scores if s == 0)
    score_global = round(sum(scores) / total, 1) if total > 0 else 0

    return {
        "score_global": score_global,
        "conformes": conformes,
        "partiels": partiels,
        "non_conformes": non_conformes,
        "total": total,
        "items": items,
    }


def process_aiact(norme_data: dict) -> dict:
    exigences = norme_data.get("exigences", [])
    scores = []
    items = []

    for ex in exigences:
        preuve_existe = check_file_exists(ex.get("fichier_preuve"))
        score = statut_to_score(ex["statut"])
        scores.append(score)

        items.append({
            "id": ex["id"],
            "article": ex["article"],
            "label": ex["label"],
            "statut": ex["statut"],
            "badge": statut_badge(ex["statut"]),
            "maturite": ex.get("maturite", 0),
            "maturite_label": maturite_label(ex.get("maturite", 0)),
            "preuve_path": ex.get("fichier_preuve"),
            "preuve_existe": preuve_existe,
            "gap": ex.get("gap"),
            "score": score,
        })

    total = len(scores)
    conformes = sum(1 for s in scores if s == 100)
    partiels = sum(1 for s in scores if s == 50)
    non_conformes = sum(1 for s in scores if s == 0)
    score_global = round(sum(scores) / total, 1) if total > 0 else 0

    return {
        "score_global": score_global,
        "conformes": conformes,
        "partiels": partiels,
        "non_conformes": non_conformes,
        "total": total,
        "items": items,
        "produits": norme_data.get("produits", {}),
    }


def process_generic(norme_data: dict) -> dict:
    """Traitement générique pour NIS2, HDS, SecNumCloud, PASSI."""
    exigences = norme_data.get("exigences", [])
    if not exigences:
        # Norme sans exigences détaillées encore (planifiée)
        return {
            "score_global": 0,
            "conformes": 0,
            "partiels": 0,
            "non_conformes": 0,
            "total": 0,
            "items": [],
            "statut_global": norme_data.get("statut_global", "planifie"),
            "maturite_globale": norme_data.get("maturite_globale", 0),
        }

    scores = []
    items = []
    for ex in exigences:
        preuve_existe = check_file_exists(ex.get("fichier_preuve"))
        score = statut_to_score(ex["statut"])
        scores.append(score)
        items.append({
            "id": ex["id"],
            "article": ex.get("article", ""),
            "label": ex["label"],
            "statut": ex["statut"],
            "badge": statut_badge(ex["statut"]),
            "maturite": ex.get("maturite", 0),
            "maturite_label": maturite_label(ex.get("maturite", 0)),
            "preuve_path": ex.get("fichier_preuve"),
            "preuve_existe": preuve_existe,
            "score": score,
        })

    total = len(scores)
    score_global = round(sum(scores) / total, 1) if total > 0 else 0
    return {
        "score_global": score_global,
        "conformes": sum(1 for s in scores if s == 100),
        "partiels": sum(1 for s in scores if s == 50),
        "non_conformes": sum(1 for s in scores if s == 0),
        "total": total,
        "items": items,
    }


# ---------------------------------------------------------------------------
# Vérification des documents de gouvernance
# ---------------------------------------------------------------------------

def process_documents(docs_data: dict) -> list:
    result = []
    for key, doc in docs_data.items():
        exists = check_file_exists(doc["chemin"])
        if exists:
            size = (ROOT / doc["chemin"]).stat().st_size
        else:
            size = 0

        result.append({
            "fichier": key,
            "chemin": doc["chemin"],
            "label": doc["label"],
            "statut": doc["statut"],
            "badge": statut_badge("conforme" if doc["statut"] == "complet" else
                                   "partiel" if doc["statut"] == "partiel" else
                                   "non_conforme" if doc["statut"] == "absent" else "planifie"),
            "existe": exists,
            "taille_lignes": doc.get("taille_lignes", 0),
            "taille_octets": size,
            "action": doc.get("action"),
        })
    return result


# ---------------------------------------------------------------------------
# Calcul score global CPL
# ---------------------------------------------------------------------------

def compute_global_score(normes_output: dict) -> dict:
    """Score pondéré par priorité : RGPD (p1) > ISO (p2) > AI Act (p2) > NIS2 (p3)."""
    poids = {"rgpd": 30, "iso27001": 25, "aiact": 25, "nis2": 10, "hds": 5, "secnumcloud": 3, "passi": 2}

    total_poids = 0
    score_pondere = 0

    for norme_id, poid in poids.items():
        data = normes_output.get(norme_id, {})
        score = data.get("score_global", 0)
        score_pondere += score * poid
        total_poids += poid

    score_global = round(score_pondere / total_poids, 1) if total_poids > 0 else 0

    # Niveau de maturité global
    if score_global >= 85:
        niveau = "Défini (3)"
        couleur = "#27AE60"
    elif score_global >= 60:
        niveau = "Reproductible (2)"
        couleur = "#F39C12"
    elif score_global >= 30:
        niveau = "Initial (1)"
        couleur = "#E67E22"
    else:
        niveau = "Initial bas (1)"
        couleur = "#E74C3C"

    return {
        "score_global": score_global,
        "niveau_maturite": niveau,
        "couleur": couleur,
        "poids_utilises": poids,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n[Gouvernance Dashboard] Calcul de conformité CPL...")
    print(f"  ROOT = {ROOT}")
    print(f"  Manifest = {MANIFEST_PATH.relative_to(ROOT)}")

    if not MANIFEST_PATH.exists():
        print(f"  ✗ Manifest introuvable : {MANIFEST_PATH}")
        return

    manifest = load_json(MANIFEST_PATH)
    normes_manifest = manifest.get("normes", {})
    docs_manifest = manifest.get("documents_gouvernance", {})

    normes_output: dict = {}

    # RGPD
    print("  ▶ Traitement RGPD...")
    normes_output["rgpd"] = process_rgpd(normes_manifest["rgpd"])

    # ISO 27001
    print("  ▶ Traitement ISO 27001...")
    normes_output["iso27001"] = process_iso27001(normes_manifest["iso27001"])

    # AI Act
    print("  ▶ Traitement AI Act...")
    normes_output["aiact"] = process_aiact(normes_manifest["aiact"])

    # Génériques
    for norme_id in ["nis2", "hds", "secnumcloud", "passi"]:
        print(f"  ▶ Traitement {norme_id.upper()}...")
        normes_output[norme_id] = process_generic(normes_manifest[norme_id])

    # Documents de gouvernance
    print("  ▶ Vérification des documents de gouvernance...")
    documents_output = process_documents(docs_manifest)

    # Score global
    global_score = compute_global_score(normes_output)

    # Consolidation du rapport
    output = {
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "generated_by": "update_gouvernance_data.py",
        "global": global_score,
        "normes": {
            norme_id: {
                **normes_manifest[norme_id],
                **normes_output.get(norme_id, {}),
            }
            for norme_id in normes_manifest
        },
        "documents_gouvernance": documents_output,
        "roadmap": manifest.get("roadmap", {}),
        "niveaux_maturite_cmm": manifest.get("niveaux_maturite_cmm", {}),
    }

    save_json(OUTPUT_PATH, output)

    # Affichage synthèse
    print(f"\n{'=' * 60}")
    print(f"  SCORE GLOBAL CPL : {global_score['score_global']}%")
    print(f"  Niveau : {global_score['niveau_maturite']}")
    print(f"{'=' * 60}")
    for norme_id, data in normes_output.items():
        score = data.get("score_global", 0)
        bar = "█" * int(score // 10) + "░" * (10 - int(score // 10))
        print(f"  {norme_id.upper():15s} [{bar}] {score:5.1f}%")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
