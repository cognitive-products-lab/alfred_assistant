# Vision — Architecture cognitive ALFRED & indépendance au LLM externe
## Cognitive Products Lab — ALFRED

> Version 1.0 — 2026-08-14
> Statut : CONCEPTION VALIDÉE + chantier P0 démarré et livré
> Origine : document de cadrage `archi neuronale alfred.docx` (Bureau de
> Céline, dialogue retranscrit), étudié et confronté au code réel le
> 14/08/2026.

---

## 1. Vue d'ensemble

Le document source pose une thèse : ALFRED ne doit pas être un LLM
généraliste entouré d'outils, mais un **système d'IA composé** — plusieurs
composants spécialisés, chacun aussi simple que possible, orchestrés par un
routeur déterministe, avec les LLM externes (OpenAI, Anthropic) en **dernier
recours** plutôt qu'au cœur du système.

Quatre principes structurent la vision :

- **Local-first** — le traitement local est toujours essayé en premier.
- **Modularité** — chaque composant est remplaçable indépendamment.
- **Sobriété** — un LLM n'est sollicité que si une règle ou un petit modèle
  ne suffit pas (5 niveaux de coût, de 0 = règles à 4 = API externe).
- **Indépendance progressive** — OpenAI/Anthropic deviennent un filet de
  sécurité, pas une dépendance structurelle.

L'architecture cible décrit un `ALFRED Cognitive Bus` reliant `IntentNet`
(intention), `StateNet` (état système), `VisionNet`/`AudioNet` (perception),
`MemoryNet` (politique KEEP/MERGE/UPDATE/EXPIRE/IGNORE), `SafetyNet`
(politique de confidentialité qui peut bloquer le cloud même si un modèle
recommande l'inverse) et un `RouterNet` déterministe en V1 (règles → outil →
mémoire → modèle local → Ollama → cloud en dernier recours). Le document
insiste sur une règle de décision (section 25 du docx) : *« un réseau
neuronal n'est intégré à ALFRED que s'il apporte une valeur mesurable
supérieure à une solution déterministe ou algorithmique suffisamment
simple »* — c'est ce principe qui gouverne l'ordre de priorité retenu
ci-dessous, plutôt que la roadmap en 7 phases du document source (qui est
une vision cible, pas un plan séquencé sur le code existant).

---

## 2. Constat — l'écart n'est pas où on l'attendrait

Un audit du code réel (`src/`) le 14/08/2026 a montré que l'écart principal
n'est **pas** un manque de briques, mais des **briques déjà écrites et
jamais reliées entre elles** :

