from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.06
FILE         : src/knowledge/knowledge_schema.py
ROLE         : Schéma de métadonnées Knowledge (provenance, fraîcheur, confidentialité)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Complète les fiches knowledge avec un schéma de provenance additif — voir
docs/architecture/vision_knowledge_training_finetuning_alfred.md, P0.
"""

"""
ALFRED — knowledge_schema.py
Additif et rétrocompatible : ne modifie jamais les fichiers JSON sur disque.
Les 1137 fiches existantes sont écrites à la main et déjà validées par
Céline (source_type="document", status="VALIDATED" par défaut) ; seule une
connaissance acquise dynamiquement par un futur pipeline d'acquisition
porterait ces champs directement dans son JSON dès sa création — auquel cas
ils priment sur ces valeurs par défaut.
"""

from typing import Any

# Statuts de cycle de vie proposés par le document source (section 6) —
# distinct du "status" registry existant ("active"/"existing", filtre de
# chargement dans KnowledgeLoader.build_index()) : ne jamais confondre les
# deux clés, d'où metadata["status"] en sous-dict plutôt qu'un champ
# top-level qui écraserait le status registry.
KNOWLEDGE_LIFECYCLE_STATUSES = (
    "ACTIVE", "STALE", "TO_VERIFY", "CONFLICT", "REJECTED", "ARCHIVED",
    "VALIDATED",
)

DEFAULT_METADATA: dict[str, Any] = {
    "source_type": "document",
    "acquired_at": None,
    "verified_at": None,
    "confidence": None,
    "freshness_policy": "STATIC",
    # Corpus personnel de Céline (business, psychologie, CPL...) : défaut
    # conservateur, jamais destiné à sortir sans décision explicite —
    # cohérent avec la contrainte non négociable #5 du document source
    # (Safety/Privacy peut interdire toute sortie cloud).
    "privacy_level": "LOCAL_ONLY",
    "training_eligible": False,
    "status": "VALIDATED",
}


def normalize_knowledge_metadata(data: dict[str, Any]) -> dict[str, Any]:
    """
    Complète les champs de provenance/fraîcheur/confidentialité d'une fiche
    knowledge avec des valeurs par défaut quand absents.

    Lit exclusivement le sous-objet data["provenance"] — jamais les clés
    top-level de la fiche. Les 1137 fiches existantes ont leur propre schéma
    éditorial avec des clés top-level qui portent déjà un sens différent
    (ex. data["status"] == "active"/"draft", un statut de publication de la
    fiche, pas le cycle de vie VALIDATED/STALE/... introduit ici) — bug
    détecté par le test test_registry_status_untouched_by_metadata :
    lire data.get("status") directement aurait fait passer "active" pour un
    statut de cycle de vie, silencieusement faux sur la quasi-totalité du
    corpus. "provenance" est un espace de nommage neuf, absent des 1137
    fiches actuelles (vérifié), donc sans collision possible.

    Args:
        data: le contenu JSON brut de la fiche (KnowledgeLoader.build_index()
              l'appelle avec le "data" déjà chargé, sans jamais le réécrire
              sur disque).

    Returns:
        Un dict avec tous les champs de DEFAULT_METADATA, valeur de
        data["provenance"] si présente et non nulle, sinon valeur par défaut.
    """
    metadata = dict(DEFAULT_METADATA)
    if not isinstance(data, dict):
        return metadata
    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        return metadata
    for key in metadata:
        value = provenance.get(key)
        if value is not None:
            metadata[key] = value
    return metadata
