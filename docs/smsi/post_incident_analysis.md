# Analyse Post-Incident et Leçons Apprises

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.27  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Responsable Sécurité  
> **Statut :** Approuvé

---

## 1. Objectif

Formaliser le retour d'expérience après chaque incident de sécurité P1/P2 (et optionnellement P3) afin d'améliorer continuellement la posture de sécurité ALFRED.

---

## 2. Déclenchement

| Niveau | Obligation analyse post-incident |
|---|---|
| P1 — Critique | Obligatoire — rapport dans les 5 jours ouvrés |
| P2 — Haute | Obligatoire — rapport dans les 10 jours ouvrés |
| P3 — Modérée | Recommandé |
| P4 — Faible | Optionnel |

---

## 3. Template Rapport Post-Incident

```
RAPPORT POST-INCIDENT — [INC-AAAA-MM-DD-NNN]
═══════════════════════════════════════════════

1. RÉSUMÉ EXÉCUTIF
   - Date/heure détection :
   - Date/heure résolution :
   - Durée totale :
   - Niveau de gravité :
   - Systèmes affectés :
   - Données exposées (OUI/NON + périmètre si OUI) :

2. CHRONOLOGIE DÉTAILLÉE
   - [H+0] Détection :
   - [H+X] Actions :
   - [H+X] Résolution :

3. CAUSE RACINE
   - Cause technique :
   - Cause organisationnelle :
   - Facteurs aggravants :

4. IMPACT
   - Confidentialité des données : [AUCUN / FAIBLE / MODÉRÉ / ÉLEVÉ]
   - Intégrité des données : [AUCUN / FAIBLE / MODÉRÉ / ÉLEVÉ]
   - Disponibilité des services : [AUCUN / FAIBLE / MODÉRÉ / ÉLEVÉ]
   - Personnes concernées (nombre) :

5. ACTIONS DE REMÉDIATION
   - Actions immédiates réalisées :
   - Actions correctives planifiées :
   - Responsable / échéance :

6. LEÇONS APPRISES
   - Ce qui a bien fonctionné :
   - Ce qui doit être amélioré :
   - Recommandations :

7. SUIVI
   - Actions ouvertes :
   - Date revue de direction :
   - Signataire : Céline Darras — Fondatrice / Responsable Sécurité
```

---

## 4. Registre des Analyses Post-Incident

| ID Incident | Date | Gravité | Cause racine | Rapport disponible |
|---|---|---|---|---|
| _(aucun incident P1/P2 à ce jour)_ | — | — | — | — |

---

## 5. Intégration dans l'amélioration continue

Les leçons apprises sont transmises à :
- La revue de direction annuelle (`revue_direction.md`)
- La gestion des non-conformités (`actions_correctives.md`)
- La mise à jour des procédures de sécurité concernées

---

## 6. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.5.27 |

> **Cognitive Products Lab — Confidentiel interne**
