# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS

> Généré le 18/06/2026 15:46 depuis `dashboard_data.json` (mis à jour le 15/06/2026 13:29:58)
> Progression technique : **67.2%** · Full projet : **48.7%**
> 729 fichiers détectés / 1068 cible full

## Synthèse globale

| Statut | Nb | % | Priorité |
|--------|---:|--:|----------|
| 🟡 Partiel | 190 | 26.1% | 🟡 Sprint |
| 🟦 Codé — à tester | 238 | 32.6% | 🟡 Sprint |
| 🧪 Testé — à valider | 3 | 0.4% | 🧪 Tests |
| ✅ Validé ✅ | 244 | 33.5% | ✅ Done |
| ⚙️ Structurel | 54 | 7.4% | ✅ Done |

## Backlog par bloc

### 🟡 B01 — Interaction conversationnelle intelligente `70.6%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 1 |
| Codés (à tester) | 19 |
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
| `src/conversation/input/context_builder.py` | 🟦 Codé — à tester | Tester |
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

### 🟡 B02 — Mémoire & RAG `69.6%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 0 |
| Codés (à tester) | 13 |
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
| `knowledges/professional/engineering/ai/semantic_memory.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/memory/episodic_memory.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/memory/memory_context_linking.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/memory/memory_decay_rules.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/memory/memory_learning_rules.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/memory/memory_prioritization.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/memory/memory_system.json` | 🟦 Codé — à tester | Tester |
| `src/memory/episodic_memory.py` | 🟦 Codé — à tester | Tester |
| `src/memory/long_term_memory.py` | 🟦 Codé — à tester | Tester |
| `src/memory/memory_indexer.py` | 🟦 Codé — à tester | Tester |
| `src/memory/rag_stub.py` | 🟦 Codé — à tester | Tester |
| `src/rag/rag_engine.py` | 🟦 Codé — à tester | Tester |

### 🟡 B03 — Émotions & Régulation `76.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 11 |
| Testés | 0 |
| Codés (à tester) | 8 |
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
| `knowledges/cpl/human_communication/emotional_intelligence.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/cognition/decision_fatigue.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/emotional_intelligence/active_listening.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/emotional_intelligence/emotional_management.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/emotional_intelligence/emotional_patterns.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/psychology/burnout_prevention.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/psychology/resilience.json` | 🟦 Codé — à tester | Tester |
| `tests/test_b02_b03.py` | 🟦 Codé — à tester | Tester |

### 🟡 B04 — Sécurité & Protection `64.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 1 |
| Testés | 0 |
| Codés (à tester) | 9 |
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
| `knowledges/cpl/ethics_governance/accessibility_principles.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/ethics_governance/ethical_ai_framework.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/ethics_governance/governance_model.json` | 🟦 Codé — à tester | Tester |
| `knowledges/system/ethics/ethical_framework.json` | 🟦 Codé — à tester | Tester |
| `pyproject.toml` | 🟦 Codé — à tester | Tester |

### 🟡 B05 — Organisation & Assistance `74.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 5 |
| Testés | 0 |
| Codés (à tester) | 6 |
| Partiels | 2 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/actions/tasks.json` | 🟡 Partiel | Compléter |
| `data/v2/scenarios/daily_organization.json` | 🟡 Partiel | Compléter |
| `knowledges/cpl/execution/decision_making_framework.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/execution/project_management_core.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/execution/risk_management.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/execution/task_prioritization.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/human_organization/energy_management.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/organization.json` | 🟦 Codé — à tester | Tester |

### 🟡 B06 — Communication & Lien social `64.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 1 |
| Testés | 0 |
| Codés (à tester) | 8 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `knowledges/cpl/human_communication/client_interaction.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/human_communication/communication_principles.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/argumentation_frameworks.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/assertiveness.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/communication_clarity.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/conflict_management.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/leadership_personal.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/negotiation.json` | 🟦 Codé — à tester | Tester |

