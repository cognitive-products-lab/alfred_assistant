# SOC — Security Operations Center
## Cognitive Products Lab — Architecture & Procédures

> Version 1.0 — 2026-06-16  
> Référence : ANSSI guide SOC, NIS2 art. 21, ISO 27001:2022 A.12 & A.16  
> Statut : document de conception — implémentation progressive V1 → V3

---

## 1. Vision SOC CPL

Un SOC (Security Operations Center) est le centre névralgique de surveillance,
détection et réponse aux incidents de sécurité. Pour CPL, le SOC doit être :

- **Adapté à la taille de la structure** (startup, équipe réduite)
- **Local-first compatible** (surveiller sans collecter de données personnelles)
- **Évolutif** : SOC interne léger V1 → SOC managé V3 si croissance
- **Conforme NIS2 / ANSSI** dès la conception

---

## 2. Architecture SOC — 3 niveaux évolutifs

### Niveau 1 — SOC minimal (V1, maintenant)

```
┌─────────────────────────────────────────────────────────────┐
│                    SOC NIVEAU 1 — CPL                        │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Logs locaux │    │ Logs serveur│    │ Alertes système │  │
│  │ (appareil   │    │ CPL (erreurs│    │ (crash, erreur  │  │
│  │ utilisateur)│    │ anon.)      │    │  critique)      │  │
│  └──────┬──────┘    └──────┬──────┘    └────────┬────────┘  │
│         │                  │                    │            │
│         └──────────────────┴────────────────────┘            │
│                            │                                  │
│                     ┌──────▼──────┐                          │
│                     │ Agrégateur  │  (script Python local)   │
│                     │ de logs CPL │                          │
│                     └──────┬──────┘                          │
│                            │                                  │
│                     ┌──────▼──────┐                          │
│                     │  Tableau de │  (dashboard_data.json    │
│                     │  bord RSSI  │   ou HTML existant)      │
│                     └─────────────┘                          │
│                                                              │
│  Surveillance manuelle : RSSI CPL — revue quotidienne        │
└─────────────────────────────────────────────────────────────┘
```

**Composants V1 :**
- Script de collecte de logs anonymisés locaux (`scripts/soc_log_collector.py`)
- Tableau de bord sécurité minimal (extension `dashboard/ALFRED_DASHBOARD_DYNAMIC.html`)
- Procédure de revue manuelle quotidienne (RSSI = Céline Rousselot en V1)
- Alertes email/notification sur événements critiques

### Niveau 2 — SOC semi-automatisé (V2)

