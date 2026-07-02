# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS

> Généré le 02/07/2026 17:00 depuis `dashboard_data.json` (mis à jour le 02/07/2026 17:00:19)
> Progression technique : **76.6%** · Full projet : **69.0%**
> 1115 fichiers détectés / 1471 cible full

## Synthèse globale

| Statut | Nb | % | Priorité |
|--------|---:|--:|----------|
| 🟡 Partiel | 78 | 7.0% | 🟡 Sprint |
| 🟦 Codé — à tester | 134 | 12.0% | 🟡 Sprint |
| 🧪 Testé — à valider | 3 | 0.3% | 🧪 Tests |
| ✅ Validé ✅ | 844 | 75.7% | ✅ Done |
| ⚙️ Structurel | 56 | 5.0% | ✅ Done |

## Backlog par bloc

### 🟡 B01 — Noyau conversationnel & orchestration `71.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 2 |
| Codés (à tester) | 18 |
| Partiels | 4 |
| Structurels | 4 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/dialogue_history.json` | 🟡 Partiel | Compléter |
| `src/output/tts_engine.py` | 🟡 Partiel | Compléter |
| `src/output/tts_output.py` | 🟡 Partiel | Compléter |
| `src/output/tts_piper.py` | 🟡 Partiel | Compléter |
| `config/conversation_rules.json` | 🟦 Codé — à tester | Tester |
| `data/memory/episodic/dialogue_history.json` | 🟦 Codé — à tester | Tester |
| `src/conversation/input/audio_capture.py` | 🟦 Codé — à tester | Tester |
| `src/conversation/nlp/nlp_engine_v2.py` | 🟦 Codé — à tester | Tester |
| `src/conversation/input/speech_manager.py` | 🟦 Codé — à tester | Tester |
| `src/conversation/input/text_input.py` | 🟦 Codé — à tester | Tester |
| `src/llm/llm_client_ollama.py` | 🟦 Codé — à tester | Tester |
| `src/conversation/output/tts_output.py` | 🟦 Codé — à tester | Tester |
| `src/core/response_generator.py` | 🟦 Codé — à tester | Tester |
| `tests/test_b01_speech.py` | 🟦 Codé — à tester | Tester |
| `tests/test_pipeline_llm.py` | 🟦 Codé — à tester | Tester |
| `src/conversation/input/audio_listener.py` | 🟦 Codé — à tester | Tester |
| `src/conversation/nlp/intent_classifier.py` | 🟦 Codé — à tester | Tester |
| `src/v2/fusion/fusion_engine.py` | 🟦 Codé — à tester | Tester |
| `src/v2/confidence/confidence_scorer.py` | 🟦 Codé — à tester | Tester |
| `src/v2/decision/decision_engine.py` | 🟦 Codé — à tester | Tester |
| `tests/b01_tests/test_fusion_engine.py` | 🟦 Codé — à tester | Tester |
| `tests/integration_tests/test_v2_pipeline.py` | 🟦 Codé — à tester | Tester |

### 🟢 B02 — Mémoire & contexte `80.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 0 |
| Codés (à tester) | 6 |
| Partiels | 4 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v3/memory_rules.json` | 🟡 Partiel | Compléter |
| `data/v2/memory_samples.json` | 🟡 Partiel | Compléter |
| `data/v3/memory_patterns.json` | 🟡 Partiel | Compléter |
| `src/memory/memory_manager.py` | 🟡 Partiel | Compléter |
| `data/user_memory.json` | 🟦 Codé — à tester | Tester |
| `src/memory/episodic_memory.py` | 🟦 Codé — à tester | Tester |
| `src/memory/long_term_memory.py` | 🟦 Codé — à tester | Tester |
| `src/memory/memory_indexer.py` | 🟦 Codé — à tester | Tester |
| `src/memory/rag_stub.py` | 🟦 Codé — à tester | Tester |
| `src/rag/rag_engine.py` | 🟦 Codé — à tester | Tester |

### 🟢 B03 — Émotions & adaptation comportementale `86.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 18 |
| Testés | 0 |
| Codés (à tester) | 1 |
| Partiels | 5 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/emotion_profiles.json` | 🟡 Partiel | Compléter |
| `config/v3/emotion_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/tone_profiles.json` | 🟡 Partiel | Compléter |
| `data/v3/emotion_state.json` | 🟡 Partiel | Compléter |
| `data/v3/relational_state.json` | 🟡 Partiel | Compléter |
| `tests/test_b02_b03.py` | 🟦 Codé — à tester | Tester |

### ❌ B04 — Interaction vocale `0.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

