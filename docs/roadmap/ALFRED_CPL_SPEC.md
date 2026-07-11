# ALFRED CPL — Fonctions indispensables et exigences de démonstration

> Source : `docs/alfred_cpl_fonctions_et_demo.docx` (intégré le 10/07/2026).
> Périmètre : ALFRED CPL, la déclinaison collaborateur professionnel local d'ALFRED pour entreprises clientes (Roadmap V2, voir [BACKLOG.md](../../BACKLOG.md)).
> Voir aussi le scénario de démonstration détaillé : [ALFRED_CPL_DEMO_SCENARIO.md](../../demo/ALFRED_CPL_DEMO_SCENARIO.md).

## 1. Fonctionnalités indispensables d'ALFRED CPL

### 1. Gestion des utilisateurs et des identités
- Authentification sécurisée.
- Gestion des rôles et profils.
- Habilitations par utilisateur, service et fonction.
- Authentification multifacteur pour les accès sensibles.
- Gestion des sessions, révocation et déconnexion automatique.
- Principe du moindre privilège.

### 2. Base de connaissances métier native
- Socle métier intégré dès la conception.
- Connaissances en management, gestion de projet, cybersécurité, réglementation, normes, conformité, qualité, data, IA, marketing et communication.
- Enrichissement continu de la base.
- Classification par domaine, thème, niveau de sensibilité et usage.
- Définition claire d'une « unité de connaissance ».
- Recherche sémantique et recherche par mots-clés.
- Relations entre concepts, méthodes, normes et procédures.

### 3. Personnalisation pour chaque entreprise cliente
- Ajout des procédures internes.
- Intégration des politiques de sécurité.
- Ajout des référentiels et modèles propres au client.
- Prise en compte du vocabulaire métier de l'organisation.
- Paramétrage des rôles, services et responsabilités.
- Personnalisation des réponses selon le contexte de l'entreprise.
- Séparation stricte entre les bases de connaissances des différents clients.

### 4. Gestion documentaire
- Import de documents autorisés.
- Indexation automatique.
- Détection des doublons.
- Gestion des versions.
- Identification des documents obsolètes.
- Archivage et suppression.
- Attribution d'un propriétaire à chaque document.
- Gestion des dates de validation et de révision.
- Classification des documents selon leur sensibilité.

### 5. Réponses fiables et sourcées
- Réponse à partir de sources internes autorisées.
- Affichage du document source.
- Affichage de la version et de la date.
- Citation de la section utilisée.
- Indication du niveau de confiance.
- Signalement d'une information absente.
- Détection de contradictions entre documents.
- Capacité à répondre qu'une information ne peut pas être confirmée.
- Orientation vers l'expert métier compétent.

### 6. Assistant métier
- Recherche de procédures.
- Explication de règles internes.
- Synthèse de documents.
- Comparaison de référentiels.
- Préparation de notes de cadrage.
- Création de plans d'action.
- Préparation de comptes rendus.
- Création de checklists.
- Préparation de registres de risques.
- Aide à la rédaction de procédures.
- Assistance à l'intégration des nouveaux collaborateurs.
- Orientation vers les bons services ou interlocuteurs.

### 7. Adaptation au contexte utilisateur
- Prise en compte du rôle.
- Prise en compte du service.
- Prise en compte du niveau d'expertise.
- Réponses plus ou moins détaillées selon le profil.
- Personnalisation du format de restitution.
- Mémorisation contrôlée des préférences.
- Modes de fonctionnement adaptés : travail, réunion, formation, projet ou analyse.

### 8. Sécurité Zero Trust
- Vérification systématique des demandes d'accès.
- Contrôle selon l'identité, le rôle, le terminal et le contexte.
- Aucun accès implicite lié à la présence sur le réseau interne.
- Segmentation des composants.
- Isolation des bases clients.
- Autorisations temporaires lorsque nécessaire.
- Révocation rapide des droits.
- Contrôle des accès à chaque ressource.

### 9. Security by Design
- Sécurité intégrée dès la conception.
- Chiffrement des données au repos et en transit.
- Gestion sécurisée des secrets.
- Protection des API.
- Segmentation réseau.
- Cloisonnement des environnements.
- Réduction de la surface d'attaque.
- Mise à jour des dépendances.
- Contrôle des composants tiers.
- Sauvegardes chiffrées et testées.
- Procédure de retour à un état sûr.

### 10. Secure by Default
- Accès limités par défaut.
- Fonctions sensibles désactivées par défaut.
- Journalisation activée par défaut.
- Flux externes bloqués sauf autorisation.
- Conservation minimale des données.
- Interdiction des identifiants génériques.
- Validation obligatoire avant les actions sensibles.

### 11. Protection des données
- Privacy by Design.
- Minimisation des données collectées.
- Gestion des finalités.
- Gestion des durées de conservation.
- Séparation des données personnelles et professionnelles.
- Consultation, rectification et suppression.
- Gestion du consentement lorsque nécessaire.
- Protection des sauvegardes.
- Traçabilité des accès aux données sensibles.

### 12. Hébergement et maîtrise des flux
- Déploiement local, cloud privé ou environnement souverain.
- Fonctionnement possible sur réseau isolé.
- Absence de transmission vers un service externe non autorisé.
- Cartographie des flux.
- Contrôle des connexions sortantes.
- Journal réseau.
- Liste blanche des services autorisés.
- Mode hors ligne pour les fonctions critiques.
- Possibilité de désactiver tous les connecteurs externes.

