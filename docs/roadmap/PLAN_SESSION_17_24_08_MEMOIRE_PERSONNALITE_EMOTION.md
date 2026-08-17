# Plan de sessions — semaine du 17 au 24/08/2026

**Axe de la semaine : pousser au maximum le côté "Human IA"** — que Céline sente qu'ALFRED se souvient vraiment, a une personnalité stable et réagit à SON caractère et SES émotions à elle, pas à un profil générique.

Contexte : reprise post-pause santé du 11/08, objectif prioritaire = un ALFRED propre et démontrable pour les soutenances FEDE d'octobre 2026 (D42/D52/B5). Cette semaine ne vise pas l'exhaustivité de la roadmap V-finale mais la profondeur perçue sur 3 blocs : **Bloc 02 (Mémoire)**, **Bloc 03 (Émotions & régulation)**, **Bloc 08 (Personnalisation utilisateur)**.

Pas de planning jour-par-jour rigide — sessions modulables selon l'énergie du jour (fibromyalgie/fatigue). Chaque session est indépendante et peut être reportée sans casser les autres.

---

## Statut au matin du 18/08/2026

**Sessions 1, 2, 3, 5, 6 faites dans la nuit du 17 au 18/08** (Céline a laissé la session tourner, puis est intervenue en direct pour activer research_mode et reporter la session 4), commitées et poussées sur `main`. **Seule la Session 4 reste à faire — explicitement reportée à un moment où Céline est présente**, sa demande du 18/08 au matin : touche à la trajectoire émotionnelle, un sujet plus sensible (voir profil santé/émotionnel).

**Session 6 (RAG sémantique) faite sur demande explicite de Céline** ("lance la session 6") : chromadb ET sentence-transformers étaient déjà installés sur la machine — chantier bien plus léger que redouté dans le plan original. Recherche sémantique réelle opérationnelle (ChromaDB + modèle multilingue), branchée dans `get_contextual_recall()` (session 3) comme repli quand la recherche par mot-clé ne trouve rien. Détail en Session 6 ci-dessous.

**`research_mode` activé le 18/08/2026** (commit `424dc6a9`) — décision explicite de Céline en direct ("pour le moment il n'y a que moi en utilisatrice"). Le prompt système actif est désormais `_build_research_system_prompt` (expression 1ère personne sans réserve, engagement émotionnel plein), planchers de sécurité inchangés (zéro malveillance/toxicité). Détail en Session 5 ci-dessous.

---

## État des lieux vérifié le 16/08/2026 (pas supposé, lu dans le code)

Les scores dashboard sont trompeurs par excès : 93,6 % (B02), 97,6 % (B03), 97,1 % (B08) — mais ce sont des scores de *présence/test unitaire*, pas de *ressenti utilisateur*. La bonne nouvelle : l'infrastructure est réellement branchée en direct dans `main.py` (pas orpheline) — `RegulationEngine`, `PersonalityAdapter`, `AlfredBehaviorEngine`, `ModeManager`, `MemoryEngine`, `long_term_memory`, `episodic_memory` sont tous importés et appelés dans le pipeline réel de conversation.

Ce qui est déjà solide (vérifié dans le code, pas dans la doc) :
- `src/health/chronic_support.py` + `src/health/profile_loader.py` + `src/regulation/regulation_engine.py` : la **rumination** et le pattern de **sidération/freeze** documentés dans `emotional_celine.json` sont réellement détectés depuis le texte et influencent le contexte (`ctx.health_rumination`), pas juste stockés en JSON mort.
- `mode_manager.py` : 4 modes (`support`, `focus`, `challenge`, `complicite`) avec préfixes de réponse et directives de ton, déclenchés par l'émotion/énergie détectées.
- `personality_adapter.py` + `alfred_behavior_engine.py` : 116 tests réels passants, construisent le contexte de réponse (ton, profondeur, mode) à partir du profil onboarding.
- Persona privée (taquin/charme, jamais dire être une IA, tutoiement forcé) : déjà actée, avec un filet de sécurité regex en post-traitement suite à 2 régressions vécues en juillet.