| Composant visé (docx) | État réel avant ce chantier | Fichier |
|---|---|---|
| RouterNet (routage local→cloud) | Existe, mais purement basé sur la disponibilité (exception → fallback), aucune notion de sobriété ni de sensibilité du contenu | `src/llm/llm_router.py` |
| SafetyNet (bloque le cloud sur données sensibles) | **N'existait pas sur le chemin LLM.** `allow_cloud_fallback=True` envoyait le prompt brut vers OpenAI/Anthropic dès qu'Ollama échouait, sans aucune vérification de sensibilité. `output_filter.py` ne masque que la *sortie*, pas ce qui part en entrée cloud. | — |
| Un moteur de policy Zero-Trust existe déjà | `policy_engine.py` (ALLOW/DENY/REVIEW par rôle+sensibilité+risque) — mais jamais appelé dans le flux LLM, et conçu pour l'accès à des *ressources* par *rôle*, pas pour classer la sensibilité d'un prompt de conversation | `src/security/policy_engine.py` |
| IntentNet (classification d'intention) | Code écrit (`IntentClassifier`, `config/intents_catalog.json`) mais **jamais importé** — chaque requête part en direct vers le LLM sans étape d'intention | `src/conversation/nlp/intent_classifier.py` |
| Sobriété modèle (petit modèle vs gros modèle selon la tâche) | `MODEL_PROFILES` liste déjà 3B→120B mais `MODEL = "llama3.2"` est câblé en dur, aucune sélection dynamique | `src/llm/llm_client_ollama.py`, `src/main.py:94` |
| MemoryNet (politique KEEP/MERGE/EXPIRE) | Stockage multi-couches réel (épisodique, long terme, SQLite) mais tout est loggé sans filtre — `memory_decay_rules.json`/`memory_prioritization.json` existent en JSON, non branchés à du code exécutable | `src/memory/memory_engine.py` |
| StateNet | Pas d'objet d'état unifié, mais `mode_manager.py` couvre déjà une vraie machine à états (support/focus/challenge/complicité) pilotée par l'émotion détectée — un socle partiel réutilisable | `src/regulation/mode_manager.py` |

Conséquence pratique et concrète : le Chantier 2 (sécurité chute/accompagnement,
`docs/module_securite_accompagnement/vision_securite_accompagnement_360.md`)
va manipuler des données de santé de Céline et Sébastien. Sans SafetyNet,
ces données pouvaient partir vers OpenAI/Anthropic dès qu'Ollama tombait —
un risque réel, pas théorique, ce qui a fait de la fermeture de ce trou la
priorité P0 du chantier plutôt que la construction du Cognitive Bus complet
suggérée en premier par la roadmap du document source.

---

## 3. Plan d'action retenu (4 points, priorité au risque et à la réutilisation)

L'ordre choisi diverge délibérément de la roadmap en 7 phases du document
source : celle-ci commence par construire le Cognitive Bus (gros
investissement structurel) avant la couche Safety. Ici, l'ordre suit le
risque réel et le principe même du document (« ne pas construire de neuronal
là où une règle suffit, ne pas réinventer ce qui existe déjà ») :

### P0 — Fermer la fuite de confidentialité vers le cloud ✅ **Livré 14/08/2026**

- **`src/security/safety_gate.py`** (nouveau) : classification par
  mots-clés (santé, sécurité domicile, données tierces) via
  `config/safety_rules.json`, retourne `{privacy_level, cloud_allowed,
  matched_categories}`. Volontairement niveau 0 de sobriété (règles
  explicites, pas de ML) — auditable et modifiable sans réentraînement.
- **`src/llm/llm_router.py`** : `LLMRouter.generate()` accepte désormais
  `cloud_allowed: bool`. Si `False`, le repli vers OpenAI/Anthropic est
  bloqué même si `allow_cloud_fallback=True` — la politique de contenu
  prime sur la disponibilité technique. Erreur explicite distincte
  (`"repli cloud bloqué par SafetyNet"`) plutôt qu'un échec silencieux.
- **`src/core/response_generator.py`** : calcule `cloud_allowed` via
  `is_cloud_allowed(user_message)` avant chaque appel LLM, même pattern que
  `tools_enabled` (`_should_enable_tools`) déjà en place pour le
  function-calling.
- Pourquoi un nouveau module plutôt que brancher `policy_engine.py`
  existant : ce dernier évalue un couple (rôle, ressource, action), pas la
  sensibilité d'un texte libre — le détourner aurait été plus complexe et
  moins lisible qu'un petit classifieur dédié.
- Tests : `tests/security_tests/test_safety_gate.py` (5 tests),
  `tests/b01_tests/test_llm_router_safety_gate.py` (3 tests) — 8/8 passés,
  + 58/58 tests existants (`response_generator`, `output_filter`,
  `policy_engine`) non affectés. Commit `55ac5eee`, poussé sur `main`.

### P1 — Rebrancher l'IntentNet déjà écrit ✅ **Livré 14/08/2026**

`analyze_v2()` (`src/conversation/nlp/nlp_engine_v2.py`, seul module NLP
réellement importé par `main.py`) retournait un intent hardcodé à
`"conversation"` quel que soit le texte — `IntentClassifier` existait mais
n'était jamais appelé. Rebranché : catégories étendues
(`emotional_support`, `engineering`) en réutilisant les mots-clés déjà
rédigés dans `config/intents_catalog.json`, vocabulaire choisi pour
recouper `multi_signal_fusion_engine.py::_INTENT_TO_MODE` (sinon
l'intention détectée resterait sans effet sur le mode ALFRED recommandé).
Tests : `test_intent_net_wiring.py` (4 tests). Commit `3833b802`.

### P2 — Sobriété réelle des modèles ✅ **Livré 14/08/2026**

`MODEL_PROFILES` listait déjà plusieurs tailles de modèle (3B à 120B) mais
`MODEL` était câblé en dur, jamais différencié par tâche. `OllamaLLMClient`
accepte désormais un `tools_model` optionnel (dédié aux tours
function-calling, là où llama3.2 a montré ~35-40 % d'échecs le
24/07/2026), configurable via `ALFRED_LLM_TOOLS_MODEL`. **Décision
volontaire : pas de changement de modèle par défaut** — la latence d'un
modèle plus lourd sur le matériel réel (Miniforum MS-S1 Max) n'a pas
encore été validée ; le mécanisme est livré, l'activation reste un choix à
faire une fois mesurée. Tests : `test_ollama_tools_model.py` (7 tests).
Commit `9a564880`.

### P3 — Politique mémoire écrite (MemoryNet léger) ✅ **Livré 14/08/2026**

`memory_engine.py` (`MemoryEngine`, seul chemin d'écriture mémoire
réellement exercé par `main.py` — `save_fact()`/SQLite `long_term_memory.py`
existent mais ne sont appelés nulle part en prod) loguait chaque échange
sans filtre ni purge : `dialogue_history.json` grandissait indéfiniment.
Ajout d'un `retention_days` optionnel (règle déterministe, pas de ML) qui
purge les échanges au-delà de N jours au chargement et après chaque
écriture. **Décision volontaire : `None` par défaut** (historique conservé
indéfiniment, comportement inchangé) — c'est de l'historique de
conversation personnel, la décision de le purger revient à Céline, pas à
un défaut silencieux. Tests : `test_memory_engine_retention.py` (5 tests).
Commit `0194051c`.

### P4 — Différé, pas engagé maintenant

Cognitive Bus événementiel complet, StateNet unifié, Learning LLM
propriétaire/LoRA, offres commerciales Standard/Adaptive/Pro. Investissement
structurel important que le document source lui-même conditionne à un gain
mesurable (section 25) — prématuré tant que P0-P3 ne sont pas stabilisés et
qu'aucun dataset ALFRED (Intent/Routing/Memory) n'existe encore pour
justifier un composant appris. `mode_manager.py` couvre déjà une partie du
StateNet ; l'étendre suffira longtemps avant d'avoir besoin d'un bus
d'événements complet.

---

## 4. Suivi

| Point | Statut | Commit |
|---|---|---|
| P0 — SafetyNet (blocage cloud) | ✅ Livré, testé | `55ac5eee` (2026-08-14) |
| P1 — IntentNet rebranché | ✅ Livré, testé | `3833b802` (2026-08-14) |
| P2 — Sobriété modèle | ✅ Livré, testé | `9a564880` (2026-08-14) |
| P3 — MemoryNet léger | ✅ Livré, testé | `0194051c` (2026-08-14) |
| P4 — Cognitive Bus / Learning LLM | Différé (pas de date) | — |

Les 4 points ont été traités un par un (implémentation → tests → commit
local dédié) le 14/08/2026. **Push différé** : une autre session travaillait
en parallèle sur le même dépôt ce jour-là (collision constatée sur
`docs/roadmap/ROADMAP_MASTER_V0_VFINALE.md` et `ROADMAP.md`) — décision de
Céline de faire un push global une fois toutes les sessions terminées
plutôt que de pousser point par point et risquer d'autres collisions.

Ce document sert de source de vérité pour ce chantier ; le suivi macro
(pourcentages, epics) reste dans
`docs/roadmap/ROADMAP_MASTER_V0_VFINALE.md`, epic **b01 — Interaction
conversationnelle intelligente**.
