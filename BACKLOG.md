# ALFRED — Backlog & État d'avancement
> Dernière mise à jour : Mai 2026 — généré depuis analyse complète du dépôt
> Référence canonique des blocs : `docs/ALFRED_BLOCS_REFERENCE.md`

---

## Légende

| Symbole | Signification |
|---------|---------------|
| ✅ | Implémenté — stable, maintenance seulement |
| 🔄 | En cours — code existant, évolution prévue |
| 🏗️ | Squelette / stub — interface définie, logique à coder |
| ⬜ | Vide — dossier/fichier créé, non implémenté |
| ❌ | Absent — non encore créé |
| 🔒 | Bloqué par dépendance hardware/externe |

---

## PARTIE 1 — FONDATIONS (stables — corrections de bugs seulement)

Ces fichiers ne bougeront plus sauf correction. Ils constituent la colonne vertébrale du projet.

| Fichier | Rôle | Statut | Notes |
|---------|------|--------|-------|
| `paths.py` | Centralise tous les chemins — résout les bugs relatifs | ✅ | Stable V1 |
| `requirements.txt` | Toutes les dépendances V1→V4 consolidées | ✅ | Ajouts par version seulement |
| `pyproject.toml` | Métadonnées projet Python 3.13 | ✅ | Stable |
| `bootstrap_project.ps1` | Crée toute l'arborescence en une commande | ✅ | Stable |
| `check_tools.ps1` | Vérifie les outils installés | ✅ | Stable |
| `patch_manifest.py` | Gestion du manifest de patch | ✅ | Stable |
| `ALFRED_CONTEXT.md` | Contexte collaborateur — à mettre à jour après chaque sprint | ✅ | Doc vivante |
| `docs/ALFRED_BLOCS_REFERENCE.md` | Référentiel canonique des blocs 01→22 | ✅ | Stable |
| `config/personality_core.json` | Noyau de personnalité ALFRED | ✅ | Stable |
| `knowledges/core/alfred_core_identity.json` | Identité fondamentale ALFRED | ✅ | Stable |
| `knowledges/core/system_rules.json` | Règles système | ✅ | Stable |

---

## PARTIE 2 — BLOCS TECHNIQUES PAR VERSION

---

### BLOC 20 — Cybersécurité Zero Trust (src/security/)
> **État global : ✅ V1 STABLE — Seuls 20.06 et 20.07 restent à implémenter**

| Sous-bloc | Fichier | Statut | Version cible |
|-----------|---------|--------|---------------|
| 20.01 Gouvernance | `security_config.py` | ✅ | — |
| 20.02 Identités | `role_manager.py`, `device_registry.py` | ✅ | — |
| 20.03 Auth/MFA | `mfa_manager.py`, `session_manager.py` | ✅ | — |
| 20.04 RBAC | `permission_manager.py`, `access_control.py` | ✅ | — |
| 20.05 Chiffrement | `encryption_service.py`, `output_filter.py`, `secret_manager.py` | ✅ | — |
| **20.06 Sécurité réseau** | *(à créer)* | ❌ | **V3** |
| **20.07 Sécurité API** | *(à créer)* | ❌ | **V3** |
| 20.08 Détection intrusion | `threat_detector.py`, `behavioral_detector.py`, `prompt_guard.py` | ✅ | — |
| 20.09 Journalisation | `security_logger.py`, `audit_trail.py` | ✅ | — |
| 20.10 Vulnérabilités | `input_validator.py` | ✅ | — |
| 20.11 Incidents | `incident_manager.py`, `quarantine_service.py` | ✅ | — |
| 20.12 Sauvegarde | `backup_security.py` | ✅ | — |
| 20.13 Zero Trust | `policy_engine.py`, `policy_decision_point.py`, `policy_enforcement_point.py`, `zero_trust_orchestrator.py` | ✅ | — |
| 20.14 Conformité | `compliance_manager.py` | ✅ | — |
| **20.15 SOC/Cybersurveillance** | *(à créer)* | ❌ | **V3+** |

---

### BLOC 01 — Noyau conversationnel & orchestration (src/core/, src/main.py)
> **Cœur du pipeline — évolue à chaque version majeure**

