<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Politique de Gouvernance
TYPE     : Documentation gouvernance
REF      : ISO/IEC 27001:2022 — A.5.1, A.5.2, A.5.36
VERSION  : V1.1
CREATED  : 2026-07-10
UPDATED  : 2026-07-13
AUTHOR   : Cognitive Products Lab — Céline Rousselot (avec assistance Claude pour la rédaction)
STATUS   : Approuvé
============================================================
-->
# Politique de Gouvernance
## Cognitive Products Lab — ALFRED

> **Référence :** ISO/IEC 27001:2022 — A.5.1, A.5.2, A.5.36
> **Version :** 1.1 — 2026-07-13
> **Approbation :** Céline Rousselot — Fondatrice
> **Statut :** Approuvé

---

## 1. Pourquoi ce document existe

Cognitive Products Lab (CPL) applique, depuis les premières sessions de développement d'ALFRED, une discipline de gouvernance de fait : chaque nouveau composant technique (base de données, module IA, intégration tierce) déclenche systématiquement une réflexion réglementaire et une documentation de preuve — pas après coup, à la conception. Cette politique **formalise** cette pratique déjà existante en un cadre explicite, pour trois raisons concrètes :

1. **Combler avant que ça manque** — intégrer les exigences réglementaires dès la conception d'un traitement (plutôt qu'en réaction à un incident ou un audit) évite les manquements structurels et les corrections coûteuses a posteriori.
2. **Faciliter l'audit** — un projet où chaque décision de traitement de données est documentée, tracée et reliée à sa base légale se prête à un audit externe sans reconstruction a posteriori de l'historique.
3. **Crédibilité** — pour un projet en préparation de déploiement public porté par une fondatrice unique, une gouvernance documentée et cohérente (même hors obligation légale stricte, cf. §4) est un signal de maturité vérifiable, pas une déclaration d'intention.

Cette politique est le document **chapeau** : elle définit comment les quatre politiques du référentiel CPL s'articulent, qui décide de quoi, et comment ces décisions sont documentées et révisées.

---

## 2. Le référentiel de gouvernance CPL — quatre politiques, un système

| Politique | Question à laquelle elle répond | Document |
|---|---|---|
| **Politique de sécurité** | Comment protège-t-on les systèmes et les données ? | `docs/smsi/politique_securite.md` |
| **Politique de gestion des données** | Quelles données sont collectées, pourquoi, combien de temps, avec quels droits pour la personne concernée ? | `docs/gouvernance/politique_gestion_donnees.md` |
| **Politique de conformité réglementaire** | Quels textes s'appliquent (ou sont suivis volontairement), et où en est-on par rapport à chacun ? | `docs/gouvernance/cadre_reglementaire_CPL.md` |
| **Politique de gouvernance** *(ce document)* | Qui décide, comment les trois politiques ci-dessus sont maintenues à jour, et comment une décision de traitement de données se documente concrètement ? | `docs/gouvernance/politique_gouvernance.md` |

Ces quatre documents ne sont pas indépendants : une politique de sécurité sans politique de gestion des données ne dit rien sur *pourquoi* on protège telle donnée ; une politique de conformité sans gouvernance ne dit rien sur *qui* est responsable de la faire vivre. Le lien entre les trois premières et le contenu concret produit (AIPD, registres, procédures) suit toujours le même circuit, décrit au §5.

---

## 3. Rôles et autorité de décision

| Rôle | Titulaire actuel | Autorité |
|---|---|---|
| **Responsable de traitement / Fondatrice** | Céline Rousselot | Approbation finale de toute politique, décision d'ouverture de traitement de données réel (ex. inscription publique), arbitrage entre exigence légale et sobriété/proportionnalité |
| **DPO de fait** | Céline Rousselot | Conformité RGPD, conduite des AIPD, point de contact CNIL |
| **RSSI de fait** | Céline Rousselot | Politique de sécurité, gestion des incidents, conformité NIS2/ISO 27001 |
| **Assistance rédactionnelle et technique** | Claude (assistant Claude Code) | Rédaction, vérification croisée des textes réglementaires, implémentation technique des mesures — **jamais l'autorité de décision finale**, qui reste à la Fondatrice |

