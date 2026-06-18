# Synthèse Gouvernance 360° — Module Profil IA Adaptative
## Cognitive Products Lab — ALFRED

> Version 1.0 — 2026-06-16  
> Périmètre : Profilage psychologique utilisateur + Adaptation comportementale ALFRED

---

## 1. Cartographie des données du module

### Types de données collectées

| ID | Données | Classification | Stockage | Durée | Chiffrement |
|----|---------|---------------|----------|-------|-------------|
| D01 | Réponses brutes questionnaires | SENSIBLES art.9 RGPD | Local uniquement | Jusqu'à traitement | Fernet AES-128 |
| D02 | Scores normalisés (0-100) | Sensibles | Local uniquement | Durée du compte + 3 mois | Fernet AES-128 |
| D03 | Paramètres ALFRED dérivés | Personnels | Local uniquement | Durée du compte + 3 mois | Fernet AES-128 |
| D04 | Profil AssessFirst (user_profile.json) | Sensibles art.9 | Local uniquement | Durée du compte + 3 mois | Aucun (non-sensible hors réponses) |
| D05 | Session state questionnaires | Techniques | Local uniquement | Session | Non |
| D06 | Audit trail accès profil | Traçabilité | Local uniquement | 5 ans (audit violations) | Non requis |
| D07 | Clé Fernet | CRITIQUE | Local uniquement — gitignored | Durée du compte | Protégée OS |

### Localisation des fichiers

```
LOCAL — appareil utilisateur uniquement :
  data/profile/user_profile.json          ← Profil AssessFirst + données dérivées
  data/profile/answers_template.json      ← Réponses en clair (transitoire)
  data/profile/answers_encrypted/*.enc    ← Réponses chiffrées (persistant)
  data/profile/keys/                      ← Clé de déchiffrement [gitignored]
  data/security/fernet.key               ← Clé principale [gitignored]

JAMAIS TRANSMIS :
  Aucune donnée de profil ne quitte l'appareil sans consentement explicite
  Aucune synchronisation cloud sans opt-in explicite de l'utilisateur
```

---

## 2. Conformité RGPD — Module profil

### Base juridique (Art. 6 + Art. 9)

| Traitement | Base juridique | Justification |
|-----------|---------------|---------------|
| Collecte réponses questionnaires | Art. 6.1.a + **Art. 9.2.a** | Consentement explicite requis — données psychologiques sensibles |
| Calcul scores + paramètres ALFRED | Art. 6.1.b | Exécution du service (contrat) |
| Stockage chiffré local | Art. 6.1.b + Art. 32 | Obligation de sécurité + service |
| Audit trail accès | Art. 6.1.f | Intérêt légitime sécurité + conformité |

**Point critique** : les données psychologiques (scores Big Five, stress, motivations) sont des **données de catégorie spéciale au sens de l'art.9 RGPD**. Le consentement doit être :
- **Explicite** : l'utilisateur doit affirmer positivement vouloir répondre
- **Éclairé** : l'utilisateur comprend ce qui est mesuré et comment c'est utilisé
- **Spécifique** : par questionnaire (pas un consentement global)
- **Révocable** : l'utilisateur peut supprimer ses données à tout moment

### Droits des personnes (Art. 12-23)

| Droit | Modalité dans ALFRED | Statut |
|-------|---------------------|--------|
| **Accès (Art. 15)** | Fonction "Voir mon profil" dans l'app | 📋 À implémenter |
| **Rectification (Art. 16)** | Refaire un questionnaire | ✅ Possible via reprise session |
| **Effacement (Art. 17)** | "Réinitialiser mon profil" + suppression clé Fernet | 📋 À implémenter |
| **Portabilité (Art. 20)** | Export JSON chiffré | 📋 À implémenter |
| **Opposition (Art. 21)** | Refus de répondre à tout moment | ✅ Natif (questionnaire optionnel) |
| **Limitation (Art. 18)** | Suspension du traitement sans suppression | 📋 À implémenter |

### AIPD (Art. 35) — Obligatoire pour T001

