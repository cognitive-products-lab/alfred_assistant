# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS

> Généré le 03/06/2026 12:31 depuis `dashboard_data.json` (mis à jour le 03/06/2026 07:00:21)
> Progression technique : **75.4%** · Full projet : **52.4%**
> 665 fichiers détectés / 1065 cible full

## Synthèse globale

| Statut | Nb | % | Priorité |
|--------|---:|--:|----------|
| 🟡 Partiel | 1 | 0.2% | 🟡 Sprint |
| 🟦 Codé — à tester | 207 | 31.1% | 🟡 Sprint |
| 🧪 Testé — à valider | 8 | 1.2% | 🧪 Tests |
| ✅ Validé ✅ | 279 | 42.0% | ✅ Done |
| ⚙️ Structurel | 52 | 7.8% | ✅ Done |
| 🔗 Alias | 112 | 16.8% | ✅ Done |
| 🔀 Fusionné | 6 | 0.9% | ✅ Done |

## Backlog par bloc

### 🟢 B01 — Interaction conversationnelle intelligente `87.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 2 |
| Codés (à tester) | 7 |
| Partiels | 0 |
| Structurels | 3 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/conversation_rules.json` | 🟦 Codé — à tester | Tester |
| `config/intents_catalog.json` | 🟦 Codé — à tester | Tester |
| `config/response_patterns.json` | 🟦 Codé — à tester | Tester |
| `data/dialogue_history.json` | 🟦 Codé — à tester | Tester |
| `data/memory/episodic/dialogue_history.json` | 🟦 Codé — à tester | Tester |
| `tests/test_b01_speech.py` | 🟦 Codé — à tester | Tester |
| `tests/test_pipeline_llm.py` | 🟦 Codé — à tester | Tester |

### 🟢 B02 — Mémoire & RAG `90.4%`

| KPI | Valeur |
|-----|--------|
| Validés | 17 |
| Testés | 0 |
| Codés (à tester) | 6 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/knowledge_settings.json` | 🟦 Codé — à tester | Tester |
| `config/rag_settings.json` | 🟦 Codé — à tester | Tester |
| `config/v3/memory_rules.json` | 🟦 Codé — à tester | Tester |
| `data/user_memory.json` | 🟦 Codé — à tester | Tester |
| `data/v2/memory_samples.json` | 🟦 Codé — à tester | Tester |
| `data/v3/memory_patterns.json` | 🟦 Codé — à tester | Tester |

### 🟢 B03 — Émotions & Régulation `87.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 14 |
| Testés | 4 |
| Codés (à tester) | 6 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/emotion_profiles.json` | 🟦 Codé — à tester | Tester |
| `config/v3/emotion_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/tone_profiles.json` | 🟦 Codé — à tester | Tester |
| `data/v3/emotion_state.json` | 🟦 Codé — à tester | Tester |
| `data/v3/relational_state.json` | 🟦 Codé — à tester | Tester |
| `tests/test_b02_b03.py` | 🟦 Codé — à tester | Tester |

### 🟡 B04 — Sécurité & Protection `76.0%`

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
| `config/quality_thresholds.json` | 🟦 Codé — à tester | Tester |
| `config/settings.json` | 🟦 Codé — à tester | Tester |
| `pyproject.toml` | 🟦 Codé — à tester | Tester |

### 🟢 B05 — Organisation & Assistance `92.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 8 |
| Testés | 0 |
| Codés (à tester) | 2 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/actions/tasks.json` | 🟦 Codé — à tester | Tester |
| `data/v2/scenarios/daily_organization.json` | 🟦 Codé — à tester | Tester |

### ✅ B06 — Communication & Lien social `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 9 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### 🟡 B07 — Mobilité & Contexte externe `60.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 1 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `data/context/user_context.json` | 🟦 Codé — à tester | Tester |