> ⚠️ Aucun bloc 'Dashboard ancien' ne correspondait à ce Bloc officiel 04 lors de la réconciliation du 02/07/2026 — les fichiers STT/TTS (src/conversation/input/, src/conversation/output/) sont actuellement comptés sous Bloc 01. Décision à prendre : les extraire vers Bloc 04 ou laisser Bloc 04 vide.

### 🟡 B05 — Gestion utilisateur `72.6%`

| KPI | Valeur |
|-----|--------|
| Validés | 8 |
| Testés | 0 |
| Codés (à tester) | 17 |
| Partiels | 1 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/personality.json` | 🟡 Partiel | Compléter |
| `config/personality_core.json` | 🟦 Codé — à tester | Tester |
| `config/user_adaptation_profile.json` | 🟦 Codé — à tester | Tester |
| `data/personality/instances/personality_core_instance.json` | 🟦 Codé — à tester | Tester |
| `data/personality/templates/personality_core.json` | 🟦 Codé — à tester | Tester |
| `data/personality/templates/personality_core_template_public.json` | 🟦 Codé — à tester | Tester |
| `data/preferences_profile.json` | 🟦 Codé — à tester | Tester |
| `data/profile/user_profile.json` | 🟦 Codé — à tester | Tester |
| `data/users/instances/user_celine_instance.json` | 🟦 Codé — à tester | Tester |
| `data/users/templates/user_adaptation_profile.json` | 🟦 Codé — à tester | Tester |
| `data/users/templates/user_profile_template_public.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/behavioral_modes.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/context_awareness.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/personalization_engine.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/system_rules.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/user_adaptation.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/self_alignment/routines/feedback_loop.json` | 🟦 Codé — à tester | Tester |
| `src/core/alfred_behavior_engine.py` | 🟦 Codé — à tester | Tester |

### 🟢 B06 — Assistance quotidienne `91.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 11 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 2 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/actions/tasks.json` | 🟡 Partiel | Compléter |
| `data/v2/scenarios/daily_organization.json` | 🟡 Partiel | Compléter |

### 🟠 B07 — Apprentissage & routines `40.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 1 |
| Structurels | 0 |
| Manquants | 0 |

> 🟪 Roadmap V2 — ALFRED Android : client mobile léger connecté au core ALFRED_PC (LLM + mémoire + knowledge). Accès distant via API REST/WebSocket sécurisé + tunnel WireGuard (ER605). Auth JWT + TLS mutuel. UI conversationnelle Android (Kotlin ou Flutter à trancher).

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/context/user_context.json` | 🟡 Partiel | Compléter |

### 🟡 B08 — Supervision système `76.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 4 |
| Testés | 0 |
| Codés (à tester) | 6 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `.env.example` | 🟦 Codé — à tester | Tester |
| `.gitignore` | 🟦 Codé — à tester | Tester |
| `config/ethics_rules.json` | 🟦 Codé — à tester | Tester |
| `config/settings.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/ethics/ethical_framework.json` | 🟦 Codé — à tester | Tester |
| `pyproject.toml` | 🟦 Codé — à tester | Tester |

### ✅ B09 — API & microservices `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 15 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### 🟢 B10 — Intelligence artificielle avancée `96.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 16 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 1 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `src/knowledge/knowledge_router.py` | 🟡 Partiel | Compléter |

### 🟢 B11 — Data & pilotage `88.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 3 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/kpi_config.json` | 🟡 Partiel | Compléter |
| `config/v2/product_roadmap.json` | 🟡 Partiel | Compléter |
| `data/v2/product_state.json` | 🟡 Partiel | Compléter |

### 🟢 B12 — Collaboration professionnelle `89.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 9 |
| Testés | 0 |
| Codés (à tester) | 4 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

> 🟪 Roadmap V2 — ALFRED CPL : collaborateur professionnel interactif. Interface mode pro (brainstorming, revue docs, suivi projets), knowledges métier CPL (IA, cybersécurité, entrepreneuriat, droit numérique), co-rédaction, mémoire des décisions. Module src/collaboration/ créé (12.01-12.05 : projet, coordination, décisions, documents, rapport co-rédigé) — reste : brainstorming assisté, knowledges/professional/cpl/.

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `src/collaboration/project/project_store.py` | 🟦 Codé — à tester | Tester |
| `src/collaboration/project/project_manager.py` | 🟦 Codé — à tester | Tester |
| `src/start_alfred_cpl.bat` | 🟦 Codé — à tester | Tester |
| `src/start_alfred_hybride.bat` | 🟦 Codé — à tester | Tester |

