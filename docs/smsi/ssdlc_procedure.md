# Cycle de Développement Sécurisé (SSDLC)

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.25  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Phases SSDLC ALFRED

### Phase 1 — Exigences Sécurité
- Identification des exigences de sécurité dès la conception
- Classification des données traitées (C1→C4)
- Analyse de risques préliminaire
- Référentiel : RGPD, ISO 27001, EU AI Act, NIS2

### Phase 2 — Conception (Privacy & Security by Design)
- Architecture Zero Trust
- Principe du moindre privilège
- Chiffrement par défaut des données sensibles
- AIPD si données sensibles Art. 9 concernées

### Phase 3 — Développement
- Revue de code sécurité (auto-revue V1, pair-review V2+)
- Pas de secrets dans le code source (variables d'environnement)
- Gestion des dépendances : versions fixées, audit régulier
- Conventions de nommage sécurisé

### Phase 4 — Tests
- Suite de tests de sécurité automatisés (651 tests A+)
- Tests unitaires de chaque module de sécurité
- `pytest tests/security_tests/ -v`
- Vérification que tous les tests passent avant merge

### Phase 5 — Déploiement
- Pas de déploiement si tests de sécurité échouent
- Vérification de la configuration (baseline)
- Rotation des clés si nécessaire
- Documentation des changements

### Phase 6 — Maintenance
- Monitoring continu (`behavioral_detector.py`, `audit_trail.py`)
- Gestion des vulnérabilités (`vuln_management.md`)
- Mises à jour régulières des dépendances
- Revue de code périodique

---

## 2. Checklist Sécurité Développeur (pré-commit)

```
☐ Aucun secret ou clé en clair dans le code
☐ Données sensibles chiffrées si stockées
☐ Entrées utilisateur validées et sanitisées
☐ Pas de SQL injection possible (si applicable)
☐ Logs ne contiennent pas de données personnelles en clair
☐ Tests de sécurité passent (pytest tests/security_tests/)
☐ Dépendances auditées (pip audit)
```

---

## 3. Outils SSDLC

| Outil | Usage | Fréquence |
|---|---|---|
| Git + GitHub | Versioning, code review | Continu |
| pytest | Tests de sécurité automatisés | Chaque commit |
| pip audit / safety | Audit dépendances | Hebdomadaire |
| Claude Code | Revue de code assistée IA | Chaque module |

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.25 |

> **Cognitive Products Lab — Confidentiel interne**