| Fichier | Contenu actuel | Statut | Évolue vers |
|---------|---------------|--------|-------------|
| `src/main.py` | Pipeline texte V1.2 complet — 978 lignes | 🔄 | Évolue à chaque sprint — seul point d'entrée officiel |
| `src/core/alfred_behavior_engine.py` | Moteur comportemental — 549 lignes | 🔄 | Enrichissement V2 (fusion décision) |
| `src/core/response_generator.py` | Générateur de réponses — 499 lignes | 🔄 | V2 (confidence scoring), V3 (LLM local) |
| `src/core/personality_adapter.py` | Adaptation personnalité — 427 lignes | 🔄 | V2 (modes dynamiques), V3 (deep relational) |
| `src/llm/llm_router.py` | Routeur LLM (Ollama/OpenAI) | ✅ | Ajout llama-cpp V3 |
| `src/llm/llm_client_ollama.py` | Client Ollama | ✅ | Stable |
| `src/llm/llm_client_openai.py` | Client OpenAI | ✅ | Stable |

**Backlog :**
- [ ] **[V2]** Brancher `src/v2/fusion/` dans `alfred_behavior_engine.py`
- [ ] **[V2]** Brancher `src/v2/confidence/` dans `response_generator.py`
- [ ] **[V3]** Intégrer pipeline vocal dans `main.py` (STT/TTS) via `src/v3/orchestrator/`
- [ ] **[V3]** Brancher `llm_client_local.py` (llama-cpp) dans `nlp_engine_v2.py`

---

### BLOC 02 — Mémoire & contexte (src/memory/)
> **Pipeline mémoire V1 fonctionnel — RAG bloqué sur ChromaDB**

| Fichier | Contenu actuel | Statut | Évolue vers |
|---------|---------------|--------|-------------|
| `src/memory/memory_manager.py` | Chef d'orchestre mémoire — 296 lignes | 🔄 | V2 (indexation), V3 (RAG) |
| `src/memory/episodic_memory.py` | Mémoire épisodique — 263 lignes | 🔄 | V3 (enrichissement sémantique) |
| `src/memory/long_term_memory.py` | Mémoire long terme SQLite — 374 lignes | ✅ | Stable V1 |
| `src/memory/memory_engine.py` | Moteur mémoire — 159 lignes | 🔄 | V2 |
| `src/memory/memory_indexer.py` | Indexeur mémoire — 175 lignes | 🔄 | V3 (embeddings) |
| `src/memory/memory_answer_engine.py` | Moteur réponse depuis mémoire | 🔄 | V2/V3 |
| `src/memory/rag_stub.py` | **Interface ChromaDB stable — implémentation V3+** | 🏗️ | **V3** (ChromaDB local) |

**Backlog :**
- [ ] **[V2]** `src/v2/knowledge/` — implémentation recherche sémantique légère
- [ ] **[V3]** Implémenter `rag_stub.py` → `rag_engine.py` avec ChromaDB local (HDD 4 To)
- [ ] **[V3]** Brancher embeddings dans `memory_indexer.py`
- [ ] **[V3]** `src/v3/memory/` — mémoire contextuelle long terme étendue

---

### BLOC 03 — Émotions & adaptation comportementale (src/regulation/)
> **Détection textuelle V2 fonctionnelle — prosodie audio V3 stub**

| Fichier | Contenu actuel | Statut | Évolue vers |
|---------|---------------|--------|-------------|
| `src/regulation/emotion_detector.py` | Détection V2 (texte) — 303 lignes | 🔄 | V3 : `detect_emotion_from_audio_stub()` → librosa |
| `src/regulation/mode_manager.py` | Gestion 4 modes (support/focus/challenge/complicité) — 337 lignes | 🔄 | V3 (transitions adaptatives) |
| `src/regulation/wellbeing_tracker.py` | Suivi bien-être — 286 lignes | 🔄 | V3 (historique émotionnel) |
| `src/regulation/protection_guard.py` | Protection éthique — 228 lignes (note V2→V3 interne) | 🔄 | V3 (enrichissement) |

**Backlog :**
- [ ] **[V3]** Implémenter `detect_emotion_from_audio_stub()` avec librosa (pitch, débit, énergie)
- [ ] **[V3]** `src/v3/emotion/` — pipeline émotion multi-modal (texte + audio)
- [ ] **[V3]** Transitions d'états avatar synchronisées avec l'émotion

---

