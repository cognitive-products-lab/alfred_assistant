# Plan d'action — Qualité data & gouvernance dashboards

**Préparé le** : 2026-07-13
**Pour** : reprise au poste PC (ALFRED_PC, D:\PROJET_ALFRED\)
**Portée** : synthèse de tous les points ouverts identifiés lors de l'audit blocs 1→29,
de la construction du dashboard qualité data, et de la formalisation des Blocs 23/24/25.
**Où retrouver le détail vivant** : `dashboard/dashboard_quality_data/dashboard_quality_data.json`
(section `alerts`) pour les alertes générées automatiquement — ce document ajoute le
contexte, la priorité et la marche à suivre que le dashboard seul ne donne pas.

---

## Légende priorité

| Niveau | Signification | Délai indicatif |
|--------|----------------|------------------|
| **C5** | Critique — donnée sensible exposée à un accès non prévu, agir en premier | dès le retour PC |
| **C4** | Élevée — incohérence ou lacune de gouvernance qui fausse le pilotage | cette semaine |
| **C3** | Modérée — dette de qualité, pas de risque immédiat | ce mois-ci |
| **C2** | Faible — amélioration continue, au fil de l'eau | quand disponible |
| **C1** | Sans urgence — déjà vérifié / nice-to-have | pas de délai |

> Ne pas confondre avec la classification **C1_PUBLIC→C4_SECRET** de `asset_classifier.py`
> (sensibilité d'un fichier) — l'échelle ci-dessus note l'**urgence de traitement**, pas la
> sensibilité de la donnée.

## Colonne "Qui agit"

| Symbole | Signification |
|---------|----------------|
| 🤖 **Claude seul** | Peut être fait à distance dès maintenant, sans le PC ni le réseau local |
| 🖥️ **PC requis** | Nécessite l'environnement réel (fichiers `.env`/secrets non versionnés, Windows Task Scheduler, réseau local, Android Studio/émulateur, ou simplement confirmer un état qui n'existe que là-bas) |
| 👤 **Décision requise** | Arbitrage fonctionnel/produit/sécurité qui n'appartient qu'à toi (OWNER) — Claude peut préparer les options mais ne doit pas trancher seul |

---

## Ordre d'exécution recommandé

1. ~~**C5 — A, B**~~ ✅ tranchés le 13/07/2026 (voir détail ci-dessous — A a généré un nouveau
   point C4-P, mise en conformité technique réelle, à faire sur PC).
2. **C4 — C, D, E, F, P** : lacunes de fiabilité du pilotage, blocage PoC Android, application
   technique de la décision A.
3. **C3 — G, H, I, J** : dette de gouvernance/documentation, pas urgent mais structurant.
4. **En continu — K, M** : poursuite du registre qualité data (Claude peut continuer seul).
5. **C2 — L** : merge des 2 PR une fois C/D/E/F/P au moins tranchés.
6. **C1 — N, O** : déjà vérifié / étape future déjà annoncée.

---

## C5 — Critique

### A. ✅ TRANCHÉ le 13/07/2026 — Référentiels santé (`config/health/`) lisibles par AI_MODULE
- **Décision** : mettre en conformité avec l'exigence (niveau de sécurité prévu 4/5 = CRITICAL).
- **Fait** : `AI_MODULE` retiré de `authorized_roles.read` sur DQ-027 (`config/health/*.json`) —
  ne reste que `OWNER` en lecture et en écriture. L'alerte `acces_non_autorise` a disparu du
  dashboard (0 alerte critique restante sur ce point, vérifié par régénération +
  `pytest tests/dashboard_tests/` → 84 passed).