L'Analyse d'Impact sur la Protection des Données est **obligatoire** pour le traitement T001 car :
1. Données de catégorie spéciale (Art. 35.3.b) — profil psychologique
2. Profilage automatisé avec effets sur la personne (Art. 35.3.a)
3. Nouvelles technologies (IA adaptative)

**Fichier à créer** : `docs/audits/rgpd/rgpd_aipd_t001.md`  
**Échéance** : avant toute mise en production (Q3 2026)

---

## 3. Conformité AI Act — Module profil

### Classification du risque

| Produit | Niveau de risque | Justification |
|---------|-----------------|---------------|
| ALFRED (B2C) | **Risque élevé potentiel** | Profilage psychologique à effets comportementaux (Annexe III pt.4 — RH et gestion individuelle) |
| ALFRED CPL (B2B) | **Risque élevé** | Usage dans un contexte professionnel pour évaluation/accompagnement individus |
| ARTHUR | **Risque élevé** | Systèmes IA destinés aux mineurs |

### Exigences applicables (systèmes haut risque)

| Article | Exigence | Statut CPL |
|---------|---------|-----------|
| Art. 9 | Système de gestion des risques IA | ❌ Non réalisé |
| Art. 10 | Gouvernance données d'entraînement | ⚠️ Partiel |
| Art. 11 | Documentation technique | ⚠️ Partiel (`docs/profil_systeme/`) |
| Art. 12 | Journalisation et traçabilité | ⚠️ Partiel (`schema_tracabilite_donnees.json`) |
| Art. 13 | Transparence utilisateur | ❌ Non réalisé |
| Art. 14 | Supervision humaine | ⚠️ Partiel |
| Art. 17 | Qualité système de management qualité | ❌ Non réalisé |

**Échéance AI Act** : Août 2026 pour les systèmes haut risque déjà déployés.

---

## 4. Sécurité by Design — Mesures en place

### Chiffrement (Fernet AES-128-CBC)

```python
# Via cryptography library
from cryptography.fernet import Fernet

key = Fernet.generate_key()   # 256 bits → AES-128-CBC
f = Fernet(key)
token = f.encrypt(data)       # authentifié + chiffré
data_back = f.decrypt(token)  # vérifie l'intégrité avant déchiffrement
```

**Propriétés** :
- Chiffrement symétrique AES-128-CBC
- Authentification de message (HMAC-SHA256) — détecte toute altération
- IV aléatoire par chiffrement — pas de réutilisation
- Timestamp intégré — protection replay (configurable)

### Séparation des données et des clés

```
PRINCIPE : une faille sur les données ≠ compromis de la clé

data/profile/answers_encrypted/   ← données chiffrées (peut être committé théoriquement)
data/security/fernet.key          ← clé (JAMAIS commitée — gitignored)
```

La clé et les données ne doivent jamais être au même endroit, ni dans le même commit.

### Traçabilité des accès (Audit Trail)

Conformément à `docs/gouvernance/schema_tracabilite_donnees.json`, chaque donnée possède un audit trail obligatoire :

```json
{
  "audit_trail": {
    "creation": {
      "date": "2026-06-16T09:00:00Z",
      "qui": "utilisateur",
      "pourquoi": "passation questionnaire Q01"
    },
    "consultations": [
      {
        "date": "2026-06-17T08:30:00Z",
        "qui": "ALFRED (système)",
        "pourquoi": "personnalisation réponse conversation"
      }
    ],
    "modifications": [],
    "suppression": null
  }
}
```

### Règles absolues de sécurité

1. **JAMAIS** de données psychologiques dans les logs système (ni en clair, ni hashées)
2. **JAMAIS** de commit des réponses, des scores ou des clés (voir `.gitignore`)
3. **JAMAIS** de transmission hors de l'appareil sans consentement opt-in explicite
4. **TOUJOURS** chiffrer avant de persister (même localement)
5. **TOUJOURS** supprimer les données en clair après chiffrement
6. **TOUJOURS** valider les réponses avant persistance (`_validate_answer`)
7. **TOUJOURS** journaliser les accès au profil avec horodatage UTC

---

## 5. SOC — Surveillance du module profil

