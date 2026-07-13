# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS

> Généré le 13/07/2026 14:00 depuis `dashboard_data.json` (mis à jour le 12/07/2026 01:01:52)
> Progression technique : **86.8%** · Full projet : **95.7%**
> 1391 fichiers détectés / 1306 cible full

## Synthèse globale

| Statut | Nb | % | Priorité |
|--------|---:|--:|----------|
| 🟡 Partiel | 103 | 7.4% | 🟡 Sprint |
| 🟦 Codé — à tester | 86 | 6.2% | 🟡 Sprint |
| 🧪 Testé — à valider | 265 | 19.1% | 🧪 Tests |
| ✅ Validé ✅ | 812 | 58.4% | ✅ Done |
| ⚙️ Structurel | 126 | 9.1% | ✅ Done |
| 📦 Archivé | 1 | 0.1% | ✅ Done |

## Backlog par bloc

### 🟢 B01 — Interaction conversationnelle intelligente `86.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 25 |
| Testés | 29 |
| Codés (à tester) | 1 |
| Partiels | 5 |
| Structurels | 8 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/dialogue_history.json` | 🟡 Partiel | Compléter |
| `src/output/tts_engine.py` | 🟡 Partiel | Compléter |
| `src/output/tts_output.py` | 🟡 Partiel | Compléter |
| `src/output/tts_piper.py` | 🟡 Partiel | Compléter |
| `src/start_alfred.bat` | 🟡 Partiel | Compléter |
| `tests/manual/voice_loop_manual.py` | 🟦 Codé — à tester | Tester |

### 🟢 B02 — Mémoire & RAG `81.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 8 |
| Testés | 14 |
| Codés (à tester) | 0 |
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

### 🟢 B03 — Émotions & Régulation `94.8%`

| KPI | Valeur |
|-----|--------|
| Validés | 60 |
| Testés | 7 |
| Codés (à tester) | 0 |
| Partiels | 5 |
| Structurels | 13 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/emotion_profiles.json` | 🟡 Partiel | Compléter |
| `config/v3/emotion_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/tone_profiles.json` | 🟡 Partiel | Compléter |
| `data/v3/emotion_state.json` | 🟡 Partiel | Compléter |
| `data/v3/relational_state.json` | 🟡 Partiel | Compléter |

### 🟢 B04 — Sécurité & Protection `87.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 6 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

### 🟢 B05 — Organisation & Assistance `90.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 11 |
| Testés | 1 |
| Codés (à tester) | 0 |
| Partiels | 2 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/actions/tasks.json` | 🟡 Partiel | Compléter |
| `data/v2/scenarios/daily_organization.json` | 🟡 Partiel | Compléter |

### 🟢 B06 — Communication & Lien social `95.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 23 |
| Testés | 6 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### 🟡 B07 — Mobilité & Contexte externe `73.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 1 |
| Codés (à tester) | 0 |
| Partiels | 1 |
| Structurels | 1 |
| Manquants | 0 |