- **Vérification faite dans le code** : aucun point de contrôle RBAC (`require_access`/
  `check_access`) ne gate aujourd'hui le chargement de `config/health/*.json` — ces fichiers
  sont lus directement par `src/health/*.py`, `src/regulation/regulation_engine.py` et
  `src/core/pipeline_bridge.py`, sans médiation RBAC. **Ce qui est fait** : la politique
  déclarée (registre qualité data) est maintenant conforme. **Ce qui reste ouvert** :
  aucune application technique réelle de cette restriction dans le pipeline — si l'on veut que
  ce soit réellement bloqué (pas seulement documenté), il faut ajouter un contrôle d'accès
  explicite dans ces 3 modules avant lecture. C'est un changement de comportement du pipeline
  santé/adaptation → 🖥️ **à tester en conditions réelles sur le PC** avant de le coder/committer
  (risque de casser l'adaptation comportementale temps réel si mal isolé). Nouveau point à
  traiter, ajouté en C4 ci-dessous (C4-P).

### B. ✅ TRANCHÉ le 13/07/2026 — Logs de sécurité / audit trail, écriture par AI_MODULE
- **Décision demandée** : vérifier la pertinence ; si pertinent, documenter ; sinon, adapter.
- **Vérifié dans le code** : `AI_MODULE` n'a que l'écriture (append), jamais la lecture (déjà
  restreinte à `OWNER`/`ADMIN`). `security_logger.log_event()`/`audit_trail.write_audit_event()`
  sont appelés depuis 55 fichiers du pipeline, y compris les modules IA — retirer cet accès
  casserait la journalisation des actions de l'IA elle-même, contraire au principe Zero Trust
  "assume breach" (tout composant, y compris l'IA, doit logger ce qu'il fait).
- **Conclusion : pertinent.** Documenté comme dérogation officielle plutôt que retiré — nouveau
  champ `access_exceptions` ajouté au schéma du registre (rôle, scope read/write, justification,
  qui a revu, quand). Le moteur d'alertes distingue maintenant une dérogation documentée
  (nouveau type `acces_derogatoire_documente`, sévérité `info`) d'un vrai accès non autorisé
  (`acces_non_autorise`, `critical`) — 2 tests ajoutés pour vérifier ce comportement (84 tests
  au total, tous verts).
- **Fait** : DQ-003 complétée avec la dérogation justifiée et revue par OWNER le 13/07/2026.

---

## C4 — Élevée

### C. Trois fichiers de sécurité runtime attendus mais absents du disque
- **Preuve** : `data/security/access_decisions_history.json`, `incident_register.json`,
  `trusted_devices_runtime.json` sont dans `dashboard_data_manifest.json` (Bloc 20) mais
  n'existent pas — DQ-045. Ils comptent pourtant dans le calcul d'avancement B20 (189/181,
  >100 %), donnant un **faux sentiment de complétude sécurité**.
- **Action** : soit les créer (schéma à définir avec les modules qui devraient les alimenter :
  `incident_manager.py`, `policy_decision_point.py`, `device_registry.py`), soit les retirer du
  manifest s'ils ne sont pas prioritaires actuellement.
- **Qui agit** : 🤖 Claude peut proposer un schéma JSON vide structuré à distance ; 🖥️ le
  contenu réel (incidents effectivement survenus, décisions d'accès réelles) ne peut venir que
  du système qui tourne sur le PC.

### D. Trois fichiers dupliqués et obsolètes à la racine de `dashboard/`
- **Preuve vérifiée aujourd'hui** :
  - `dashboard/dashboard_manifest.json` — 20 blocs seulement (b01→b20), dernière génération
    02/05/2026. `PATHS.dashboard_manifest` (`paths.py:98`) n'est utilisé **nulle part** dans le
    code sauf un `print()` de debug (`paths.py:247`) — wiring mort.
  - `dashboard/dashboard_data.json` — stale depuis le 04/07/2026 (1,36 Mo), alors que
    `dashboard/dashboard_data/dashboard_data.json` (le vrai, régénéré aujourd'hui) fait 1,56 Mo.
  - `dashboard/validation_registry.json` — 19 Ko, contre 532 Ko pour
    `dashboard/dashboard_data/validation_registry.json` (le vrai).
  - Les 3 ne sont référencés que par un test superficiel (`test_dashboard_json_files_are_valid_json`
    dans `tests/b20_tests/test_smoke_batch1.py`) qui vérifie juste "est-ce du JSON valide" —
    aucune dépendance fonctionnelle réelle trouvée.
- **Action** : archiver les 3 fichiers (`dashboard/_archive/`, comme déjà fait pour d'autres
  manifests obsolètes), retirer leurs 3 entrées de `DASHBOARD_JSON_FILES` dans
  `test_smoke_batch1.py`, et soit supprimer soit rediriger `PATHS.dashboard_manifest` dans
  `paths.py` vers le vrai chemin.
- **Qui agit** : 🤖 **Claude peut le faire intégralement à distance** — vérification déjà faite,
  risque faible, mais je n'ai pas exécuté cette suppression sans ton feu vert explicite (fichiers
  déjà présents dans le dépôt, pas créés par moi).

### E. Résolution des chemins `ALFRED_WEB/` — sensibilité à la casse
- **Preuve** : `EXTERNAL_ROOTS = {"ALFRED_WEB/": ALFRED_ROOT}` dans `update_dashboard_data.py`
  suppose un dossier `ALFRED_WEB` (majuscules). Le dépôt GitHub s'appelle `alfred_web`
  (minuscules — vérifié via `git remote -v`). Dans cet environnement (Linux, sensible à la
  casse), le scan du Bloc 21 détecte **0 fichier sur 82 attendus**.
- **Nuance** : sur Windows (NTFS), la résolution de chemin est insensible à la casse, donc ça
  fonctionne probablement chez toi si le dossier local s'appelle `ALFRED_WEB`. Mais c'est un
  bug de portabilité qui **cassera** dès qu'un clone est fait avec le nom exact du dépôt GitHub
  (`alfred_web`), ou sur toute machine Linux/Mac (CI, ce sandbox, etc.).
- **Action** : confirmer le nom exact du dossier local sur ton PC, puis rendre la résolution
  insensible à la casse dans `_resolve_path()` (ou committer un alias).
- **Qui agit** : 🖥️ confirmation du nom réel du dossier nécessaire ; 🤖 Claude peut coder le
  correctif ensuite.

### F. `interface/companion_api.py` et `start_companion_api.bat` absents du dépôt
- **Preuve** : `ALFRED_ANDROID/README.md` documente ces deux fichiers comme prérequis pour
  faire tourner le PoC Compagnon côté ALFRED_PC. Recherche exhaustive (tous fichiers, toutes
  branches de `alfred_assistant`) : **aucune trace**, ni sur `main` ni sur la branche de travail.
- **Action** : soit ces fichiers existent en local non commités sur ton PC (à committer), soit
  ils restent à développer. Dans les deux cas le PoC Android n'est pas utilisable tel quel
  depuis ce dépôt distant.
- **Qui agit** : 🖥️ à vérifier sur le PC (fichier local non poussé ?) ; si à développer, 🤖
  Claude peut rédiger un premier jet à distance à partir du contrat d'API déjà documenté côté
  client (`CompanionApiService.kt` : `GET /api/status`, `GET /api/notifications`, jeton
  `COMPANION_API_TOKEN`), mais 🖥️ le test réel (build + émulateur + connexion) nécessite le PC.

### P. (nouveau, issu de A) Appliquer techniquement la restriction santé dans le pipeline
- **Contexte** : suite à la décision A, `config/health/*.json` est maintenant restreint à
  `OWNER` dans le registre de gouvernance, mais **rien ne l'empêche techniquement** — ces
  fichiers sont lus directement par `src/health/*.py`, `src/regulation/regulation_engine.py`,
  `src/core/pipeline_bridge.py` sans aucun point de contrôle RBAC.
- **Action** : ajouter un contrôle d'accès explicite (`require_access`/`check_access`, ou
  équivalent) avant le chargement de ces fichiers dans les 3 modules concernés.
- **Qui agit** : 🖥️ **PC requis** — c'est un changement de comportement du pipeline
  d'adaptation santé/comportementale, à tester en conditions réelles (le pipeline complet avec
  modèles LLM locaux ne tourne pas dans cet environnement de préparation) avant de committer.
  🤖 Claude peut préparer un premier jet de patch si utile comme base de travail.

