# Chantier — 3 prochaines étapes après la synchronisation labiale

> Rédigé le 23/07/2026 — description du travail à fournir, **pas encore commencé**.
> Ordre décidé par Céline : Google Home/Calendar d'abord, puis Mémoire/Connaissances/
> Appareils/Émotions, puis TaskEngine. Reprendre une fois le chantier synchro labiale
> (session parallèle) terminé — voir `project_backlog_next_session.md` (mémoire).

---

## Chantier 1 — Connexion Google Home + Google Calendar

### État actuel réel (vérifié 23/07/2026)

Rien n'existe encore côté intégration, seulement des points d'ancrage :

- **Aucun code Google** dans `src/` — ni OAuth, ni client Calendar, ni client Home. Seuls
  des commentaires-jalons (`src/ui/desktop_quick_actions.py:24`) et une ligne de
  `requirements.txt` commentée (`# requests ... Google Home, etc.`).
- **UI déjà en place mais placeholder** : nav "Agenda" (`interface/desktop_ui/index.html`,
  `#view-agenda`) affiche *"Ton calendrier complet, synchronisé et enrichi par ALFRED,
  arrivera dans une prochaine version."* Le bouton "Ajouter un événement" du tableau de
  bord (`#qa-new-event`) affiche déjà, honnêtement, *"Bientôt disponible — nécessite la
  connexion à Google Agenda."*
- **Un moteur existant à réutiliser, pas à dupliquer** : `src/v3/proactive/reminder_engine.py`
  (validé, JSON local `data/memory/reminders.json`) gère déjà création/liste/échéance/
  suppression de rappels — la synchro Google Calendar doit s'articuler avec lui (import
  d'événements Google → rappels/agenda locaux), pas repartir de zéro.
- **Google Home** : mentionné uniquement dans `BACKLOG.md` (roadmap V2, bloc B19
  domotique) comme provider confirmé, pattern Adapter prévu (`google_home_adapter.py`).
  `src/v4/` (actions/, integration/, orchestrator/, home_state/, scenarios/, security/,
  triggers/) n'a que des `__init__.py` vides — aucun code réel.
- Céline a déjà les identifiants Google Cloud, gardés hors du chat.

### Objectif

Une vraie connexion OAuth Google (Calendar en priorité, Home dans un second temps si le
temps le permet), avec synchronisation lecture (et si possible écriture) des événements
d'agenda, affichés dans la page Agenda réelle (plus de placeholder) et exploitables par
ALFRED en conversation ("qu'est-ce que j'ai aujourd'hui ?").

### Étapes à construire

1. **Cadrage sécurité/scopes** — définir précisément les scopes OAuth demandés (lecture
   seule Calendar au minimum ; écriture si un besoin réel est confirmé). Documenter le
   choix dans `docs/gouvernance/` ou `docs/rgpd/` (nouvelle donnée externe = mise à jour
   du registre RGPD existant, cf. page qualité-données publiée le 19/07).
2. **Flux d'authentification** — décider du mécanisme (Desktop App OAuth avec
   `google-auth-oauthlib`, flux local avec navigateur système + callback local), stockage
   sécurisé du token (chiffrement Fernet déjà utilisé ailleurs dans le projet pour ce
   type de secret, cf. `src/security/`).
3. **Client Calendar** — nouveau module (ex. `src/integrations/google_calendar_client.py`,
   même famille que `weather_client.py` créé cette session) : lecture des événements à
   venir, format normalisé.
4. **Pont avec l'existant** — décider comment les événements Google s'articulent avec
   `reminder_engine.py` (import direct vers rappels ? modèle séparé "événements agenda"
   distinct des rappels ALFRED ?).
5. **Page Agenda réelle** — remplacer le placeholder `#view-agenda` par un vrai rendu
   des événements, connecté via une nouvelle méthode bridge (`get_calendar_events`)
   dans `src/alfred_desktop.py`, sur le modèle de `get_weather`/`get_planning`.