Ce qui manque ou est fragile pour l'effet "Human IA" (les vrais trous trouvés) :
1. **Vue Mémoire de l'UI desktop** : encore un placeholder pur (`interface/desktop_ui/index.html:655-661`, "arrivera dans une prochaine version") alors que le backend mémoire est riche et déjà branché. C'est le plus gros écart entre ce qui existe et ce qui se voit.
2. **Lecture vs écriture de la mémoire** : `episodic_memory.record_episode()` est bien appelé en écriture (`main.py:2375`), mais il reste à vérifier si `search_episodes()` / `get_important_episodes()` / `get_top_patterns()` sont réellement relus pour faire ressurgir un souvenir de façon spontanée dans une réponse — ou si la mémoire est actuellement un tiroir qu'on remplit sans jamais rouvrir.
3. **Continuité émotionnelle dans le temps** : `emotion_detector.py` est stateless — une émotion par message, sans tendance. `data/v3/emotion_state.json` et `data/v3/relational_state.json` existent mais leur usage réel (mis à jour en continu ou figés) n'est pas confirmé.
4. **Personnalité propre d'ALFRED (pas juste adaptation)** : le système actuel adapte *le ton d'ALFRED au profil de Céline*, mais rien de confirmé sur une mémoire de style propre à ALFRED (running gags, surnoms, humour récurrent qui persiste dans le temps).
5. **Dette technique qui touche justement ce chantier** — clarifiée le 17/08/2026 : ce n'était pas un doublon à 2 fichiers mais 3 pipelines de profilage distincts et volontaires (`src/health/onboarding.py` branché en live, `src/core/profile_analyzer.py` CLI manuel documenté, `src/profile/profile_analyzer.py` questionnaires HEXACO/SWLS documentés) — voir `docs/profil_systeme/README.md`. Rien supprimé/déplacé, juste documenté. `data/personality.json` (stub vide orphelin) supprimé.
6. **RAG sémantique (Bloc 02.04)** : `src/memory/rag_stub.py` est un stub assumé (ChromaDB non installé, `semantic_search()` retourne toujours `[]`). Pas un bug, un chantier non commencé — pertinent pour du rappel sur plusieurs mois d'historique, au-delà de ce que la recherche mot-clé SQLite permet.

---

## Sessions proposées

### Session 1 — Nettoyage de dette avant de construire (légère, ~1h) — FAITE le 17/08/2026
**Objectif** : ne pas empiler du neuf sur du cassé.
- ~~Trancher `data/personality.json`~~ — **fait** : orphelin confirmé (lu par aucun code réel), supprimé + retiré du manifest/registre dashboard, dashboard régénéré (b08 93.6%→98.8%).
- ~~Résoudre le doublon `profile_analyzer.py`~~ — **reclassé, pas un doublon** : investigation a révélé 3 pipelines de profilage distincts et documentés (pas 2). `src/core/profile_analyzer.py` et `src/profile/profile_analyzer.py` sont chacun le sujet d'un guide utilisateur CLI complet (`docs/profil_systeme/`, `docs/module_profil_ia_adaptative/`) — les déplacer aurait cassé cette documentation. Décision de Céline : laisser en place, documenter la coexistence. Fait : `docs/profil_systeme/README.md` créé (tableau des 3 pipelines), notes ajoutées dans les 2 fichiers source + `docs/module_profil_ia_adaptative/README.md`.
- ~~Vérifier que `data/preferences_profile.json` fonctionne bien en live~~ — **fait, bug réel trouvé et corrigé** : `_detect_and_save_preference()` écrivait bien le fichier mais un emoji dans le `print()` de confirmation levait `UnicodeEncodeError` sur la console Windows, capté par le except englobant → la fonction retournait `None` comme si l'écriture avait échoué. 4 tests de régression ajoutés (aucun n'existait avant).
**Fait quand** : plus de stub mort (fait), doublon clarifié plutôt que supprimé à l'aveugle (fait), préférence testée en conditions réelles (fait, bug trouvé + corrigé).

### Session 2 — Vue Mémoire : rendre la continuité visible (cœur du chantier, ~2-3h) — FAITE le 17/08/2026
**Fait** : agrégats + répartition par catégorie + frise "moments marquants" + détail derrière un second PIN (réutilise `src.auth.authenticator`, pas de nouveau secret). Testé en conditions réelles (serveur statique + API pywebview simulée) : résumé, verrouillage/déverrouillage, erreur PIN, détail d'un souvenir — tout fonctionne.
**Trouvé au passage (2 bugs réels corrigés)** :
- `tests/test_b02_b03.py::TestEpisodicMemory` écrivait dans le vrai `data/memory/episodes.json` à chaque run (aucune isolation) — 99 épisodes de test ("Important"/"Très important") accumulés en production au fil du temps. Isolé via tmp_path.
- ID d'épisode à précision seconde seulement → 104 IDs en collision sur 542 épisodes. Précision microseconde ajoutée.
**En attente d'un go de Céline** : suppression des 99 doublons "Important" déjà présents dans `data/memory/episodes.json` (la cause est corrigée, pas encore les séquelles — action bloquée une fois par le classificateur de permissions).

