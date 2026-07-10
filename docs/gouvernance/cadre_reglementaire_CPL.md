# Cadre réglementaire — Cognitive Products Lab
## Référentiel de conformité données, gouvernance & cybersécurité

> Version 1.1 — 2026-07-10
> Statut : Document de référence — mise à jour annuelle obligatoire
> Ce document s'applique à **tous** les produits CPL : ALFRED, ALFRED CPL, ARTHUR
> Voir aussi : `docs/gouvernance/politique_gouvernance.md` (comment ce référentiel est appliqué et révisé)

---

## 1. Principes fondateurs

CPL applique par défaut la **règle du niveau le plus strict** : lorsque plusieurs
réglementations s'appliquent à un même traitement, c'est la plus contraignante
qui prime. Aucune optimisation réglementaire à la baisse n'est autorisée.

---

## 2. Réglementations applicables

### 2.1 Protection des données personnelles

#### RGPD — Règlement (UE) 2016/679
Base réglementaire principale. Principes obligatoires :
- **Licéité, loyauté, transparence** (art. 5.1.a)
- **Limitation des finalités** (art. 5.1.b) — usage strictement conforme à la finalité déclarée
- **Minimisation des données** (art. 5.1.c) — collecter uniquement le nécessaire
- **Exactitude** (art. 5.1.d)
- **Limitation de conservation** (art. 5.1.e)
- **Intégrité et confidentialité** (art. 5.1.f)
- **Responsabilité** (art. 5.2) — CPL doit pouvoir démontrer sa conformité

Obligations CPL :
- Registre des activités de traitement (art. 30) → `registre_traitements_CPL.md`
- AIPD pour traitements à risque élevé (art. 35)
- DPO désigné si traitement à grande échelle de données sensibles
- Notification CNIL sous 72h en cas de violation (art. 33)
- Privacy by Design & by Default (art. 25)