### 🟠 B07 — Mobilité & Contexte externe `40.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 1 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/context/user_context.json` | 🟡 Partiel | Compléter |

### 🟡 B08 — Personnalisation utilisateur `68.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 0 |
| Codés (à tester) | 17 |
| Partiels | 3 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/personality.json` | 🟡 Partiel | Compléter |
| `data/preferences_profile.json` | 🟡 Partiel | Compléter |
| `data/profile/user_profile.json` | 🟡 Partiel | Compléter |
| `config/personality_core.json` | 🟦 Codé — à tester | Tester |
| `config/user_adaptation_profile.json` | 🟦 Codé — à tester | Tester |
| `data/personality/instances/personality_core_instance.json` | 🟦 Codé — à tester | Tester |
| `data/personality/templates/personality_core.json` | 🟦 Codé — à tester | Tester |
| `data/personality/templates/personality_core_template_public.json` | 🟦 Codé — à tester | Tester |
| `data/users/instances/user_celine_instance.json` | 🟦 Codé — à tester | Tester |
| `data/users/templates/user_adaptation_profile.json` | 🟦 Codé — à tester | Tester |
| `data/users/templates/user_profile_template_public.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/behavioral_modes.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/context_awareness.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/personalization_engine.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/system_rules.json` | 🟦 Codé — à tester | Tester |
| `knowledges/core/user_adaptation.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/self_alignment/habits/discipline.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/self_alignment/routines/feedback_loop.json` | 🟦 Codé — à tester | Tester |
| `src/core/alfred_behavior_engine.py` | 🟦 Codé — à tester | Tester |
| `src/core/personality_adapter.py` | 🟦 Codé — à tester | Tester |

### 🟡 B09 — Productivité & Copilote pro `75.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 5 |
| Testés | 0 |
| Codés (à tester) | 8 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `knowledges/cpl/product_ia/product_design_methodology.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/product_ia/tech_tradeoff_framework.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/product_ia/user_needs_analysis.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/skills/softskills/problem_solving.json` | 🟦 Codé — à tester | Tester |
| `knowledges/professional/decision/decision_models.json` | 🟦 Codé — à tester | Tester |
| `knowledges/professional/decision/decision_support.json` | 🟦 Codé — à tester | Tester |
| `knowledges/professional/decision/root_cause_analysis.json` | 🟦 Codé — à tester | Tester |
| `knowledges/professional/decision/tradeoff_analysis.json` | 🟦 Codé — à tester | Tester |

### ❌ B10 — Collaboration & Coordination `0.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### 🟢 B11 — Intelligence cognitive avancée `82.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 9 |
| Testés | 0 |
| Codés (à tester) | 7 |
| Partiels | 1 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `src/knowledge/knowledge_router.py` | 🟡 Partiel | Compléter |
| `knowledges/human/cognition/cognitive_load.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/cognition/critical_thinking.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/cognition/focus_management.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/cognition/multi_step_reasoning.json` | 🟦 Codé — à tester | Tester |
| `knowledges/human/cognition/uncertainty_management.json` | 🟦 Codé — à tester | Tester |
| `knowledges/professional/engineering/ai/reasoning_advanced.json` | 🟦 Codé — à tester | Tester |
| `knowledges/professional/engineering/ai/reasoning_engine.json` | 🟦 Codé — à tester | Tester |

### 🟡 B12 — Pilotage business & Stratégie `73.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 7 |
| Testés | 0 |
| Codés (à tester) | 6 |
| Partiels | 3 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/kpi_config.json` | 🟡 Partiel | Compléter |
| `config/v2/product_roadmap.json` | 🟡 Partiel | Compléter |
| `data/v2/product_state.json` | 🟡 Partiel | Compléter |
| `knowledges/cpl/business_piloting/pricing_strategy.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/business_piloting/profitability_analysis.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/business_piloting/revenue_mix_strategy.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/strategy/business_model_design.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/strategy/strategy_fundamentals.json` | 🟦 Codé — à tester | Tester |
| `knowledges/cpl/strategy/value_proposition_framework.json` | 🟦 Codé — à tester | Tester |

### 🟡 B13 — Compagnon pédiatrique / ARTHUR `66.7%`

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

### ✅ B14 — IoT & Intégrations `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

