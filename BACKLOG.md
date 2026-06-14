# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS

> Généré le 14/06/2026 23:48 depuis `dashboard_data.json` (mis à jour le 14/06/2026 23:47:58)
> Progression technique : **66.0%** · Full projet : **48.0%**
> 727 fichiers détectés / 1068 cible full

## Synthèse globale

| Statut | Nb | % | Priorité |
|--------|---:|--:|----------|
| ❌ A créer | 2 | 0.3% | 🔴 Urgent |
| 🟡 Partiel | 190 | 26.1% | 🟡 Sprint |
| 🟦 Codé — à tester | 247 | 34.0% | 🟡 Sprint |
| 🧪 Testé — à valider | 18 | 2.5% | 🧪 Tests |
| ✅ Validé ✅ | 218 | 30.0% | ✅ Done |
| ⚙️ Structurel | 54 | 7.4% | ✅ Done |

## Backlog par bloc

### 🟡 B01 — Interaction conversationnelle intelligente `67.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 3 |
| Testés | 4 |
| Codés (à tester) | 18 |
| Partiels | 4 |
| Structurels | 4 |
| Manquants | 1 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/memory/episodic/dialogue_history.json` | ❌ A créer | Créer |
| `data/dialogue_history.json` | 🟡 Partiel | Compléter |
| `src/output/tts_engine.py` | 🟡 Partiel | Compléter |
| `src/output/tts_output.py` | 🟡 Partiel | Compléter |
| `src/output/tts_piper.py` | 🟡 Partiel | Compléter |
| `config/conversation_rules.json` | 🟦 Codé — à tester | Tester |
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

### 🟡 B02 — Mémoire & RAG `67.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 0 |
| Codés (à tester) | 12 |
| Partiels | 4 |
| Structurels | 2 |
| Manquants | 1 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/user_memory.json` | ❌ A créer | Créer |
| `config/v3/memory_rules.json` | 🟡 Partiel | Compléter |
| `data/v2/memory_samples.json` | 🟡 Partiel | Compléter |
| `data/v3/memory_patterns.json` | 🟡 Partiel | Compléter |
| `src/memory/memory_manager.py` | 🟡 Partiel | Compléter |
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

### 🟡 B03 — Émotions & Régulation `73.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 7 |
| Testés | 4 |
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

### 🟡 B05 — Organisation & Assistance `65.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 2 |
| Testés | 0 |
| Codés (à tester) | 9 |
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
| `src/auth/auth_manager.py` | 🟦 Codé — à tester | Tester |
| `src/auth/login_handler.py` | 🟦 Codé — à tester | Tester |
| `src/auth/user_session.py` | 🟦 Codé — à tester | Tester |

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

### 🟡 B11 — Intelligence cognitive avancée `76.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 4 |
| Testés | 5 |
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
| Validés | 7 |
| Testés | 2 |
| Codés (à tester) | 44 |
| Partiels | 1 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `assets/models/tts/fr_FR/ALIASES` | 🟡 Partiel | Compléter |
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
| `assets/avatars/avatar_medium/base_medium/alfred_medium_excited.png` | 🟦 Codé — à tester | Tester |
| *... 15 autres* | | |

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

### 🟡 B18 — Knowledge & Intelligence System `62.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 63 |
| Testés | 2 |
| Codés (à tester) | 21 |
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
| *... 138 autres* | | |

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

### 🟢 B20 — Cybersécurité Zero Trust `89.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 31 |
| Testés | 0 |
| Codés (à tester) | 13 |
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
| `src/security/api_security.py` | 🟦 Codé — à tester | Tester |
| `src/security/network_security.py` | 🟦 Codé — à tester | Tester |
| `src/security/soc_monitor.py` | 🟦 Codé — à tester | Tester |
| `src/security/data_protection.py` | 🟦 Codé — à tester | Tester |
| `src/security/html_report.py` | 🟦 Codé — à tester | Tester |
| `src/security/rate_limiter.py` | 🟦 Codé — à tester | Tester |
| `src/security/security_dashboard.py` | 🟦 Codé — à tester | Tester |
| `src/security/security_governance.py` | 🟦 Codé — à tester | Tester |

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

## 🟦 Sprint — Fichiers codés à tester (247)

Ces fichiers sont implémentés mais n'ont pas encore de tests.

**B01**
- `config/conversation_rules.json`
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
- `src/auth/auth_manager.py`
- `src/auth/login_handler.py`
- `src/auth/user_session.py`
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
- `ALFRED_CONTEXT.md`
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
- `src/security/api_security.py`
- `src/security/data_protection.py`
- `src/security/html_report.py`
- `src/security/network_security.py`
- `src/security/rate_limiter.py`
- `src/security/security_dashboard.py`
- `src/security/security_governance.py`
- `src/security/soc_monitor.py`
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
## 🟪 Scaffolding Roadmap V2-V4 — config/data non connectés (audit 14/06/2026)

