# Chiffrement Intégral des Disques — Poste de Travail

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.7.8  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. État du chiffrement — PC Alfred

| Disque | Système | Solution | Algorithme | Statut |
|---|---|---|---|---|
| **Disque D:** (données ALFRED) | Windows 11 Pro | VeraCrypt | AES-256 | ✅ Chiffré |
| **Disque C:** (OS) | Windows 11 Pro | BitLocker | AES-128/256 | ✅ Actif (Windows) |
| **LaCie externe** (sauvegardes) | — | VeraCrypt | AES-256 | ✅ Chiffré |

---

## 2. Configuration VeraCrypt — Disque D:

- **Volume :** D:\ — Volume chiffré complet
- **Algorithme :** AES-256 en mode XTS
- **Hash :** SHA-512
- **Clé :** Mot de passe fort (>20 caractères) + fichier clé optionnel
- **Montage :** Au démarrage Windows (volume système secondaire)
- **Démontage automatique :** Après inactivité (10 min)

---

## 3. Procédures

### Montage / Démontage
- Montage : automatique via VeraCrypt au démarrage, authentification requise
- Démontage : automatique après inactivité ou arrêt PC
- Démontage d'urgence : raccourci clavier configuré

### Gestion du mot de passe VeraCrypt
- Mot de passe stocké hors-ligne uniquement (papier en lieu sûr)
- Rotation annuelle recommandée
- Jamais stocké en clair sur le système

### Sauvegarde des en-têtes VeraCrypt
- En-tête de volume sauvegardé hors-ligne (permet récupération si en-tête corrompu)

---

## 4. Vérification d'audit

| Vérification | Fréquence | Dernière vérif. |
|---|---|---|
| Vérification chiffrement actif D: | Mensuelle | 2026-06-18 |
| Test montage/démontage | Trimestrielle | 2026-06-18 |
| Vérification intégrité LaCie | Trimestrielle | 2026-06-18 |

---

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.7.8 |

> **Cognitive Products Lab — Confidentiel interne**