### 🟡 B13 — Santé & soutien émotionnel `66.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 5 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `src/health/chronic_support.py` | 🟦 Codé — à tester | Tester |
| `src/health/health_profile.py` | 🟦 Codé — à tester | Tester |
| `src/health/interaction_adapter.py` | 🟦 Codé — à tester | Tester |
| `src/health/onboarding.py` | 🟦 Codé — à tester | Tester |
| `src/health/profile_loader.py` | 🟦 Codé — à tester | Tester |

### ✅ B14 — IoT & environnement connecté `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

> 🟪 Roadmap V2 — Architecture IoT esquissée (src/v4/). Systèmes disponibles : Google Home + Tuya. Implémenter : tinytuya (accès local/cloud) + Google Home API, pattern Adapter (tuya_adapter.py + google_home_adapter.py).

### 🟡 B15 — Présence visuelle & avatar `66.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 9 |
| Testés | 0 |
| Codés (à tester) | 44 |
| Partiels | 1 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `assets/models/tts/fr_FR/ALIASES` | 🟡 Partiel | Compléter |
| `src/ui/alfred_app.py` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_open.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_idle_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_idle_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_open.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_open.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_a.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_e.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_i.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_o.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_u.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_m.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_listening.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_thinking.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_thinking_full.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_explaining.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_happy.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_working.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_confused.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_cybersecurity.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_love.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_medium/base_medium/alfred_medium_excited.png` | 🟦 Codé — à tester | Tester |
| *... 15 autres* | | |

### 🟠 B16 — Démonstration & Scénarisation (réservé — Bloc 16 non assigné officiellement, docs/ALFRED_BLOCS_REFERENCE.md) `43.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 1 |
| Partiels | 5 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/scenario_catalog.json` | 🟡 Partiel | Compléter |
| `data/v2/scenario_results.json` | 🟡 Partiel | Compléter |
| `data/v2/scenarios/career_transition.json` | 🟡 Partiel | Compléter |
| `data/v2/scenarios/isolation_support.json` | 🟡 Partiel | Compléter |
| `data/v2/scenarios/mental_overload.json` | 🟡 Partiel | Compléter |
| `tests/test_pipeline.py` | 🟦 Codé — à tester | Tester |

### 🟢 B17 — Génération multimédia `94.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 72 |
| Testés | 0 |
| Codés (à tester) | 12 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_debut_journee.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_fin_journee.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_nuit.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_debut fin journee.jpg` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_matinee.jpg` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_soiree.jpg` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/interieur/bureau/open_office/background_paysage_interieur_bureau_open_office.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_debut_journee.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_fin_journee.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_nuit.jpg` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/interieur/specifique/sport/background_portrait_interieur_sport.png` | 🟦 Codé — à tester | Tester |
| `assets/backgrounds/mode_portrait/orientation portrait/specifique/Transport/background_portrait_exterieur_transport_debut fin journee.jpg` | 🟦 Codé — à tester | Tester |

### 🟢 B18 — Base de connaissances & culture `96.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 566 |
| Testés | 1 |
| Codés (à tester) | 0 |
| Partiels | 38 |
| Structurels | 27 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v1/basic_pipeline_rules.json` | 🟡 Partiel | Compléter |
| `config/v2/confidence_rules.json` | 🟡 Partiel | Compléter |
| `config/v2/decision_rules.json` | 🟡 Partiel | Compléter |
| `config/v2/edge_cases.json` | 🟡 Partiel | Compléter |
| `config/v2/fallback_rules.json` | 🟡 Partiel | Compléter |
| `config/v2/feature_matrix.json` | 🟡 Partiel | Compléter |
| `config/v2/learning_rules.json` | 🟡 Partiel | Compléter |
| `config/v2/naming_conventions.json` | 🟡 Partiel | Compléter |
| `config/v2/proactivity_rules.json` | 🟡 Partiel | Compléter |
| `config/v2/signal_weights.json` | 🟡 Partiel | Compléter |
| `config/v3/confidence_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/conversation_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/fusion_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/learning_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/orchestrator_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/pattern_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/priority_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/proactive_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/relational_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/trigger_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/workflow_rules.json` | 🟡 Partiel | Compléter |
| `data/v2/experience_state.json` | 🟡 Partiel | Compléter |
| `data/v2/feedback_log.json` | 🟡 Partiel | Compléter |
| `data/v2/learning_state.json` | 🟡 Partiel | Compléter |
| `data/v2/robustness_results.json` | 🟡 Partiel | Compléter |
| `data/v3/behavior_state.json` | 🟡 Partiel | Compléter |
| `data/v3/context_memories.json` | 🟡 Partiel | Compléter |
| `data/v3/conversation_state.json` | 🟡 Partiel | Compléter |
| `data/v3/feedback_log_v3.json` | 🟡 Partiel | Compléter |
| `data/v3/fusion_results.json` | 🟡 Partiel | Compléter |
| *... 8 autres* | | |

### 🟡 B19 — Infrastructure & extensions `60.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 10 |
| Structurels | 5 |
| Manquants | 0 |