*Note : comme documenté dans `docs/smsi/raci_securite.md`, CPL est en phase mono-fondatrice — tous les rôles humains sont cumulés par Céline Rousselot. La séparation des rôles est prévue lors du recrutement (cf. roadmap `cadre_reglementaire_CPL.md` §4).*

**Principe explicite sur le rôle de l'assistance IA dans la gouvernance** : Claude peut rédiger, vérifier des textes contre les sources légales, identifier des gaps ou incohérences (voir exemples réels au §6), et proposer des corrections. Claude ne peut pas approuver une politique, ni décider qu'un traitement de données réel peut s'ouvrir au public — ces décisions restent, sans exception, celles de la Fondatrice. Toute production de Claude sur ces sujets est explicitement marquée comme en attente de validation tant qu'elle ne l'a pas été (cf. AIPD-ALFRED-002, §8 du document, en attente au moment de la rédaction de cette politique).

---

## 4. Principe : conformité au-delà du strict champ légal

CPL applique un principe de gouvernance explicite, au-delà de la seule obligation légale : **se conformer volontairement à un référentiel reconnu, même hors du champ d'application légal strict, quand cela sert la crédibilité et la solidité du projet.**

Exemple concret : NIS2 ne s'applique pas légalement à CPL (micro-entreprise, aucun secteur des Annexes I/II de la directive ne correspond à ALFRED — vérifié le 10/07/2026 sur le texte consolidé, cf. `docs/smsi/procedure_signalement_nis2.md` §1.1). CPL maintient néanmoins une procédure de signalement d'incidents alignée sur l'Art. 23 NIS2, pour la même raison qu'une entreprise hors du champ de DORA peut choisir de s'aligner sur ses exigences de résilience opérationnelle : la maturité de gouvernance qui en résulte est utile indépendamment de l'obligation.

Ce principe **ne s'applique pas en sens inverse** : une obligation légale réelle (RGPD, qui s'applique à tout responsable de traitement quelle que soit sa taille) n'est jamais traitée comme optionnelle sous prétexte de proportionnalité. La sobriété s'applique au *dimensionnement des moyens* (cf. bilan critique du PoC Hadoop, `docs/hadoop_poc_bilan.md`), jamais à l'*existence de l'obligation* elle-même.

---

## 5. Circuit de décision — d'un nouveau traitement de données à sa documentation

Tout nouveau traitement de données personnelles (nouvelle table, nouvelle collection, nouveau flux vers un tiers) suit ce circuit avant toute mise en production réelle :

1. **Conception** — le traitement est décrit : quelles données, quelle finalité, quelle base légale (Art. 6/9 RGPD).
2. **Évaluation du besoin d'AIPD** — si le traitement est nouveau, utilise une nouvelle technologie, ou présente un risque pour les droits des personnes (cf. critères Art. 35 RGPD, considérants 89-91), une AIPD est rédigée avant la mise en service réelle.
3. **Documentation de preuve** — le traitement est relié à un fichier de preuve concret (code, procédure, AIPD) référencé dans le registre de conformité (`dashboard/dashboard_conformite/dashboard_conformite.json` et `dashboard/dashboard_gouvernance/_manifest.json`).
4. **Statut honnête, jamais présumé conforme** — un traitement documenté mais non encore validé par la Fondatrice est marqué `en_cours`/`partial`, jamais `conforme`/`done`, tant que la validation explicite n'a pas eu lieu.
5. **Gate de mise en production** — si l'AIPD identifie des manquements (droits des personnes non implémentés, mesure de sécurité manquante), le traitement reste désactivé ou limité aux tests jusqu'à ce que les manquements soient corrigés ou explicitement acceptés par la Fondatrice.
6. **Révision** — chaque politique et chaque AIPD est revue annuellement, à chaque évolution réglementaire significative, et à chaque changement substantiel du traitement concerné.

