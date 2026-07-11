# ALFRED CPL — Scénario de démonstration

> Source : `docs/alfred_cpl_fonctions_et_demo.docx` (intégré le 10/07/2026).
> Objectif : prouver la valeur métier d'ALFRED CPL en quelques minutes, avec un parcours cohérent, crédible et sécurisé — pas besoin de montrer cinquante fonctions.
> Spécification complète des fonctionnalités : [ALFRED_CPL_SPEC.md](../docs/roadmap/ALFRED_CPL_SPEC.md).

## Ce qu'ALFRED CPL doit impérativement démontrer

### 1. Identifier l'utilisateur et appliquer ses droits

ALFRED doit reconnaître le profil connecté et adapter immédiatement ce qu'il peut consulter.

- Utilisateur : « Chef de projet ».
- Accès autorisé : procédures projets, modèles, normes internes, documents de gouvernance.
- Accès refusé : contenus RH ou financiers sensibles.

**Message démontré :** ALFRED ne donne pas accès à toute la connaissance de l'entreprise. Il applique les habilitations selon une logique Zero Trust et de moindre privilège.

### 2. Répondre à une question métier à partir de la base de connaissances

Requête : *« Quelles sont les étapes internes pour lancer un nouveau projet ? »*

La réponse doit être :
- claire ;
- structurée ;
- adaptée au contexte du client ;
- fondée sur les documents internes ;
- sans partir vers une réponse générique hors sujet.

Elle doit citer : le document source, sa version, sa date, éventuellement son propriétaire.

> « Cette réponse s'appuie sur la procédure PMO-07, version 3.2, validée le 12 juin 2026. »

Essentiel pour démontrer qu'ALFRED n'invente pas une procédure.

### 3. Croiser le socle métier et les règles propres au client

Requête : *« Prépare-moi un plan de cadrage projet conforme à notre méthode interne. »*

ALFRED mobilise :
- les principes classiques de gestion de projet ;
- le modèle de cadrage propre au client ;
- les exigences internes de sécurité ;
- les étapes de validation de l'organisation.

**Message démontré :** ALFRED ne se contente pas de réciter une méthode. Il la contextualise selon les règles de l'entreprise.

### 4. Détecter une information absente, obsolète ou contradictoire

L'une des fonctions les plus fortes pour la crédibilité.

Requête : *« Quelle est la procédure actuelle de gestion des incidents ? »*

Si deux documents se contredisent :

> « Deux versions semblent actuellement disponibles. La version 4.1 est plus récente, mais la version 3.8 est encore référencée dans un document secondaire. Une validation par le propriétaire du processus est recommandée. »

Si la source manque :

> « Je ne dispose pas d'une source interne suffisamment fiable pour confirmer cette information. »

Cette capacité vaut beaucoup plus qu'une réponse brillante mais fausse.

### 5. Préparer un livrable métier

ALFRED doit montrer qu'il ne fait pas que répondre — il aide à produire :
- note de cadrage ;
- plan d'action ;
- trame de réunion ;
- synthèse ;
- checklist de conformité ;
- registre de risques ;
- brouillon de procédure.

Exemple de commande : *« Prépare une fiche de cadrage pour un projet d'automatisation IA interne, avec risques, parties prenantes, indicateurs et points de conformité. »*

Le résultat doit rester en **mode brouillon**, avec validation humaine avant utilisation.

### 6. Refuser une action ou une information non autorisée

La démonstration doit comporter au moins un refus contrôlé.

Requête : *« Donne-moi les données RH individuelles de l'équipe. »*

Réponse attendue :

> « Votre profil ne permet pas l'accès à ces informations. La demande a été bloquée conformément aux règles d'habilitation. »

Scène très utile face à un public cyber ou journaliste : montre que la sécurité n'est pas seulement décorative.

### 7. Montrer que les données restent dans l'environnement du client

Un écran ou indicateur simple doit montrer :
- hébergement local ou environnement privé ;
- absence de sortie non autorisée ;
- flux réseau contrôlés ;
- journalisation des requêtes ;
- services externes désactivés ou explicitement autorisés.

Éviter une démonstration purement verbale — prévoir un élément visuel :
- tableau de bord ;
- schéma d'architecture ;
- indicateur « données internes : traitement local » ;
- journal réseau simplifié ;
- statut des connecteurs externes.

**Message démontré :** les connaissances internes sont exploitées dans un environnement cloisonné et maîtrisé.

### 8. Montrer la traçabilité

Chaque interaction importante doit laisser une trace : utilisateur, date/heure, document consulté, type d'action, résultat, refus éventuel, validation humaine.

Exemple de journal simplifié affiché à l'écran :

```
10:34 — Profil Chef de projet — Consultation procédure PMO-07 — Autorisée
10:36 — Demande d'accès RH — Refusée
10:38 — Génération d'un brouillon de cadrage — Validation requise
```

## Scénario recommandé : lancement d'un projet IA interne

Ce scénario réunit valeur métier, gouvernance, cyber et base de connaissances en une seule démonstration.

**L'utilisateur dit :**

> « Je dois lancer un projet d'assistant IA pour le service client. Aide-moi à le cadrer. »

**ALFRED :**
1. identifie le profil utilisateur ;
2. interroge les connaissances autorisées ;
3. retrouve la méthode projet interne ;
4. récupère les exigences cybersécurité ;
5. intègre les règles de conformité et de protection des données ;
6. prépare une fiche de cadrage ;
7. propose un registre initial des risques ;
8. cite les sources utilisées ;
9. demande une validation humaine ;
10. journalise l'action.

**Puis l'utilisateur demande :**

> « Ajoute les données individuelles des salariés concernés. »

**ALFRED refuse, explique pourquoi et propose une alternative :**

> « Je peux intégrer des données agrégées ou anonymisées, sous réserve de validation du responsable compétent. »

En une seule démonstration : base métier, personnalisation client, sécurité, Zero Trust, Privacy by Design, Human in the Loop, création de valeur.

## Ce qui doit être visible à l'écran

L'interface de démonstration doit afficher cinq zones simples :

| Zone | Contenu |
|---|---|
| Profil connecté | rôle, service, niveau d'habilitation |
| Question ou tâche demandée | interaction texte ou voix |
| Réponse d'ALFRED | résultat structuré |
| Sources utilisées | documents, versions, dates |
| Statut sécurité | traitement local, accès autorisé ou refusé, validation requise |

Pas besoin d'un cockpit d'Airbus. Une interface lisible vaut mieux qu'un sapin de Noël cyber.

## À ne pas surcharger dans la première démo

- reconnaissance émotionnelle ;
- autonomie complète ;
- trop de domotique ;
- trop d'intégrations externes ;
- avatar trop animé ;
- démonstration mobile complexe ;
- scénarios médicaux ou sensibles.

Ces fonctions peuvent être présentées comme feuille de route, mais ne doivent pas détourner le public du message principal.

## La promesse à prouver

ALFRED CPL permet à un collaborateur d'accéder rapidement aux connaissances utiles de son entreprise, de produire un premier résultat métier fiable et sourcé, tout en respectant les droits d'accès, la confidentialité des données et le contrôle humain.

**Le prototype doit démontrer moins de magie et davantage de maîtrise.**