6. **Consentement utilisateur** — gate de consentement explicite avant tout appel Google
   (même principe que `weather_prefs.py`/`context_consent_prefs.py` créés cette session),
   pas d'appel externe sans accord.
7. **Google Home (si temps disponible)** — scope réduit dans un premier temps : lister
   les appareils, état on/off. Nouveau module `src/v4/integration/google_home_adapter.py`
   (l'emplacement est déjà prévu dans la roadmap).
8. **Tests + headers** — chaque nouveau module avec son test (`tests/`), header
   PROJECT/BLOCK/FILE/ROLE/AUTHOR/CREATED/VERSION/STATUS, règle constante du projet.

### Risques / points à trancher avant de coder

- Le flux OAuth desktop (navigateur système + callback local) demande un port local
  d'écoute temporaire — vérifier compatibilité avec le pare-feu/segmentation VLAN déjà
  en place (voir mémoire réseau).
- Écriture (créer/modifier un événement Google depuis ALFRED) est un chantier plus risqué
  que la lecture seule — commencer lecture seule, écriture seulement sur demande explicite.

---

## Chantier 2 — Pages réelles Mémoire / Connaissances / Appareils / Émotions

### État actuel réel (vérifié 23/07/2026)

Les 4 pages existent dans la nav mais sont du pur placeholder, texte identique en
substance : *"arrivera dans une prochaine version"* (`#view-memoire`, `#view-connaissances`,
`#view-emotions`, `#view-appareils` dans `index.html`).

Les données réelles existent déjà côté backend, mais seulement pour de petits widgets du
tableau de bord — pas pour ces pages dédiées :
- `get_devices()` / `get_emotion_state()` (`src/alfred_desktop.py`) déjà réels, déjà
  appelés, mais seulement pour les petits widgets `renderDevices`/`renderEmotion` du
  tableau de bord.
- Mémoire : modules réels disponibles (`src/memory/episodic_memory.py`,
  `long_term_memory.py`, `memory_engine.py`, `memory_indexer.py`, `memory_answer_engine.py`).
- Connaissances : moteur de recherche réel déjà utilisé côté "Actions rapides"
  (`search_knowledge()` dans `desktop_quick_actions.py`, s'appuie sur
  `src/knowledge/retrieval_engine.py`) — donc la brique de recherche existe, juste pas
  encore une page de navigation/consultation dédiée.
- Émotions : `src/regulation/emotion_detector.py`, `wellbeing_tracker.py`,
  `emotion_override_prefs.py` (créé cette session) déjà réels.
- Appareils : `src/ui/device_settings.py` (caméras/micros), `data/security/trusted_devices.json`.

### Objectif

Quatre pages consultables réellement utiles (pas de nouvelle collecte de données —
tout exposer ce qui existe déjà), chacune avec au minimum : liste/historique consultable,
un filtre ou une recherche simple, actions de base cohérentes avec ce que permet déjà le
backend (ex. corriger une émotion mal détectée, existe déjà via `correct_emotion`).

### Étapes à construire (par page, indépendantes — peuvent être livrées une par une)

1. **Mémoire** : nouvelle méthode bridge listant les souvenirs long-terme/épisodiques
   (pagination si volume important), page listant/recherchant dedans. Décider du niveau
   de détail affiché (respect vie privée — c'est la mémoire personnelle de Céline).
2. **Connaissances** : page de consultation/recherche dans la base de connaissance
   ALFRED (distincte des fichiers utilisateur — cf. `search_knowledge` déjà scopé
   explicitement à la base ALFRED, pas aux fichiers perso).
3. **Émotions** : historique des estimations émotionnelles dans le temps (graphique ou
   liste chronologique), bouton de correction déjà existant (`correct_emotion`) à
   brancher dans cette page plutôt que seulement le petit widget dashboard.
4. **Appareils** : vraie liste des appareils connus/de confiance, statut, action
   révocation si pertinent (`trusted_devices.json` déjà structuré pour ça).
5. Pour chacune : nouvelle méthode bridge dans `src/alfred_desktop.py`, remplacement du
   bloc placeholder HTML par le rendu réel, tests + headers.

### Risques / points à trancher

- Volume de données mémoire potentiellement grand — prévoir pagination/limite dès le
  départ plutôt que tout charger d'un coup.
- Décider si ces 4 pages sortent en un seul lot ou une par une (plus sûr à livrer/tester
  une par une, cohérent avec le rythme de cette session).

---

## Chantier 3 — TaskEngine

### État actuel réel (vérifié 23/07/2026)

- **Aucun TaskEngine n'existe** — recherche `src/` : zéro résultat.
- `data/actions/tasks.json` : schéma vide (`"tasks": []`), header explicite :
  *"SCHEMA_DEFINI — pas encore chargé par le code (aucun TaskEngine implémenté,
  contrairement à ReminderEngine qui existe déjà)"*, modelé volontairement sur le schéma
  du ReminderEngine "pour cohérence future."
- Page "Tâches" (`#view-taches`) : placeholder standard. Bouton "Ajouter une tâche"
  (`#qa-new-task`) affiche déjà honnêtement *"Bientôt disponible — nécessite le moteur de
  tâches (en cours de construction)."*
- Modèle à suivre déjà dans le projet : `src/v3/proactive/reminder_engine.py` (validé,
  JSON local, create/list/due/delete, one-shot + récurrent) — le TaskEngine est censé en
  être l'analogue "pour des tâches sans échéance stricte" (dixit le header de `tasks.json`).

### Objectif

Un vrai moteur de tâches (créer, lister, marquer fait, prioriser, supprimer), persistant
en JSON local comme le ReminderEngine, branché sur la page Tâches réelle et sur le bouton
"Ajouter une tâche" déjà présent dans l'UI.

### Étapes à construire

1. **`src/v3/proactive/task_engine.py`** (ou équivalent) — CRUD tâches, priorité,
   statut (à faire / en cours / fait), persistance dans `data/actions/tasks.json`
   (schéma déjà défini, juste à charger/écrire réellement).
2. **Différenciation Tâche vs Rappel** — clarifier la frontière avec `reminder_engine.py`
   (une tâche n'a pas d'échéance stricte contrairement à un rappel) pour éviter la
   duplication déjà signalée comme risque dans le header du fichier JSON.
3. **Bridge + UI** — méthodes `get_tasks`/`create_task`/`complete_task`/`delete_task`
   dans `src/alfred_desktop.py`, remplacement du placeholder `#view-taches`, branchement
   réel du bouton `#qa-new-task` (déjà en place, juste à connecter).
4. **Lien conversationnel** — permettre à ALFRED de créer/lister des tâches en langage
   naturel (cohérent avec les autres capacités conversationnelles existantes).
5. Tests + headers, comme toujours.

### Risques / points à trancher

- Éviter la duplication fonctionnelle avec `reminder_engine.py` — bien définir la
  distinction avant de coder plutôt qu'après.
- Le compteur "Tâches" affiché dans le sidebar (badge visible sur "Tâches" dans les
  captures d'écran) est peut-être déjà un chiffre statique/démo à vérifier/corriger une
  fois le vrai moteur branché.

---

## Rappel de méthode (constant sur ce projet)

- Chaque nouveau script → son test dans `tests/`, header PROJECT/BLOCK/FILE/ROLE/AUTHOR/
  CREATED/VERSION/STATUS.
- Tutoiement partout côté UI/texte utilisateur (jamais de "vous").
- Consentement explicite avant tout nouvel appel réseau externe (pattern déjà en place
  pour la météo).
- Vérifier en conditions réelles (app lancée, captures d'écran) avant de déclarer un
  chantier terminé — ne pas se fier uniquement à la lecture de code ou aux tests unitaires.
- `git add` ciblé uniquement sur les fichiers réellement modifiés par le chantier en
  cours — ne jamais `git add -A` (risque de sessions parallèles actives sur ce dépôt).