### 🟡 B08 — Personnalisation utilisateur `79.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 11 |
| Testés | 2 |
| Codés (à tester) | 13 |
| Partiels | 0 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/behavior_rules_softskills.json` | 🟦 Codé — à tester | Tester |
| `config/personality_core.json` | 🟦 Codé — à tester | Tester |
| `config/self_alignment_rules.json` | 🟦 Codé — à tester | Tester |
| `config/user_adaptation_profile.json` | 🟦 Codé — à tester | Tester |
| `data/personality.json` | 🟦 Codé — à tester | Tester |
| `data/personality/instances/personality_core_instance.json` | 🟦 Codé — à tester | Tester |
| `data/personality/templates/personality_core.json` | 🟦 Codé — à tester | Tester |
| `data/personality/templates/personality_core_template_public.json` | 🟦 Codé — à tester | Tester |
| `data/preferences_profile.json` | 🟦 Codé — à tester | Tester |
| `data/profile/user_profile.json` | 🟦 Codé — à tester | Tester |
| `data/users/instances/user_celine_instance.json` | 🟦 Codé — à tester | Tester |
| `data/users/templates/user_adaptation_profile.json` | 🟦 Codé — à tester | Tester |
| `data/users/templates/user_profile_template_public.json` | 🟦 Codé — à tester | Tester |

### ✅ B09 — Productivité & Copilote pro `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### ❌ B10 — Collaboration & Coordination `0.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

### ✅ B11 — Intelligence cognitive avancée `100.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 10 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

### 🟢 B12 — Pilotage business & Stratégie `92.5%`

| KPI | Valeur |
|-----|--------|
| Validés | 13 |
| Testés | 0 |
| Codés (à tester) | 3 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/kpi_config.json` | 🟦 Codé — à tester | Tester |
| `config/v2/product_roadmap.json` | 🟦 Codé — à tester | Tester |
| `data/v2/product_state.json` | 🟦 Codé — à tester | Tester |

### ❌ B13 — Compagnon pédiatrique / ARTHUR `0.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 0 |
| Partiels | 0 |
| Structurels | 0 |
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

### 🟡 B15 — Présence visuelle & Avatar `62.1%`

| KPI | Valeur |
|-----|--------|
| Validés | 2 |
| Testés | 0 |
| Codés (à tester) | 43 |
| Partiels | 1 |
| Structurels | 1 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `assets/models/tts/fr_FR/ALIASES` | 🟡 Partiel | Compléter |
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
| `assets/avatars/avatar_medium/base_medium/alfred_medium_very_excited.png` | 🟦 Codé — à tester | Tester |
| *... 14 autres* | | |

### 🟠 B16 — Démonstration & Scénarisation `56.7%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 6 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v2/scenario_catalog.json` | 🟦 Codé — à tester | Tester |
| `data/v2/scenario_results.json` | 🟦 Codé — à tester | Tester |
| `data/v2/scenarios/career_transition.json` | 🟦 Codé — à tester | Tester |
| `data/v2/scenarios/isolation_support.json` | 🟦 Codé — à tester | Tester |
| `data/v2/scenarios/mental_overload.json` | 🟦 Codé — à tester | Tester |
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

### 🟢 B18 — Knowledge & Intelligence System `82.6%`

| KPI | Valeur |
|-----|--------|
| Validés | 61 |
| Testés | 0 |
| Codés (à tester) | 54 |
| Partiels | 0 |
| Structurels | 27 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `.env` | 🟦 Codé — à tester | Tester |
| `ALFRED_CONTEXT.md` | 🟦 Codé — à tester | Tester |
| `README.md` | 🟦 Codé — à tester | Tester |
| `bootstrap_project.ps1` | 🟦 Codé — à tester | Tester |
| `check_tools.ps1` | 🟦 Codé — à tester | Tester |
| `config/alfred_project.json` | 🟦 Codé — à tester | Tester |
| `config/router_rules.json` | 🟦 Codé — à tester | Tester |
| `config/routing_rules.json` | 🟦 Codé — à tester | Tester |
| `config/tagging_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v1/basic_pipeline_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v2/confidence_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v2/decision_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v2/edge_cases.json` | 🟦 Codé — à tester | Tester |
| `config/v2/fallback_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v2/feature_matrix.json` | 🟦 Codé — à tester | Tester |
| `config/v2/learning_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v2/module_mapping.json` | 🟦 Codé — à tester | Tester |
| `config/v2/naming_conventions.json` | 🟦 Codé — à tester | Tester |
| `config/v2/proactivity_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v2/signal_weights.json` | 🟦 Codé — à tester | Tester |
| `config/v3/confidence_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/conversation_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/fusion_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/learning_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/orchestrator_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/pattern_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/priority_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/proactive_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/relational_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v3/trigger_rules.json` | 🟦 Codé — à tester | Tester |
| *... 24 autres* | | |