### BLOC 04 — Interaction vocale (src/conversation/)
> **Façades V1 stables — implémentation réelle V3 (Whisper + Piper déjà codé)**

| Fichier | Contenu actuel | Statut | Évolue vers |
|---------|---------------|--------|-------------|
| `src/conversation/input/audio_capture.py` | **Stub V1 — interface définie, toujours False** | 🏗️ | **V3** (Whisper local) |
| `src/conversation/input/audio_listener.py` | NotImplementedError intentionnel | 🏗️ | **V3** |
| `src/conversation/input/stt_whisper.py` | Module STT Whisper — 214 lignes | 🔄 | **V3** (dépend GPU RTX) |
| `src/conversation/input/speech_manager.py` | Orchestrateur STT — 215 lignes | 🔄 | V3 |
| `src/conversation/input/nlp_engine_v2.py` | NLP V2 — 223 lignes, **TODO V3: hook LLM local** | 🔄 | V3 (brancher llm_client_local) |
| `src/conversation/input/context_builder.py` | Builder de contexte — 211 lignes | 🔄 | V3 |
| `src/conversation/input/text_input.py` | Entrée texte terminal | ✅ | Stable (mode fallback) |
| `src/conversation/input/voice_profile.py` | Profils voix — 163 lignes | ✅ | Stable |
| `src/conversation/output/tts_output.py` | **Façade V1 — affichage terminal, stub TTS** | 🏗️ | V3 (Piper activé) |
| `src/conversation/output/tts_piper.py` | **Piper TTS CODÉ — 393 lignes, fr_FR-upmc-medium** | 🔄 | **V3** (dépend `sounddevice`) |
| `src/conversation/output/tts_engine.py` | Moteur TTS abstrait | 🔄 | V3 |
| `src/conversation/nlp/nlp_engine.py` | NLP V1 — 232 lignes | ✅ | Remplacé par nlp_engine_v2 |
| `src/conversation/nlp/nlp_engine_v2.py` | NLP V2 (doublon intentionnel /nlp/) | 🔄 | Nettoyage structure V2 |

**Backlog :**
- [ ] **[V3]** Activer `audio_capture.py` avec sounddevice + Whisper (vérifier RTX 5080)
- [ ] **[V3]** Connecter `tts_piper.py` comme moteur actif dans `tts_output.py`
- [ ] **[V3]** Brancher hook LLM dans `nlp_engine_v2.py` (ligne 125)
- [ ] **[V3]** `src/v3/conversation/` — pipeline vocal complet
- [ ] **[TECH DEBT]** Unifier les deux `nlp_engine_v2.py` (src/conversation/input/ et src/conversation/nlp/)

---

### BLOC 05 — Gestion utilisateur (src/auth/)
> **Structure créée, contenu vide**

| Fichier | Statut | Version cible |
|---------|--------|---------------|
| `src/auth/__init__.py` | ⬜ Vide | V2 |
| `data/users/instances/` | ✅ Données JSON présentes | Stable |
| `config/user_adaptation_profile.json` | ✅ Config présente | Stable |

**Backlog :**
- [ ] **[V2]** Implémenter module auth (login, session, profil)
- [ ] **[V2]** Connecter `src/v2/experience/` pour profil adaptatif utilisateur

---

### BLOC 06 — Assistance quotidienne (src/assistant_actions/)
> **Dossier créé, vide**

| Fichier | Statut | Version cible |
|---------|--------|---------------|
| `src/assistant_actions/__init__.py` | ⬜ Vide | V2 |
| `data/actions/` | ✅ Structure présente | — |

**Backlog :**
- [ ] **[V2]** Implémenter agenda, rappels, gestion tâches
- [ ] **[V2]** `src/v2/scenarios/` — scénarios d'assistance

---

### BLOC 07 — Apprentissage & routines
> **Dépend entièrement de V3**

| Fichier | Statut | Version cible |
|---------|--------|---------------|
| `src/v3/learning/__init__.py` | ⬜ Vide | **V3** |
| `data/context/` | ✅ Structure présente | — |

**Backlog :**
- [ ] **[V3]** Implémenter `src/v3/learning/` — analyse habitudes, recommandations
- [ ] **[V3]** `src/v3/proactive/` — comportement proactif

---

### BLOC 08 — Supervision système
> **Géré par config — pas de module dédié**

