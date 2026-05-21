# ALFRED — Structure officielle des blocs (référence canonique)

> **Document de référence** — à utiliser pour les entêtes de fichiers, le dashboard,
> le module_mapping et tout nouveau document. Ne jamais improviser un numéro de bloc.

---

## Format des entêtes fichier

### Fichiers Python (`.py`)

```python
# ============================================================
# ALFRED — src/<module>/<fichier>.py
# Bloc XX.YY — <Intitulé du sous-code>
#
# 📚 NOTION EXAM :
#   DXX-Y — Capsule Z : <Intitulé exact du cours FEDE>
#
# 🎯 UTILITÉ ALFRED :
#   <Ce que ce module fait concrètement dans le système>
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   <Concept couvert>
# ============================================================
```

### Fichiers JSON (`.json`) — templates, configs, knowledges

```json
{
  "_alfred_header": {
    "file": "<chemin/relatif/depuis/racine.json>",
    "bloc": "Bloc XX.YY — <Intitulé du sous-code>",
    "notion_exam": "DXX-Y — Capsule Z : <Intitulé exact du cours FEDE>",
    "utilite_alfred": "<Ce que ce fichier fait concrètement dans le système>",
    "domaine": "<Domaine fonctionnel couvert>"
  }
}
```

> Le champ `_alfred_header` doit toujours être le **premier champ** du JSON.
> Les parsers JSON ignorent les clés inconnues — aucun impact fonctionnel.

---

## Structure officielle — Blocs 01 à 20

### Bloc 01 — Noyau conversationnel & orchestration
| Code  | Fonction principale         |
|-------|-----------------------------|
| 01.01 | Gestion des conversations   |
| 01.02 | Compréhension des intentions|
| 01.03 | Gestion du contexte         |
| 01.04 | Orchestration des modules   |
| 01.05 | Gestion des réponses        |