> 🟪 Roadmap V2 — ALFRED Android : client mobile léger connecté au core ALFRED_PC (LLM + mémoire + knowledge). Accès distant via API REST/WebSocket sécurisé + tunnel WireGuard (ER605). Auth JWT + TLS mutuel. UI conversationnelle Android (Kotlin ou Flutter à trancher).

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/context/user_context.json` | 🟡 Partiel | Compléter |

### 🟢 B08 — Personnalisation utilisateur `86.5%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 17 |
| Codés (à tester) | 0 |
| Partiels | 2 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/personality.json` | 🟡 Partiel | Compléter |
| `data/preferences_profile.json` | 🟡 Partiel | Compléter |

### 🟢 B09 — Productivité & Copilote pro `96.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 111 |
| Testés | 6 |
| Codés (à tester) | 1 |
| Partiels | 12 |
| Structurels | 22 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `scripts/backup_vscode_settings.ps1` | 🟡 Partiel | Compléter |
| `scripts/complete_dpa_openai.bat` | 🟡 Partiel | Compléter |
| `scripts/setup_minisforum_ms_s1_max.ps1` | 🟡 Partiel | Compléter |
| `scripts/check_tools.ps1` | 🟡 Partiel | Compléter |
| `scripts/complete_vlan.bat` | 🟡 Partiel | Compléter |
| `scripts/list_installed_programs.ps1` | 🟡 Partiel | Compléter |
| `scripts/ranger_projet.ps1` | 🟡 Partiel | Compléter |
| `scripts/install_cpl_workstation_tools.ps1` | 🟡 Partiel | Compléter |
| `tools/dashboard_tools/dashboard_tests/dashboard_test_server.bat` | 🟡 Partiel | Compléter |
| `tools/dashboard_tools/dashboard_security/dashboard_security_server.bat` | 🟡 Partiel | Compléter |
| `tools/dashboard_tools/dashboard_data/dashboard_data_server.bat` | 🟡 Partiel | Compléter |
| `tools/dashboard_tools/dashboard_gouvernance/dashboard_gouvernance_server.bat` | 🟡 Partiel | Compléter |
| `tools/dashboard_tools/dashboard_data/archive script/repair_manifest_paths.py` | 🟦 Codé — à tester | Tester |

### 🟡 B10 — Collaboration & Coordination `76.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 2 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 3 |
| Structurels | 0 |
| Manquants | 0 |

> 🟪 Roadmap V2 — ALFRED CPL : collaborateur professionnel interactif. Interface mode pro (brainstorming, revue docs, suivi projets), knowledges métier CPL (IA, cybersécurité, entrepreneuriat, droit numérique), co-rédaction, mémoire des décisions. Module src/collaboration/ + knowledges/professional/cpl/ à créer.

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v3/orchestrator_rules.json` | 🟡 Partiel | Compléter |
| `config/v3/workflow_rules.json` | 🟡 Partiel | Compléter |
| `src/v3/orchestrator/__init__.py` | 🟡 Partiel | Compléter |

### 🟢 B11 — Intelligence cognitive avancée `91.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 12 |
| Testés | 7 |
| Codés (à tester) | 0 |
| Partiels | 1 |
| Structurels | 3 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `src/knowledge/knowledge_router.py` | 🟡 Partiel | Compléter |

### 🟢 B12 — Pilotage business & Stratégie `96.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 48 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 3 |
| Structurels | 8 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/kpi_config.json` | 🟡 Partiel | Compléter |
| `config/v2/product_roadmap.json` | 🟡 Partiel | Compléter |
| `data/v2/product_state.json` | 🟡 Partiel | Compléter |

### 🟢 B13 — Compagnon pédiatrique / ARTHUR `83.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 5 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

### ✅ B14 — IoT & Intégrations `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

> 🟪 Roadmap V2 — Architecture IoT esquissée (src/v4/). Systèmes disponibles : Google Home + Tuya. Implémenter : tinytuya (accès local/cloud) + Google Home API, pattern Adapter (tuya_adapter.py + google_home_adapter.py).

### 🟢 B15 — Présence visuelle & Avatar `85.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 16 |
| Testés | 44 |
| Codés (à tester) | 2 |
| Partiels | 1 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `assets/models/tts/fr_FR/ALIASES` | 🟡 Partiel | Compléter |
| `src/ui/alfred_app.py` | 🟦 Codé — à tester | Tester |
| `src/ui/webcam_widget.py` | 🟦 Codé — à tester | Tester |

### 🟠 B16 — Démonstration & Scénarisation `46.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 1 |
| Codés (à tester) | 0 |
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

### 🟢 B17 — Visual Generation contextuelle `97.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 72 |
| Testés | 12 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### 🟢 B18 — Knowledge & Intelligence System `82.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 169 |
| Testés | 71 |
| Codés (à tester) | 76 |
| Partiels | 44 |
| Structurels | 32 |
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
| *... 90 autres* | | |

### 🟡 B19 — Domotique Intelligente `60.0%`

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