```
┌─────────────────────────────────────────────────────────────┐
│                    SOC NIVEAU 2 — CPL                        │
│                                                              │
│  Sources de logs → SIEM léger (ex: Wazuh open source)       │
│                         │                                    │
│              ┌──────────▼──────────┐                        │
│              │  Règles de détection│  (règles ANSSI adaptées)│
│              │  automatisées       │                         │
│              └──────────┬──────────┘                        │
│                         │                                    │
│              ┌──────────▼──────────┐                        │
│              │  Alertes automatiques│  (RSSI + DPO si        │
│              │  avec triage        │   données personnelles) │
│              └──────────┬──────────┘                        │
│                         │                                    │
│              ┌──────────▼──────────┐                        │
│              │  Playbooks de       │  (procédures de         │
│              │  réponse aux        │   réponse par type      │
│              │  incidents          │   d'incident)           │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Niveau 3 — SOC managé (V3, si croissance significative)

Externalisation partielle vers un **MSSP** (Managed Security Service Provider)
certifié ANSSI, avec conservation de la supervision interne.

---

## 3. Périmètre de surveillance

### 3.1 Ce que le SOC surveille

| Source | Événements surveillés | Criticité | Rétention logs |
|--------|----------------------|-----------|---------------|
| **Serveur CPL** | Connexions, tentatives d'accès, erreurs HTTP, volumes anormaux | CRITIQUE | 12 mois |
| **Système d'authentification** | Échecs auth, connexions inhabituelles, MFA bypass | CRITIQUE | 24 mois |
| **API ALFRED (future)** | Requêtes anormales, rate limiting, injection | ÉLEVÉE | 12 mois |
| **Dépôt GitHub** | Commits, accès, modifications de secrets | ÉLEVÉE | 24 mois |
| **Dépendances logicielles** | CVE nouvelles sur dépendances (Dependabot) | ÉLEVÉE | 6 mois |
| **Infrastructure** | Disponibilité, performance, certificats TLS | MOYENNE | 6 mois |
| **Audit trail données** | Accès non autorisés aux données, suppressions massives | CRITIQUE | 5 ans |

### 3.2 Ce que le SOC NE surveille PAS (protection vie privée)

- Contenu des conversations utilisateurs
- Données de profil psychologique
- Toute donnée personnelle non agrégée et non anonymisée

---

## 4. Indicateurs de sécurité (KPI SOC)

### KPI de détection

| Indicateur | Cible | Seuil d'alerte |
|-----------|-------|----------------|
| **MTTD** (Mean Time To Detect) | < 4h | > 24h = critique |
| **MTTR** (Mean Time To Respond) | < 8h | > 72h = critique |
| **Taux de faux positifs** | < 10% | > 30% = révision règles |
| **Couverture des actifs surveillés** | 100% actifs critiques | < 80% = critique |
| **Disponibilité du SOC** | 95% heures ouvrées (V1) | — |

### KPI de conformité

| Indicateur | Cible | Fréquence |
|-----------|-------|-----------|
| Délai notification CNIL (violation) | < 72h | Par incident |
| Délai notification ANSSI (NIS2) | < 24h alerte / 72h rapport | Par incident |
| Revue des logs | Quotidienne (V1) | Continue |
| Tests d'intrusion | Annuels | Annuelle |
| Mise à jour correctifs critiques | < 72h après publication | Continue |
| Formation équipe cybersécurité | 1x/an minimum | Annuelle |

---

## 5. Classification des incidents

### Niveau 1 — CRITIQUE (réponse immédiate < 1h)
- Violation de données personnelles confirmée
- Accès non autorisé aux systèmes de production
- Ransomware ou malware actif
- Compromission de clés de chiffrement
- Accès non autorisé aux données d'un mineur (ARTHUR)

**Actions :** Confinement immédiat → Notification DPO/RSSI → Évaluation impact RGPD → Notification CNIL si requis → Post-mortem

### Niveau 2 — ÉLEVÉ (réponse < 4h)
- Tentative d'intrusion détectée (non aboutie)
- Anomalie significative dans les logs d'accès
- Vulnérabilité critique dans une dépendance active
- Perte ou vol d'un appareil utilisateur contenant des données

**Actions :** Investigation → Containment → Remédiation → Documentation

### Niveau 3 — MOYEN (réponse < 24h)
- Tentatives répétées d'authentification échouées
- Certificat TLS expirant sous 7 jours
- Anomalie de performance pouvant indiquer un DDoS
- Vulnérabilité haute dans une dépendance

**Actions :** Analyse → Plan de remédiation → Correction planifiée

### Niveau 4 — FAIBLE (réponse < 72h)
- Alerte de veille (nouveau CVE sans impact immédiat)
- Anomalie de log non critique
- Mise à jour de sécurité disponible (non critique)

**Actions :** Documentation → Priorisation dans backlog sécurité

---

## 6. Playbooks de réponse aux incidents

### Playbook 1 — Violation de données personnelles

```
DÉTECTION
    │
    ▼ (< 1h)
Confinement immédiat de la source
    │
    ▼ (< 2h)
Évaluation : données concernées ? nombre de personnes ? risque ?
    │
    ├── Risque faible → Documentation registre violations uniquement
    │
    └── Risque moyen/élevé
            │
            ▼ (< 72h après détection)
        Notification CNIL (portail notifications.cnil.fr)
            │
            ▼ (si risque élevé pour les personnes)
        Notification des personnes concernées (sans délai)
            │
            ▼
        Post-mortem + mesures correctives + mise à jour registre
```

### Playbook 2 — Compromission d'identifiants

```
ALERTE (connexion suspecte / MFA bypass)
    │
    ▼ Immédiat
Désactivation du compte compromis
    │
    ▼ < 30 min
Rotation de tous les secrets associés
    │
    ▼ < 1h
Investigation : étendue de l'accès, données consultées
    │
    ▼ < 4h
Évaluation RGPD : violation de données à notifier ?
    │
    ▼
Renforcement des contrôles d'accès + formation si cause humaine
```

### Playbook 3 — Perte/vol d'appareil utilisateur

```
SIGNALEMENT par l'utilisateur
    │
    ▼ Immédiat