Les dossiers `config/v2/`, `config/v3/`, `config/v4/`, `data/v2/`, `data/v3/`,
`data/v4/` (~70 fichiers, majoritairement `{}` / `{"x": []}` / `{"x": {}}`,
y compris `config/v2/module_mapping.json` et `config/v2/decision_rules.json`
qui ont un contenu mais ne sont lus par aucun code) sont des squelettes
préparés pour les versions futures, **0 référence dans le code actuel**.

À distinguer de `src/v2/` (25 fichiers) et `src/v3/` (27 fichiers), qui eux
sont importés par `main.py` / `alfred_behavior_engine.py` / tests et doivent
être conservés tels quels.

**Action** : ne pas traiter individuellement — à revoir lors de l'audit
dédié des dossiers de versions (`src/v1`, `src/v2`, `src/v2pp`, `src/v3`,
`src/v4`).

## 🟦 B05 — Authentification non testée (audit 14/06/2026)

`src/auth/auth_manager.py`, `src/auth/login_handler.py` et
`src/auth/user_session.py` (BLOCK B05, STATUS: ACTIVE) sont la chaîne de
connexion réellement utilisée par `main.py` (`start_auto_session`), mais
étaient absents de `dashboard_data_manifest.json` (non comptés dans la
progression B05) et n'ont **aucun test dédié** — `tests/security/test_pentest_auth.py`
couvre `session_manager`/`mfa_manager` (B20), pas ces 3 fichiers.

**Fait** : ajoutés au manifest B05 (regen dashboard/BACKLOG).
**Reste à faire** : écrire des tests unitaires pour `auth_manager.py`,
`login_handler.py`, `user_session.py`.

## 🟡 B05 — data/actions/tasks.json (audit 14/06/2026)

`data/actions/tasks.json` (`{"tasks": []}`) est un placeholder de données
runtime, **0 référence dans le code actuel** — prévu pour une future
gestion de tâches/actions B05 (Organisation & Assistance), pas encore
implémentée.

## ⚪ B07 — Mobilité & Contexte externe (audit 14/06/2026)

B07 reste un bloc roadmap quasi non démarré : seul `data/context/user_context.json`
(`{"location": "home", "energy_level": "normal"}`) est suivi (1/25 cible,
1.6% "full"), utilisé par `pipeline_bridge.py`, `health/profile_loader.py`,
`regulation_engine.py` — mais aucun module dédié "mobilité" (GPS, contexte
externe, capteurs) n'existe dans `src/`.

**Action** : aucune, confirmation que B07 est un bloc V2 non démarré.

## 🟦 B01 — src/output/*.py absents du manifest (audit 14/06/2026)

`src/output/__init__.py`, `tts_engine.py`, `tts_output.py`, `tts_piper.py`
(headers BLOCK: B04, STATUS: TESTED) sont des proxies (`from
src.conversation.output.X import *`) réellement utilisés par
`speech_manager.py` et `tests/test_b01_speech.py` — fonctionnellement de la
synthèse vocale (B01), absents de `dashboard_data_manifest.json`
(même pattern que le gap B05 auth ci-dessus).

**Fait** : ajoutés au manifest B01 (regen dashboard/BACKLOG).

## 🟡 B08 — data/personality.json (audit 14/06/2026)

`data/personality.json` (`{"core": {}, "adaptation": {}}`) est un
placeholder, **0 référence dans le code actuel** — les données réelles de
personnalité sont dans `data/personality/templates/` et
`data/personality/instances/`, utilisées par `personality_adapter.py`.

## 🟢 B08 — Tests récupérés depuis la branche backup (audit 14/06/2026)

`tests/b08_tests/test_behavior_engine.py`, `test_personality_adapter.py` et
`__init__.py` existaient sur la branche `backup_b0adae0_lost_work` (commit
`f22f145`, jamais mergé dans `dev`) mais étaient absents de `dev`
(seuls des `.pyc` orphelins subsistaient dans `__pycache__`).

**Fait** : fichiers récupérés et réintégrés dans `tests/b08_tests/` —
116 tests, tous passent (`pytest tests/b08_tests/`).

## ⚪ B10 — Collaboration & Coordination (audit 14/06/2026)

B10 a 0 fichier dans le manifest et aucun code source taggué `BLOCK: B10`
n'existe dans `src/` — bloc roadmap non démarré, comme B07.

**Action** : aucune, confirmation que B10 est un bloc V2/V3 non démarré.

