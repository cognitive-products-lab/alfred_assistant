# Registre des activités de traitement — Cognitive Products Lab
## Conformité RGPD art. 30

> Version 1.0 — 2026-06-16  
> Responsable de traitement : Céline Rousselot — Cognitive Products Lab  
> Obligation légale : art. 30 RGPD (obligatoire pour tout organisme traitant des données)  
> Mise à jour : à chaque nouveau traitement ou modification

---

## Informations sur le responsable de traitement

| Champ | Valeur |
|-------|--------|
| **Dénomination** | Cognitive Products Lab (CPL) |
| **Représentant légal** | Céline Rousselot |
| **Adresse** | À compléter |
| **Email contact privacy** | À définir (ex: privacy@cognitive-products-lab.com) |
| **DPO** | À désigner formellement |

---

## Traitement #001 — Profilage psychologique utilisateur ALFRED

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T001 |
| **Nom** | Profilage psychologique adaptatif utilisateur |
| **Produit** | ALFRED (B2C) |
| **Date création** | 2026-06-16 |
| **Dernière mise à jour** | 2026-06-16 |
| **Mise à jour par** | Céline Rousselot |
| **Finalité** | Personnaliser le comportement d'ALFRED selon le profil psychologique de l'utilisateur (personnalité, motivations, style cognitif, résilience, valeurs) pour améliorer l'expérience et l'adaptation de l'assistant |
| **Base juridique** | Art. 6.1.a RGPD (consentement explicite) + Art. 9.2.a RGPD (consentement explicite pour données sensibles) |
| **Catégories de données** | Données psychologiques (profil personnalité, scores motivationnels, style cognitif), données comportementales déduites — CATÉGORIE SPÉCIALE art. 9 |
| **Catégories de personnes** | Utilisateurs adultes (≥ 18 ans) du produit ALFRED |
| **Destinataires** | Utilisateur seul — aucune transmission à des tiers |
| **Transfert hors UE** | NON |
| **Durée conservation** | Durée du compte + 3 mois après fermeture |
| **Lieu de stockage** | Appareil local de l'utilisateur uniquement |
| **Mesures de sécurité** | Chiffrement Fernet (AES-128-CBC), clé séparée des données, accès local uniquement, audit trail chiffré |
| **AIPD requise** | OUI — données psychologiques sensibles (art. 35.3.b RGPD) |
| **Sous-traitants** | Aucun |

---

## Traitement #002 — Adaptation comportementale dynamique ALFRED

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T002 |
| **Nom** | Mémoire adaptative et personnalisation dynamique |
| **Produit** | ALFRED, ALFRED CPL |
| **Date création** | 2026-06-16 |
| **Finalité** | Adapter en temps réel le ton, la structure et le contenu des réponses d'ALFRED en fonction de l'état émotionnel détecté et des préférences apprises de l'utilisateur |
| **Base juridique** | Art. 6.1.b RGPD (exécution du contrat de service) + consentement pour données émotionnelles |
| **Catégories de données** | Historique conversationnel, préférences apprises, état émotionnel détecté, contexte d'usage |
| **Catégories de personnes** | Utilisateurs ALFRED et ALFRED CPL |
| **Destinataires** | Utilisateur seul |
| **Transfert hors UE** | NON |
| **Durée conservation** | 12 mois glissants (configurable) |
| **Lieu de stockage** | Appareil local uniquement |
| **Mesures de sécurité** | Chiffrement Fernet, local-only, pas d'accès réseau pour ces données |
| **AIPD requise** | OUI — profilage comportemental (art. 35.3.a) |
| **Sous-traitants** | Aucun |

---

## Traitement #003 — Collecte de métriques d'usage anonymisées (opt-in)

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T003 |
| **Nom** | Métriques d'usage produit anonymisées |
| **Produit** | ALFRED, ALFRED CPL, ARTHUR |
| **Date création** | 2026-06-16 |
| **Finalité** | Comprendre l'utilisation des produits CPL pour améliorer les fonctionnalités, corriger les bugs et orienter la roadmap — uniquement sur données agrégées et anonymisées |
| **Base juridique** | Art. 6.1.a RGPD (consentement explicite opt-in) |
| **Catégories de données** | Métriques d'usage (fréquence, fonctionnalités utilisées, durée sessions, performances techniques) — anonymisées et agrégées, sans identifiant direct ou indirect |
| **Catégories de personnes** | Utilisateurs ayant consenti à ce traitement (opt-in) |
| **Destinataires** | Équipe produit CPL (données agrégées uniquement) |
| **Transfert hors UE** | NON |
| **Durée conservation** | 24 mois |
| **Lieu de stockage** | Serveur CPL — France |
| **Mesures de sécurité** | Anonymisation irréversible avant collecte, agrégation, chiffrement serveur AES-256, accès restreint équipe produit |
| **AIPD requise** | NON (données anonymisées — hors champ RGPD après anonymisation) |
| **Sous-traitants** | Hébergeur serveur FR (DPA à signer) |

---