---

## C3 — Modérée

### G. Instance utilisateur nominative non documentée
- **Preuve** : `data/users/instances/user_celine_instance.json` (6,7 Ko) — accès déjà
  correctement restreint à `OWNER` seul (pas un risque d'accès), mais `documented: false` dans
  le registre (DQ-033).
- **Action** : rédiger une description formelle (finalité, base légale, droits RGPD applicables)
  dans le registre. Pas de risque de sécurité immédiat.
- **Qui agit** : 🤖 Claude peut rédiger un projet de description ; 👤 validation du niveau de
  détail acceptable dans une documentation interne.

### H. Bloc 16 — incohérence documentaire non résolue
- **Preuve** : `ALFRED_BLOCS_REFERENCE.md` dit "Bloc 16 réservé — non assigné", mais
  `BACKLOG.md`/`dashboard_data_manifest.json` suivent un contenu réel sous ce label
  (`Démonstration & Scénarisation`, 46,7 %, fichiers de scénarios quasi vides — DQ-039).
- **Action** : trancher — soit formaliser le Bloc 16 dans le référentiel (comme B23/24/25),
  soit confirmer qu'il doit rester réservé et déplacer son contenu ailleurs.
- **Qui agit** : 👤 décision requise (relecture du contenu réel du bloc).

### I. `data/dialogue_history.json` (racine) — orphelin confirmé
- **Preuve vérifiée aujourd'hui** : recherche exhaustive dans le code — aucune référence.
  Seul `data/memory/episodic/dialogue_history.json` est utilisé (`main.py`, `main_v3.py`,
  `memory_engine.py`, `compliance_manager.py`, `data_flow_mapper.py`).
- **Action** : archiver/supprimer `data/dialogue_history.json` (racine).
- **Qui agit** : 🤖 **Claude peut le faire à distance dès confirmation.**

### J. Scaffolding V2/V3/V4 vide jamais branché — décision "construire ou archiver"
- **Preuve** : ~40 fichiers au total (Blocs 02, 03, 06, 12, 16, 18, 19 — DQ-024, 026, 029,
  015, 039, 041, 042, 043), tous créés le 02/05/2026, tous quasi vides (6 à 79 octets), jamais
  modifiés depuis. Ils comptent dans le calcul d'avancement de plusieurs blocs alors qu'ils sont
  vides.
- **Action** : décision produit bloc par bloc — soit prioriser leur mise en service (V2→V3→V4
  déjà dans la roadmap), soit les archiver pour ne plus fausser les pourcentages d'avancement.
- **Qui agit** : 👤 décision de priorisation produit ; 🤖 exécution technique (créer/archiver)
  une fois la décision prise.

---

## En continu — pas de blocage

### K. Poursuivre le registre qualité data
- Blocs 23-25/29 déjà partiellement couverts (peu de fichiers `config/`/`data/` dédiés — la
  plupart de leur contenu réel est déjà référencé ailleurs dans le registre). Reste à faire :
  relecture complète des 44 fiches par l'équipe, complément des champs `"à définir"`
  (durée de conservation, fréquence de mise à jour réelle).
- **Qui agit** : 🤖 Claude peut continuer seul ; 👤 relecture finale nécessaire avant de
  considérer le registre "fiable" pour piloter de vraies décisions d'accès.

### M. Compléter les champs incertains au fil de l'eau
- Plusieurs fiches ont `retention_period`/`update_frequency` marqués "à définir" — à préciser
  quand l'information réelle est connue (ex. politique de rétention pour les scaffolding une
  fois leur sort tranché au point J).