## 🟦 B11 — src/v3/fusion + src/v3/proactive absents du manifest (audit 14/06/2026)

7 fichiers `src/v3/fusion/{confidence_engine,contradiction_detector,
multi_signal_fusion_engine}.py` et `src/v3/proactive/{date_parser,
proactive_engine,reminder_detector,reminder_engine}.py` (BLOCK: B11,
STATUS: TESTED/STABLE) sont importés par `main.py` et couverts par
`tests/b11_tests/` mais étaient absents de `dashboard_data_manifest.json`.

**Fait** : ajoutés au manifest B11 (regen dashboard/BACKLOG) — B11 passe
de 12 à 19 fichiers (58.4% "full").

## 🟦 B13 — src/health/*.py absents du manifest, sans tests (audit 14/06/2026)

`src/health/{__init__,chronic_support,health_profile,interaction_adapter,
onboarding,profile_loader}.py` (BLOCK: B13, STATUS: ACTIVE) constituent le
module "ARTHUR" (suivi santé/bien-être, onboarding, adaptation
d'interaction), réellement utilisés par `main.py`, `regulation_engine.py`,
`core/personality_adapter.py` — mais le manifest B13 était entièrement vide
(0/25 cible).

**Fait** : ajoutés au manifest B13 (regen dashboard/BACKLOG) — B13 passe de
0% à 66.7% tech / 16.0% "full".
**Reste à faire** : ces 5 fichiers n'ont **aucun test dédié** — à prévoir
(`tests/b13_tests/`).

## 🟦 B15 — src/ui/*.py absents du manifest (audit 14/06/2026)

8 fichiers `src/ui/{alfred_app,avatar_controller,avatar_engine,
avatar_renderer,background_manager,device_settings,sound_wave,
ui_bridge}.py` (BLOCK: B15, STATUS: STABLE/TESTED/ACTIVE) sont entièrement
couverts par `tests/b15_tests/` (8 fichiers de test) mais étaient absents
de `dashboard_data_manifest.json`.

**Fait** : ajoutés au manifest B15 (regen dashboard/BACKLOG) — B15 passe de
47 à 55 fichiers (146.4% "full", déjà au-delà de la cible grâce aux assets
avatar).

## ⚪ B14/B16 — scaffolding déjà couvert (audit 14/06/2026)

`src/v4/{actions,home_state,integration,orchestrator,scenarios,security,
triggers}/__init__.py` (B14, 8 fichiers `# ALFRED module`, 0 référence sauf
`paths.py`) et `config/v2/scenario_catalog.json` /
`data/v2/scenarios/*.json` (B16, `{"scenarios": []}` / `{}`, 0 référence)
relèvent du même scaffolding roadmap V2-V4 déjà documenté ci-dessus —
à revoir lors de l'audit dédié des dossiers de versions (tâche #11).

**Action** : aucune nouvelle action, déjà couvert.

## ⚪ B17 — Visual Generation contextuelle (audit 14/06/2026)

B17 est un bloc 100% asset (backgrounds contextuels), 84/225 fichiers
cible, 94.3% tech — aucune anomalie de tracking détectée.

**Action** : aucune.

## 🟦 B18 — src/knowledge/*.py absents du manifest (audit 14/06/2026)

5 fichiers `src/knowledge/{context_merger,domain_matcher,knowledge_ranker,
knowledge_router,taxonomy_router}.py` (BLOCK: B18, STATUS: TESTED) et
`tests/test_b18_knowledge.py` (qui les importe et les teste) étaient
absents de `dashboard_data_manifest.json`.

**Fait** : ajoutés au manifest B18 (regen dashboard/BACKLOG) — B18 passe de
254 à 260 fichiers (64.2% "full").

## ⚪ B19 — Domotique Intelligente, scaffolding V4 (audit 14/06/2026)

Les 15 fichiers du manifest B19 sont exclusivement des squelettes
`config/v4/*.json`, `data/v4/*.json` et `src/v4/{actions,home_state,
orchestrator,scenarios,triggers}/__init__.py` — relève du même scaffolding
roadmap V2-V4 déjà documenté plus haut, aucun code domotique réel n'existe
encore.

**Action** : aucune nouvelle action, déjà couvert (à revoir lors de l'audit
dossiers de versions, tâche #11).

## 🟦 B22 — tests accessibilité absents du manifest (audit 14/06/2026)

`tests/b15_tests/test_b22_accessibility.py` et
`tests/b15_tests/test_voice_output_manager.py` (seuls tests existants pour
les 10 modules `src/accessibility/*`, situés par erreur dans `b15_tests/`
au lieu de `b22_tests/`) étaient absents du manifest B22 (qui prévoit
`sub_targets.tests: 5`).

**Fait** : ajoutés au manifest B22 (regen dashboard/BACKLOG) — B22 passe de
18 à 20 fichiers (40.6% "full").
**Reste à faire** : 3 tests supplémentaires restent à écrire pour atteindre
la cible `sub_targets.tests: 5`.

## 🟦 B01 — src/v2/{fusion,confidence,decision}/*.py absents du manifest (audit 14/06/2026 — audit v1-v4)

3 fichiers `src/v2/fusion/fusion_engine.py`, `src/v2/confidence/confidence_scorer.py`,
`src/v2/decision/decision_engine.py` (header `BLOCK: B01 V2`, STATUS: ACTIVE)
sont le cœur du pipeline V2 (fusion multi-sources mémoire+knowledge+LLM,
score de confiance, décision contextuelle), importés par `main.py` et
`core/alfred_behavior_engine.py`, testés par `tests/b01_tests/test_fusion_engine.py`
et `tests/integration_tests/test_v2_pipeline.py` — tous absents du manifest.

**Fait** : ajoutés au manifest B01 (regen dashboard/BACKLOG) — B01 passe de
28 à 33 fichiers (91.2% "full").

## ⚪ Audit src/v1, src/v2pp, src/v2 (placeholders), src/v3 (placeholders), src/v4 — conclusion (audit 14/06/2026)

Bilan de l'audit dédié des dossiers de versions :
- `src/v1/__init__.py`, `src/v2pp/__init__.py` : marqueurs de package vides,
  déjà trackés dans le manifest (B18), aucune anomalie.
- `src/v2/{experience,fallback,governance,knowledge,learning,product,
  scenarios}/__init__.py`, `src/v3/{conversation,emotion,learning,memory,
  orchestrator,safety}/__init__.py` et `src/v4/{actions,home_state,
  integration,orchestrator,scenarios,security,triggers}/__init__.py` :
  tous des placeholders `# ALFRED module` déjà trackés dans le manifest
  (B18/B19), 0 référence — scaffolding roadmap confirmé, cohérent avec la
  note "Scaffolding Roadmap V2-V4" ci-dessus.
- `src/v2/fusion/fusion_engine.py`, `src/v2/confidence/confidence_scorer.py`,
  `src/v2/decision/decision_engine.py` : code réel B01 V2, gap corrigé
  ci-dessus.
- `src/v3/fusion/*` et `src/v3/proactive/*` : code réel B11, gap déjà
  corrigé lors de l'audit B10-B13.

**Conclusion** : aucun nouveau gap restant dans `src/v1`, `src/v2`,
`src/v2pp`, `src/v3`, `src/v4` — tous les fichiers de code réel sont
maintenant trackés dans le manifest.

## 🟦 B21 — ALFRED_WEB sous-évalué dans le manifest (audit 14/06/2026)

Le manifest `dashboard_data_manifest.json` ne suivait que 10 fichiers pour
B21 (cible 30, soit 22.7% "full"), alors que `docs/BACKLOG.md` d'ALFRED_WEB
indique le bloc **LIVRÉ et déployé en production** (cognitive-products-lab.fr)
depuis le 25/05/2026.

Audit du dépôt `ALFRED_WEB` (séparé, branche `main`, propre) :
- **Cœur Flask (5)** : `app.py`, `tts_engine.py`, `requirements.txt`,
  `README.md`, `babel.cfg`.
- **Templates Jinja2 (33)** : 19 templates rendus directement via
  `render_template()` (pages vitrine, dashboards, 8 articles, doc_stub,
  profil, mentions légales, contact, error, pentest_demo, security_report,
  smsi_dashboard, cpl, rse...) + `base.html` (layout) + 5 partials inclus
  (`_navbar.html`, `_footer.html`, `_article_comments.html`,
  `_construction.html`, `_template_article.html`).
- **Assets (1)** : `static/css/style.css` (les autres assets `static/`
  sont des binaires — images, fonts, PDF — non comptés, par cohérence avec
  les autres blocs).
- **Déploiement** : `Procfile`/`render.yaml` existent mais ne sont pas du
  code applicatif — sous-target `deployment_ci` ramené à 0.

**Fait** : `expected_files` B21 passe de 10 à 39 fichiers,
`target_full_files_count` 30→39, `sub_targets` ajustés
(`flask_core=5`, `templates_html=33`, `static_assets=1`,
`deployment_ci=0`). Le "full" B21 passe de 22.7% à 63.1% (39/39 fichiers
détectés, le tech 63.1% restant lié aux headers/STATUS internes
d'ALFRED_WEB non audités ici — hors périmètre ALFRED_PC).