### 🟡 B19 — Domotique Intelligente `73.3%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 10 |
| Partiels | 0 |
| Structurels | 5 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/v4/action_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v4/home_devices.json` | 🟦 Codé — à tester | Tester |
| `config/v4/orchestration_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v4/scenario_rules.json` | 🟦 Codé — à tester | Tester |
| `config/v4/trigger_rules.json` | 🟦 Codé — à tester | Tester |
| `data/v4/action_log.json` | 🟦 Codé — à tester | Tester |
| `data/v4/device_registry.json` | 🟦 Codé — à tester | Tester |
| `data/v4/home_state.json` | 🟦 Codé — à tester | Tester |
| `data/v4/sensor_state.json` | 🟦 Codé — à tester | Tester |
| `data/v4/trigger_log.json` | 🟦 Codé — à tester | Tester |

### 🟢 B20 — Cybersécurité Zero Trust `91.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 32 |
| Testés | 0 |
| Codés (à tester) | 15 |
| Partiels | 0 |
| Structurels | 2 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `config/safety_rules.json` | 🟦 Codé — à tester | Tester |
| `config/security/trusted_devices.json` | 🟦 Codé — à tester | Tester |
| `config/v3/safety_rules.json` | 🟦 Codé — à tester | Tester |
| `data/security/access_decisions_history.json` | 🟦 Codé — à tester | Tester |
| `data/security/incident_register.json` | 🟦 Codé — à tester | Tester |
| `data/security/trusted_devices_runtime.json` | 🟦 Codé — à tester | Tester |
| `logs/security/security.log` | 🟦 Codé — à tester | Tester |
| `src/security/api_security.py` | 🟦 Codé — à tester | Tester |
| `src/security/network_security.py` | 🟦 Codé — à tester | Tester |
| `src/security/soc_monitor.py` | 🟦 Codé — à tester | Tester |
| `src/security/data_protection.py` | 🟦 Codé — à tester | Tester |
| `src/security/html_report.py` | 🟦 Codé — à tester | Tester |
| `src/security/rate_limiter.py` | 🟦 Codé — à tester | Tester |
| `src/security/security_dashboard.py` | 🟦 Codé — à tester | Tester |
| `src/security/security_governance.py` | 🟦 Codé — à tester | Tester |

### 🟡 B21 — ALFRED Web Platform `60.0%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 10 |
| Partiels | 0 |
| Structurels | 0 |
| Manquants | 0 |

**Fichiers à traiter :**

