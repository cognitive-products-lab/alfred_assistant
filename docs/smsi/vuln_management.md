# Gestion des Vulnérabilités — Scan et Patching

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.8  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Maintenir un niveau de sécurité adéquat en identifiant, évaluant et remédiant de manière proactive les vulnérabilités affectant ALFRED et l'infrastructure CPL.

---

## 2. Périmètre

- Code source ALFRED (dépendances Python, bibliothèques)
- OS Windows 11 Pro (PC Alfred)
- Infrastructure réseau (ER605, SG108E)
- Services tiers (OpenAI API)

---

## 3. Processus de gestion des vulnérabilités

### 3.1 Identification

| Source | Fréquence | Outil / Méthode |
|---|---|---|
| Dépendances Python | À chaque build + hebdomadaire | `pip audit` / `safety check` |
| OS Windows | Mensuelle | Windows Update automatique |
| Réseau / Firmware | Trimestrielle | Vérification manuelle TP-Link |
| CVE NIST | Mensuelle | Veille https://nvd.nist.gov |
| Tests de sécurité ALFRED | À chaque commit | Suite 651 tests (`pytest tests/security_tests/`) |

### 3.2 Classification (CVSS)

| Score CVSS | Sévérité | Délai de remédiation |
|---|---|---|
| 9.0 – 10.0 | Critique | 24 heures |
| 7.0 – 8.9 | Haute | 72 heures |
| 4.0 – 6.9 | Modérée | 7 jours |
| 0.1 – 3.9 | Faible | 30 jours |

### 3.3 Remédiation

1. Évaluer l'impact sur ALFRED (exploitabilité dans le contexte CPL)
2. Appliquer le patch/update si disponible
3. Si pas de patch : mesures compensatoires (isolation, désactivation)
4. Documenter dans le registre des vulnérabilités
5. Valider la remédiation (re-test)

---

## 4. Registre des vulnérabilités actives

| ID | Date détection | Composant | Sévérité | Statut | Résolution |
|---|---|---|---|---|---|
| _(aucune vulnérabilité critique active à ce jour)_ | — | — | — | — | — |

---

## 5. Commandes de scan

```bash
# Audit dépendances Python
pip audit

# Vérification sécurité avec safety
pip install safety && safety check

# Tests sécurité ALFRED
pytest tests/security_tests/ -v --tb=short
```

---

## 6. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.8 |

> **Cognitive Products Lab — Confidentiel interne**