> 🟪 Roadmap V2 — Providers domotiques confirmés : Google Home + Tuya (tinytuya). Intégration à brancher sur src/v4/ lors de l'implémentation B14.

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v4/action_rules.json` | 🟡 Partiel | Compléter |
| `config/v4/home_devices.json` | 🟡 Partiel | Compléter |
| `config/v4/orchestration_rules.json` | 🟡 Partiel | Compléter |
| `config/v4/scenario_rules.json` | 🟡 Partiel | Compléter |
| `config/v4/trigger_rules.json` | 🟡 Partiel | Compléter |
| `data/v4/action_log.json` | 🟡 Partiel | Compléter |
| `data/v4/device_registry.json` | 🟡 Partiel | Compléter |
| `data/v4/home_state.json` | 🟡 Partiel | Compléter |
| `data/v4/sensor_state.json` | 🟡 Partiel | Compléter |
| `data/v4/trigger_log.json` | 🟡 Partiel | Compléter |

### 🟢 B20 — Cybersécurité, Zero Trust & conformité `92.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 39 |
| Testés | 0 |
| Codés (à tester) | 5 |
| Partiels | 3 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v3/safety_rules.json` | 🟡 Partiel | Compléter |
| `data/security/access_decisions_history.json` | 🟡 Partiel | Compléter |
| `data/security/trusted_devices_runtime.json` | 🟡 Partiel | Compléter |
| `config/safety_rules.json` | 🟦 Codé — à tester | Tester |
| `config/security/audit_retention_policy.json` | 🟦 Codé — à tester | Tester |
| `config/security/trusted_devices.json` | 🟦 Codé — à tester | Tester |
| `data/security/incident_register.json` | 🟦 Codé — à tester | Tester |
| `logs/security/security.log` | 🟦 Codé — à tester | Tester |

### ✅ B21 — ALFRED WEB PLATFORM `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 45 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### 🟡 B22 — Accessibility & Cognitive Assistance `71.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 15 |
| Partiels | 0 |
| Structurels | 5 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `docs/accessibility/ALFRED_Accessibility_Policy.pdf` | 🟦 Codé — à tester | Tester |
| `src/accessibility/accessibility_manager.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/wcag_checker.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/audio/text_reader.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/audio/voice_output_manager.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/cognitive/summarizer.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/cognitive/explain_terms.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/cognitive/fatigue_reducer.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/cognitive/neurodiversity.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/translation/translator.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/ui/visual_adapter.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/ui/android_a11y.py` | 🟦 Codé — à tester | Tester |
| `src/accessibility/ui/web_a11y.py` | 🟦 Codé — à tester | Tester |
| `tests/b15_tests/test_b22_accessibility.py` | 🟦 Codé — à tester | Tester |
| `tests/b15_tests/test_voice_output_manager.py` | 🟦 Codé — à tester | Tester |

## 🟦 Sprint — Fichiers codés à tester (134)

Ces fichiers sont implémentés mais n'ont pas encore de tests.

