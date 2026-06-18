# Audits Internes SMSI

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.9.2  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Évaluer périodiquement la conformité du SMSI ALFRED aux exigences ISO 27001 et aux politiques internes.

---

## 2. Programme d'audit

| Type | Fréquence | Périmètre |
|---|---|---|
| Audit automatique gouvernance | À chaque commit + quotidien | Toutes les exigences (manifest JSON) |
| Audit interne SMSI complet | Semestriel | ISO 27001, RGPD, AI Act, NIS2 |
| Audit ciblé modules sécurité | Trimestriel | Tests 651 + modules critiques |
| Revue de direction | Annuelle | Bilan global SMSI |

---

## 3. Méthode d'audit automatique

Le système d'audit est automatisé via :
- `tools/dashboard_tools/dashboard_gouvernance/generate_audit_report.py`
- Génère un rapport horodaté dans `dashboard/dashboard_gouvernance/reports/`
- Vérification automatique des fichiers de preuve sur disque
- Score calculé automatiquement (done=1.0, partial=0.5, todo=0.0)

---

## 4. Historique des audits

| Date | Type | Score global | Grade | Rapport |
|---|---|---|---|---|
| 2026-06-18 | Audit automatique initial | 42.0% | C | audit_gouvernance_20260618_110747.md |

---

## 5. Plan d'audit semestriel (S2 2026)

**Prévu :** Décembre 2026  
**Périmètre :** Toutes les normes actives (RGPD, ISO 27001, AI Act, NIS2)  
**Méthode :** Audit automatique + vérification manuelle des nouvelles preuves  
**Objectif :** Score ≥ 65% — Grade B

---

## 6. Non-conformités identifiées

Les non-conformités détectées lors des audits sont traitées dans `actions_correctives.md`.

---

## 7. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création programme d'audit — conformité ISO A.9.2 |

> **Cognitive Products Lab — Confidentiel interne**