| Fichier | Statut |
|---------|--------|
| `config/ethics_rules.json` | ✅ Stable |
| `config/safety_rules.json` | ✅ Stable |
| Logs système | 🔄 Via security_logger.py |

**Backlog :**
- [ ] **[V2]** Créer module monitoring / health check système
- [ ] **[V3]** Dashboard temps réel (intégrer dans ALFRED_DASHBOARD.html)

---

### BLOC 15 — Présence visuelle & Avatar (src/ui/, assets/avatar/)
> **⚠️ PRIORITÉ CRITIQUE — rien de codé côté Kivy**

| Composant | Statut | Version cible |
|-----------|--------|---------------|
| `src/ui/__init__.py` | ⬜ Vide | — |
| Sprites PNG (6 calques) | ✅ Assets présents dans `assets/avatar/` | — |
| Moteur Kivy (calques, animations) | ❌ **Non codé** | **V1 MVP** |
| Blink automatique (3-6 sec, 150ms) | ❌ Non codé | **V1 MVP** |
| Sync bouche TTS (mouth_1→5) | ❌ Non codé | **V1 MVP** |
| Halo pulsation dynamique | ❌ Non codé | **V1 MVP** |
| Gestion états (neutral/happy/calm/surprised) | ❌ Non codé | **V1 MVP** |

**Backlog :**
- [ ] **[V1 MVP — PRIORITÉ 1]** Créer `src/ui/avatar_engine.py` — moteur Kivy 6 calques
- [ ] **[V1 MVP — PRIORITÉ 1]** Implémenter blink automatique
- [ ] **[V1 MVP — PRIORITÉ 2]** Sync labiale TTS (écoute events `tts_piper.py`)
- [ ] **[V1 MVP — PRIORITÉ 2]** Halo pulsation selon état émotionnel
- [ ] **[V2]** Expressions faciales (happy, calm, surprised)
- [ ] **[V3]** Avatars chibi (notifications, overlay)
- [ ] **[V3]** Transitions fluides entre états

---

### BLOC 18 — Base de connaissances & culture (knowledges/, src/knowledge/)
> **Base JSON présente (291 fichiers) — moteur de routage V2 opérationnel**

| Fichier | Contenu actuel | Statut |
|---------|---------------|--------|
| `src/knowledge/knowledge_router.py` | Routeur — 350 lignes, VERSION 2.0.0 | 🔄 |
| `src/knowledge/domain_matcher.py` | Matcher domaines — 213 lignes | 🔄 |
| `src/knowledge/knowledge_ranker.py` | Classement pertinence — 264 lignes | 🔄 |
| `src/knowledge/retrieval_engine.py` | Moteur récupération — 156 lignes | 🔄 |
| `src/knowledge/knowledge_loader.py` | Chargeur JSON | ✅ |
| `src/knowledge/taxonomy_router.py` | Routeur taxonomie — 194 lignes | 🔄 |
| `src/knowledge/context_merger.py` | Fusion contextes — 236 lignes | 🔄 |
| `knowledges/` (291 fichiers JSON) | Base de connaissances complète | ✅ |

**Backlog :**
- [ ] **[V2]** `src/v2/knowledge/` — enrichissement sémantique du routage
- [ ] **[V3]** Branchement RAG (ChromaDB) dans `retrieval_engine.py`
- [ ] **[V3+]** Enrichissement continu des knowledges (human, professional, lifestyle, culture)

---

### BLOC 19 — Infrastructure & extensions
> **V4 — Dépend de la domotique**

| Composant | Statut | Version cible |
|-----------|--------|---------------|
| `src/v4/integration/__init__.py` | ⬜ Vide | V4 |
| `src/v4/home_state/__init__.py` | ⬜ Vide | V4 |
| `config/v4/` | Structure présente | V4 |

**Backlog :**
- [ ] **[V4]** Implémenter paho-mqtt pour IoT
- [ ] **[V4]** `src/v4/home_state/` — état maison connectée
- [ ] **[V4]** `src/v4/integration/` — API équipements domotiques

---

### BLOC 22 — Accessibilité & Assistance cognitive (src/accessibility/)
> **Squelettes présents — implémentation légère V1**

