# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS

> Généré le 06/07/2026 14:20 depuis `dashboard_data.json` (mis à jour le 06/07/2026 14:16:56)
> Progression technique : **85.3%** · Full projet : **92.1%**
> 1362 fichiers détectés / 1277 cible full

## Synthèse globale

| Statut | Nb | % | Priorité |
|--------|---:|--:|----------|
| 🟡 Partiel | 103 | 7.6% | 🟡 Sprint |
| 🟦 Codé — à tester | 249 | 18.3% | 🟡 Sprint |
| 🧪 Testé — à valider | 172 | 12.6% | 🧪 Tests |
| ✅ Validé ✅ | 716 | 52.6% | ✅ Done |
| ⚙️ Structurel | 121 | 8.9% | ✅ Done |
| 📦 Archivé | 1 | 0.1% | ✅ Done |

## Backlog par bloc

### 🟢 B01 — Interaction conversationnelle intelligente `86.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 23 |
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

### 🟢 B08 — Personnalisation utilisateur `85.9%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 16 |
| Codés (à tester) | 1 |
| Partiels | 2 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/personality.json` | 🟡 Partiel | Compléter |
| `data/preferences_profile.json` | 🟡 Partiel | Compléter |
| `src/profile/profile_analyzer.py` | 🟦 Codé — à tester | Tester |

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

### 🟡 B18 — Knowledge & Intelligence System `78.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 167 |
| Testés | 0 |
| Codés (à tester) | 149 |
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
| *... 163 autres* | | |

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

### 🟢 B20 — Cybersécurité Zero Trust `80.6%`

| KPI | Valeur |
|-----|--------|
| Validés | 75 |
| Testés | 6 |
| Codés (à tester) | 93 |
| Partiels | 5 |
| Structurels | 13 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v3/safety_rules.json` | 🟡 Partiel | Compléter |
| `data/security/access_decisions_history.json` | 🟡 Partiel | Compléter |
| `data/security/trusted_devices_runtime.json` | 🟡 Partiel | Compléter |
| `dashboard/ALFRED_DASHBOARD_DYNAMIC.html` | 🟡 Partiel | Compléter |
| `dashboard/dashboard_data/ALFRED_DASHBOARD_DYNAMIC.html` | 🟡 Partiel | Compléter |
| `config/safety_rules.json` | 🟦 Codé — à tester | Tester |
| `config/security/audit_retention_policy.json` | 🟦 Codé — à tester | Tester |
| `config/security/trusted_devices.json` | 🟦 Codé — à tester | Tester |
| `data/security/incident_register.json` | 🟦 Codé — à tester | Tester |
| `logs/security/security.log` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_gouvernance/dashboard_gouvernance.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_gouvernance/dashboard_gouvernance_dynamique.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_gouvernance/index.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_gouvernance/norm.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_security/dashboard_security.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_security/dashboard_security_dynamique.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_tests/dashboard_tests.html` | 🟦 Codé — à tester | Tester |
| `dashboard/dashboard_tests/dashboard_tests_dynamique.html` | 🟦 Codé — à tester | Tester |
| `scripts/alfred_dashboard.html` | 🟦 Codé — à tester | Tester |
| `scripts/complete_dpa_openai.py` | 🟦 Codé — à tester | Tester |
| `scripts/complete_vlan.py` | 🟦 Codé — à tester | Tester |
| `scripts/fix_avatar_alpha.py` | 🟦 Codé — à tester | Tester |
| `src/security/consent_art9.py` | 🟦 Codé — à tester | Tester |
| `templates/html_dashboard_template.html` | 🟦 Codé — à tester | Tester |
| `tests/dashboard_tests/test_dashboard_gouvernance.py` | 🟦 Codé — à tester | Tester |
| `tests/dashboard_tests/test_dashboard_pipeline.py` | 🟦 Codé — à tester | Tester |
| `tests/security/test_pentest_auth.py` | 🟦 Codé — à tester | Tester |
| `tests/security/test_pentest_encryption.py` | 🟦 Codé — à tester | Tester |
| `tests/security/test_pentest_input.py` | 🟦 Codé — à tester | Tester |
| *... 68 autres* | | |

### 🟢 B21 — ALFRED Web Platform `99.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 63 |
| Testés | 2 |
| Codés (à tester) | 1 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `ALFRED_WEB/scripts/i18n_cadrage.py` | 🟦 Codé — à tester | Tester |

### 🟢 B22 — Accessibility & Cognitive Assistance `89.5%`

| KPI | Valeur |
|-----|--------|
| Validés | 6 |
| Testés | 9 |
| Codés (à tester) | 1 |
| Partiels | 0 |
| Structurels | 5 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `src/accessibility/wcag_checker.py` | 🟦 Codé — à tester | Tester |