### 🟢 B20 — Cybersécurité Zero Trust `95.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 143 |
| Testés | 26 |
| Codés (à tester) | 5 |
| Partiels | 5 |
| Structurels | 13 |
| Manquants | 2 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v3/safety_rules.json` | 🟡 Partiel | Compléter |
| `data/security/access_decisions_history.json` | 🟡 Partiel | Compléter |
| `data/security/trusted_devices_runtime.json` | 🟡 Partiel | Compléter |
| `dashboard/ALFRED_DASHBOARD_DYNAMIC.html` | 🟡 Partiel | Compléter |
| `dashboard/dashboard_data/ALFRED_DASHBOARD_DYNAMIC.html` | 🟡 Partiel | Compléter |
| `scripts/complete_dpa_openai.py` | 🟦 Codé — à tester | Tester |
| `scripts/complete_vlan.py` | 🟦 Codé — à tester | Tester |
| `scripts/fix_avatar_alpha.py` | 🟦 Codé — à tester | Tester |
| `tools/apply_headers.py` | 🟦 Codé — à tester | Tester |
| `tools/dashboard_tools/dashboard_data/update_dashboard_data.py` | 🟦 Codé — à tester | Tester |

### 🟢 B21 — ALFRED Web Platform `99.5%`

| KPI | Valeur |
|-----|--------|
| Validés | 76 |
| Testés | 2 |
| Codés (à tester) | 1 |
| Partiels | 0 |
| Structurels | 3 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `ALFRED_WEB/scripts/i18n_cadrage.py` | 🟦 Codé — à tester | Tester |

### 🟢 B22 — Accessibility & Cognitive Assistance `90.5%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 10 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 5 |
| Manquants | 0 |

### ✅ B29 — Démonstrateur Big Data Hadoop `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 11 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

> PoC ciblé (pas une infra de production) — regard critique assumé sur le surdimensionnement à l'échelle actuelle d'ALFRED, cf. docs/hadoop_poc_bilan.md.

## 🟦 Sprint — Fichiers codés à tester (86)

Ces fichiers sont implémentés mais n'ont pas encore de tests.

