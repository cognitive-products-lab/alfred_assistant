# Revue de Code et Audit de Sécurité Applicative

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.28  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Détecter les vulnérabilités et les défauts de conception sécurité dans le code ALFRED avant mise en production.

---

## 2. Types de revue de code

| Type | Fréquence | Portée | Méthode |
|---|---|---|---|
| Revue pré-commit | Chaque commit | Module modifié | Auto-revue + checklist |
| Revue de module | À chaque nouveau module | Module complet | Revue approfondie |
| Audit trimestriel | Trimestrielle | Base de code complète | Audit systématique |
| Revue assistée IA | Sur demande | Module ciblé | Claude Code `/code-review` |

---

## 3. Checklist Revue de Sécurité

### Contrôle d'accès
- [ ] Authentification vérifiée avant toute action sensible
- [ ] Autorisation vérifiée (rôle utilisateur)
- [ ] Pas de bypass possible (URL directe, paramètre caché)

### Gestion des données
- [ ] Données sensibles chiffrées au repos (Fernet AES-256)
- [ ] Pas de données personnelles dans les logs
- [ ] Minimisation des données (ne stocker que le nécessaire)
- [ ] Durée de conservation respectée

### Entrées / Sorties
- [ ] Validation de toutes les entrées utilisateur
- [ ] Sanitisation avant traitement
- [ ] Pas d'injection possible (commandes, chemins)
- [ ] Filtrage des sorties (`output_filter.py`)

### Secrets et cryptographie
- [ ] Aucun secret en clair dans le code
- [ ] Utilisation de l'algorithme de chiffrement standard (Fernet)
- [ ] Rotation des clés prévue

### Journalisation
- [ ] Actions critiques journalisées dans `audit_trail.py`
- [ ] Logs ne contiennent pas de données sensibles en clair
- [ ] Intégrité des logs assurée

---

## 4. Historique des audits

| Date | Type | Portée | Résultats | Commit |
|---|---|---|---|---|
| 2026-06-18 | Audit module | Modules sécurité (43 modules) | A+ — 651/651 tests | 7ed7604 |

---

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.28 |

> **Cognitive Products Lab — Confidentiel interne**
