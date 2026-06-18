<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Plan de Sauvegarde et de Restauration
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.8.13
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Plan de Sauvegarde et de Restauration

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.13  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Garantir la disponibilité et la restaurabilité des données critiques ALFRED après sinistre, erreur humaine ou défaillance matérielle.

---

## 2. Périmètre des sauvegardes

| Actif | Criticité | RPO | RTO |
|---|---|---|---|
| Code source ALFRED | Critique | 0 (Git temps réel) | 1h |
| Données personnelles utilisateurs (`data/`) | Critique | 24h | 4h |
| Configuration sécurité (`config/security/`) | Critique | 24h | 2h |
| Clés cryptographiques | Critique | Immédiate (hors-ligne) | 2h |
| Documentation SMSI (`docs/`) | Haute | 24h | 8h |
| Dashboards (`dashboard/`) | Modérée | 24h | 8h |
| Journaux d'audit | Haute | 24h | 4h |

**RPO (Recovery Point Objective) :** Perte de données maximale acceptable  
**RTO (Recovery Time Objective) :** Délai de restauration maximal acceptable

---

## 3. Stratégie 3-2-1

| Copie | Support | Localisation | Chiffrement |
|---|---|---|---|
| **Copie 1** | Disque D: PC Alfred | Domicile | ✅ VeraCrypt AES-256 |
| **Copie 2** | Disque LaCie externe | Domicile (rangement séparé) | ✅ VeraCrypt AES-256 |
| **Copie 3** | Dépôt Git privé | Cloud (distant) | ✅ HTTPS + 2FA GitHub |

---

## 4. Fréquence et planning

| Type de sauvegarde | Fréquence | Support |
|---|---|---|
| Code source (Git push) | À chaque commit | GitHub (Copie 3) |
| Données complètes ALFRED | Quotidienne (automatique) | LaCie (Copie 2) |
| Configuration sécurité | À chaque modification | Git + LaCie |
| Sauvegarde complète système | Hebdomadaire | LaCie |
| Clés cryptographiques | À chaque rotation | Hors-ligne sécurisé |

---

## 5. Procédure de sauvegarde manuelle

```bash
# Sauvegarde données ALFRED
python scripts/backup_alfred.py --destination "E:/backup/alfred_$(date +%Y%m%d)"

# Vérification intégrité sauvegarde
python scripts/backup_alfred.py --verify --path "E:/backup/alfred_<date>"
```

---

## 6. Procédure de restauration

### Restauration partielle (fichiers isolés)
1. Identifier la version à restaurer dans l'historique Git ou le backup LaCie
2. Restaurer le(s) fichier(s) ciblé(s)
3. Vérifier l'intégrité et les droits d'accès
4. Valider via tests unitaires si applicable

### Restauration complète (sinistre total)
1. Monter le volume LaCie chiffré
2. Restaurer `data/` en priorité (données personnelles)
3. Restaurer `config/security/` (clés et paramètres)
4. Cloner le dépôt Git (code source)
5. Réinstaller les dépendances (`pip install -r requirements.txt`)
6. Valider via la suite de tests (`pytest tests/security_tests/`)
7. Documenter l'incident de restauration

---

## 7. Tests de restauration

| Date | Type | Résultat | Durée |
|---|---|---|---|
| 2026-06-18 | Test partiel (données) | ✅ Succès | 15 min |

**Fréquence requise :** Test trimestriel minimum

---

## 8. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.13 |

> **Cognitive Products Lab — Confidentiel interne**