#### Loi Informatique et Libertés (LIL)
Loi n° 78-17 du 6 janvier 1978, modifiée par loi n° 2018-493 du 20 juin 2018
et ordonnance n° 2018-1125 du 12 décembre 2018.
- Renforce le RGPD en droit français
- Compétence de la **CNIL** (Commission Nationale de l'Informatique et des Libertés)
- Conditions spécifiques pour les données de santé, judiciaires et des mineurs

#### Recommandations CNIL applicables à CPL
- **Référentiel IA de la CNIL** (2023-2024) — systèmes d'IA et protection des données
- **Guide CNIL « IA générative »** — transparence, loyauté, droits des personnes
- **Recommandation CNIL sur les cookies et traceurs**
- **Référentiel CNIL sur la santé** — si ARTHUR collecte des données de santé enfants
- **Référentiel CNIL sur les mineurs** — exigences renforcées < 15 ans (droit français : seuil à 15 ans vs 16 ans RGPD)

> ⚠️ **Important ARTHUR** : En droit français, le seuil de consentement autonome d'un mineur
> est fixé à **15 ans** (art. 45 LIL) et non 16 ans comme le RGPD. CPL applique 15 ans.

---

### 2.2 Réglementation IA

#### EU AI Act — Règlement (UE) 2024/1689
En vigueur depuis août 2024. Calendrier d'application :
- Systèmes IA interdits : février 2025 (déjà applicable)
- Systèmes IA à haut risque : août 2026
- Autres dispositions : août 2027

**Classification CPL :**

| Produit | Cas d'usage | Niveau de risque AI Act | Obligations |
|---------|------------|------------------------|-------------|
| ALFRED | Assistant personnel adaptatif | Risque limité | Transparence Art. 50 (et non Art. 52, corrigé le 10/07/2026 — vérifié sur texte consolidé, cf. `docs/smsi/enregistrement_registre_ue_ia.md` §2) — informer l'utilisateur qu'il interagit avec une IA |
| ALFRED CPL | Aide à la décision RH/managériale | **Risque élevé potentiel** (annexe III) | AIPD IA, logging, supervision humaine, notice conformité |
| ARTHUR | Assistance éducative/santé enfants | **Risque élevé** (art. 6 + annexe III) | Toutes obligations haut risque |

**Obligations systèmes à risque élevé (ALFRED CPL + ARTHUR) :**
- Système de gestion des risques (art. 9)
- Gouvernance des données d'entraînement (art. 10)
- Documentation technique complète (art. 11)
- Journalisation automatique (art. 12)
- Transparence envers utilisateurs (art. 13)
- Surveillance humaine obligatoire (art. 14)
- Exactitude, robustesse, cybersécurité (art. 15)
- Enregistrement auprès de l'autorité nationale

---

### 2.3 Cybersécurité

#### Directive NIS2 — Directive (UE) 2022/2555
Transposée en droit français par loi n° 2023-703 du 1er août 2023.

**Vérifié le 10/07/2026 sur le texte consolidé** (https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32022L2555) : CPL **ne relève pas du champ d'application légal** de NIS2, ni par la taille (micro-entreprise, sous le seuil "moyenne entreprise" des Annexes de la recommandation 2003/361/CE) ni par le secteur (aucune des catégories des Annexes I/II — énergie, santé, infrastructure numérique, fournisseurs numériques, etc. — ne correspond à ALFRED). Détail complet : `docs/smsi/procedure_signalement_nis2.md` §1.1.

CPL maintient néanmoins volontairement les mesures et la procédure de signalement alignées sur NIS2 (même logique que DORA hors champ) — voir `docs/gouvernance/politique_gouvernance.md` §4 :
- Mesures de gestion des risques cybersécurité (art. 21)
- Notification des incidents sous 24h (alerte initiale) puis 72h (rapport détaillé) à l'ANSSI
- Responsabilité des organes dirigeants sur la cybersécurité

#### Recommandations ANSSI (Agence Nationale de la Sécurité des Systèmes d'Information)
Référentiels appliqués par CPL :
- **Guide ANSSI « Sécurité des systèmes d'IA »** (2024)
- **PSSIE** (Politique de Sécurité des Systèmes d'Information de l'État) — comme référence bonne pratique
- **RGS v2** (Référentiel Général de Sécurité) — mesures organisationnelles et techniques
- **Guide ANSSI « Développement sécurisé »** — bonnes pratiques code sécurisé
- **Guide ANSSI « Recommandations sur la protection des données à caractère personnel »**
- **SecNumCloud** — objectif de conformité pour tout hébergement cloud futur

**Mesures minimales ANSSI appliquées par CPL :**
1. Authentification forte (MFA) pour tout accès aux systèmes CPL
2. Gestion des identités et des accès (IAM) avec principe du moindre privilège
3. Chiffrement de bout en bout des données sensibles
4. Journalisation et surveillance (SOC si applicable)
5. Gestion des vulnérabilités et correctifs sous 72h pour critiques
6. Plan de continuité et de reprise d'activité (PCA/PRA)
7. Tests d'intrusion annuels
8. Formation cybersécurité de l'équipe (au minimum annuelle)

#### Cyber Resilience Act (CRA) — Règlement (UE) 2024/2847
En vigueur décembre 2024. Application progressive jusqu'en décembre 2027.
S'applique aux produits comportant des éléments numériques.
ALFRED/ARTHUR = produits logiciels avec composants connectés → CRA applicable.

Obligations CRA pour CPL :
- Cybersécurité par conception (secure by design)
- Gestion des vulnérabilités sur toute la durée de vie du produit
- Documentation de sécurité fournie avec le produit
- Signalement des vulnérabilités activement exploitées sous 24h à l'ENISA

---

### 2.4 Données de santé (ARTHUR)

Si ARTHUR collecte ou traite des données de santé d'enfants :

#### HDS — Hébergement de Données de Santé (art. L.1111-8 CSP)
- Obligation d'hébergement certifié HDS pour toutes données de santé
- Certification délivrée par organismes accrédités COFRAC
- CPL doit utiliser un hébergeur certifié HDS ou obtenir la certification

#### Référentiel de Sécurité SNDS / RNDS
Si connexion à des données de santé nationales : conformité au référentiel
de la CNIL et du Ministère de la Santé.

#### Convention relative aux droits de l'enfant (ONU, 1989)
Art. 16 : protection vie privée de l'enfant. Art. 17 : accès à une information
appropriée. Intégré dans la conception d'ARTHUR.

---

### 2.5 Gouvernance & responsabilité

#### ISO 27001:2022 — Sécurité de l'information
Norme internationale de référence. CPL vise la conformité ISO 27001 comme
objectif structurant, même sans certification formelle à ce stade.
Chapitres prioritaires : A.5 (Politiques), A.8 (Actifs), A.9 (Contrôle d'accès),
A.12 (Cryptographie), A.16 (Incidents), A.18 (Conformité).

#### ISO 29101:2018 — Cadre de référence pour la protection de la vie privée
Complète le RGPD avec un cadre technique d'architecture Privacy by Design.

#### ISO/IEC 27701:2019 — Système de management de la protection de la vie privée
Extension ISO 27001 pour la gestion de la vie privée (SMVP). Aligné RGPD.

#### Référentiel AFNOR NF Z74-400 (Accessibilité numérique)
Complémentaire à l'Accessibility Policy déjà dans `docs/gouvernance/`.

---

### 2.6 Extension d'architecture de données (juillet 2026)

Préparation au déploiement public d'ALFRED_WEB (08-09/07/2026) : premier système de comptes utilisateurs (PostgreSQL), extension MongoDB (préférences, scaffolding conversations), PoC Hadoop ciblé sur logs anonymisés. Détail technique et bilan critique (sobriété numérique) : mémoire projet `project_bdd_extension_deploiement_public`, `docs/hadoop_poc_bilan.md`. Couverture RGPD : AIPD-ALFRED-002 (`docs/rgpd/aipd_comptes_deploiement_public.md`), pas encore validée — gate actif tant que les droits des personnes ne sont pas implémentés côté ALFRED_WEB.

---

## 3. Matrice de conformité par produit

| Réglementation | ALFRED | ALFRED CPL | ARTHUR |
|---------------|--------|------------|--------|
| RGPD art. 6 (bases juridiques) | ✅ Obligatoire | ✅ Obligatoire | ✅ Obligatoire |
| RGPD art. 9 (données sensibles) | ⚠️ Profil psychologique | ⚠️ Profil psychologique | ✅ Données mineurs + santé |
| LIL / CNIL | ✅ Obligatoire | ✅ Obligatoire | ✅ Obligatoire + seuil 15 ans |
| Consentement parental | ❌ Non requis | ❌ Non requis | ✅ Obligatoire |
| EU AI Act — risque limité | ✅ | — | — |
| EU AI Act — risque élevé | — | ⚠️ À évaluer | ✅ Obligatoire |
| NIS2 | ⚠️ Si entité concernée | ⚠️ Si entité concernée | ⚠️ Si entité concernée |
| ANSSI recommandations | ✅ Obligatoire | ✅ Obligatoire | ✅ Obligatoire |
| CRA (Cyber Resilience Act) | ✅ Obligatoire | ✅ Obligatoire | ✅ Obligatoire |
| HDS | ❌ Non requis | ❌ Non requis | ✅ Si données santé |
| ISO 27001 (cible) | ✅ | ✅ | ✅ |

---

## 4. Organisation de la conformité chez CPL

### Rôles et responsabilités

| Rôle | Responsable | Périmètre |
|------|------------|-----------|
| **Responsable de traitement** | Céline Rousselot (Fondatrice CPL) | Tous traitements CPL |
| **DPO (Délégué Protection Données)** | À désigner formellement (obligatoire si traitement à grande échelle de données sensibles) | Conseil, contrôle, CNIL |
| **RSSI (Responsable Sécurité SI)** | À désigner | Cybersécurité, NIS2, ANSSI |
| **Responsable conformité IA** | À désigner | AI Act, CNIL IA |
| **Responsable produit** | Céline Rousselot | Implémentation Privacy by Design |

### Documents de gouvernance obligatoires

| Document | Statut | Révision |
|----------|--------|----------|
| Registre des activités de traitement (art. 30 RGPD) | `registre_traitements_CPL.md` | Annuelle + à chaque nouveau traitement |
| Politique de gestion des données | `docs/gouvernance/politique_gestion_donnees.md` | Annuelle |
| Politique de gouvernance | `docs/gouvernance/politique_gouvernance.md` | Annuelle |
| Schéma de traçabilité | `schema_tracabilite_donnees.json` | Annuelle |
| AIPD données de santé | `docs/rgpd/aipd_donnees_sante.md` (AIPD-ALFRED-001) | À chaque modification significative |
| AIPD comptes/déploiement public | `docs/rgpd/aipd_comptes_deploiement_public.md` (AIPD-ALFRED-002) — en attente de validation | À chaque modification significative |
| Politique de sécurité (SMSI) | `docs/smsi/politique_securite.md` | Annuelle |
| Procédure notification violation | `docs/smsi/procedure_notification_violation_72h.md` | Annuelle |
| Registre des violations | À créer | Tenu en continu |
| Procédure exercice des droits | À créer côté ALFRED_WEB (existe côté ALFRED_PC local, cf. AIPD-002 §5) | Annuelle |

### Calendrier de conformité

| Échéance | Action |
|----------|--------|
| T0 (maintenant) | Rédiger registre des traitements, schéma traçabilité, politique collecte |
| T0 + 1 mois | Nommer DPO et RSSI, rédiger PSSI formelle |
| T0 + 3 mois | AIPD pour ALFRED CPL et ARTHUR, premier test d'intrusion |
| T0 + 6 mois | Audit de conformité RGPD + AI Act, formation équipe |
| T0 + 12 mois | Révision annuelle de tous les documents, renouvellement tests de sécurité |
| Août 2026 | Conformité totale AI Act systèmes haut risque (ARTHUR, ALFRED CPL) |

---

## 5. Violations et incidents — procédure

### Violation de données personnelles (art. 33-34 RGPD)
1. **H+0** : Détection et confinement immédiat
2. **H+24** : Alerte interne, évaluation du risque
3. **H+72** : Notification CNIL (si risque pour les personnes) via portail CNIL
4. **Si risque élevé** : Notification des personnes concernées sans délai (art. 34)
5. **Documentation** : Inscription au registre des violations (obligatoire même si notification non requise)

### Incident cybersécurité (NIS2 / ANSSI)
1. **H+24** : Alerte initiale à l'ANSSI (si entité NIS2 concernée)
2. **H+72** : Rapport intermédiaire
3. **J+30** : Rapport final
4. **CRA** : Vulnérabilité activement exploitée → signalement ENISA sous 24h

---

## 6. Mise à jour et révision

Ce document doit être révisé :
- **Annuellement** (révision planifiée)
- **À chaque évolution réglementaire significative** (nouveau règlement, recommandation CNIL, guide ANSSI)
- **À chaque nouveau traitement de données** ou modification majeure d'un traitement existant
- **Après tout incident de sécurité**

Prochaine révision prévue : **juin 2027**

**Historique des révisions :**
| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-06-16 | Création |
| 1.1 | 2026-07-10 | NIS2 reformulé hors champ légal/conformité volontaire (vérifié sur texte consolidé) ; correction Art. 52→Art. 50 AI Act ; ajout §2.6 extension architecture données (comptes PostgreSQL, MongoDB, PoC Hadoop) ; mise à jour table documents de gouvernance (AIPD-002, nouvelles politiques) |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*  
*Fondatrice & Responsable de traitement : Céline Rousselot*