| Fichier | Lignes | Statut | Version cible |
|---------|--------|--------|---------------|
| `accessibility_manager.py` | 60 | 🏗️ Squelette | V2 |
| `audio/text_reader.py` | 47 | 🏗️ Squelette | V2 |
| `audio/voice_output_manager.py` | 44 | 🏗️ Squelette | V2/V3 |
| `translation/translator.py` | 37 | 🏗️ Squelette | V2 |
| `cognitive/summarizer.py` | 36 | 🏗️ Squelette | V3 |
| `cognitive/explain_terms.py` | 53 | 🏗️ Squelette | V3 |
| `accessibility/ui/` | ⬜ Vide | — | V3 |

**Backlog :**
- [ ] **[V2]** Implémenter traduction multilingue (translator.py)
- [ ] **[V2]** Mode lecture vocale + restitution audio
- [ ] **[V3]** Résumés intelligents + explication termes techniques
- [ ] **[V3]** Modes neurodiversité (dyslexie, fatigue cognitive)
- [ ] **[V3]** Accessibilité Android (Kivy)

---

### BLOC 21 — ALFRED WEB PLATFORM
> **🔄 Débuté — dépôt séparé : `cognitive-products-lab/alfred_web`**
> Chemin local : `D:\PROJET_ALFRED\ALFRED_WEB`

| Composant | Statut | Version cible |
|-----------|--------|---------------|
| Repo `alfred_web` | 🔄 Débuté | V2+ |
| Flask app (`app.py`) | 🔄 En cours | V2+ |
| Templates HTML/Jinja2 | 🔄 En cours | V2+ |
| Dashboard web progression | ⬜ À coder | V2+ |
| SEO + accessibilité web | ⬜ À coder | V2+ |
| Sécurité formulaires (Bloc 21.09) | ⬜ À coder | V2+ |
| Déploiement / CI-CD (Bloc 21.10) | ⬜ À coder | V3 |

**Backlog :**
- [x] **[V2+]** ~~Créer `ALFRED_WEB/`~~ → repo `alfred_web` débuté ✅
- [ ] **[V2+]** Compléter pages vitrine (projet, roadmap publique, contact)
- [ ] **[V2+]** Dashboard progression en ligne (Bloc 21.06)
- [ ] **[V2+]** SEO + accessibilité WCAG (Bloc 21.08)
- [ ] **[V3]** Déploiement + CI/CD (Bloc 21.10)

---

## PARTIE 3 — MODULES V2/V3/V4 — ÉTAT VIDE (à implémenter intégralement)

> ⚠️ **Tous ces dossiers contiennent uniquement un `__init__.py` vide.** Ce sont des réservations d'architecture.

### V2 — Intelligence & décision fusionnée

| Module | Chemin | Rôle prévu | Priorité |
|--------|--------|-----------|----------|
| `fusion` | `src/v2/fusion/` | Fusion multi-sources (mémoire + knowledge + LLM) | 🔴 Haute |
| `decision` | `src/v2/decision/` | Moteur de décision contextuelle | 🔴 Haute |
| `confidence` | `src/v2/confidence/` | Score de confiance réponse | 🔴 Haute |
| `knowledge` | `src/v2/knowledge/` | Enrichissement base de connaissances | 🟡 Moyenne |
| `learning` | `src/v2/learning/` | Apprentissage préférences utilisateur | 🟡 Moyenne |
| `experience` | `src/v2/experience/` | Profil expérience utilisateur | 🟡 Moyenne |
| `fallback` | `src/v2/fallback/` | Stratégie de repli (LLM absent) | 🟡 Moyenne |
| `governance` | `src/v2/governance/` | Règles de gouvernance IA | 🟢 Basse |
| `scenarios` | `src/v2/scenarios/` | Scénarios d'usage typiques | 🟢 Basse |
| `product` | `src/v2/product/` | Gestion produit (état, KPI) | 🟢 Basse |

### V3 — Compagnon cognitif adaptatif