Vérification chiffrement Fernet actif → Si oui : risque réduit
    │
    ▼ < 2h
Évaluation : clé Fernet compromise ? données accessibles sans clé ?
    │
    ├── Clé sécurisée séparément → Données inaccessibles → Documentation
    │
    └── Risque d'accès aux données
            │
            ▼
        Évaluation RGPD violation → Procédure playbook 1
            │
            ▼
        Rotation des clés de chiffrement sur nouvel appareil
```

---

## 7. Veille sécurité

### Sources de veille obligatoires

| Source | Fréquence | Responsable |
|--------|-----------|-------------|
| **CERT-FR** (cert.ssi.gouv.fr) | Quotidienne | RSSI |
| **ANSSI alertes** (ssi.gouv.fr) | Quotidienne | RSSI |
| **CVE NIST NVD** (dépendances projet) | Automatisée (Dependabot GitHub) | Développement |
| **CNIL actualités** (cnil.fr) | Hebdomadaire | DPO |
| **AI Act Watch** (aiawatch.eu) | Mensuelle | Responsable conformité IA |
| **Bulletins sécurité Python** | Automatisée | CI/CD pipeline |

### Processus de veille

1. **Veille automatisée** : Dependabot activé sur GitHub pour les dépendances
2. **Veille manuelle** : RSSI consulte CERT-FR + ANSSI chaque matin
3. **Triage** : CVE critique → Patch sous 72h / CVE haute → Patch sous 7 jours
4. **Documentation** : Chaque CVE traitée consignée dans le registre de sécurité

---

## 8. Tests de sécurité

### Plan de tests annuel

| Test | Fréquence | Périmètre | Prestataire |
|------|-----------|-----------|-------------|
| **Test d'intrusion (pentest)** | Annuel | Serveur CPL + API | Prestataire PASSI (certifié ANSSI) |
| **Audit de code sécurité** | À chaque release majeure | Code source | Interne + outil SAST |
| **Test de restauration** (PRA) | Semestriel | Sauvegardes | Interne |
| **Exercice de gestion d'incident** | Annuel | Équipe CPL | Interne |
| **Scan de vulnérabilités** | Mensuel | Infrastructure | Outil automatisé (ex: OpenVAS) |
| **Test chiffrement** | À chaque changement | Données sensibles | Interne |

---

## 9. Journalisation (Logging)

### Format de log standardisé CPL

```json
{
  "timestamp": "2026-06-16T08:30:00.000Z",
  "log_id": "uuid-v4",
  "level": "INFO|WARNING|ERROR|CRITICAL",
  "source": "alfred_api|auth_service|soc_collector",
  "event_type": "auth_success|auth_failure|data_access|config_change|...",
  "actor": "user_pseudonym|system|admin_role",
  "resource": "resource_type_only (pas de données perso)",
  "action": "read|write|delete|export|login|logout",
  "result": "success|failure|denied",
  "ip_hash": "hash(IP) — jamais IP brute",
  "session_id": "pseudonymisé",
  "metadata": {}
}
```

### Règles de journalisation

- ❌ Jamais de données personnelles dans les logs (noms, emails, contenu messages)
- ❌ Jamais d'IP brutes — hachage systématique (SHA-256 salé)
- ✅ Pseudonymisation de tous les identifiants
- ✅ Horodatage UTC systématique
- ✅ Chiffrement des logs au repos
- ✅ Intégrité des logs vérifiable (hachage enchaîné)
- ✅ Accès aux logs : RSSI uniquement (principe moindre privilège)

---

## 10. Feuille de route SOC

| Étape | Échéance | Actions |
|-------|----------|---------|
| **V1 — SOC minimal** | T0 (maintenant) | Script collecte logs, dashboard sécurité, procédures manuelles, veille CERT-FR |
| **V1.5 — Automatisation partielle** | T0 + 3 mois | Alertes automatiques email/notification, Dependabot actif, revue logs quotidienne automatisée |
| **V2 — SIEM léger** | T0 + 12 mois | Wazuh ou équivalent open source, règles détection ANSSI, playbooks automatisés |
| **V3 — SOC managé** | T0 + 24 mois (si croissance) | MSSP certifié ANSSI, SOC 24/7, pentest semestriel |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*  
*RSSI désigné : à nommer formellement (Céline Rousselot assure ce rôle en V1)*  
*Révision : annuelle + après tout incident de niveau 1 ou 2*