---

## 6. Exemple réel — ce circuit appliqué (08-10/07/2026)

Ce circuit n'est pas théorique ; il vient d'être appliqué texte à l'appui sur l'extension d'architecture de données réalisée pour préparer le déploiement public d'ALFRED_WEB :

1. Conception de comptes utilisateurs PostgreSQL, préférences/conversations MongoDB, PoC Hadoop (08-09/07/2026).
2. AIPD-ALFRED-002 rédigée (10/07/2026, `docs/rgpd/aipd_comptes_deploiement_public.md`) — évaluation honnête des risques, identification de manquements réels (aucun droit des personnes implémenté côté ALFRED_WEB, pas de purge en cascade PostgreSQL→MongoDB, pas de rate limiting).
3. Intégrée au registre de conformité comme `RGPD-12`, statut `en_cours`/`partial` — **pas** `conforme`, reflétant honnêtement l'absence de validation. Au passage, une entrée préexistante (`RGPD-11`, AIPD données de santé) a été trouvée avec une preuve fantôme jamais vérifiée depuis sa création — corrigée vers le vrai fichier.
4. Gate explicite documenté dans le code (`ALFRED_WEB/auth/routes.py`) et cette politique : pas d'inscription publique réelle tant que les manquements identifiés au point 2 ne sont pas traités.
5. Score de conformité global recalculé en conséquence : 84% (Grade B), une baisse volontaire et cohérente avec le gate — pas un chiffre optimisé pour paraître bien.

C'est ce mécanisme — trouver et corriger les incohérences plutôt que les laisser dormir dans un registre — qui constitue la valeur réelle de cette gouvernance, plus que le score affiché à un instant donné.

---

## 5bis. Règle de gouvernance continue — toute brique de code déclenche la gouvernance de sa donnée