**Dossiers src/** : `src/conversation/`, `src/core/`, `src/llm/`

---

### Bloc 02 — Mémoire & contexte
| Code  | Fonction principale         |
|-------|-----------------------------|
| 02.01 | Mémoire courte              |
| 02.02 | Mémoire longue              |
| 02.03 | Historique utilisateur      |
| 02.04 | Contextualisation intelligente |
| 02.05 | Synchronisation mémoire     |

**Dossiers src/** : `src/memory/`, `src/rag/`

---

### Bloc 03 — Émotions & adaptation comportementale
| Code  | Fonction principale         |
|-------|-----------------------------|
| 03.01 | Détection émotionnelle      |
| 03.02 | Adaptation comportementale  |
| 03.03 | Gestion empathique          |
| 03.04 | Personnalité dynamique      |
| 03.05 | Gestion relationnelle       |

**Dossiers src/** : `src/regulation/`

---

### Bloc 04 — Interaction vocale
| Code  | Fonction principale         |
|-------|-----------------------------|
| 04.01 | Reconnaissance vocale (STT) |
| 04.02 | Synthèse vocale (TTS)       |
| 04.03 | Détection sonore            |
| 04.04 | Hotword & écoute            |
| 04.05 | Gestion audio temps réel    |

**Dossiers src/** : `src/conversation/input/` (STT), `src/conversation/output/` (TTS)

---

### Bloc 05 — Gestion utilisateur
| Code  | Fonction principale         |
|-------|-----------------------------|
| 05.01 | Profils utilisateurs        |
| 05.02 | Préférences                 |
| 05.03 | Permissions & rôles         |
| 05.04 | Authentification            |
| 05.05 | Personnalisation            |

**Dossiers src/** : `src/auth/`, `config/personality_core.json`

---

### Bloc 06 — Assistance quotidienne
| Code  | Fonction principale         |
|-------|-----------------------------|
| 06.01 | Agenda                      |
| 06.02 | Rappels intelligents        |
| 06.03 | Gestion des tâches          |
| 06.04 | Assistance quotidienne      |
| 06.05 | Notifications               |

**Dossiers src/** : `src/assistant_actions/`, `data/actions/`

---

### Bloc 07 — Apprentissage & routines
| Code  | Fonction principale         |
|-------|-----------------------------|
| 07.01 | Analyse des habitudes       |
| 07.02 | Recommandations             |
| 07.03 | Automatisation des routines |
| 07.04 | Amélioration continue       |
| 07.05 | Analyse comportementale     |

**Dossiers src/** : `src/v3/learning/`, `data/context/`

---

### Bloc 08 — Supervision système
| Code  | Fonction principale         |
|-------|-----------------------------|
| 08.01 | Monitoring système          |
| 08.02 | Gestion des erreurs         |
| 08.03 | Logs & traçabilité          |
| 08.04 | Maintenance                 |
| 08.05 | Diagnostic système          |

**Dossiers src/** : `config/ethics_rules.json`, `.env`, logs système

---

### Bloc 09 — API & microservices *(ALFRED CPL)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 09.01 | API internes                |
| 09.02 | API externes                |
| 09.03 | Microservices               |
| 09.04 | Gestion des flux            |
| 09.05 | Interopérabilité            |

---

### Bloc 10 — Intelligence artificielle avancée *(ALFRED CPL)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 10.01 | NLP avancé                  |
| 10.02 | Raisonnement IA             |
| 10.03 | IA émotionnelle             |
| 10.04 | Génération de contenu       |
| 10.05 | Optimisation IA             |

---

### Bloc 11 — Data & pilotage *(ALFRED CPL)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 11.01 | Collecte de données         |
| 11.02 | Analyse des données         |
| 11.03 | KPI & dashboards            |
| 11.04 | Reporting                   |
| 11.05 | Gouvernance data            |

**Fichiers** : `config/v2/kpi_config.json`, `data/v2/product_state.json`

---

### Bloc 12 — Collaboration professionnelle *(ALFRED CPL)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 12.01 | Gestion de projet           |
| 12.02 | Coordination d'équipe       |
| 12.03 | Support décisionnel         |
| 12.04 | Communication professionnelle |
| 12.05 | Gestion documentaire        |

**Fichiers** : `config/v2/product_roadmap.json`, knowledges CPL

---

### Bloc 13 — Santé & soutien émotionnel *(ARTHUR)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 13.01 | Suivi bien-être             |
| 13.02 | Soutien émotionnel          |
| 13.03 | Gestion fatigue & stress    |
| 13.04 | Assistance santé            |
| 13.05 | Interaction adaptée         |

---

### Bloc 14 — IoT & environnement connecté *(ARTHUR)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 14.01 | Domotique                   |
| 14.02 | Capteurs intelligents       |
| 14.03 | Gestion des équipements     |
| 14.04 | Automatisation environnementale |
| 14.05 | Supervision IoT             |

**Dossiers src/** : `src/v4/integration/`, `src/v4/home_state/`

---

### Bloc 15 — Présence visuelle & avatar *(ARTHUR)*
| Code  | Fonction principale         |
|-------|-----------------------------|
| 15.01 | Avatar                      |
| 15.02 | Expressions faciales        |
| 15.03 | Animations                  |
| 15.04 | Synchronisation labiale     |
| 15.05 | Interface visuelle          |

**Assets** : `assets/avatar/`, `assets/backgrounds/`

---

> ⚠️ **Bloc 16 réservé** — non assigné dans la structure officielle v1.

---

### Bloc 17 — Génération multimédia
| Code  | Fonction principale         |
|-------|-----------------------------|
| 17.01 | Génération d'images         |
| 17.02 | Génération vidéo            |
| 17.03 | Génération audio            |
| 17.04 | Génération graphique        |
| 17.05 | Génération documentaire     |

**Assets** : `assets/backgrounds/` (200+ PNG), `assets/ui/`

---

### Bloc 18 — Base de connaissances & culture
| Code  | Fonction principale              |
|-------|----------------------------------|
| 18.01 | Culture générale                 |
| 18.02 | Univers fictionnels              |
| 18.03 | Sciences & technologies          |
| 18.04 | Psychologie & cognition          |
| 18.05 | Santé & bien-être                |
| 18.06 | Histoire & géopolitique          |
| 18.07 | Productivité & méthodes          |
| 18.08 | Domotique & IoT                  |
| 18.09 | Sécurité & cybersécurité         |
| 18.10 | Base métier & expertise          |

**Dossiers** : `knowledges/` (250 fichiers), `src/knowledge/`

---

### Bloc 19 — Infrastructure & extensions
| Code  | Fonction principale             |
|-------|---------------------------------|
| 19.01 | Infrastructure locale           |
| 19.02 | Réseau                          |
| 19.03 | Synchronisation multi-appareils |
| 19.04 | Gestion des périphériques       |
| 19.05 | Scalabilité V1 → V3             |

**Dossiers** : `config/v4/`, `src/v4/orchestrator/`

---

### Bloc 20 — Cybersécurité, Zero Trust & conformité
| Code  | Fonction principale              | Fichier src/security/             |
|-------|----------------------------------|-----------------------------------|
| 20.01 | Gouvernance cybersécurité        | `security_config.py`              |
| 20.02 | Gestion des identités & accès    | `role_manager.py`, `device_registry.py` |
| 20.03 | Authentification & MFA           | `mfa_manager.py`, `session_manager.py`  |
| 20.04 | Contrôle RBAC & permissions      | `permission_manager.py`, `access_control.py` |
| 20.05 | Chiffrement & protection données | `encryption_service.py`, `output_filter.py` |
| 20.06 | Sécurité réseau                  | *(à implémenter)*                 |
| 20.07 | Sécurité API & microservices     | *(à implémenter)*                 |
| 20.08 | Détection d'intrusion            | `threat_detector.py`, `behavioral_detector.py`, `prompt_guard.py` |
| 20.09 | Journalisation & audit           | `security_logger.py`, `audit_trail.py` |
| 20.10 | Gestion des vulnérabilités       | `input_validator.py`              |
| 20.11 | Réponse à incident               | `incident_manager.py`, `quarantine_service.py` |
| 20.12 | Sauvegarde & reprise             | `backup_security.py`              |
| 20.13 | Zero Trust                       | `policy_engine.py`, `policy_decision_point.py`, `policy_enforcement_point.py`, `zero_trust_orchestrator.py` |
| 20.14 | Conformité & réglementation      | `compliance_manager.py`           |
| 20.15 | Supervision SOC & cybersurveillance | *(à implémenter)*              |

> **Hors liste** : `secret_manager.py` → Bloc 20.05 (chiffrement)

---

## Correspondance dashboard B-system → Blocs officiels

| Dashboard (ancien) | Label dashboard               | Bloc officiel | Label officiel                        |
|--------------------|-------------------------------|---------------|---------------------------------------|
| B01                | Interaction conversationnelle | **Bloc 01**   | Noyau conversationnel & orchestration |
| B02                | Mémoire & RAG                 | **Bloc 02**   | Mémoire & contexte                    |
| B03                | Émotions & Régulation         | **Bloc 03**   | Émotions & adaptation comportementale |
| B04                | Sécurité & Protection         | **Bloc 08**   | Supervision système *(fichiers config/ethics)* |
| B05                | Organisation & Assistance     | **Bloc 06**   | Assistance quotidienne                |
| B06                | Communication & Lien social   | **Bloc 12**   | Collaboration professionnelle         |
| B07                | Mobilité & Contexte externe   | **Bloc 07**   | Apprentissage & routines              |
| B08                | Personnalisation utilisateur  | **Bloc 05**   | Gestion utilisateur                   |
| B09                | Productivité & Copilote pro   | **Bloc 09**   | API & microservices *(CPL)*           |
| B10                | Collaboration & Coordination  | **Bloc 12**   | Collaboration professionnelle *(CPL)* |
| B11                | Intelligence cognitive avancée| **Bloc 10**   | Intelligence artificielle avancée *(CPL)* |
| B12                | Pilotage business & Stratégie | **Bloc 11**   | Data & pilotage *(CPL)*              |
| B13                | Compagnon pédiatrique / ARTHUR| **Bloc 13**   | Santé & soutien émotionnel *(ARTHUR)* |
| B14                | IoT & Intégrations            | **Bloc 14**   | IoT & environnement connecté          |
| B15                | Présence visuelle & Avatar    | **Bloc 15**   | Présence visuelle & avatar            |
| B16                | Démonstration & Scénarisation | *(réservé)*   | Bloc 16 non assigné                   |
| B17                | Visual Generation contextuelle| **Bloc 17**   | Génération multimédia                 |
| B18                | Knowledge & Intelligence System | **Bloc 18** | Base de connaissances & culture       |
| B19                | Domotique Intelligente        | **Bloc 19**   | Infrastructure & extensions           |
| B20                | Cybersécurité Zero Trust      | **Bloc 20**   | Cybersécurité, Zero Trust & conformité|

---

## Règles d'usage

1. **Entêtes fichiers** : utiliser `Bloc XX.YY` (ex. `Bloc 20.04 — Contrôle RBAC & permissions`)
2. **Dashboard** : utiliser l'identifiant court `Bloc 01` à `Bloc 20` + label officiel
3. **Jamais** : inventer un numéro, utiliser "B04" seul sans vérification dans ce document
4. **secret_manager.py** : anciennement étiqueté `20.06`, à reclasser `20.05` lors de la prochaine mise à jour des entêtes
5. **Bloc 16** : réservé — ne pas assigner de fichiers
6. **Bloc 20.06 et 20.07** : sous-codes à implémenter (sécurité réseau, sécurité API)