| Module | Chemin | Rôle prévu | Priorité |
|--------|--------|-----------|----------|
| `orchestrator` | `src/v3/orchestrator/` | Orchestrateur vocal complet | 🔴 Haute |
| `conversation` | `src/v3/conversation/` | Pipeline conversationnel V3 | 🔴 Haute |
| `emotion` | `src/v3/emotion/` | Émotion multi-modal (texte + audio) | 🔴 Haute |
| `memory` | `src/v3/memory/` | RAG + mémoire sémantique | 🔴 Haute |
| `reasoning` | `src/v3/reasoning/` | Raisonnement IA avancé | 🟡 Moyenne |
| `fusion` | `src/v3/fusion/` | Fusion V3 (tout les modules) | 🟡 Moyenne |
| `learning` | `src/v3/learning/` | Apprentissage comportemental | 🟡 Moyenne |
| `proactive` | `src/v3/proactive/` | Comportement proactif | 🟢 Basse |
| `safety` | `src/v3/safety/` | Garde-fous éthiques V3 | 🟡 Moyenne |

### V4 — Environnement connecté & domotique

| Module | Chemin | Rôle prévu | Priorité |
|--------|--------|-----------|----------|
| `orchestrator` | `src/v4/orchestrator/` | Orchestrateur domotique | 🟢 V4 |
| `home_state` | `src/v4/home_state/` | État maison (capteurs, équipements) | 🟢 V4 |
| `integration` | `src/v4/integration/` | API domotique (MQTT, HTTP) | 🟢 V4 |
| `actions` | `src/v4/actions/` | Actions automatisées | 🟢 V4 |
| `scenarios` | `src/v4/scenarios/` | Scénarios domotiques | 🟢 V4 |
| `triggers` | `src/v4/triggers/` | Déclencheurs contextuels | 🟢 V4 |
| `security` | `src/v4/security/` | Sécurité IoT | 🟢 V4 |

---

## PARTIE 4 — DETTE TECHNIQUE

| Problème | Fichier(s) | Priorité | Action |
|----------|-----------|----------|--------|
| Doublon `nlp_engine_v2.py` | `src/conversation/input/` et `src/conversation/nlp/` | 🟡 | Unifier en V2 |
| `src/v1/__init__.py` vide | `src/v1/` | 🟢 | Décider : migrer V1 vers structure versionnée ou supprimer |
| `src/dialogue/__init__.py` vide | `src/dialogue/` | 🟡 | Implémenter ou supprimer |
| `src/rag/__init__.py` non listé | `src/rag/` | 🟡 | Décider : utiliser rag_stub ou dédier |
| `ALFRED_CONTEXT.md` daté d'Avril 2026 | — | 🟡 | Mettre à jour après chaque sprint majeur |
| `src/security.py` legacy (si encore présent) | `src/security.py` | 🔴 | Supprimer — Bloc 20 gagne |
| V4 "trop léger" (mentionné ALFRED_CONTEXT) | `src/v4/` | 🟢 | Retravailler au sprint V4 |

---

## PARTIE 5 — PRODUITS DÉRIVÉS (hors ALFRED core)

### ALFRED CPL (Blocs 09, 10, 11, 12)
> **Non initié — réservations d'architecture uniquement**

| Composant | Statut | Notes |
|-----------|--------|-------|
| `ALFRED_CPL/` | ❌ Absent | Dépôt distinct prévu |
| Blocs 09-12 (API, IA avancée, Data, Collaboration) | ❌ | Post-V2 ALFRED core |
| `knowledges/cpl/` | ✅ Structure présente | Base connaissance CPL |

**Backlog :**
- [ ] **[Post-V2]** Créer dépôt ALFRED_CPL distinct
- [ ] **[Post-V2]** Implémenter Blocs 09-12 sur base ALFRED core

### ARTHUR (Blocs 13, partiellement 14-15)
> **En attente d'avis professionnels de santé**

| Composant | Statut | Notes |
|-----------|--------|-------|
| `ARTHUR/` | ❌ Absent | Dépôt distinct — en attente |
| Bloc 13 (santé/soutien) | ❌ | Bloqué — validation médicale requise |
| Bloc 14 IoT | Partiellement avec V4 | — |
| Assets ARTHUR | ✅ Avatar turquoise dans `assets/` | — |

**Backlog :**
- [ ] **[Post-V3 + validation médicale]** Initier ARTHUR
- [ ] **[Thèse]** Cadre RGPD mineurs à définir avant tout codage

---

## PARTIE 6 — INFRASTRUCTURE PROJET

### Dashboard & Outillage

