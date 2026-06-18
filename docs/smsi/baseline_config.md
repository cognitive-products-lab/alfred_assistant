# Gestion de Configuration Sécurisée — Baseline

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.9  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Définir et maintenir une configuration de référence (baseline) sécurisée pour tous les composants d'ALFRED, afin de détecter les dérives de configuration.

---

## 2. Baseline Configuration ALFRED

### 2.1 Fichiers de configuration de sécurité

| Fichier | Contenu | Classification |
|---|---|---|
| `config/security/security_settings.json` | Paramètres globaux sécurité, classification C1→C4 | C3 |
| `config/security/roles_permissions.json` | RBAC — rôles et permissions | C3 |
| `config/security/network_policy.json` | Politique réseau | C3 |
| `config/features.json` | Fonctionnalités activables/désactivables | C2 |

### 2.2 Paramètres de référence (baseline)

```json
{
  "security_baseline": {
    "mfa_required": true,
    "encryption_algorithm": "AES-256-Fernet",
    "key_rotation_days": 90,
    "session_timeout_minutes": 30,
    "max_login_attempts": 3,
    "audit_log_enabled": true,
    "behavioral_detection_enabled": true,
    "output_filter_enabled": true,
    "min_password_length": 20,
    "classification_levels": ["C1", "C2", "C3", "C4"]
  }
}
```

---

## 3. Contrôle des dérives de configuration

### 3.1 Méthode

- **Git diff** : Toute modification de fichier de configuration est tracée via Git
- **Tests automatisés** : Les tests de sécurité (651 tests) valident les paramètres critiques
- **Revue mensuelle** : Comparaison manuelle avec la baseline documentée ici

### 3.2 Processus de modification de configuration

1. Justification documentée de la modification
2. Test en environnement dev (branche Git)
3. Revue (auto-revue en V1, revue pair en V2+)
4. Merge avec message de commit explicite
5. Mise à jour de ce document si baseline modifiée

---

## 4. Historique des modifications baseline

| Date | Modification | Justification | Commit Git |
|---|---|---|---|
| 2026-06-18 | Baseline initiale créée | Conformité ISO A.8.9 | — |

---

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.9 |

> **Cognitive Products Lab — Confidentiel interne**
