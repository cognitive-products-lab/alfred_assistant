# Enrichissement quotidien de la base de connaissances ALFRED — Instructions permanentes

**Statut** : actif, continu, sans date de fin. Démarré le 11/07/2026 (exécution manuelle de reprise), automatisé chaque jour à 5h00 à partir du 12/07/2026 via la tâche planifiée `alfred-knowledge-daily-enrichment`. Répartition 20 CPL / 40 socle imposée à partir du 17/07/2026 (voir section « Répartition quotidienne des 60 fichiers »).

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

## Répartition quotidienne des 60 fichiers (règle obligatoire depuis le 20/08/2026, remplace la version du 17/07/2026)

Répartition précise imposée par Céline le 20/08/2026 (appliquée avec succès au Lot 13, volet « rotation standard »), à respecter sur le total de 60 fichiers (créations + mises à jour comptent dans leur quota respectif) :
- **20 fichiers domaine `cpl`** (ALFRED CPL) — non négociable, en rotation sur les 12 sous-domaines cpl (`cpl.business_strategy` inclus normalement depuis sa consolidation du 20/08/2026 ; `cpl.demo_scenario` reste plus faible car ensemble fermé par nature) — voir la liste « Domaines spécifiques à ALFRED CPL » ci-dessous.
- **10 fichiers domaine `secteurs_activite`** — angles nouveaux uniquement sur les 9 secteurs déjà créés (sante, finance_banque, industrie_manufacturiere, retail_distribution, secteur_public, energie, construction_btp, assurance, transport_logistique) : ne pas dupliquer les 5 fiches de base déjà existantes par secteur (profil_secteur, normes_reglementation, enjeux_risques, vocabulaire_metier, pestel) — vérifier le contenu déjà présent dans `knowledges/secteurs_activite/<secteur>/` avant de choisir un sujet.
- **10 fichiers psychologie/émotions** (`human/psychology/`, `human/emotional_intelligence/`).
- **15 fichiers culture cinéma/musique/lecture** (`knowledges/cinema/`, `knowledges/arts/musique/`, `knowledges/arts/litterature/`), répartis de façon équilibrée entre les trois thèmes.
- **5 fichiers domaines au choix** — bloc volontairement libre, à utiliser pour combler les manques ponctuels identifiés dans le registre au moment du lot (ne pas le figer sur un domaine fixe).

Si la cible de 60 n'est pas atteinte dans un lot (qualité prioritaire sur le volume, cf. règle déjà en vigueur) : produire en priorité les 20 fichiers CPL au complet en premier, puis les autres blocs dans l'ordre ci-dessus jusqu'à épuisement du temps disponible — ne jamais réduire le quota CPL pour compenser un retard ailleurs. Le bloc CPL (20) reste la seule partie strictement non négociable.

Au sein de chaque bloc, continuer à mélanger les sous-thèmes et à éviter de concentrer sur un seul domaine ou sous-domaine, sauf besoin prioritaire documenté.

Voir aussi `docs/roadmap/plan_knowledges_3_mois.xlsx` (révisé le 20/08/2026) pour la déclinaison de cette répartition en quotas hebdomadaires par sous-domaine sur 3 mois.

## Gestion des doublons

Avant de créer un fichier : chercher l'existant sur le même sujet (registry + arborescence du domaine), préférer mise à jour/enrichissement/fusion si cela améliore la cohérence, documenter toute fusion/MAJ importante/suppression de doublon dans le récapitulatif.

## Étapes techniques de fin de lot (obligatoires)

1. Valider chaque nouveau fichier JSON (`json.load`).
2. Régénérer le registre : `python D:\PROJET_ALFRED\ALFRED_PC\tools\knowledge_tools\generate_knowledge_registry.py`.
3. Mettre à jour `taxonomy.json` (nouveaux domaines/sous-domaines/intents/linked_knowledge) et `manifest.json` (`domains`, `total_domains`, `recently_added_lots`, `last_update`) si de nouveaux domaines/sous-domaines majeurs ont été créés.
4. Ajouter une entrée au journal `knowledges/index/daily_enrichment_log.md`.
5. **Obligatoire depuis le 17/07/2026 (consigne Céline) : `git add`, `git commit`, `git push origin main` des fichiers `knowledges/` créés/modifiés/supprimés par le lot.** Se limiter au périmètre `knowledges/` (ne pas ajouter des fichiers modifiés ailleurs dans le dépôt par une autre session en cours, conformément à la vigilance sessions parallèles déjà en place) : `git add knowledges/`. Message de commit court indiquant le numéro de lot et le résumé (ex. `knowledges: lot 10 - 60 fiches (20 cpl / 40 socle)`). Avant de pousser, vérifier avec `git status`/`git diff --stat -- knowledges/` qu'aucun fichier sensible (secrets, tokens, registres d'incidents) ne s'est glissé dans `knowledges/` — cas normalement exclu par construction mais à vérifier par principe. `alfred_assistant` (ce dépôt) est **public** sur GitHub.

## Écart connu disque / registre (ne pas re-signaler comme anomalie)

Le nombre de fichiers `.json` réellement présents sous `knowledges/` (compte `find`) sera toujours supérieur de 8 au nombre indexé par `knowledge_registry.json`. Cet écart est normal : il correspond aux fichiers techniques listés dans `taxonomy.json.loading_policy.technical_files_not_loaded_as_knowledge` (`manifest.json`, `taxonomy.json`, `domain_links.json`, `retrieval_rules.json`, `governance_rules.json`, `knowledge_template.json`, `knowledge_registry.json`) plus un fichier `cpl/human_organization/__init__.py`. Documenté le 16/07/2026 (Lot 8) pour éviter qu'il soit reconstaté comme une incohérence à chaque lot — vérifier seulement si l'écart change (signe qu'un fichier technique a été ajouté/retiré).

## Récapitulatif obligatoire après chaque lot

Fournir : nb fichiers créés / mis à jour / fusionnés / doublons évités, domaines et sous-domaines couverts, domaines spécifiques ALFRED CPL couverts, nouveaux domaines créés + justification, nouveaux modèles JSON introduits, nouveaux champs de métadonnées introduits, fichiers ayant nécessité une MAJ importante, incohérences/limites détectées, recommandations pour le prochain lot. Ce récapitulatif doit aussi être ajouté (résumé) au journal `daily_enrichment_log.md`.