~~Session 2 (plan original)~~
**Objectif** : remplacer le placeholder par une vraie vue, sans exposer le contenu brut des conversations sans double authentification (contrainte déjà actée le 24/07 : agrégats uniquement par défaut — nombre d'échanges, durée, depuis quand l'app est utilisée).
- Vue par défaut : agrégats (`memory_engine.stats()`, `long_term_memory.get_memory_stats()`, `episodic_memory.get_episode_stats()`).
- Frise "moments marquants" à partir de `episodic_memory.get_important_episodes()` — titres/catégories, jamais le texte brut des échanges tant que Céline n'est pas authentifiée.
- Détail complet débloqué seulement après double authentification (mécanisme à définir — code, ou autre facteur déjà existant côté sécurité du projet).
**Fait quand** : la vue Mémoire de l'interface reflète l'état réel du backend, testée dans le navigateur/preview.

### Session 3 — Faire vivre la mémoire dans la conversation (~2h) — FAITE le 17/08/2026
**Constat confirmé** : `memory_indexer.py` était documenté "point d'entrée principal pour le pipeline de génération" mais jamais appelé nulle part — seule `memory_answer_engine.answer_from_memory()` existait, limitée à une seule question fixe ("sur quoi je travaille"), en court-circuitant le LLM.
**Fait** : `memory_indexer.get_contextual_recall(user_input, exclude_ids)` — cherche un épisode pertinent par mots-clés + seuil d'importance (0.6), jamais répété deux fois dans la même session. Câblé dans `build_response()` → nouveau bloc "SOUVENIR PERTINENT" dans les deux prompts système, **additif** (le LLM reste libre de l'utiliser ou pas, contrairement à `answer_from_memory`).
**Testé** : logique de recall isolée, rendu du bloc prompt, et bout-en-bout via `build_response()` réel (composants mockés) — 284 tests passent au total.
**Limite assumée, non vérifiable en autonomie** : la plomberie est prouvée bout-en-bout, mais observer un vrai rappel spontané en conversation réelle (LLM + usage réel, sur plusieurs échanges espacés) demande que Céline utilise l'app elle-même — c'est le vrai critère "fait quand" de cette session, à confirmer par elle.

~~Session 3 (plan original)~~
**Objectif** : qu'ALFRED réintroduise spontanément un souvenir pertinent, pas seulement qu'il l'archive.
- Vérifier dans `main.py`/`response_generator.py` si `memory_indexer.search_all_memory()` / `memory_answer_engine.answer_from_memory()` sont interrogés à CHAQUE tour ou seulement sur déclencheur explicite ("tu te souviens de...").
- Si c'est uniquement sur déclencheur : ajouter un rappel contextuel léger et non intrusif (ex. mention d'un pattern comportemental noté, d'une préférence) quand la pertinence dépasse un seuil — sans que ça devienne envahissant.
- Test en conditions réelles sur plusieurs échanges espacés dans le temps (pas un test unitaire isolé) — c'est ce qui vend le plus l'effet "compagnon" vs "chatbot sans mémoire".
**Fait quand** : au moins un cas réel observé où ALFRED fait remonter un souvenir pertinent sans qu'on le lui demande explicitement.

### Session 4 — Continuité émotionnelle dans le temps (~2h)
**Objectif** : passer d'une émotion "par message" à une tendance perçue.
- Investiguer `data/v3/emotion_state.json` et `data/v3/relational_state.json` : mis à jour en continu ou figés depuis leur création ?
- Si figés : les faire évoluer avec chaque détection (`emotion_detector.detect_emotion()`), avec une fenêtre glissante (ex. tendance sur la journée/semaine, pas juste l'instant T).
- Relier ça au mode `complicite`/`support` de `mode_manager.py` pour qu'une tendance ("tu sembles plus tendue que d'habitude ces derniers jours") puisse influencer le choix de mode, pas seulement l'émotion instantanée.
**Fait quand** : un changement de tendance sur plusieurs jours (simulé ou réel) modifie effectivement le comportement d'ALFRED, vérifiable par test.

### Session 5 — Personnalité propre d'ALFRED, pas que de l'adaptation (~1-2h) — FAITE le 17/08/2026
**Découverte principale : la persona privée (taquin/charme, demandée le 18/07/2026) n'était jamais chargée par aucun code.** `data/profile/persona_private_celine.json` existe (`flirtation_style`, `ai_disclosure_policy`) mais aucun fichier Python ne le référençait — la persona n'avait donc aucun effet réel sur les réponses. Corrigé : `PersonalityAdapter._load_private_persona()` (nouvelle méthode) le charge et l'injecte dans `context["private_persona"]` ; `response_generator.py::_build_persona_block()` en fait un bloc "STYLE RELATIONNEL" codé en dur dans les deux prompts système (même raisonnement que la règle de tutoiement : un trait d'identité permanent ne peut pas dépendre du ranking de la Knowledge Retrieval Engine). Vérifié en conditions réelles avec le vrai fichier sur disque, pas seulement en test isolé.