- **Qui agit** : 🤖 Claude peut proposer des valeurs par défaut cohérentes avec le RGPD register
  existant ; 👤 confirmation finale.

---

## C2 — Faible

### L. Merger les 2 PR ouvertes une fois les points ci-dessus au moins tranchés
- **PR #15** (`alfred_assistant`) : dashboard qualité data + Blocs 23/24/25 + registre (44
  fiches). Draft, propre, aucune CI configurée sur ce dépôt.
- **PR #1** (`ALFRED_ANDROID`) : en-têtes Bloc 24 sur les 6 fichiers Kotlin. Draft, propre.
- **Qui agit** : 👤 merge à ta main (droits + relecture finale).

---

## C1 — Sans urgence / déjà vérifié

### N. Templates suffixés `_public` — vérifiés sûrs aujourd'hui
- `data/personality/templates/personality_core_template_public.json` et
  `data/users/templates/user_profile_template_public.json` ont été lus intégralement : aucune
  donnée réelle, uniquement des champs `null`/génériques, explicitement documentés "sans
  données personnelles". **Rien à faire** — juste à re-vérifier si leur contenu évolue avant
  toute future publication (DQ-032, DQ-034).

### O. Sélection des statistiques publiables (déjà annoncée comme étape future)
- Tel que précisé au départ : ce dashboard reste interne, la sélection de ce qui peut être
  publié sur le site se fera plus tard, au cas par cas. Pas d'action avant que tu ne donnes le
  feu vert bloc par bloc.
- **Qui agit** : 👤 décision à venir, pas de délai fixé.

---

## Résumé exécutif (pour lecture rapide)

| # | Sujet | Priorité | Qui agit |
|---|-------|----------|----------|
| A | Accès santé AI_MODULE sous-habilité | C5 | ✅ tranché (registre corrigé) |
| B | Accès logs sécurité AI_MODULE sous-habilité | C5 | ✅ tranché (dérogation documentée) |
| C | 3 fichiers sécurité runtime manquants | C4 | 🖥️🤖 |
| D | 3 duplicatas obsolètes racine dashboard/ | C4 | 🤖 (attend feu vert) |
| E | Casse `ALFRED_WEB/` — scan B21 à 0 % | C4 | 🖥️ puis 🤖 |
| F | `companion_api.py` introuvable | C4 | 🖥️ puis 🤖 |
| P | Appliquer techniquement la restriction santé (issu de A) | C4 | 🖥️ (pipeline à tester) |
| G | Instance Céline non documentée | C3 | 🤖👤 |
| H | Bloc 16 réservé vs contenu réel | C3 | 👤 |
| I | `dialogue_history.json` orphelin | C3 | 🤖 (attend feu vert) |
| J | ~40 fichiers scaffolding vides | C3 | 👤 puis 🤖 |
| K | Poursuite registre (blocs restants) | continu | 🤖 |
| M | Champs "à définir" à compléter | continu | 🤖👤 |
| L | Merge PR #15 et #1 | C2 | 👤 |
| N | Templates `_public` | C1 | ✅ fait |
| O | Sélection stats publiables | C1 | 👤 (futur) |