**B01**
- `config/conversation_rules.json`
- `data/memory/episodic/dialogue_history.json`
- `src/conversation/input/audio_capture.py`
- `src/conversation/input/audio_listener.py`
- `src/conversation/input/speech_manager.py`
- `src/conversation/input/text_input.py`
- `src/conversation/nlp/intent_classifier.py`
- `src/conversation/nlp/nlp_engine_v2.py`
- `src/conversation/output/tts_output.py`
- `src/core/response_generator.py`
- `src/llm/llm_client_ollama.py`
- `src/v2/confidence/confidence_scorer.py`
- `src/v2/decision/decision_engine.py`
- `src/v2/fusion/fusion_engine.py`
- `tests/b01_tests/test_fusion_engine.py`
- `tests/integration_tests/test_v2_pipeline.py`
- `tests/test_b01_speech.py`
- `tests/test_pipeline_llm.py`
**B02**
- `data/user_memory.json`
- `src/memory/episodic_memory.py`
- `src/memory/long_term_memory.py`
- `src/memory/memory_indexer.py`
- `src/memory/rag_stub.py`
- `src/rag/rag_engine.py`
**B03**
- `tests/test_b02_b03.py`
**B05**
- `config/personality_core.json`
- `config/user_adaptation_profile.json`
- `data/personality/instances/personality_core_instance.json`
- `data/personality/templates/personality_core.json`
- `data/personality/templates/personality_core_template_public.json`
- `data/preferences_profile.json`
- `data/profile/user_profile.json`
- `data/users/instances/user_celine_instance.json`
- `data/users/templates/user_adaptation_profile.json`
- `data/users/templates/user_profile_template_public.json`
- `knowledges/core/behavioral_modes.json`
- `knowledges/core/context_awareness.json`
- `knowledges/core/personalization_engine.json`
- `knowledges/core/system_rules.json`
- `knowledges/core/user_adaptation.json`
- `knowledges/human/self_alignment/routines/feedback_loop.json`
- `src/core/alfred_behavior_engine.py`
**B08**
- `.env.example`
- `.gitignore`
- `config/ethics_rules.json`
- `config/settings.json`
- `knowledges/system/ethics/ethical_framework.json`
- `pyproject.toml`
**B12**
- `src/collaboration/project/project_manager.py`
- `src/collaboration/project/project_store.py`
- `src/start_alfred_cpl.bat`
- `src/start_alfred_hybride.bat`
**B13**
- `src/health/chronic_support.py`
- `src/health/health_profile.py`
- `src/health/interaction_adapter.py`
- `src/health/onboarding.py`
- `src/health/profile_loader.py`
**B15**
- `assets/avatars/avatar_medium/base_medium/alfred_medium_confused.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_cybersecurity.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_excited.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_explaining.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_happy.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_idea.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_listening.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_love.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_a.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_a.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_e.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_e.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_i.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_i.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_m.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_m.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_o.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_o.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_u.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_u.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_thinking.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_thinking_full.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_very_excited.png`
- `assets/avatars/avatar_medium/base_medium/alfred_medium_working.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_closed.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_half.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_open.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_idle_eyes_closed.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_idle_eyes_half.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_closed.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_half.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_open.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_closed.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_half.png.png`
- `assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_open.png.png`
- `assets/models/tts/fr_FR/MODEL_CARD`
- `assets/models/tts/fr_FR/fr_FR-mls_1840-low.onnx`
- `assets/models/tts/fr_FR/fr_FR-mls_1840-low.onnx.json`
- `assets/models/tts/fr_FR/fr_FR-upmc-medium.onnx`
- `assets/models/tts/fr_FR/fr_FR-upmc-medium.onnx.json`
- `assets/voices/fr_FR-upmc-medium.onnx`
- `assets/voices/fr_FR-upmc-medium.onnx.json`
- `src/ui/alfred_app.py`
**B16**
- `tests/test_pipeline.py`
**B17**
- `assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_debut_journee.png`
- `assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_fin_journee.png`
- `assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_nuit.png`
- `assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_debut fin journee.jpg`
- `assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_matinee.jpg`
- `assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_soiree.jpg`
- `assets/backgrounds/mode_portrait/interieur/bureau/open_office/background_paysage_interieur_bureau_open_office.png`
- `assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_debut_journee.png`
- `assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_fin_journee.png`
- `assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_nuit.jpg`
- `assets/backgrounds/mode_portrait/interieur/specifique/sport/background_portrait_interieur_sport.png`
- `assets/backgrounds/mode_portrait/orientation portrait/specifique/Transport/background_portrait_exterieur_transport_debut fin journee.jpg`
**B20**
- `config/safety_rules.json`
- `config/security/audit_retention_policy.json`
- `config/security/trusted_devices.json`
- `data/security/incident_register.json`
- `logs/security/security.log`
**B22**
- `docs/accessibility/ALFRED_Accessibility_Policy.pdf`
- `src/accessibility/accessibility_manager.py`
- `src/accessibility/audio/text_reader.py`
- `src/accessibility/audio/voice_output_manager.py`
- `src/accessibility/cognitive/explain_terms.py`
- `src/accessibility/cognitive/fatigue_reducer.py`
- `src/accessibility/cognitive/neurodiversity.py`
- `src/accessibility/cognitive/summarizer.py`
- `src/accessibility/translation/translator.py`
- `src/accessibility/ui/android_a11y.py`
- `src/accessibility/ui/visual_adapter.py`
- `src/accessibility/ui/web_a11y.py`
- `src/accessibility/wcag_checker.py`
- `tests/b15_tests/test_b22_accessibility.py`
- `tests/b15_tests/test_voice_output_manager.py`
