<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Procédure de Consentement Renforcé — Art. 9 RGPD
TYPE     : Documentation Gouvernance RGPD
REF      : RGPD Art. 9.2.a — Consentement explicite données sensibles
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Procédure de Consentement Renforcé — Art. 9 RGPD
## Données sensibles — Cognitive Products Lab / ALFRED

> **Référence :** RGPD Art. 9.2.a — Consentement explicite données sensibles  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Pourquoi un consentement renforcé

L'Art. 9 RGPD interdit en principe le traitement des données dites "sensibles" (santé, opinions politiques, croyances religieuses, données biométriques, données génétiques, orientation sexuelle...). La seule exception applicable ici est le **consentement explicite de la personne concernée** (Art. 9.2.a).

ALFRED peut traiter des données sensibles lorsque l'utilisateur partage volontairement des informations de santé ou de bien-être psychologique dans ses conversations.

---

## 2. Exigences du consentement Art. 9

Le consentement doit être :
- **Libre** : sans pression ni condition à l'accès au service
- **Spécifique** : pour chaque catégorie de données sensibles
- **Éclairé** : l'utilisateur comprend ce qui est traité et pourquoi
- **Univoque / Explicite** : action affirmative claire (pas de case pré-cochée)
- **Révocable** : à tout moment, sans frais ni préjudice

---

## 3. Formulaire de consentement — Données de santé/bien-être

### Texte du consentement (à afficher lors de l'onboarding ou à la 1ère donnée sensible)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONSENTEMENT DONNÉES SENSIBLES — ART. 9 RGPD
Cognitive Products Lab / ALFRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALFRED peut mémoriser des informations que vous partagez
sur votre santé physique, votre bien-être mental, ou
votre état émotionnel pour personnaliser son assistance.

Ces données sont classifiées C3 (Confidentiel) et bénéficient
de protections renforcées :
  ✓ Chiffrement AES-256 au repos
  ✓ Accès MFA obligatoire
  ✓ Aucun partage sans votre accord explicite

Vos droits :
  → /forget pour effacer vos données à tout moment
  → /export pour obtenir une copie
  → /settings pour modifier vos préférences

En tapant OUI, vous consentez explicitement au traitement
de vos données de santé/bien-être par ALFRED.

Consentez-vous ? (OUI / NON)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 4. Enregistrement du consentement

Le consentement est enregistré dans `data/profile/user_profile.json` avec :
- Horodatage de l'accord
- Version du texte présenté
- Canal (onboarding / runtime)
- Possibilité de révocation

Structure JSON :
```json
{
  "consents": {
    "sensitive_data_art9": {
      "status": "granted",
      "date": "2026-06-18T11:00:00Z",
      "text_version": "1.0",
      "revocable_via": "/forget ou /settings"
    }
  }
}
```

---

## 5. Révocation du consentement

L'utilisateur peut révoquer son consentement à tout moment via :
- Commande `/forget sensible` — efface les données de santé
- Commande `/settings consent` — accès aux préférences de consentement

La révocation n'affecte pas la licéité du traitement antérieur.

---

## 6. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité RGPD Art. 9.2.a |

> **Cognitive Products Lab — Confidentiel interne**