| Fichier | Statut | Action |
|---------|--------|--------|
| `ALFRED_WEB/app.py` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/requirements.txt` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/README.md` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/base.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/index.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/contact.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/apprentissages.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/progression.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/templates/projet.html` | 🟦 Codé — à tester | Tester |
| `ALFRED_WEB/static/css/style.css` | 🟦 Codé — à tester | Tester |

### 🟡 B22 — Accessibility & Cognitive Assistance `72.2%`

| KPI | Valeur |
|-----|--------|
| Validés | 0 |
| Testés | 0 |
| Codés (à tester) | 13 |
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

## 🟦 Sprint — Fichiers codés à tester (207)

Ces fichiers sont implémentés mais n'ont pas encore de tests.

**B01**
- `config/conversation_rules.json`
- `config/intents_catalog.json`
- `config/response_patterns.json`
- `data/dialogue_history.json`
- `data/memory/episodic/dialogue_history.json`
- `tests/test_b01_speech.py`
- `tests/test_pipeline_llm.py`
**B02**
- `config/knowledge_settings.json`
- `config/rag_settings.json`
- `config/v3/memory_rules.json`
- `data/user_memory.json`
- `data/v2/memory_samples.json`
- `data/v3/memory_patterns.json`
**B03**
- `config/v2/emotion_profiles.json`
- `config/v3/emotion_rules.json`
- `config/v3/tone_profiles.json`
- `data/v3/emotion_state.json`
- `data/v3/relational_state.json`
- `tests/test_b02_b03.py`
**B04**
- `.env.example`
- `.gitignore`
- `config/ethics_rules.json`
- `config/quality_thresholds.json`
- `config/settings.json`
- `pyproject.toml`
**B05**
- `data/actions/tasks.json`
- `data/v2/scenarios/daily_organization.json`
**B07**
- `data/context/user_context.json`
**B08**
- `config/behavior_rules_softskills.json`
- `config/personality_core.json`
- `config/self_alignment_rules.json`
- `config/user_adaptation_profile.json`
- `data/personality.json`
- `data/personality/instances/personality_core_instance.json`
- `data/personality/templates/personality_core.json`
- `data/personality/templates/personality_core_template_public.json`
- `data/preferences_profile.json`
- `data/profile/user_profile.json`
- `data/users/instances/user_celine_instance.json`
- `data/users/templates/user_adaptation_profile.json`
- `data/users/templates/user_profile_template_public.json`
**B12**
- `config/v2/kpi_config.json`
- `config/v2/product_roadmap.json`
- `data/v2/product_state.json`
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
**B16**
- `config/v2/scenario_catalog.json`
- `data/v2/scenario_results.json`
- `data/v2/scenarios/career_transition.json`
- `data/v2/scenarios/isolation_support.json`
- `data/v2/scenarios/mental_overload.json`
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
- `bootstrap_project.ps1`
- `check_tools.ps1`
- `config/alfred_project.json`
- `config/router_rules.json`
- `config/routing_rules.json`
- `config/tagging_rules.json`
- `config/v1/basic_pipeline_rules.json`
- `config/v2/confidence_rules.json`
- `config/v2/decision_rules.json`
- `config/v2/edge_cases.json`
- `config/v2/fallback_rules.json`
- `config/v2/feature_matrix.json`
- `config/v2/learning_rules.json`
- `config/v2/module_mapping.json`
- `config/v2/naming_conventions.json`
- `config/v2/proactivity_rules.json`
- `config/v2/signal_weights.json`
- `config/v3/confidence_rules.json`
- `config/v3/conversation_rules.json`
- `config/v3/fusion_rules.json`
- `config/v3/learning_rules.json`
- `config/v3/orchestrator_rules.json`
- `config/v3/pattern_rules.json`
- `config/v3/priority_rules.json`
- `config/v3/proactive_rules.json`
- `config/v3/relational_rules.json`
- `config/v3/trigger_rules.json`
- `config/v3/workflow_rules.json`
- `data/v2/experience_state.json`
- `data/v2/feedback_log.json`
- `data/v2/learning_state.json`
- `data/v2/robustness_results.json`
- `data/v3/behavior_state.json`
- `data/v3/context_memories.json`
- `data/v3/conversation_state.json`
- `data/v3/feedback_log_v3.json`
- `data/v3/fusion_results.json`
- `data/v3/fusion_state.json`
- `data/v3/learning_state_v3.json`
- `data/v3/orchestrator_state.json`
- `data/v3/proactive_results.json`
- `data/v3/proactive_state.json`
- `data/v3/safety_state.json`
- `data/v3/workflow_log.json`
- `paths.py`
- `requirements.txt`
- `scripts/clean_project.ps1`
- `scripts/deploy_knowledges.ps1`
- `scripts/fix_response_generator_rename.ps1`
- `scripts/ranger_fichiers_blocs.ps1`
- `scripts/update_knowledge_registry.ps1`
**B19**
- `config/v4/action_rules.json`
- `config/v4/home_devices.json`
- `config/v4/orchestration_rules.json`
- `config/v4/scenario_rules.json`
- `config/v4/trigger_rules.json`
- `data/v4/action_log.json`
- `data/v4/device_registry.json`
- `data/v4/home_state.json`
- `data/v4/sensor_state.json`
- `data/v4/trigger_log.json`
**B20**
- `config/safety_rules.json`
- `config/security/trusted_devices.json`
- `config/v3/safety_rules.json`
- `data/security/access_decisions_history.json`
- `data/security/incident_register.json`
- `data/security/trusted_devices_runtime.json`
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
- `ALFRED_WEB/app.py`
- `ALFRED_WEB/requirements.txt`
- `ALFRED_WEB/static/css/style.css`
- `ALFRED_WEB/templates/apprentissages.html`
- `ALFRED_WEB/templates/base.html`
- `ALFRED_WEB/templates/contact.html`
- `ALFRED_WEB/templates/index.html`
- `ALFRED_WEB/templates/progression.html`
- `ALFRED_WEB/templates/projet.html`
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