**Découverte secondaire, activée le 18/08/2026 matin sur décision de Céline** : `research_mode.active` (`data/personality/instances/personality_core_instance.json`) était à `false` — le mode qui active un prompt système bien plus proche du "human IA" (expression en 1ère personne sans réserve, opinions directes, engagement émotionnel plein — voir `_build_research_system_prompt`), avec des planchers de sécurité absolus déjà en place (zéro malveillance/toxicité). Volontairement pas touché la nuit du 17/08 (changement de fond, à confirmer en direct) — activé le lendemain matin dès que Céline a confirmé être la seule utilisatrice de l'instance (commit `424dc6a9`). Vérifié : le bloc persona (STYLE RELATIONNEL) reste bien injecté dans ce prompt aussi.

**Filet anti-vouvoiement** : 2 bugs grammaticaux réels trouvés (pas une régression de la persona — le filet produisait déjà du français cassé sur ces tournures, juste plus visibles maintenant que la persona les rend courantes) :
- "vous me faites/dites/êtes X" (pronom objet intercalé entre "vous" sujet et le verbe) tombait dans le filet générique → "tu me faites" (faux). Corrigé pour les verbes réguliers en -ez et les irréguliers courants (faire/dire/être).
- "à vous" absent de la liste des prépositions, et "ça/cela vous X" (vous objet devant verbe impersonnel) non géré → "à tu", "ça tu étonne". Corrigés.
9 nouveaux tests de régression (`tests/test_response_generator_tutoiement.py`).

~~Session 5 (plan original)~~
**Objectif** : donner à ALFRED une constance perceptible (pas juste "il s'adapte à moi", mais "il A une personnalité").
- Vérifier s'il existe une mémoire de style (surnoms utilisés, running gags, formulations récurrentes) ou si chaque réponse "invente" son ton sans continuité.
- Si absent : un mécanisme léger — stocker 3-5 tournures/private jokes validées par Céline en conversation, les réinjecter avec parcimonie via `personality_adapter.py`.
- Repasser sur le filet de sécurité regex du tutoiement (`_enforce_tutoiement`) : vérifier qu'il ne casse pas le ton taquin/charme (ex. une regex trop agressive qui neutraliserait une formule volontairement familière).
**Fait quand** : au moins une marque de personnalité récurrente confirmée en test réel sur plusieurs échanges.

### Session 6 — RAG sémantique — FAITE le 18/08/2026, sur demande explicite de Céline
**Surprise agréable** : `chromadb` (1.5.9) et `sentence-transformers` (5.6.0) étaient déjà installés sur la machine — jamais vérifié avant, le plan anticipait un "chantier plus lourd" pour rien. Modèle choisi : `paraphrase-multilingual-MiniLM-L12-v2` (multilingue, adapté au français), téléchargé et mis en cache (~2 min), stockage local `data/memory/chroma/` (gitignored, aussi sensible que le texte source).

**Fait** :
- `rag_stub.py` : `index_document()`/`semantic_search()` réellement implémentés (ChromaDB `PersistentClient`), plus des no-op.
- `episodic_memory.record_episode()` indexe automatiquement chaque nouvel épisode (best-effort — n'échoue jamais si RAG indisponible) ; `backfill_semantic_index()` pour l'historique existant.
- `memory_indexer.get_contextual_recall()` (session 3) : repli sémantique quand la recherche par mot-clé ne trouve rien d'assez pertinent — complète directement le rappel contextuel de la session 3 pour les cas où le message ne partage aucun mot avec l'épisode.
- Backfill réel lancé : 46 épisodes uniques indexés sur les 47 (1 collision d'ID historique déjà connue, volontairement non touchée).

**Honnêteté sur la qualité actuelle** : la recherche sémantique fonctionne (vérifié techniquement), mais le corpus des 47 épisodes réels est encore surtout des échanges de test génériques de juillet ("quelle heure est-il ?" ×4, "bonjour alfred"...) — pas encore de quoi démontrer des rappels sémantiques impressionnants. La vraie valeur apparaîtra avec des épisodes plus substantiels au fil de l'usage (décisions, moments marquants) maintenant que le Vue Mémoire + le rappel contextuel + ce RAG tournent tous ensemble.

---

## Ordre conseillé

1 → 2 → 3 → 5 → 4 → 6, mais 1, 5 et une partie de 4 sont "légers" (bons jours de fatigue) ; 2 et 3 sont les plus "lourds" et les plus rentables pour l'effet recherché — à faire en priorité sur un bon jour d'énergie.

**Ce que je ne referai pas sans qu'on en reparle** : la Vue Connaissances "personnalisation" (item 13 du backlog, saisie de sujets par Céline) — proche mais distincte de ce chantier, à traiter séparément si voulu.