## 🟦 Sprint — Fichiers codés à tester (249)

Ces fichiers sont implémentés mais n'ont pas encore de tests.

**B01**
- `tests/manual/voice_loop_manual.py`
**B08**
- `src/profile/profile_analyzer.py`
**B09**
- `tools/dashboard_tools/dashboard_data/archive script/repair_manifest_paths.py`
**B15**
- `src/ui/alfred_app.py`
- `src/ui/webcam_widget.py`
**B18**
- `.env`
- `README.md`
- `config/alfred_project.json`
- `config/router_rules.json`
- `config/v2/module_mapping.json`
- `knowledges/architecture/architectural_styles.json`
- `knowledges/architecture/architecture_history.json`
- `knowledges/architecture/interior_design_basics.json`
- `knowledges/architecture/sustainable_architecture.json`
- `knowledges/architecture/urban_planning.json`
- `knowledges/cinema/animation_history.json`
- `knowledges/cinema/cinematography_basics.json`
- `knowledges/cinema/documentary_film.json`
- `knowledges/cinema/film_directors.json`
- `knowledges/cinema/film_genres.json`
- `knowledges/cinema/film_history.json`
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
- `knowledges/economics/behavioral_economics.json`
- `knowledges/economics/financial_markets.json`
- `knowledges/economics/history_of_economic_thought.json`
- `knowledges/economics/international_trade.json`
- `knowledges/economics/macroeconomics_basics.json`
- `knowledges/economics/microeconomics_advanced.json`
- `knowledges/economics/microeconomics_basics.json`
- `knowledges/economics/personal_finance.json`
- `knowledges/economics/public_economics.json`
- `knowledges/environment/biodiversity_conservation.json`
- `knowledges/environment/circular_economy.json`
- `knowledges/environment/climate_change_solutions.json`
- `knowledges/environment/environmental_policy.json`
- `knowledges/environment/renewable_energy.json`
- `knowledges/environment/sustainable_development.json`
- `knowledges/environment/water_resources.json`
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
- `knowledges/human/psychology/behavioral_patterns.json`
- `knowledges/human/psychology/motivation.json`
- `knowledges/human/skills/softskills/adaptability.json`
- `knowledges/human/skills/softskills/creativity.json`
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
- `knowledges/law/constitutional_law.json`
- `knowledges/law/consumer_law.json`
- `knowledges/law/criminal_law_basics.json`
- `knowledges/law/digital_law.json`
- `knowledges/law/human_rights_law.json`
- `knowledges/law/international_law.json`
- `knowledges/law/labor_law_basics.json`
- `knowledges/law/law_basics.json`
- `knowledges/linguistics/language_acquisition.json`
- `knowledges/linguistics/linguistics_fundamentals.json`
- `knowledges/linguistics/phonetics_phonology.json`
- `knowledges/linguistics/semantics_pragmatics.json`
- `knowledges/linguistics/sociolinguistics.json`
- `knowledges/linguistics/syntax_morphology.json`
- `knowledges/manifest.json`
- `knowledges/nutrition/dietary_patterns.json`
- `knowledges/nutrition/gut_microbiome.json`
- `knowledges/nutrition/macronutrients_deep.json`
- `knowledges/nutrition/micronutrients_vitamins.json`
- `knowledges/nutrition/nutrition_fundamentals.json`
- `knowledges/nutrition/sports_nutrition.json`
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
- `knowledges/sociology/collective_action.json`
- `knowledges/sociology/cultural_sociology.json`
- `knowledges/sociology/deviance_social_control.json`
- `knowledges/sociology/social_stratification.json`
- `knowledges/sociology/sociology_fundamentals.json`
- `knowledges/sociology/sociology_of_organizations.json`
- `knowledges/sociology/urban_sociology.json`
- `knowledges/sports_science/biomechanics_basics.json`
- `knowledges/sports_science/recovery_performance.json`
- `knowledges/sports_science/sports_physiology.json`
- `knowledges/sports_science/sports_psychology.json`
- `knowledges/sports_science/training_principles.json`
- `knowledges/taxonomy.json`
- `paths.py`
- `requirements.txt`
- `scripts/clean_project.ps1`
- `tests/test_b18_knowledge.py`
**B20**
- `config/safety_rules.json`
- `config/security/audit_retention_policy.json`
- `config/security/trusted_devices.json`
- `dashboard/dashboard_conformite/_manifest.json`
- `dashboard/dashboard_data.json`
- `dashboard/dashboard_data/dashboard_data.json`
- `dashboard/dashboard_data/dashboard_data_manifest.json`
- `dashboard/dashboard_data/validation_registry.json`
- `dashboard/dashboard_gouvernance/dashboard_gouvernance.html`
- `dashboard/dashboard_gouvernance/dashboard_gouvernance_dynamique.html`
- `dashboard/dashboard_gouvernance/index.html`
- `dashboard/dashboard_gouvernance/norm.html`
- `dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py`
- `dashboard/dashboard_manifest.json`
- `dashboard/dashboard_security/dashboard_security.html`
- `dashboard/dashboard_security/dashboard_security_dynamique.html`
- `dashboard/dashboard_tests/dashboard_tests.html`
- `dashboard/dashboard_tests/dashboard_tests_dynamique.html`
- `dashboard/validation_registry.json`
- `data/security/incident_register.json`
- `logs/security/security.log`
- `scripts/alfred_dashboard.html`
- `scripts/complete_dpa_openai.py`
- `scripts/complete_vlan.py`
- `scripts/fix_avatar_alpha.py`
- `src/security/consent_art9.py`
- `templates/html_dashboard_template.html`
- `tests/dashboard_tests/test_dashboard_gouvernance.py`
- `tests/dashboard_tests/test_dashboard_pipeline.py`
- `tests/security/test_pentest_auth.py`
- `tests/security/test_pentest_encryption.py`
- `tests/security/test_pentest_input.py`
- `tests/security/test_pentest_zero_trust.py`
- `tests/security_tests/test_access_control.py`
- `tests/security_tests/test_api_security.py`
- `tests/security_tests/test_asset_classifier.py`
- `tests/security_tests/test_audit_trail.py`
- `tests/security_tests/test_backup_security.py`
- `tests/security_tests/test_backup_security_v2.py`
- `tests/security_tests/test_behavioral_detector.py`
- `tests/security_tests/test_compliance_manager.py`
- `tests/security_tests/test_data_protection.py`
- `tests/security_tests/test_device_registry.py`
- `tests/security_tests/test_encryption_service.py`
- `tests/security_tests/test_html_report.py`
- `tests/security_tests/test_incident_correlation.py`
- `tests/security_tests/test_incident_manager.py`
- `tests/security_tests/test_input_validator.py`
- `tests/security_tests/test_key_rotation_and_dr.py`
- `tests/security_tests/test_mfa_manager.py`
- `tests/security_tests/test_network_security.py`
- `tests/security_tests/test_network_security_v12.py`
- `tests/security_tests/test_output_filter.py`
- `tests/security_tests/test_pentest_report.py`
- `tests/security_tests/test_permission_manager.py`
- `tests/security_tests/test_policy_decision_point.py`
- `tests/security_tests/test_policy_enforcement_point.py`
- `tests/security_tests/test_policy_engine.py`
- `tests/security_tests/test_prompt_guard.py`
- `tests/security_tests/test_quarantine_service.py`
- `tests/security_tests/test_rate_limiter.py`
- `tests/security_tests/test_rgpd_rights.py`
- `tests/security_tests/test_risk_engine.py`
- `tests/security_tests/test_role_manager.py`
- `tests/security_tests/test_secret_manager.py`
- `tests/security_tests/test_secret_manager_v11.py`
- `tests/security_tests/test_security_config.py`
- `tests/security_tests/test_security_dashboard.py`
- `tests/security_tests/test_security_governance.py`
- `tests/security_tests/test_security_logger.py`
- `tests/security_tests/test_session_anomaly_detector.py`
- `tests/security_tests/test_session_manager.py`
- `tests/security_tests/test_soc_monitor.py`
- `tests/security_tests/test_threat_detector.py`
- `tests/security_tests/test_tls_manager.py`
- `tests/security_tests/test_unicode_sanitizer.py`
- `tests/security_tests/test_zero_trust_orchestrator.py`
- `tools/apply_headers.py`
- `tools/audit_statuts.py`
- `tools/dashboard_tools/dashboard_data/compare_manifest_target.py`
- `tools/dashboard_tools/dashboard_data/compare_manifest_target_complet.py`
- `tools/dashboard_tools/dashboard_data/extract_missing_dashboard.py`
- `tools/dashboard_tools/dashboard_data/update_dashboard_data.py`
- `tools/dashboard_tools/dashboard_gouvernance/dashboard_gouvernance.py`
- `tools/dashboard_tools/dashboard_gouvernance/generate_audit_report.py`
- `tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py`
- `tools/dashboard_tools/dashboard_security/dashboard_security.py`
- `tools/dashboard_tools/dashboard_tests/dashboard_test.py`
- `tools/generate_backlog.py`
- `tools/knowledge_tools/generate_knowledge_registry.py`
- `tools/profile_tools/generate_alfred_params.py`
- `tools/profile_tools/test_alfred_profile_integration.py`
- `tools/startup_refresh.py`
**B21**
- `ALFRED_WEB/scripts/i18n_cadrage.py`
**B22**
- `src/accessibility/wcag_checker.py`