### 🟡 B15 — Présence visuelle & Avatar `66.5%`

| KPI | Valeur |
|-----|--------|
| Validés | 8 |
| Testés | 0 |
| Codés (à tester) | 45 |
| Partiels | 1 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `assets/models/tts/fr_FR/ALIASES` | 🟡 Partiel | Compléter |
| `src/ui/alfred_app.py` | 🟦 Codé — à tester | Tester |
| `src/ui/device_settings.py` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_open.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_open.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_closed.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_half.png.png` | 🟦 Codé — à tester | Tester |
| `assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_open.png.png` | 🟦 Codé — à tester | Tester |
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
| *... 16 autres* | | |

### 🟠 B16 — Démonstration & Scénarisation `43.3%`

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

### 🟢 B17 — Visual Generation contextuelle `94.3%`

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

### 🟡 B18 — Knowledge & Intelligence System `62.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 65 |
| Testés | 1 |
| Codés (à tester) | 20 |
| Partiels | 147 |
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
| *... 137 autres* | | |

### 🟡 B19 — Domotique Intelligente `60.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 10 |
| Structurels | 5 |
| Manquants | 0 |

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

### 🟢 B20 — Cybersécurité Zero Trust `92.2%`

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

### 🟡 B21 — ALFRED Web Platform `63.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 3 |
| Testés | 1 |
| Codés (à tester) | 34 |
| Partiels | 1 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `ALFRED_WEB/babel.cfg` | 🟡 Partiel | Compléter |
| `ALFRED_WEB/requirements.txt` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/README.md` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/static/css/style.css` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/base.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/index.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/projet.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/apprentissages.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/travaux.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/hardware.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/setup_bureau.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/pentest_demo.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/security_report.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/dashboard_security.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/dashboard_tests.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/smsi_dashboard.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/cpl.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/rse.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/articles.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/articles_categorie.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/article_perte_donnees.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/article_ia_accessibilite_zero_trust.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/article_teletravail_flexible_sante_agefiph.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/article_carriere_grc_flexibilite_facteur_humain.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/article_accessibilite_fr_en_lecture_vocale.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/doc_stub.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/profil.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/mentions_legales.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/contact.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/error.html` | 🟦 Codé — à tester | Tester |
| *... 5 autres* | | |

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

## 🟦 Sprint — Fichiers codés à tester (238)

Ces fichiers sont implémentés mais n'ont pas encore de tests.

**B01**
- `config/conversation_rules.json`
- `data/memory/episodic/dialogue_history.json`
- `src/conversation/input/audio_capture.py`
- `src/conversation/input/audio_listener.py`
- `src/conversation/input/context_builder.py`
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
- `knowledges/professional/engineering/ai/semantic_memory.json`
- `knowledges/system/memory/episodic_memory.json`
- `knowledges/system/memory/memory_context_linking.json`
- `knowledges/system/memory/memory_decay_rules.json`
- `knowledges/system/memory/memory_learning_rules.json`
- `knowledges/system/memory/memory_prioritization.json`
- `knowledges/system/memory/memory_system.json`
- `src/memory/episodic_memory.py`
- `src/memory/long_term_memory.py`
- `src/memory/memory_indexer.py`
- `src/memory/rag_stub.py`
- `src/rag/rag_engine.py`
**B03**
- `knowledges/cpl/human_communication/emotional_intelligence.json`
- `knowledges/human/cognition/decision_fatigue.json`
- `knowledges/human/emotional_intelligence/active_listening.json`
- `knowledges/human/emotional_intelligence/emotional_management.json`
- `knowledges/human/emotional_intelligence/emotional_patterns.json`
- `knowledges/human/psychology/burnout_prevention.json`
- `knowledges/human/psychology/resilience.json`
- `tests/test_b02_b03.py`
**B04**
- `.env.example`
- `.gitignore`
- `config/ethics_rules.json`
- `config/settings.json`
- `knowledges/cpl/ethics_governance/accessibility_principles.json`
- `knowledges/cpl/ethics_governance/ethical_ai_framework.json`
- `knowledges/cpl/ethics_governance/governance_model.json`
- `knowledges/system/ethics/ethical_framework.json`
- `pyproject.toml`
**B05**
- `knowledges/cpl/execution/decision_making_framework.json`
- `knowledges/cpl/execution/project_management_core.json`
- `knowledges/cpl/execution/risk_management.json`
- `knowledges/cpl/execution/task_prioritization.json`
- `knowledges/cpl/human_organization/energy_management.json`
- `knowledges/human/skills/softskills/organization.json`
**B06**
- `knowledges/cpl/human_communication/client_interaction.json`
- `knowledges/cpl/human_communication/communication_principles.json`
- `knowledges/human/skills/softskills/argumentation_frameworks.json`
- `knowledges/human/skills/softskills/assertiveness.json`
- `knowledges/human/skills/softskills/communication_clarity.json`
- `knowledges/human/skills/softskills/conflict_management.json`
- `knowledges/human/skills/softskills/leadership_personal.json`
- `knowledges/human/skills/softskills/negotiation.json`
**B08**
- `config/personality_core.json`
- `config/user_adaptation_profile.json`
- `data/personality/instances/personality_core_instance.json`
- `data/personality/templates/personality_core.json`
- `data/personality/templates/personality_core_template_public.json`
- `data/users/instances/user_celine_instance.json`
- `data/users/templates/user_adaptation_profile.json`
- `data/users/templates/user_profile_template_public.json`
- `knowledges/core/behavioral_modes.json`
- `knowledges/core/context_awareness.json`
- `knowledges/core/personalization_engine.json`
- `knowledges/core/system_rules.json`
- `knowledges/core/user_adaptation.json`
- `knowledges/human/self_alignment/habits/discipline.json`
- `knowledges/human/self_alignment/routines/feedback_loop.json`
- `src/core/alfred_behavior_engine.py`
- `src/core/personality_adapter.py`
**B09**
- `knowledges/cpl/product_ia/product_design_methodology.json`
- `knowledges/cpl/product_ia/tech_tradeoff_framework.json`
- `knowledges/cpl/product_ia/user_needs_analysis.json`
- `knowledges/human/skills/softskills/problem_solving.json`
- `knowledges/professional/decision/decision_models.json`
- `knowledges/professional/decision/decision_support.json`
- `knowledges/professional/decision/root_cause_analysis.json`
- `knowledges/professional/decision/tradeoff_analysis.json`
**B11**
- `knowledges/human/cognition/cognitive_load.json`
- `knowledges/human/cognition/critical_thinking.json`
- `knowledges/human/cognition/focus_management.json`
- `knowledges/human/cognition/multi_step_reasoning.json`
- `knowledges/human/cognition/uncertainty_management.json`
- `knowledges/professional/engineering/ai/reasoning_advanced.json`
- `knowledges/professional/engineering/ai/reasoning_engine.json`
**B12**
- `knowledges/cpl/business_piloting/pricing_strategy.json`
- `knowledges/cpl/business_piloting/profitability_analysis.json`
- `knowledges/cpl/business_piloting/revenue_mix_strategy.json`
- `knowledges/cpl/strategy/business_model_design.json`
- `knowledges/cpl/strategy/strategy_fundamentals.json`
- `knowledges/cpl/strategy/value_proposition_framework.json`
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
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_closed.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_half.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_open.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_closed.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_half.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_closed.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_half.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_open.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_closed.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_half.png.png`
- `assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_open.png.png`
- `assets/models/tts/fr_FR/MODEL_CARD`
- `assets/models/tts/fr_FR/fr_FR-mls_1840-low.onnx`
- `assets/models/tts/fr_FR/fr_FR-mls_1840-low.onnx.json`
- `assets/models/tts/fr_FR/fr_FR-upmc-medium.onnx`
- `assets/models/tts/fr_FR/fr_FR-upmc-medium.onnx.json`
- `assets/voices/fr_FR-upmc-medium.onnx`
- `assets/voices/fr_FR-upmc-medium.onnx.json`
- `src/ui/alfred_app.py`
- `src/ui/device_settings.py`
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
**B18**
- `.env`
- `README.md`
- `config/alfred_project.json`
- `config/router_rules.json`
- `config/v2/module_mapping.json`
- `knowledges/culture/universes/dc/alfred_pennyworth.json`
- `knowledges/culture/universes/dc/batman.json`
- `knowledges/culture/universes/dc/joker.json`
- `knowledges/culture/universes/marvel/jarvis.json`
- `knowledges/human/psychology/behavioral_patterns.json`
- `knowledges/human/psychology/motivation.json`
- `knowledges/human/skills/softskills/adaptability.json`
- `knowledges/human/skills/softskills/creativity.json`
- `knowledges/index/knowledge_registry.json`
- `knowledges/manifest.json`
- `knowledges/taxonomy.json`
- `paths.py`
- `requirements.txt`
- `scripts/clean_project.ps1`
- `tests/test_b18_knowledge.py`
**B20**
- `config/safety_rules.json`
- `config/security/audit_retention_policy.json`
- `config/security/trusted_devices.json`
- `data/security/incident_register.json`
- `logs/security/security.log`
**B21**
- `ALFRED_WEB/README.md`
- `ALFRED_WEB/requirements.txt`
- `ALFRED_WEB/static/css/style.css`
- `ALFRED_WEB/templates/_article_comments.html`
- `ALFRED_WEB/templates/_construction.html`
- `ALFRED_WEB/templates/_footer.html`
- `ALFRED_WEB/templates/_navbar.html`
- `ALFRED_WEB/templates/_template_article.html`
- `ALFRED_WEB/templates/apprentissages.html`
- `ALFRED_WEB/templates/article_accessibilite_fr_en_lecture_vocale.html`
- `ALFRED_WEB/templates/article_carriere_grc_flexibilite_facteur_humain.html`
- `ALFRED_WEB/templates/article_ia_accessibilite_zero_trust.html`
- `ALFRED_WEB/templates/article_perte_donnees.html`
- `ALFRED_WEB/templates/article_teletravail_flexible_sante_agefiph.html`
- `ALFRED_WEB/templates/articles.html`
- `ALFRED_WEB/templates/articles_categorie.html`
- `ALFRED_WEB/templates/base.html`
- `ALFRED_WEB/templates/contact.html`
- `ALFRED_WEB/templates/cpl.html`
- `ALFRED_WEB/templates/dashboard_security.html`
- `ALFRED_WEB/templates/dashboard_tests.html`
- `ALFRED_WEB/templates/doc_stub.html`
- `ALFRED_WEB/templates/error.html`
- `ALFRED_WEB/templates/hardware.html`
- `ALFRED_WEB/templates/index.html`
- `ALFRED_WEB/templates/mentions_legales.html`
- `ALFRED_WEB/templates/pentest_demo.html`
- `ALFRED_WEB/templates/profil.html`
- `ALFRED_WEB/templates/projet.html`
- `ALFRED_WEB/templates/rse.html`
- `ALFRED_WEB/templates/security_report.html`
- `ALFRED_WEB/templates/setup_bureau.html`
- `ALFRED_WEB/templates/smsi_dashboard.html`
- `ALFRED_WEB/templates/travaux.html`
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
