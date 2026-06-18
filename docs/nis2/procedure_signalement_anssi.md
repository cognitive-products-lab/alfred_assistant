# Procédure de Signalement des Incidents à l'Autorité Compétente
## NIS2 — Directive (UE) 2022/2555 — Art. 23

---

**Référence :** PROC-NIS2-SIG-001  
**Version :** 1.0  
**Date :** 2026-06-18  
**Propriétaire :** Cognitive Products Lab — Céline  
**Autorité compétente :** ANSSI (Agence nationale de la sécurité des systèmes d'information)  
**CSIRT national :** CERT-FR

---

## 1. Contexte NIS2 et applicabilité

### 1.1 Positionnement d'ALFRED

La Directive NIS2 (transposée en droit français par la loi n°2024-XXX) s'applique aux entités essentielles et importantes dans des secteurs critiques.

| Critère | ALFRED V1 (usage personnel) | ALFRED CPL V2+ (commercial) |
|---|---|---|
| Entité essentielle | Non | À évaluer si secteur santé |
| Entité importante | Non | À évaluer (>50 salariés ou CA >10M€) |
| Obligation signalement NIS2 | Non obligatoire | Obligatoire |

**Conclusion V1 :** L'obligation de signalement NIS2 ne s'applique pas encore à ALFRED dans sa version personnelle. Cette procédure est établie en anticipation de la commercialisation (V2/V3) et comme bonne pratique.

### 1.2 Seuils NIS2 à surveiller

- **Entité importante :** >50 salariés OU CA >10M€ annuel
- **Entité essentielle :** >250 salariés OU CA >50M€ — secteurs critiques (santé, numérique, énergie…)

---

## 2. Types d'incidents à signaler (Art. 23 NIS2)

Dès que NIS2 s'applique, les incidents suivants déclenchent l'obligation de signalement :

### 2.1 Incidents significatifs (signalement obligatoire)

Un incident est **significatif** si :
- Il a causé ou est susceptible de causer une perturbation opérationnelle grave des services
- Il a causé ou est susceptible de causer des pertes financières significatives
- Il a affecté ou est susceptible d'affecter d'autres personnes physiques ou morales

| Exemples pour ALFRED | Significatif ? |
|---|---|
| Compromission complète du système ALFRED | Oui |
| Fuite massive de données de santé utilisateurs | Oui |
| Ransomware paralysant le service | Oui |
| Indisponibilité prolongée ALFRED_WEB (>24h) | Probablement |
| Incident isolé sur un seul compte utilisateur | Non (si contenté) |

---

## 3. Délais de notification NIS2

```
H+0   DÉTECTION de l'incident significatif
  │
H+24  ── ALERTE INITIALE ───────────────────────────────────
  │        • Notifier l'ANSSI / CERT-FR
  │        • Information minimale : nature, étendue estimée
  │        • Canal : https://www.cert.ssi.gouv.fr/contact/
  │
H+72  ── NOTIFICATION INTERMÉDIAIRE (si demandée) ──────────
  │        • Mise à jour de l'évaluation
  │        • Mesures de confinement prises
  │
J+30  ── RAPPORT FINAL ──────────────────────────────────────
           • Description complète de l'incident
           • Causes racines identifiées
           • Mesures correctives et préventives
           • Évaluation de l'impact transfrontalier (si applicable)
```

---

## 4. Procédure de signalement

### 4.1 Alerte initiale (H+24)

**Canal :** Portail ANSSI / CERT-FR  
**URL :** https://www.cert.ssi.gouv.fr/contact/  
**Email :** cert-fr@ssi.gouv.fr  
**Téléphone urgence :** +33 1 71 75 84 68 (CERT-FR)

**Informations à fournir à H+24 :**

```
Organisation      : Cognitive Products Lab
Contact           : Céline — darkmiroir@gmail.com
Secteur           : Services numériques / IA
Date détection    : YYYY-MM-DD HH:MM UTC
Nature incident   : [compromission / fuite / ransomware / DoS / autre]
Systèmes affectés : PC ALFRED / ALFRED_WEB / données utilisateur
Mesures prises    : [confinement initial]
Impact estimé     : [nombre utilisateurs affectés]
```

### 4.2 Rapport final (J+30)

Le rapport final doit inclure :
1. Chronologie détaillée de l'incident
2. Analyse des causes racines (5 Pourquoi)
3. Impact final mesuré (données, utilisateurs, disponibilité)
4. Mesures correctives déployées
5. Mesures préventives planifiées
6. Évaluation du risque résiduel post-remédiation

> Le rapport post-incident SMSI (`docs/smsi/post_incident_analysis.md`) sert de base au rapport final NIS2.

---

## 5. Articulation avec les autres obligations

| Obligation | Délai | Référence |
|---|---|---|
| Notification CNIL (violation RGPD) | 72h | `docs/rgpd/procedure_notification_violation_72h.md` |
| Alerte CERT-FR (NIS2) | 24h | Ce document |
| Rapport final NIS2 | 30 jours | Ce document |
| Analyse post-incident SMSI | 5-10 jours | `docs/smsi/post_incident_analysis.md` |

**Priorités en cas d'incident simultané :**
1. Confinement immédiat
2. Alerte CERT-FR si NIS2 applicable (H+24)
3. Notification CNIL si violation RGPD (H+72)
4. Rapport post-incident SMSI
5. Rapport final NIS2 (J+30)

---

## 6. Préparation et exercices

### 6.1 Contacts à maintenir à jour

| Organisme | Contact | URL |
|---|---|---|
| CERT-FR | cert-fr@ssi.gouv.fr | https://www.cert.ssi.gouv.fr |
| ANSSI | communication@ssi.gouv.fr | https://www.ssi.gouv.fr |
| CNIL (violations) | — | https://notifications.cnil.fr |

### 6.2 Exercice de simulation annuel

Un exercice de simulation d'incident est planifié annuellement pour tester :
- [ ] La détection via `security_governance.py` et `audit_trail.py`
- [ ] La procédure de confinement
- [ ] La rédaction de la notification CERT-FR
- [ ] Les délais effectifs (MTTD, MTTR)

---

## 7. Revue

| | |
|---|---|
| **Validé par** | Céline |
| **Date** | 2026-06-18 |
| **Prochaine revue** | 2027-06-18 ou lors du passage en entité NIS2 |
| **Mise à jour requise si** | Commercialisation ALFRED · Dépassement seuils NIS2 · Évolution législative |

---

*Document confidentiel interne — Cognitive Products Lab*  
*Conforme Directive (UE) 2022/2555 — NIS2, Art. 23*  
*Transposition française : Loi de programmation militaire + ordonnance NIS2*
