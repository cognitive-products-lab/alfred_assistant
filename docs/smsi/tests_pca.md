<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Tests PCA et Exercices de Reprise
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.8.14
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Tests PCA et Exercices de Reprise

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.14  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Vérifier régulièrement que le Plan de Continuité d'Activité (`pca.md`) est opérationnel et que les délais RTO/RPO sont atteignables.

---

## 2. Planning des tests

| Type de test | Fréquence | Prochain test |
|---|---|---|
| Test de restauration partielle (données) | Trimestrielle | Septembre 2026 |
| Test de restauration complète | Semestrielle | Décembre 2026 |
| Exercice de simulation (scénario ransomware) | Annuelle | Décembre 2026 |
| Test accès PC de secours | Semestrielle | Décembre 2026 |

---

## 3. Résultats des tests

| Date | Type | Scénario | RTO réel | RPO réel | Résultat | Observations |
|---|---|---|---|---|---|---|
| 2026-06-18 | Test partiel | Restauration données depuis LaCie | 15 min | 24h | ✅ Succès | Sauvegarde LaCie opérationnelle |

---

## 4. Procédure de test trimestriel

### Test T1 — Restauration partielle
1. Identifier un ensemble de fichiers à restaurer (ex : `data/users/`)
2. Copier la sauvegarde LaCie vers un répertoire temporaire isolé
3. Mesurer le temps de restauration
4. Vérifier l'intégrité des fichiers restaurés (hash)
5. Valider via `pytest tests/security_tests/` si applicable
6. Documenter le résultat dans ce tableau

### Test T2 — PC de secours
1. Démarrer le PC portable de secours
2. Cloner le dépôt Git : `git clone <repo>`
3. Installer les dépendances : `pip install -r requirements.txt`
4. Vérifier que ALFRED démarre correctement
5. Documenter le résultat

---

## 5. Actions correctives post-test

Toute défaillance détectée lors d'un test est traitée comme une non-conformité et documentée dans `actions_correctives.md`.

---

## 6. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.14 |

> **Cognitive Products Lab — Confidentiel interne**