| Composant | Statut | Notes |
|-----------|--------|-------|
| `dashboard/ALFRED_DASHBOARD.html` | ✅ Fonctionnel | Interface de suivi |
| `tools/dashboard_tools/update_dashboard_data.py` | ✅ 578 lignes | Robuste |
| `tools/dashboard_tools/compare_manifest_target.py` | ✅ | Comparaison cible |
| `tools/knowledge_tools/generate_knowledge_registry.py` | ✅ | Registre knowledges |

### Tests

| Fichier | Couverture | Statut |
|---------|-----------|--------|
| `tests/test_b01_speech.py` | Speech/STT | 🔄 À compléter V3 |
| `tests/test_b02_b03.py` | Mémoire + Émotions | 🔄 |
| `tests/test_pipeline.py` | Pipeline intégration | 🔄 |
| `tests/test_pipeline_llm.py` | Pipeline LLM | 🔄 |
| `tests/test_tts_piper.py` | Piper TTS | 🔄 |
| `tests/test_security.py` | Sécurité Zero Trust | ✅ Créé — 24 classes, ~120 tests |
| Tests avatar/UI | ❌ Absent | V2 |

**Backlog :**
- [x] **[V1]** ~~Créer tests unitaires Bloc 20 (sécurité — 25 modules critiques)~~ → `tests/test_security.py` ✅
- [ ] **[V2]** Tests d'intégration pipeline complet
- [ ] **[V3]** Tests end-to-end vocal

---

## RÉSUMÉ — SYNTHÈSE PAR VERSION

### V1 — État actuel

| Catégorie | État |
|-----------|------|
| Pipeline texte (main.py) | ✅ Fonctionnel |
| Personnalité + mémoire | ✅ Fonctionnel |
| Knowledge routing | ✅ Fonctionnel (V2.0.0) |
| Émotions (texte) | ✅ Fonctionnel |
| Sécurité Zero Trust | ✅ Complet (25 modules) |
| TTS Piper | 🔄 Codé, dépend hardware |
| Interface Kivy / Avatar | ❌ Non codé |
| Tests sécurité | ✅ Créés (test_security.py) |

**Ce qui manque pour finir V1 proprement :**
1. Moteur avatar Kivy (6 calques + blink + halo)
2. Tests unitaires Bloc 20
3. Mise à jour `ALFRED_CONTEXT.md`

---

### V2 — Prochaine version majeure

**Objectif :** Fusion intelligence + décision + expérience utilisateur

| À implémenter | Module |
|---------------|--------|
| Fusion multi-sources | `src/v2/fusion/` |
| Score confiance | `src/v2/confidence/` |
| Décision contextuelle | `src/v2/decision/` |
| Profil adaptatif | `src/v2/experience/` |
| Stratégie fallback | `src/v2/fallback/` |
| Auth module | `src/auth/` |
| Accessibilité V2 | `src/accessibility/` |
| Web platform (vitrine) | `alfred_web` (repo séparé) 🔄 débuté |

---

### V3 — Vision compagnon cognitif

**Objectif :** Pipeline vocal complet + RAG + émotions audio + raisonnement IA

| À implémenter | Module | Dépendance hardware |
|---------------|--------|---------------------|
| Pipeline vocal complet | `main.py` + `src/v3/orchestrator/` | sounddevice + micro |
| STT Whisper actif | `audio_capture.py` | Whisper installé |
| TTS Piper actif | `tts_output.py` → `tts_piper.py` | Piper + fr_FR voice |
| LLM local | `nlp_engine_v2.py` hook V3 | llama-cpp + modèle |
| RAG ChromaDB | `rag_stub.py` → réel | ChromaDB + HDD 4 To |
| Émotion audio | `emotion_detector.py` stub | librosa |
| Orchestrateur V3 | `src/v3/orchestrator/` | — |
| Sécurité réseau/API | Blocs 20.06/20.07 | — |

---

### V4 — Domotique & environnement connecté

**Objectif :** ALFRED intégré dans l'environnement (IoT, domotique)
> À initier uniquement après V3 stable

| À implémenter | Module |
|---------------|--------|
| MQTT IoT | `src/v4/integration/` |
| État maison | `src/v4/home_state/` |
| Actions automatisées | `src/v4/actions/` |
| Scénarios domotiques | `src/v4/scenarios/` |

---

*Backlog généré depuis analyse complète du dépôt — Mai 2026*
*Prochaine mise à jour : après sprint V1 MVP Avatar*