## Traitement #004 — Profilage enfant ARTHUR (données mineur)

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T004 |
| **Nom** | Profil adaptatif enfant ARTHUR |
| **Produit** | ARTHUR |
| **Date création** | 2026-06-16 |
| **Finalité** | Adapter les interactions d'ARTHUR au profil émotionnel, aux besoins et aux centres d'intérêt de l'enfant utilisateur, dans le cadre défini et supervisé par le représentant légal |
| **Base juridique** | Art. 9.2.a RGPD + Art. 8 RGPD + Art. 45 LIL (consentement écrit du représentant légal obligatoire, seuil 15 ans en droit français) |
| **Catégories de données** | Profil comportemental enfant, bien-être émotionnel simplifié, centres d'intérêt, données de santé si collectées — CATÉGORIES SPÉCIALES art. 9 + données mineur |
| **Catégories de personnes** | Enfants < 15 ans (droit français) — représentant légal en tant que responsable du consentement |
| **Destinataires** | Représentant légal + enfant sous supervision parentale — aucun tiers |
| **Transfert hors UE** | NON ABSOLU |
| **Durée conservation** | Jusqu'aux 18 ans de l'enfant + possibilité de transfert à l'enfant devenu majeur ou suppression à sa demande |
| **Lieu de stockage** | Appareil familial local uniquement |
| **Mesures de sécurité** | Chiffrement Fernet, authentification forte représentant légal, séparation stricte profil enfant/adulte, audit trail parental, HDS si données santé |
| **AIPD requise** | OUI OBLIGATOIRE — données mineur sensibles, risque élevé (art. 35 RGPD + recommandation CNIL) |
| **Sous-traitants** | Aucun |
| **Note spéciale** | Avis professionnel de santé pédiatrique requis avant mise en production. Consultation CNIL recommandée. |

---

## Traitement #005 — Contrôle parental ARTHUR

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T005 |
| **Nom** | Système de contrôle parental et supervision ARTHUR |
| **Produit** | ARTHUR |
| **Date création** | 2026-06-16 |
| **Finalité** | Permettre au représentant légal de configurer, surveiller et adapter l'environnement numérique d'ARTHUR pour l'enfant dans le respect de son développement et de sa sécurité |
| **Base juridique** | Art. 6.1.b (exécution du contrat avec le représentant légal) + obligation légale de protection des mineurs |
| **Catégories de données** | Paramètres de contrôle parental, logs d'accès résumés (non verbatim), alertes de contenu |
| **Catégories de personnes** | Représentants légaux d'enfants utilisateurs d'ARTHUR |
| **Destinataires** | Représentant légal uniquement |
| **Transfert hors UE** | NON |
| **Durée conservation** | Durée du compte ARTHUR + 3 mois |
| **Lieu de stockage** | Appareil familial local |
| **Mesures de sécurité** | Authentification forte (mot de passe distinct), chiffrement Fernet, accès séparé de l'interface enfant |
| **AIPD requise** | OUI — traitement de données relatives à des mineurs |
| **Sous-traitants** | Aucun |

---

## Traitement #006 — Logs techniques et gestion des incidents

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T006 |
| **Nom** | Journalisation sécurité et technique |
| **Produit** | ALFRED, ALFRED CPL, ARTHUR |
| **Date création** | 2026-06-16 |
| **Finalité** | Assurer la sécurité, la disponibilité et l'intégrité des systèmes CPL — détecter les incidents de sécurité, déboguer les anomalies techniques |
| **Base juridique** | Art. 6.1.c (obligation légale — NIS2, RGPD art. 32) + Art. 6.1.f (intérêt légitime sécurité) |
| **Catégories de données** | Logs techniques pseudonymisés (événements système, erreurs, connexions hashées), audit trail sécurité |
| **Catégories de personnes** | Utilisateurs des produits CPL (données pseudonymisées) |
| **Destinataires** | RSSI CPL, DPO si incident de données |
| **Transfert hors UE** | NON |
| **Durée conservation** | 12 mois (logs techniques) / 24 mois (logs sécurité) / 5 ans (audit trail violations) |
| **Lieu de stockage** | Serveur CPL — France (logs serveur) + appareil local (logs locaux) |
| **Mesures de sécurité** | Pseudonymisation (IP hashées, identifiants pseudonymisés), chiffrement, accès RSSI uniquement, intégrité vérifiable |
| **AIPD requise** | NON (traitement limité, base légale solide, mesures de protection robustes) |
| **Sous-traitants** | Hébergeur FR (DPA signé) |

---

## Traitement #007 — Feedback volontaire utilisateur (opt-in)

| Champ | Valeur |
|-------|--------|
| **ID traitement** | CPL-T007 |
| **Nom** | Collecte de feedback utilisateur |
| **Produit** | ALFRED, ALFRED CPL, ARTHUR |
| **Date création** | 2026-06-16 |
| **Finalité** | Recueillir les retours volontaires des utilisateurs sur l'expérience produit pour orienter les améliorations |
| **Base juridique** | Art. 6.1.a RGPD (consentement — acte positif de soumission) |
| **Catégories de données** | Avis, notes, commentaires libres soumis volontairement — pseudonymisés |
| **Catégories de personnes** | Utilisateurs ayant choisi de soumettre un feedback |
| **Destinataires** | Équipe produit CPL |
| **Transfert hors UE** | NON |
| **Durée conservation** | 36 mois |
| **Lieu de stockage** | Serveur CPL — France |
| **Mesures de sécurité** | Pseudonymisation, chiffrement serveur, accès restreint |
| **AIPD requise** | NON |
| **Sous-traitants** | Hébergeur FR (DPA signé) |

---

## Registre des violations de données

*(Tenu en continu — voir procédure Playbook 1 dans `soc_cpl.md`)*

| ID | Date détection | Nature | Données concernées | Personnes concernées | Notif. CNIL | Notif. personnes | Résolution | Mesures correctives |
|----|---------------|--------|-------------------|---------------------|------------|-----------------|-----------|---------------------|
| — | — | — | — | — | — | — | — | — |

---

## Exercice des droits des personnes

*(Journal des demandes reçues et traitées)*

| ID | Date demande | Type de droit | Produit | Traitement ciblé | Date réponse | Résultat |
|----|-------------|---------------|---------|------------------|-------------|---------|
| — | — | — | — | — | — | — |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*  
*Révision obligatoire : annuelle + à chaque nouveau traitement*
