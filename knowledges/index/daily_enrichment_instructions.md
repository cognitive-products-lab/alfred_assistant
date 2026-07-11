# Enrichissement quotidien de la base de connaissances ALFRED — Instructions permanentes

**Statut** : actif, continu, sans date de fin. Démarré le 11/07/2026 (exécution manuelle de reprise), automatisé chaque jour à 5h00 à partir du 12/07/2026 via la tâche planifiée `alfred-knowledge-daily-enrichment`.

## Mission

Chaque jour, créer **60 fichiers JSON de connaissances** complets, substantiels et exploitables dans `D:\PROJET_ALFRED\ALFRED_PC\knowledges`, et/ou mettre à jour des fichiers existants lorsque cela est plus pertinent que d'en créer de nouveaux.

## Références obligatoires à lire avant de commencer un lot

- `knowledges/knowledge_template.json` — structure obligatoire de chaque fichier (champs, valeurs autorisées, exemple).
- `knowledges/taxonomy.json` — domaines et sous-domaines existants, intents, `linked_knowledge`.
- `knowledges/manifest.json` — vue d'ensemble des domaines, `total_domains`, lots précédents.
- `knowledges/knowledge_registry.json` — registre courant (généré automatiquement, ne pas éditer à la main).
- `knowledges/index/daily_enrichment_log.md` — journal des lots précédents : lire les dernières entrées pour connaître les domaines déjà couverts récemment et éviter la répétition/déséquilibre.

## Domaines de connaissances (non limitatif)

Sciences, Histoire, Technologie, Arts, Compétences pratiques, Géographie, Médecine (jamais de diagnostic), Mathématiques, Philosophie, Économie, Droit, Environnement, Culture générale, Éducation, Psychologie, Sociologie, Communication, Management, Gestion de projet, Cybersécurité, Intelligence artificielle, Gouvernance des données, Réglementation, Éthique, Accessibilité, Numérique responsable — et tout autre domaine pertinent.

## Domaines spécifiques à ALFRED CPL (non limitatif)

Fonctionnalités, architecture fonctionnelle/technique, mémoire (statique/dynamique/long terme), interaction utilisateur, personnalisation, scénarios d'usage/démo/pro/quotidien, sécurité locale, local-first, offline-first, confidentialité, Zero Trust, Security/Privacy/AI-Governance by Design, droits et accès, traçabilité, journalisation, explicabilité, consentement, gouvernance des décisions IA, gestion des alertes/rappels/agenda/tâches/priorités, assistance (gestion de projet, management, gouvernance, risques, conformité, cybersécurité, gouvernance des données, transformation digitale, innovation, rédaction pro, réunions, soutenances, entretiens, décision, veille), accessibilité numérique, interfaces vocales, vision par ordinateur, analyse sémantique, intelligence émotionnelle adaptative, prévention manipulation émotionnelle, relation humain-machine, limites éthiques, continuité de service, haute dispo, résilience, sauvegarde/restauration, incidents, supervision, maintenance évolutive, documentation, procédures (installation/config/MAJ/test/déploiement/récupération), gouvernance du cycle de vie.

## Création de nouveaux domaines — règles

Autorisé et recommandé quand cela enrichit ALFRED CPL, structure mieux une connaissance absente/insuffisante, répond à un nouveau cas d'usage, couvre un sujet émergent, évite un classement artificiel, facilite recherche/réutilisation/maintenance, renforce la cohérence long terme.

Avant de créer un domaine : vérifier qu'un domaine équivalent n'existe pas déjà (voir `taxonomy.json`/`manifest.json`), éviter le vague/redondant/trop spécialisé, définir un nom clair et stable, définir le périmètre, préciser les types de connaissances à y intégrer, créer un modèle JSON spécifique si nécessaire, documenter la création dans le récapitulatif du lot.

## Contenu obligatoire de chaque fichier JSON

Respecter strictement `knowledge_template.json` (`template_structure`) : `knowledge_id` (format `domain.subdomain.knowledge_name`), `title`, `version`, `status`, `domain`, `subdomain`, `category`, `summary`, `purpose`, `tags` (≥3), `intents`, `usage_context`, `priority`, `safety_level`, `content` (`definition`, `core_principles`, `rules`, `examples` ≥1, `best_practices` ≥1, `anti_patterns`), `retrieval_hints` (`priority_keywords`, `related_domains`, `related_knowledge`, `retrieval_priority`), `behavior_rules` (`tone`, `response_style`, `max_complexity`, `allow_humor`), `safety_notes` (`allowed_usage`, `restricted_usage`, `forbidden_usage`, `fallback_behavior`), `metadata` (`author`, `creation_date` JJ/MM/AAAA, `last_update`, `review_status`, `reviewed_by`, `source_type`, `language`, `retrieval_ready`, `rag_compatible`).

Langue : français (`"language": "fr"`) sauf domaine explicitement anglophone.

## Exigences de qualité

- JSON valide, chargeable sans erreur (`json.load`).
- snake_case pour les identifiants et noms de fichiers.
- Contenu factuel, pédagogique, réellement exploitable, sans réécriture nécessaire.
- Pas de doublon : vérifier le registre/l'arborescence du domaine ciblé avant création.
- Pas de contradiction avec les connaissances existantes.
- Pas de données personnelles/confidentielles/sensibles sans justification et classification (`safety_level`).
- Respecter `safety_rules` du template : jamais de credentials/secrets, jamais de diagnostic médical, jamais de guidance illégale, toujours un `fallback_behavior`.

## Répartition quotidienne des 60 fichiers (équilibre à maintenir)

Mélanger : connaissances générales, professionnelles, techniques, réglementaires, cybersécurité, IA, gouvernance, spécifiques ALFRED CPL, mises à jour de fichiers existants, et création de nouveaux domaines quand pertinent. Ne pas concentrer sur un seul domaine sauf besoin prioritaire documenté.

## Gestion des doublons

Avant de créer un fichier : chercher l'existant sur le même sujet (registry + arborescence du domaine), préférer mise à jour/enrichissement/fusion si cela améliore la cohérence, documenter toute fusion/MAJ importante/suppression de doublon dans le récapitulatif.

## Étapes techniques de fin de lot (obligatoires)

1. Valider chaque nouveau fichier JSON (`json.load`).
2. Régénérer le registre : `python D:\PROJET_ALFRED\ALFRED_PC\tools\knowledge_tools\generate_knowledge_registry.py`.
3. Mettre à jour `taxonomy.json` (nouveaux domaines/sous-domaines/intents/linked_knowledge) et `manifest.json` (`domains`, `total_domains`, `recently_added_lots`, `last_update`) si de nouveaux domaines/sous-domaines majeurs ont été créés.
4. Ajouter une entrée au journal `knowledges/index/daily_enrichment_log.md`.

## Récapitulatif obligatoire après chaque lot

Fournir : nb fichiers créés / mis à jour / fusionnés / doublons évités, domaines et sous-domaines couverts, domaines spécifiques ALFRED CPL couverts, nouveaux domaines créés + justification, nouveaux modèles JSON introduits, nouveaux champs de métadonnées introduits, fichiers ayant nécessité une MAJ importante, incohérences/limites détectées, recommandations pour le prochain lot. Ce récapitulatif doit aussi être ajouté (résumé) au journal `daily_enrichment_log.md`.