### Événements surveillés (V1)

| Événement | Niveau | Action |
|-----------|--------|--------|
| Tentative d'accès au fichier de clé | ALERTE | Log + notification |
| Réponse hors-échelle répétée | INFO | Log |
| Questionnaire complété | INFO | Log + calcul score |
| Profil exporté | INFO | Log + confirmation utilisateur |
| Profil supprimé | INFO | Log + confirmation 2 étapes |
| Erreur déchiffrement (clé incorrecte) | ALERTE | Log + blocage temporaire |
| Modification du fichier clé | CRITIQUE | Log + invalidation session |

### Format de log standardisé

```json
{
  "timestamp": "2026-06-16T09:00:00Z",
  "niveau": "INFO",
  "source": "profile_module",
  "evenement": "questionnaire_complete",
  "details": {
    "questionnaire_id": "q01_bien_etre_subjectif",
    "items_repondus": 14,
    "duree_min": 8
  },
  "utilisateur_hash": "sha256_pseudonyme",
  "action_requise": null
}
```

**Note** : Le log ne contient JAMAIS de valeur de réponse ni de score.

---

## 6. Périodicité et re-test

### Calendrier de re-passation recommandé

```
Mois 1  → Passation initiale complète (toutes les dimensions)
Mois 2  → Q07 (engagement/burnout) + Q05 (stress)
Mois 3  → Q07 + Q05 + Q04 (chronotype si changement saisonnier)
Mois 6  → Q02 (IE) + Q08 (communication) + re-évaluation
Mois 12 → Q01 (Big Five) + Q03 (valeurs) + Q06 (RIASEC) + rapport annuel

Événement de vie → relance Q05 (stress) + Q07 (engagement) + Q00 (qualitatif)
```

### Alertes de dérive

Si PSS > 12 ET UWES < 2.5 lors du re-test mensuel :
- ALFRED active le mode "soutien renforcé"
- check_in_frequency → "quotidien"
- challenge_level → "confort"
- Message optionnel d'ALFRED sur la gestion du stress (non médical)

---

## 7. Responsabilités (RACI simplifié)

| Activité | Utilisateur | DPO/RSSI (Céline) | ALFRED (IA) | Développeur |
|----------|-------------|------------------|------------|------------|
| Consentement questionnaire | **R/A** | I | I | I |
| Passation questionnaire | **R** | I | C | I |
| Calcul scores | I | I | **R/A** | C |
| Chiffrement données | I | A | **R** | C |
| Consultation profil | **R** | I | **R** | I |
| Mise à jour profil | **R** | I | **R** | I |
| Suppression données | **R/A** | I | C | I |
| Audit trail | I | **R/A** | R | C |
| Maintenance code | I | A | I | **R** |
| Mise à jour réglementaire | I | **R/A** | I | C |

R = Responsible · A = Accountable · C = Consulted · I = Informed

---

## 8. Documents associés

| Document | Chemin | Statut |
|----------|--------|--------|
| Registre des traitements (art.30) | `docs/gouvernance/registre_traitements_CPL.md` | ✅ Complet |
| Cadre réglementaire complet | `docs/gouvernance/cadre_reglementaire_CPL.md` | ✅ Complet |
| Cartographie des données | `docs/gouvernance/cartographie_donnees_CPL.md` | ⚠️ Partiel |
| Schéma traçabilité | `docs/gouvernance/schema_tracabilite_donnees.json` | ✅ Complet |
| SOC CPL | `docs/gouvernance/soc_cpl.md` | ✅ Complet |
| **AIPD T001** | `docs/audits/rgpd/rgpd_aipd_t001.md` | ❌ À créer |
| **PSSI formelle** | `docs/gouvernance/PSSI_formelle.md` | ❌ À créer |
| Sécurité données (profil) | `docs/profil_systeme/securite_donnees.md` | ✅ Complet |
| Chantier audit certification | `docs/gouvernance/CHANTIER_AUDIT_CERTIFICATION.md` | ✅ Complet |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*  
*Révision recommandée : semestrielle + à chaque changement réglementaire majeur*