**B01**
- `tests/manual/voice_loop_manual.py`
**B09**
- `tools/dashboard_tools/dashboard_data/archive script/repair_manifest_paths.py`
**B15**
- `src/ui/alfred_app.py`
- `src/ui/webcam_widget.py`
**B18**
- `knowledges/cpl/business_strategy/consulting_governance.json`
- `knowledges/cpl/business_strategy/customer_persona_business.json`
- `knowledges/cpl/business_strategy/customer_retention.json`
- `knowledges/cpl/business_strategy/delivery_quality_framework.json`
- `knowledges/cpl/business_strategy/go_to_market_advanced.json`
- `knowledges/cpl/business_strategy/innovation_portfolio_management.json`
- `knowledges/cpl/business_strategy/market_segmentation_strategy.json`
- `knowledges/cpl/business_strategy/pricing_psychology.json`
- `knowledges/cpl/business_strategy/product_service_hybrid_model.json`
- `knowledges/cpl/business_strategy/recurring_revenue_models.json`
- `knowledges/cpl/business_strategy/resource_optimization.json`
- `knowledges/cpl/business_strategy/saas_transition_strategy.json`
- `knowledges/cpl/business_strategy/service_margin_management.json`
- `knowledges/cpl/business_strategy/strategic_decision_framework.json`
- `knowledges/cpl/business_strategy/value_based_pricing.json`
- `knowledges/human/interaction/conversation_repair.json`
- `knowledges/human/interaction/decision_support_under_stress.json`
- `knowledges/human/interaction/emotion_transition_detection.json`
- `knowledges/human/interaction/frustration_management.json`
- `knowledges/human/interaction/mental_fatigue_detection.json`
- `knowledges/human/interaction/multi_turn_context_management.json`
- `knowledges/human/interaction/psychological_safety.json`
- `knowledges/human/interaction/relational_balance.json`
- `knowledges/human/interaction/silence_and_pause_management.json`
- `knowledges/human/interaction/social_energy_management.json`
- `knowledges/human/interaction/stress_response_patterns.json`
- `knowledges/human/interaction/supportive_language.json`
- `knowledges/human/wellbeing/decision_energy_conservation.json`
- `knowledges/human/wellbeing/energy_budgeting.json`
- `knowledges/human/wellbeing/executive_dysfunction.json`
- `knowledges/human/wellbeing/fatigue_patterns.json`
- `knowledges/human/wellbeing/focus_recovery_balance.json`
- `knowledges/human/wellbeing/medical_boundary_rules.json`
- `knowledges/human/wellbeing/mental_overload_patterns.json`
- `knowledges/human/wellbeing/motivation_fluctuation_patterns.json`
- `knowledges/human/wellbeing/recovery_cycles.json`
- `knowledges/human/wellbeing/recovery_management.json`
- `knowledges/human/wellbeing/sleep_hygiene_basics.json`
- `knowledges/human/wellbeing/stress_reduction_support.json`
- `knowledges/human/wellbeing/stress_signals.json`
- `knowledges/human/wellbeing/support_without_diagnosis.json`
- `knowledges/human/wellbeing/wellbeing_non_medical_support.json`
- `knowledges/professional/engineering/reasoning/contradiction_detection.json`
- `knowledges/professional/engineering/reasoning/fallback_reasoning.json`
- `knowledges/professional/engineering/reasoning/goal_alignment_reasoning.json`
- `knowledges/professional/engineering/reasoning/hallucination_detection.json`
- `knowledges/professional/engineering/reasoning/memory_reasoning_links.json`
- `knowledges/professional/engineering/reasoning/meta_reasoning_basics.json`
- `knowledges/professional/engineering/reasoning/multi_agent_reasoning.json`
- `knowledges/professional/engineering/reasoning/probabilistic_reasoning_basics.json`
- `knowledges/professional/engineering/reasoning/reasoning_failure_patterns.json`
- `knowledges/professional/engineering/reasoning/reasoning_orchestration.json`
- `knowledges/professional/engineering/reasoning/retrieval_augmented_reasoning.json`
- `knowledges/professional/engineering/reasoning/self_consistency_reasoning.json`
- `knowledges/professional/engineering/reasoning/task_decomposition_reasoning.json`
- `knowledges/professional/engineering/reasoning/tree_of_thoughts.json`
- `knowledges/professional/engineering/reasoning/uncertainty_reasoning.json`
- `knowledges/professional/governance_ai/compliance_monitoring.json`
- `knowledges/professional/governance_ai/decision_transparency.json`
- `knowledges/professional/governance_ai/eu_ai_act_basics.json`
- `knowledges/professional/governance_ai/explainability_xai.json`
- `knowledges/professional/governance_ai/gdpr_ai_intersection.json`
- `knowledges/professional/governance_ai/traceability_principles.json`
- `knowledges/professional/iot/iot_device_segmentation.json`
- `knowledges/professional/iot/iot_threat_basics.json`
- `knowledges/professional/iot/local_network_security.json`
- `knowledges/professional/iot/offline_first_home_automation.json`
- `knowledges/professional/iot/presence_detection.json`
- `knowledges/professional/iot/room_state_modeling.json`
- `knowledges/professional/iot/smart_alert_prioritization.json`
- `knowledges/professional/iot/smart_home_basics.json`
- `knowledges/professional/product_management/advanced/product_governance.json`
- `knowledges/professional/product_management/advanced/product_health_monitoring.json`
- `knowledges/professional/product_management/advanced/product_kpi_frameworks.json`
- `knowledges/professional/product_management/advanced/product_scaling_strategy.json`
- `scripts/clean_project.ps1`
**B20**
- `scripts/complete_dpa_openai.py`
- `scripts/complete_vlan.py`
- `scripts/fix_avatar_alpha.py`
- `tools/apply_headers.py`
- `tools/dashboard_tools/dashboard_data/update_dashboard_data.py`
**B21**
- `ALFRED_WEB/scripts/i18n_cadrage.py`
