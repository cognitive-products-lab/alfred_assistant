<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Procédure Signalement Incidents NIS2 — Art. 23
TYPE     : Documentation SMSI
REF      : Directive (UE) 2022/2555 — NIS2
VERSION  : V1.1
CREATED  : 2026-06-18
UPDATED  : 2026-07-10
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Procédure de Signalement d'Incidents — NIS2 Art. 23

> **Référence :** Directive (UE) 2022/2555 — NIS2 Art. 23, texte consolidé :
> https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32022L2555
> **Version :** 1.1 — 2026-07-10
> **Propriétaire :** Cognitive Products Lab — Céline Darras
> **Statut :** Approuvé

---

## 1. Contexte NIS2

La Directive NIS2 impose aux entités essentielles et importantes de signaler les incidents significatifs à l'autorité nationale compétente (en France : **ANSSI** et **CERT-FR**).

### 1.1 Analyse du champ d'application — CPL est hors champ légal

Vérification faite le 10/07/2026 sur le texte consolidé de la directive (référence ci-dessus), pas sur une estimation :

**Critère de taille (considérant 7, renvoyant à la recommandation 2003/361/CE, art. 2)** : NIS2 s'applique par principe aux entités qui constituent des **entreprises moyennes ou plus grandes** (≥ 50 salariés ou > 10 M€ de chiffre d'affaires/bilan annuel), sauf exceptions listées pour les micro/petites entreprises jouant "un rôle essentiel" pour un secteur donné. Cognitive Products Lab est une **micro-entreprise** (fondatrice seule).

**Critère sectoriel (Annexes I et II)** : le champ d'application est une liste fermée de secteurs — énergie, transport, banque, infrastructures des marchés financiers, santé, eau potable/eaux usées, **infrastructure numérique** (points d'échange internet, DNS, cloud, centres de données, CDN, prestataires de confiance, réseaux de communications électroniques), gestion TIC interentreprises, administration publique, espace, services postaux, gestion des déchets, chimie, agroalimentaire, fabrication (dispositifs médicaux, électronique, machines, véhicules), et **fournisseurs numériques** (places de marché en ligne, moteurs de recherche en ligne, plateformes de réseaux sociaux). ALFRED_WEB (site vitrine + comptes utilisateurs en développement) et ALFRED_PC (assistant local-first) ne correspondent à aucune de ces catégories.

**Conclusion :** CPL/ALFRED **ne relève pas du champ d'application légal de NIS2**, ni par la taille ni par le secteur, à la date de cette analyse.

### 1.2 Pourquoi cette procédure existe quand même — conformité volontaire

Cette procédure reste maintenue et appliquée **volontairement**, indépendamment de l'obligation légale — la même logique que l'approche retenue pour d'autres textes hors champ actuel (ex. DORA pour le secteur financier) : se mettre en conformité sur des référentiels reconnus, même sans y être contraint, sert deux objectifs concrets pour un projet en préparation de déploiement public :

1. **Crédibilité** — démontrer, preuves à l'appui (cette procédure, `docs/smsi/`, dashboard conformité), une maturité de gouvernance alignée sur les standards européens actuels, utile face à un jury, des utilisateurs, ou de futurs partenaires/investisseurs.
2. **Anticipation** — si ALFRED_WEB grandit (déploiement public réel, hébergement cloud tiers pouvant le faire basculer dans la catégorie "fournisseur numérique"), la procédure est déjà opérationnelle plutôt qu'à improviser sous contrainte de délai légal.

**Seuil de réexamen :** revalider ce statut si CPL dépasse le seuil de micro-entreprise, ou si ALFRED_WEB devient un service d'informatique en nuage, un hébergeur de données/DNS, ou toute autre catégorie de l'Annexe I/II.

---

## 2. Critères d'incident significatif (Art. 23 NIS2)

Un incident est significatif si :
- Il a causé ou est susceptible de causer une **perturbation opérationnelle grave**
- Il a causé des **pertes financières importantes** pour l'entité
- Il a affecté ou est susceptible d'affecter **d'autres personnes physiques ou morales** de manière considérable

---

## 3. Délais de notification (Art. 23.4)

| Délai | Obligation |
|---|---|
| **24 heures** | Alerte précoce à l'ANSSI/CERT-FR (si suspicion d'acte illicite ou impact transfrontalier) |
| **72 heures** | Notification d'incident complète avec évaluation initiale (gravité, indicateurs) |
| **1 mois** | Rapport final complet avec cause racine, mesures prises, impact |

---

## 4. Canal de signalement

**CERT-FR :** https://www.cert.ssi.gouv.fr/contact/  
**ANSSI — portail signalement :** https://www.ssi.gouv.fr  
**Email urgence CERT-FR :** cert-fr.cossi@ssi.gouv.fr  
**Téléphone CERT-FR :** +33 1 71 75 84 68

---

## 5. Contenu de la notification initiale (72h)

1. Identité de l'entité notifiante (CPL — Cognitive Products Lab)
2. Date et heure de détection
3. Description de l'incident (nature, systèmes affectés)
4. Évaluation préliminaire de la gravité et de l'impact
5. Mesures de containment déjà prises
6. Existence d'une violation de données personnelles (lien RGPD)

---

## 6. Lien avec la procédure incidents ALFRED

Cette procédure s'articule avec :
- `procedure_incidents.md` — procédure générale de gestion des incidents
- `procedure_notification_violation.md` — notification CNIL si données personnelles
- `data/security/incident_register.json` — registre centralisé

---

## 7. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité NIS2 Art. 23 |
| 1.1 | 2026-07-10 | Claude (assistant) | Vérification du champ d'application sur le texte consolidé (§1.1) — hors champ confirmé (taille + secteur). Reformulation en conformité volontaire assumée (§1.2), même logique que DORA. |

> **Cognitive Products Lab — Confidentiel interne**