Le circuit du §5 s'applique à un *traitement de données* identifié comme tel. Cette règle **généralise le principe à toute brique ou modification de code**, sans attendre qu'un traitement de données personnelles soit explicitement reconnu comme tel — parce que dans la pratique, une nouvelle donnée technique (fichier de log, registre d'état, cache local) précède souvent la prise de conscience qu'elle mérite une gouvernance, pas l'inverse (cf. §6 : `access_decisions_history.json` était référencé dans un manifest depuis mai 2026 sans qu'aucun code ne l'alimente ni ne le gouverne, découvert seulement le 13/07/2026).

**Édictée le 13/07/2026, décision de la Fondatrice.**

Toute nouvelle brique ou modification substantielle du code doit désormais déclencher automatiquement :

1. **La mise à jour du manifeste et du registre des données** — `dashboard/dashboard_data/dashboard_data_manifest.json` (fichiers attendus par bloc) et `dashboard/dashboard_quality_data/data_quality_registry.json` (fiche de gouvernance par donnée).
2. **L'identification des nouvelles données créées, utilisées ou modifiées** — toute donnée persistante nouvelle (fichier, table, collection) obtient une fiche registre avant — ou au plus tard au moment de — sa mise en service.
3. **La classification, la sécurité, la rétention et les rôles d'accès** — chaque fiche renseigne `sensitivity_classification` (C1→C4), `security_level_planned` (1→5), `retention_period`, `authorized_roles` — pas de valeurs "à définir" laissées sans échéance sur une donnée déjà `utilisee`.
4. **La mise à jour documentaire** — en-têtes de fichiers (`Bloc XX.YY`, cf. `docs/ALFRED_BLOCS_REFERENCE.md`), politiques concernées (celle-ci, `politique_gestion_donnees.md` si donnée personnelle), et le plan d'action en cours s'il y en a un.
5. **L'exécution des tests et dashboards concernés** — `pytest` sur les tests touchés, régénération des dashboards impactés (`update_dashboard_data.py`, `update_quality_data_dashboard.py`, etc.) avant tout commit.
6. **La création d'une alerte si une information de gouvernance manque** — le moteur d'alertes de `dashboard_quality_data` (`donnee_non_documentee`, `donnee_non_definie`, `controle_acces_absent`, `acces_non_autorise`, `acces_role_inconnu`, `donnee_creee_non_utilisee`, `statut_obsolete`, `purge_en_retard`) est le mécanisme de détection : une fiche incomplète ou un accès incohérent avec le niveau de sécurité déclaré produit une alerte visible, jamais un silence.

**Statut honnête, même principe qu'au §5** : une fiche registre créée mais non revue par la Fondatrice reste `documented: false` ou porte une note explicite de vérification en attente — jamais présumée conforme par défaut.

**Précédent d'application** : la journalisation des décisions Zero Trust (`data/security/access_decisions_history.json`, cf. §6-bis ci-dessous) est le premier cas traité selon cette règle — code, fiche registre, tests et documentation livrés ensemble, pas en différé.

---

## 6bis. Exemple réel — cette règle appliquée (13/07/2026)

1. Audit du plan d'action qualité data (`dashboard/dashboard_quality_data/PLAN_ACTION_2026-07-13.md`, point C) : `data/security/access_decisions_history.json` attendu par le manifest depuis mai 2026, jamais alimenté par aucun module — écart réel entre l'avancement affiché du Bloc 20 (>100%, faussé) et l'état réel.
2. Décision de la Fondatrice : créer le fichier avec un vrai code producteur plutôt qu'un fichier vide décoratif.
3. `src/security/policy_decision_point.py::decide_access()` journalise désormais chaque décision Zero Trust (append-only, plafonné, best-effort — n'échoue jamais une décision d'accès si l'écriture échoue).
4. Fiche registre `DQ-045` mise à jour (classification, rétention, rôles, `access_exceptions` documentant pourquoi `AI_MODULE` peut écrire sans pouvoir lire).
5. 6 tests dédiés (`tests/security_tests/test_policy_decision_point_history.py`), tous verts avant commit.
6. `target_full_files_count` du Bloc 20 recalibré (181→200) pour que l'ajout de fichiers de gouvernance légitimes ne fasse plus mécaniquement dépasser 100% d'avancement affiché.

---

## 7. Gestion documentaire

| Règle | Application |
|---|---|
| Chaque politique/procédure a un header structuré (PROJECT/BLOCK/DOCUMENT/VERSION/CREATED/UPDATED/AUTHOR/STATUS) | Toutes les politiques `docs/smsi/` et `docs/gouvernance/` |
| Chaque modification substantielle incrémente la version et ajoute une ligne au tableau de révision | Voir §8 de chaque politique |
| Les références légales pointent vers le texte consolidé officiel (EUR-Lex, CNIL), pas une paraphrase non sourcée | Depuis le 10/07/2026 pour les documents révisés — à généraliser progressivement |
| Un document non encore approuvé par la Fondatrice porte un statut explicite (`En attente`, `Brouillon`) — jamais `Approuvé` par défaut | Tous documents |

---

## 8. Révision

Cette politique est révisée annuellement, à chaque évolution réglementaire majeure, et à chaque changement organisationnel significatif (recrutement, ouverture publique réelle du service).

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-07-10 | Céline Rousselot (rédaction assistée Claude) | Création — formalise le référentiel de gouvernance CPL (4 politiques), le circuit de décision AIPD, et le principe de conformité volontaire hors champ légal |
| 1.1 | 2026-07-13 | Céline Rousselot (rédaction assistée Claude) | Ajout §5bis/§6bis — règle de gouvernance continue : toute brique ou modification de code déclenche automatiquement mise à jour manifeste/registre, classification/sécurité/rétention/rôles, mise à jour documentaire, tests/dashboards, et alerte si information manquante. Opérationnalisée via `dashboard/dashboard_quality_data/` (registre + moteur d'alertes). |

> **Cognitive Products Lab — Confidentiel interne**