### 13. Journalisation et audit
- Historique des connexions.
- Historique des recherches.
- Documents consultés.
- Réponses produites.
- Actions autorisées ou refusées.
- Validations humaines.
- Modifications de la base de connaissances.
- Export des journaux pour audit.
- Protection contre l'altération des traces.
- Tableau de bord de supervision.

### 14. Contrôle humain
- Validation avant toute action sensible.
- Possibilité de corriger une réponse.
- Possibilité de refuser une proposition.
- Possibilité d'interrompre une action.
- Affichage clair des limites du système.
- Distinction entre information, recommandation et décision.
- Escalade vers un humain.
- Traçabilité de la décision finale.

### 15. Autonomie progressive
- Niveau 1 : informer.
- Niveau 2 : suggérer.
- Niveau 3 : préparer.
- Niveau 4 : exécuter une action limitée.
- Niveau 5 : intervention humaine obligatoire.

Chaque fonctionnalité doit être associée à un niveau de risque, un niveau d'habilitation et un mécanisme de retour arrière.

### 16. Prévention des risques propres à l'IA
- Protection contre les injections de prompt.
- Contrôle des documents ingérés.
- Détection de contenus malveillants.
- Protection contre la fuite de contexte.
- Limitation des outils accessibles au modèle.
- Filtrage des réponses sensibles.
- Détection d'anomalies.
- Tests réguliers de robustesse.
- Gestion des hallucinations.
- Protection contre l'empoisonnement de la base de connaissances.

### 17. Gouvernance de la connaissance
- Propriétaire désigné pour chaque domaine.
- Processus de validation.
- Processus de mise à jour.
- Gestion des versions.
- Archivage.
- Suppression des contenus obsolètes.
- Contrôle qualité.
- Traçabilité des modifications.
- Indicateurs sur la fraîcheur des connaissances.
- Revue périodique des contenus.

### 18. Gouvernance de l'IA
- Registre des cas d'usage.
- Classification des risques.
- Documentation des modèles utilisés.
- Documentation des données.
- Suivi des performances.
- Suivi des incidents.
- Procédure de retrait d'une fonctionnalité.
- Gestion des changements.
- Revue humaine régulière.
- Alignement avec le RGPD, l'AI Act et les politiques internes.

### 19. Accessibilité
- Interaction texte et voix.
- Compatibilité avec les technologies d'assistance.
- Taille et contraste réglables.
- Reformulation simple.
- Navigation clavier.
- Réduction de la charge cognitive.
- Modes de réponse courts ou détaillés.
- Rythme d'interaction personnalisable.
- Interfaces adaptées à différents profils d'utilisateurs.

### 20. Administration
- Console administrateur.
- Gestion des utilisateurs.
- Gestion des rôles.
- Gestion des documents.
- Gestion des connecteurs.
- Gestion des politiques de sécurité.
- Suivi de la qualité de la base.
- Suivi des performances.
- Paramétrage des durées de conservation.
- Gestion des incidents et alertes.

## 2. Priorité absolue pour le prototype

Pour une première version crédible, ALFRED CPL doit au minimum disposer de :

1. authentification et rôles ;
2. base de connaissances métier ;
3. personnalisation client ;
4. recherche documentaire ;
5. réponses sourcées ;
6. génération de livrables métier ;
7. refus d'accès selon les habilitations ;
8. journalisation ;
9. validation humaine ;
10. traitement local ou environnement cloisonné ;
11. tableau de bord sécurité ;
12. gestion des versions documentaires.

**Cœur du produit :** comprendre la demande, vérifier les droits, rechercher dans les bonnes sources, produire une réponse utile et traçable, puis laisser l'humain décider.

Lors d'une démonstration, ALFRED CPL doit surtout prouver sa valeur métier en quelques minutes. Pas besoin de montrer cinquante fonctions : il faut montrer un parcours cohérent, crédible et sécurisé.

## 3. Fonctions prioritaires pour le prototype

### Indispensables
- authentification ;
- profils et habilitations ;
- interrogation de la base de connaissances ;
- réponses sourcées ;
- préparation d'un livrable ;
- refus d'accès ;
- journalisation ;
- validation humaine ;
- indication du traitement local.

### Très utiles
- interaction vocale ;
- comparaison de documents ;
- détection de versions obsolètes ;
- recherche multi-domaines ;
- export d'une synthèse ;
- tableau de bord de sécurité ;
- indicateur de confiance.

### À ne pas surcharger dans la première démo
- reconnaissance émotionnelle ;
- autonomie complète ;
- trop de domotique ;
- trop d'intégrations externes ;
- avatar trop animé ;
- démonstration mobile complexe ;
- scénarios médicaux ou sensibles.

Ces fonctions peuvent être présentées comme feuille de route, mais elles ne doivent pas détourner le public du message principal.

## 4. La promesse que la démonstration doit prouver

ALFRED CPL permet à un collaborateur d'accéder rapidement aux connaissances utiles de son entreprise, de produire un premier résultat métier fiable et sourcé, tout en respectant les droits d'accès, la confidentialité des données et le contrôle humain.

Le prototype doit donc démontrer **moins de magie et davantage de maîtrise**.

---

Pour le détail des exigences de démonstration (ce qu'ALFRED CPL doit prouver à l'écran, scénario recommandé, éléments visuels), voir [ALFRED_CPL_DEMO_SCENARIO.md](../../demo/ALFRED_CPL_DEMO_SCENARIO.md).
