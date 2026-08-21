"""
PROJECT      : ALFRED
BLOCK        : B18
FILE         : src/training/__init__.py
ROLE         : Arborescence des datasets d'entraînement ALFRED_DATA

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21

DESCRIPTION :
Implémente l'arborescence ALFRED_DATA/ proposée par le document source
(docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1,
section 12), adaptée au projet : sous data/training/ plutôt qu'un nouveau
dossier racine, cohérent avec data/knowledge/, data/memory/... déjà en
place — chaque catégorie est un sous-dossier géré par
src.training.dataset_store (fichier courant + versions figées).

Catégories du document source et leur état réel dans ce projet :

- instructions/  IMPLÉMENTÉE — src.training.instruction_dataset
- preferences/   IMPLÉMENTÉE — src.training.preference_dataset
- golden/        IMPLÉMENTÉE — src.training.golden_dataset +
                  src.training.evaluation (P2, hors arborescence
                  ALFRED_DATA du document source section 12, mais même
                  esprit : jamais mélangé aux datasets d'entraînement,
                  section 22 — "ne doit pas servir directement à entraîner").
- knowledge/     déjà couverte par data/knowledge/ (P0, avant ce module) —
                  pas dupliquée ici.
- gaps/          déjà couverte par data/knowledge/gap_dataset.jsonl (P0) —
                  pas dupliquée ici.
- intent/        DOCUMENTÉE, PAS BRANCHÉE — capturerait des exemples
                  (texte → intent) pour un futur SFT d'IntentNet. Nécessite
                  un point d'ancrage dans
                  src/conversation/nlp/intent_classifier.py qui n'existe
                  pas encore (décision volontaire : ne pas ouvrir ce
                  chantier sans qu'il soit demandé).
- routing/       DOCUMENTÉE, PAS BRANCHÉE — décisions de routage
                  local/cloud (src/llm/llm_router.py). Même statut
                  qu'intent/ : le point d'ancrage n'existe pas encore.
- memory/        DOCUMENTÉE, PAS BRANCHÉE — décisions
                  KEEP/UPDATE/MERGE/EXPIRE/IGNORE. Recoupe la dette déjà
                  répertoriée dans vision_architecture_cognitive_alfred.md
                  (memory_decay_rules.json non branché à du code exécutable).
- users/         DOCUMENTÉE, PAS BRANCHÉE — adaptation par utilisateur
                  (ALFRED Adaptive). Explicitement en P3 dans le document
                  source (section 28) : pas la priorité actuelle.

Ces quatre dernières catégories n'ont pas de module dédié : les créer
maintenant produirait du code sans appelant réel (l'anti-pattern déjà
identifié dans vision_architecture_cognitive_alfred.md — "des briques déjà
écrites et jamais reliées entre elles"). src.training.dataset_store reste
directement utilisable pour elles dès qu'un vrai point d'ancrage existe :
dataset_store.append_entry("intent", {...}) fonctionne sans code
supplémentaire.
"""
