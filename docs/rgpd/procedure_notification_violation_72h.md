# Procédure de Notification des Violations de Données Personnelles
## Délai 72h — Art. 33 & 34 RGPD

---

**Référence :** PROC-RGPD-VIOL-001  
**Version :** 1.0  
**Date :** 2026-06-18  
**Responsable :** Cognitive Products Lab — Céline  
**Destinataires :** Fondatrice · Développement · (Futur DPD)

---

## 1. Objectif

Cette procédure définit les étapes à suivre en cas de violation de données personnelles au sens de l'Art. 33 RGPD, afin de :

1. Contenir et évaluer la violation dans les premières heures
2. Notifier la CNIL dans un délai de **72 heures** après sa découverte
3. Notifier les personnes concernées si le risque est élevé (Art. 34)
4. Documenter l'incident dans le registre des violations

---

## 2. Définition d'une violation

Constitue une violation de données personnelles au sens du RGPD tout incident de sécurité entraînant, de manière accidentelle ou illicite :

- **La destruction** de données personnelles
- **La perte** de données personnelles  
- **L'altération** de données personnelles
- **La divulgation non autorisée** de données personnelles
- **L'accès non autorisé** à des données personnelles

### Exemples concrets pour ALFRED

| Incident | Violation ? | Criticité |
|---|---|---|
| Accès non autorisé au PC d'ALFRED | Oui | Élevée |
| Envoi accidentel du wellbeing_log via API | Oui | Élevée |
| Corruption du fichier user_profile.json | Oui | Moyenne |
| Export Art. 20 envoyé à une mauvaise adresse | Oui | Élevée |
| Perte d'un fichier de sauvegarde non chiffré | Oui | Élevée |
| Panne disque — données récupérées depuis backup | Non (si backup sécurisé) | — |
| Tentative de connexion MFA échouée | Non (tentative, pas violation) | — |

---

## 3. Procédure pas à pas

### Phase 1 — Découverte et confinement (H+0 → H+4)

```
┌─────────────────────────────────────────────────────────┐
│ H+0  DÉCOUVERTE                                         │
│       Détection via audit_trail.py / alerte manuelle    │
├─────────────────────────────────────────────────────────┤
│ H+1  CONFINEMENT                                        │
│       • Isoler le système affecté (déconnexion réseau)  │
│       • Révoquer les sessions actives (MFA Manager)     │
│       • Sécuriser les logs (audit_trail.py)             │
├─────────────────────────────────────────────────────────┤
│ H+2  ÉVALUATION INITIALE                                │
│       • Quelles données ? (profil / mémoire / santé)    │
│       • Quelle étendue ? (local / externe ?)            │
│       • Personnes concernées ? (Céline / futurs users)  │
│       • Décision : notification CNIL requise ?          │
└─────────────────────────────────────────────────────────┘
```

### Phase 2 — Évaluation du risque (H+2 → H+8)

Critères d'évaluation (grille ENISA) :

| Critère | Faible | Moyen | Élevé |
|---|---|---|---|
| Nature des données | Pseudonymisées | Identifiantes | Données de santé / sensibles |
| Nombre de personnes | 1 | 2-10 | >10 |
| Facilité d'identification | Difficile | Possible | Facile |
| Conséquences potentielles | Gêne | Dommage matériel | Préjudice grave |

**Seuil :** Si au moins 1 critère = Élevé → Notification CNIL obligatoire.

### Phase 3 — Notification CNIL (avant H+72)

**Portail :** https://notifications.cnil.fr/notifications/index

**Informations à fournir (Art. 33 §3) :**

```
1. Nature de la violation
   □ Confidentialité  □ Intégrité  □ Disponibilité

2. Catégories et volume approximatif de données
   Ex : données de santé · 1 personne concernée

3. Coordonnées du DPD (ou du responsable si pas de DPD)
   Nom : Céline
   Email : darkmiroir@gmail.com
   Organisation : Cognitive Products Lab

4. Conséquences probables de la violation

5. Mesures prises ou envisagées
   (confinement / correction / prévention récurrence)
```

> **Important :** Si toutes les informations ne sont pas disponibles en 72h, notifier quand même avec les éléments disponibles, puis compléter (notification échelonnée autorisée par l'Art. 33 §4).

### Phase 4 — Notification personnes concernées (si risque élevé)

Si la violation est susceptible d'engendrer un risque élevé pour les droits et libertés (Art. 34) :

**Destinataire :** Céline (utilisatrice principale)  
**Canal :** Email personnel  
**Contenu minimum :**
- Description claire de la violation
- Coordonnées du DPD/responsable
- Conséquences probables
- Mesures prises pour y remédier

**Délai :** Dans les meilleurs délais (pas de délai fixé, mais sans délai excessif).

**Exemptions :** Pas de notification si les données étaient chiffrées et la clé non compromise.

---

## 4. Documentation obligatoire

Toute violation, même ne nécessitant pas notification CNIL, doit être documentée dans le registre des violations (`data/security/incident_register.json`) :

```json
{
  "incident_id": "INC-YYYY-NNN",
  "discovered_at": "ISO8601",
  "type": "data_breach",
  "nature": ["confidentiality|integrity|availability"],
  "data_categories": ["..."],
  "persons_affected": 1,
  "cnil_notified": true,
  "cnil_notification_at": "ISO8601",
  "cnil_reference": "REF-CNIL-...",
  "persons_notified": false,
  "resolution": "...",
  "lessons_learned": "..."
}
```

---

## 5. Contacts et références

| Ressource | URL / Contact |
|---|---|
| Portail notification CNIL | https://notifications.cnil.fr/notifications/index |
| Guide CNIL violations | https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles |
| CERT-FR (incidents SI) | https://www.cert.ssi.gouv.fr/ |
| Registre incidents ALFRED | `data/security/incident_register.json` |

---

## 6. Revue

| | |
|---|---|
| **Validé par** | Céline |
| **Date** | 2026-06-18 |
| **Prochaine revue** | 2027-06-18 ou après tout incident |

---

*Document confidentiel interne — Cognitive Products Lab*
