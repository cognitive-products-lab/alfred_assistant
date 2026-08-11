# ALFRED — Roadmap maître V0 → V-Finale

> Généré le 2026-08-11 à partir de : `dashboard/dashboard_data/dashboard_data.json` (source de vérité technique, mis à jour le 11/08/2026 08:40),
> `dashboard/dashboard_data/dashboard_data_manifest.json`, `docs/ALFRED_BLOCS_REFERENCE.md` (structure officielle des 26 Blocs),
> `ROADMAP.md` (dernière mise à jour manuelle : 05/07/2026 — **obsolète sur plusieurs points, corrigé ci-dessous**),
> historique git des 4 dépôts (ALFRED_PC, ALFRED_WEB, ALFRED_CPL, ALFRED_ANDROID) et mémoire de session.
>
> **Objectif du document** : vue Epic → Sprint → User Story → Livrable de l'ensemble du projet, avec un statut honnête
> (Finalisé / Réalisé / En cours / À réaliser) par user story, base de l'exercice suivant (tableau de tâches → Gantt).

---

## 0. Deux chiffres qui résument tout

| Indicateur | Valeur | Ce qu'il mesure |
|---|---|---|
| **Avancement du périmètre courant** | **87,6 %** | Sur les 1322 fichiers *actuellement attendus* (ce qui est planifié pour le sprint/la version en cours), combien existent et sont validés. |
| **Avancement vision finale (V0→V-finale)** | **27,9 %** | Sur les **4436 fichiers cibles** de la vision complète du produit (tous produits, toute la base de connaissances), combien sont faits. |

**L'écart entre ces deux chiffres est la clé de lecture de toute la roadmap.** ALFRED est très avancé sur ce qu'il a *décidé de construire jusqu'ici*, mais la vision complète (notamment la base de connaissances à 3000 fichiers, cible du Bloc 18, qui représente à elle seule 67 % du total des 4436 fichiers cibles) reste largement à construire. Ce n'est pas un retard caché — c'est la définition même de "V-finale" : un objectif lointain et volontairement ambitieux.

**Contexte de la reprise** : aucun commit substantiel (hors synchronisation automatique quotidienne des dashboards) sur ALFRED_PC depuis le **24/07/2026**, ni sur ALFRED_WEB depuis le **23/07/2026**, ni sur ALFRED_CPL/ALFRED_ANDROID depuis le **16/07/2026** — pause liée à un impératif de santé de Céline (concentration sur son plan de révision d'examens). Objectif explicite de la reprise du 11/08 : **un projet propre et démontrable pour les soutenances FEDE d'octobre 2026** (Mastère Expert IT — IA & Big Data) — UC D42 prêt, **UC D52 en cours** (thèse ALFRED, soutenance principale à préparer), UC B5 (synthèse anglaise) à réaliser. Cette roadmap et sa mise à jour de `ROADMAP.md` (corrections section 5) sont l'objectif même de cette session, pas un simple constat de retard.

---

## 1. Les produits / dépôts du projet ALFRED

| Dépôt / dossier | Rôle | État dépôt (11/08/2026) |
|---|---|---|
| `ALFRED_PC` | Cœur du système : conversation, mémoire, émotion, sécurité, avatar, connaissances, dashboards | Actif — dernier commit fonctionnel 24/07 |
| `ALFRED_WEB` | Vitrine publique + dossier de cadrage + thèse D52 + dashboards publics | Actif — dernier commit fonctionnel 23/07 |
| `ALFRED_CPL` | Produit "collaborateur professionnel" dérivé — dépôt extrait le 13/07 | Dormant depuis 16/07 (juste une régénération de démo) |
| `ALFRED_ANDROID` | Compagnon mobile natif (Kotlin/Compose) — PoC | Dormant depuis 16/07 (juste des en-têtes KDoc) |
| `ARTHUR` (dossier) | Compagnon pédiatrique/santé — **dossier vide sur disque** | **Non démarré** — concept uniquement, cf. Bloc 13 |
| `COGNITIVE_PRODUCTS_LAB` | Documents business (business plan, étude de marché, pitch deck) datés juin 2026 | Statique — pas du code |

---

## 2. Macro-roadmap : V0 → V-finale

La structure officielle du projet repose sur **26 Epics** ("Blocs", `docs/ALFRED_BLOCS_REFERENCE.md`), chacun avec des sous-codes `XX.YY` (= granularité "user story"). Ils se répartissent en 5 grandes releases :

| Release | Contenu | Epics concernés | Statut release |
|---|---|---|---|
| **V0 — Cadrage** | Vision produit, business plan CPL, principes local-first, gouvernance 360 initiale | (pré-code, pas de Bloc dédié) | ✅ Finalisé |
| **V1 — Fondations** | Noyau conversationnel, mémoire, émotions, sécurité utilisateur, assistance quotidienne, personnalisation, cybersécurité, gouvernance, plateforme web | b01, b02, b03, b04, b05, b06, b08, b09, b11, b12, b18, b20, b21, b22, b23, b25, b29(PoC) | 🟢 Réalisé à ~90 %+ sur le périmètre courant |
| **V1.x / V1.4 — Modules actifs** | Avatar & présence visuelle, sécurité réseau physique, profil IA adaptatif | b15 (+ volet réseau de b20) | 🟢 Réalisé, 2 items reportés explicitement |
| **V2 — Extension produits & contexte** | Mobilité/contexte externe, collaboration pro (CPL), compagnon Android | b07, b10, b24 | 🟡 En cours, socle posé |
| **V3 — Expérience avancée & démonstration** | Démonstration/scénarisation, génération visuelle contextuelle, domotique intelligente | b16, b17, b19 | 🟡 En cours / 🔴 bloqué (b17) |
| **V4 / V-finale — Vision long terme** | Compagnon santé ARTHUR, IoT complet, base de connaissances à 3000 fichiers, domotique Tuya opérationnelle | b13, b14, b17 (finalisation), b18 (finalisation), b19 (finalisation) | 🔴 À réaliser en grande partie |

---

## 3. Détail par Epic

Légende statut : ✅ **Finalisé** (≥95 % périmètre courant, validé en conditions réelles) · 🟢 **Réalisé** (85–95 %, socle solide, finitions restantes) · 🟡 **En cours** (50–85 %, construction active ou partielle) · 🔴 **À réaliser** (<50 %, ou bloqué, ou non démarré).

### V1 — Fondations

#### Epic b01 — Interaction conversationnelle intelligente *(Bloc officiel 01)*
**Statut : ✅ Finalisé** — 95,8 % périmètre courant (67 fichiers attendus, 54 validés, 8 structurels, 4 partiels) · 107 % de la cible V1 initiale (dépassée).
- **Sprints réalisés** : pipeline conversationnel V1 (STT Whisper + LLM + TTS Piper) ; routeur LLM local-first Ollama→OpenAI→Anthropic ; function-calling réel branché au chat (23/07, corrige une hallucination d'UI) ; moteur de tâches complet + garde-fou anti-hallucination outils (24/07, ~35-40 % des appels d'outils llama3.2 n'aboutissaient à rien de réel avant le correctif) ; fixes TTS (élision, heure, double lecture).
- **User stories clés** :
  | Sous-code | User story | Statut |
  |---|---|---|
  | 01.01 Gestion des conversations | ✅ Finalisé | Validé, usage quotidien |
  | 01.02 Compréhension des intentions | ✅ Finalisé | NLP engine v2 validé |
  | 01.03 Gestion du contexte | 🟢 Réalisé | context_builder validé |
  | 01.04 Orchestration des modules | ✅ Finalisé | TaskEngine (24/07) + garde-fou fiabilité |
  | 01.05 Gestion des réponses | 🟡 En cours | `tts_engine.py`, `tts_output.py`, `tts_piper.py` marqués partiels au dernier passage manuel |
- **Livrable réel** : pipeline vocal + textuel bout-en-bout fonctionnel, utilisé en production quotidienne. **Point de vigilance honnête** : les 3 fichiers TTS listés « partiels » n'ont pas été revalidés depuis — à repasser en revue humaine.

#### Epic b02 — Mémoire & RAG *(Bloc officiel 02)*
**Statut : 🟢 Réalisé** — 93,6 % / 65,5 % vision finale (28 attendus, 22 validés, 4 partiels).
- User stories : mémoire courte ✅, mémoire longue 🟢, RAG 🟡 (config `memory_rules.json` v3 et `memory_manager.py` toujours listés partiels).
- **Livrable** : mémoire épisodique opérationnelle (système fondateur de V0). RAG structurant présent mais règles v3 à compléter.

#### Epic b03 — Émotions & Régulation *(Bloc officiel 03)*
**Statut : ✅ Finalisé** — 97,6 % / 87,4 % (85 attendus, 67 validés, 13 structurels, 5 partiels).
- **Livrable** : moteur de régulation émotionnelle + adaptation comportementale, `personality_adapter.py` et `response_generator.py` V2.3 branchés. Configs `emotion_profiles/rules`, `tone_profiles` encore partiels (finition mineure).

#### Epic b04 (dashboard) → Bloc officiel 08 — Sécurité & Protection utilisateur / Supervision système
**Statut : ✅ Finalisé** — 95,3 % / 71,5 % (15 attendus, 12 validés).

#### Epic b05 (dashboard) → Bloc officiel 06 — Assistance quotidienne
**Statut : 🟢 Réalisé** — 94,7 % / 71 % (15 attendus, 12 validés, 2 partiels : `tasks.json`, `daily_organization.json`).
- **Sprint marquant** : **Chantier 1 — Google Agenda**, terminé et vérifié le 23/07/2026 : lecture + écriture confirmées sur le vrai compte Google (create/list/delete/modify event depuis le chat), commit `dac0a4f`.
- **Livrable réel et vérifié** ✅ — pas une preuve fantôme, testé en conditions réelles.

#### Epic b06 (dashboard) → Bloc officiel 12 — Communication & Lien social / Collaboration pro
**Statut : ✅ Finalisé (périmètre courant)** — 100 % / 58 % vision finale (29/29 validés). Marge de croissance vers la cible finale (50 fichiers) côté collaboration professionnelle avancée.

#### Epic b08 — Personnalisation utilisateur *(Bloc officiel 05)*
**Statut : 🟢 Réalisé** — 97,1 % / 66 % (34 attendus, 30 validés, 2 partiels : `personality.json`, `preferences_profile.json`).
- **Correction au `ROADMAP.md`** : celui-ci liste encore en P1 "Remplissage Q01→Q09 utilisateur — en attente (main bloquée)". **C'est faux depuis le 18/07/2026** : l'onboarding complet (profil MBTI EXFP, dimension émotionnelle et santé) a été réalisé en conversation ce jour-là. Ligne à supprimer du backlog.

#### Epic b09 — Productivité & Copilote pro *(Bloc officiel API/microservices CPL)*
**Statut : ✅ Finalisé** — 96,8 % / 98,1 % (152 attendus — le plus gros epic en volume avec b20, 117 validés, 12 partiels, 22 structurels).

#### Epic b11 — Intelligence cognitive avancée *(Bloc officiel 10)*
**Statut : 🟢 Réalisé** — 97,4 % / 56 % (23 attendus, 19 validés, 1 partiel : `knowledge_router.py`).

#### Epic b12 — Pilotage business & Stratégie *(Bloc officiel 11)*
**Statut : 🟢 Réalisé** — 98 % / 96,3 % (59 attendus, 48 validés, 3 partiels).
- **Point de vigilance** : `config/v2/product_roadmap.json` (l'export structuré destiné à un futur dashboard roadmap) reste à l'état `"SCHEMA_DEFINI — pas encore chargé par le code"`, `milestones: []`. Le présent document (Markdown) reste la source de vérité tant que ce fichier n'est pas branché.

#### Epic b18 — Knowledge & Intelligence System *(Bloc officiel 18)*
**Statut : 🟢 Fonctionnel — apprentissage continu par design, jamais "Finalisé".**
- **Précision (11/08/2026)** : ce bloc n'est pas censé atteindre un jour un statut "Finalisé" — l'objectif est un apprentissage et un développement continus de la base de connaissances, par nature sans fin. Le niveau minimum souhaité pour être fonctionnel **est déjà atteint**. Ne pas le traiter comme "en retard" dans le Gantt ; à traiter plutôt comme un flux d'enrichissement permanent (cf. `daily_enrichment_instructions.md`, répartition CPL/socle quotidienne déjà en place), pas comme une tâche à date de fin.
- 87,2 % du périmètre courant, mais **seulement 11,3 % de la vision finale** (388 fichiers attendus aujourd'hui sur une cible de **3000**, elle-même indicative plutôt qu'un plafond réel vu la nature continue du bloc).
- 237 validés, **73 « codés — jamais testés »** (gros lot business_strategy CPL, interaction humaine, wellbeing, reasoning avancé, gouvernance IA, IoT — livrés mais non relus), 44 partiels (règles de config v2/v3, états v2/v3), 32 structurels.
- **Correction au backlog mémorisé** : l'ancien point "75 fiches de connaissance vides à rédiger" (06/07) semble résolu — **0 fichier vide détecté** aujourd'hui dans `knowledges/` (939 fichiers .json, tous non-vides). À confirmer que ce sont bien les mêmes 75 fiches.
- **Livrable** : socle solide et structuré, mais l'essentiel de la base de connaissances visée (V3/V4) reste à écrire.

#### Epic b20 — Cybersécurité Zero Trust *(Bloc officiel 20)*
**Statut : ✅ Finalisé (périmètre courant)** — 98,2 % / 92,8 % (189 attendus, 166 validés). Le plus mature avec b21.
- **Sprint marquant (05/07)** : double NAT résolu, pare-feu WAN vérifié, micro-segmentation VLAN 10/20/30 opérationnelle, faille Wi-Fi corrigée.
- **Reporté explicitement (assumé, pas un oubli)** : ACL inter-VLAN, VPN OpenVPN scopé VLAN_ADMIN, achat point d'accès Wi-Fi Omada EAP610 (prévu **août 2026 — ce mois-ci**, à vérifier si fait).

#### Epic b21 — ALFRED Web Platform *(Bloc officiel 21)*
**Statut : ✅ Finalisé — 100 % / 100 %.** Seul epic à avoir atteint sa cible finale complète (82/82 fichiers). Dossier de cadrage, thèse D52 (3 parties + conclusion + annexes), dashboards publics (conformité, gouvernance, qualité-data), articles publiés.

#### Epic b22 — Accessibility & Cognitive Assistance *(Bloc officiel 22)*
**Statut : 🟢 Réalisé (périmètre courant), 🟡 en cours vers la cible finale** — 100 % / 42 % (21 attendus sur cible 50). Modes d'accessibilité (voice_output_manager, text_reader, WCAG checker) posés ; reste à couvrir : accessibilité Android (22.13), conformité WCAG formelle (22.15), neurodiversité avancée (22.12).

#### Epic b23 — Gouvernance & pilotage du projet *(Bloc officiel 23)*
**Statut : 🟡 En cours** — 90,8 % / 90,8 % (13 attendus, 9 validés, **3 « codés — à tester »** : `update_dashboard_data.py`, `ROADMAP.md`, `BACKLOG.md`, 1 partiel).
- **Point important pour cet exercice précis** : les outils de gouvernance qui produisent les chiffres cités dans ce document (`update_dashboard_data.py`) sont eux-mêmes non "validés" à 100 % — cohérent avec l'anomalie du Bloc 17 détectée en section 4. Historique de bugs similaires déjà rencontrés (`_meta.generated` figé, "preuves fantômes" sur dashboard Conformité, corrigés en juillet).

#### Epic b25 — Documentation & politiques projet transverses *(Bloc officiel 25)*
**Statut : 🟡 En cours** — 62,2 % / 62,2 % (9 attendus, 1 validé, 6 « codés — à tester » : README_FR, LICENSE, CONTRIBUTING(_FR), CODE_OF_CONDUCT, schéma réseau SVG ; 2 partiels : `docs/architecture/README.md`, `docs/ux/README.md`).
- **Livrable** : les documents légaux/communautaires existent mais n'ont pas de statut "validé" formel (pas de revue juridique/qualité tracée).

#### Epic b29 — Démonstrateur Big Data Hadoop *(Bloc officiel 29, PoC hors trajectoire produit)*
**Statut : ✅ Finalisé — 100 % / 100 %.** PoC assumé comme tel (regard critique documenté sur le surdimensionnement, `docs/hadoop_poc_bilan.md`) — pas une brique de production, ne pas le compter dans "V-finale produit".

---

### V1.x / V1.4 — Modules actifs

#### Epic b15 — Présence visuelle & Avatar *(Bloc officiel 15)*
**Statut : 🟢 Réalisé** — 98,1 % / 56,7 % (52 attendus, 47 validés, 2 « codés — à tester » : `alfred_app.py`, `webcam_widget.py`, 1 partiel).
- **Sprints marquants** : système avatar en calques (F/G/BL/SP/M/V00-14) tous créés ; couture V-series vs f00 corrigée le 20/07 (cv2.seamlessClone, Poisson blending) ; **synchro labiale phonème-exacte implémentée et testée le 23/07** (PiperTTS→API Python, table phonème→visème câblée en JS). Renderer 6 calques, halo, sprites par état (idle/listening/thinking/speaking/support/focus + blink).
- **Point de vigilance connu** : 2 copies du modèle `.onnx` existent dans le dépôt, seule `tools/piper/models/` est chargée en prod — piège identifié à ne pas retomber dedans.
- **Livrable réel et testé** ✅.

#### Volet réseau de b20 (Sécurité réseau physique, session 05/07)
Détaillé ci-dessus dans b20 — traité comme sous-sprint et non comme epic séparé (pas de Bloc dashboard dédié).

---

### V2 — Extension produits & contexte

#### Epic b07 — Mobilité & Contexte externe *(Bloc officiel 07)*
**Statut : 🔴 À réaliser** — 86,7 % / **13 %** (3 fichiers attendus seulement — quasiment un stub). Ce bloc contient surtout, aujourd'hui, la note de vision "Roadmap V2 — ALFRED Android : client mobile léger connecté au core ALFRED_PC (API REST/WebSocket + tunnel WireGuard, JWT + TLS mutuel)". Le vrai développement mobile est suivi sous b24.

#### Epic b10 — Collaboration & Coordination *(Bloc officiel 12, volet CPL)*
**Statut : 🔴 À réaliser** — 84 % / 14 % (5 fichiers attendus, 2 validés, 3 partiels : `orchestrator_rules.json`, `workflow_rules.json`, `src/v3/orchestrator/__init__.py`).
- Cohérent avec l'état du dépôt `ALFRED_CPL` : extrait le 13/07, dormant depuis le 16/07 (une seule régénération de démo depuis, liée à la résolution d'un incident `FERNET_KEY`). Le moteur d'orchestration "collaborateur pro" (mode brainstorming, revue de docs, co-rédaction) n'est pas construit.

#### Epic b24 — ALFRED Android / Compagnon mobile natif *(Bloc officiel 24)*
**Statut : 🟡 En cours (PoC validé, produit non commencé)** — 65 % / 65 % (12 attendus, **0 validé formellement**, 10 « codés — à tester », 1 testé).
- **Sprint marquant** : PoC "Compagnon" validé de bout en bout le 02/07/2026 (build + émulateur Pixel 6 + connexion API réelle).
- **Ce qui manque pour le produit complet** (explicitement noté dans le Bloc officiel) : HTTPS (le PoC est en cleartext réseau local volontaire), notifications push, mode hors-ligne.
- **Livrable** : PoC fonctionnel mais pas de statut "validé" formel dans le dashboard — écart entre "ça marche en démo" et "c'est du produit fini" à ne pas confondre.

---

### V3 — Expérience avancée & démonstration

#### Epic b16 — Démonstration & Scénarisation *(Bloc officiel 16, formalisé le 16/07)*
**Statut : 🔴 À réaliser** — 66,7 % / 13,3 % (6 attendus, 1 testé, 5 partiels : catalogue de scénarios, résultats, et les 3 scénarios métier — transition de carrière, isolement, surcharge mentale).

#### Epic b17 — Visual Generation contextuelle *(Bloc officiel 17)*
**Statut : ✅ Périmètre volontairement réduit (décision produit, pas une anomalie).**
- **Correction (11/08/2026)** : la cible à 0 fichier n'est pas une perte de données ni un bug de manifest — Céline a tranché que le fond visuel reste **neutre**, aligné sur l'interface existante, ce qui **allège le système visuel** plutôt que de maintenir un pipeline de génération contextuelle de 200 visuels de fond par état/scénario.
- Vérification sur disque cohérente avec cette décision : `assets/backgrounds/` vide, `assets/ui/` réduit à 4 fichiers.
- L'écart avec le `BACKLOG.md` du 19/07/2026 (72 validés + 12 testés à l'époque) s'explique donc par ce choix de simplification survenu entre le 19/07 et aujourd'hui, pas par une régression outillage.
- **Action résiduelle** : mettre à jour le manifest (`dashboard_data_manifest.json`, `target_full_files_count`) pour refléter la cible réduite (le solde des 30 fichiers runtime/config, si le concept de génération visuelle contextuelle est conservé sous une forme minimale — à confirmer) plutôt que de laisser la cible affichée à 230. Sans quoi ce bloc continuera à afficher un faux 0 % dans tous les futurs rapports.

#### Epic b19 — Domotique Intelligente *(Bloc officiel 19)*
**Statut : 🔴 À réaliser — séquencement assumé.** — 73,3 % / 50 % mais **0 fichier validé** sur 15 attendus (10 partiels, 5 structurels — que des schémas de config, rien d'implémenté).
- **Précision (11/08/2026)** : développement et validation prévus une fois V1 **et** V2 entièrement finalisées — cohérent avec le blocage Tuya déjà documenté. Ne pas prioriser ce bloc dans le Gantt avant que V1/V2 soient closes.
- **Contexte mémoire** : Chantier 1B (Google Home/Nest) **bloqué définitivement le 24/07** — code écrit (commit "feat(v4): intégration Google Home/Nest + vision sécurité domestique") mais Céline n'a que des enceintes Nest, non supportées par l'API SDM (seuls thermostat/caméra/sonnette/Hub Max le sont). Ne pas redépanner l'OAuth Google Home.
- Chantier 2 (Sécurité chute/Tuya) : **vision écrite et complète** (`docs/module_securite_accompagnement/vision_securite_accompagnement_360.md`, 24/07) — Sébastien confirmé comme contact de confiance, caméras RTSP + audio bidirectionnel prévues — **mais 3 inconnues Tuya non résolues bloquent tout début de code.**
- **Livrable** : documentation de conception excellente, **zéro ligne de code fonctionnelle** à ce stade. À réaliser en V3/V4 une fois les inconnues Tuya levées.

---

### V4 / V-finale — Vision long terme

#### Epic b13 — Compagnon pédiatrique / ARTHUR *(Bloc officiel 13)*
**Statut : 🔴 Non démarré — séquencement assumé, pas un point bloquant.** — 100 % / **20 %** (6 fichiers seulement attendus, 5 validés, cible finale 30 fichiers, dossier `ARTHUR/` vide sur le disque).
- **Précision (11/08/2026)** : ARTHUR ne sera développé qu'une fois ALFRED_PC et ALFRED_CPL "au point" — c'est une séquence délibérée (V4, dépendance explicite sur la maturité des deux autres produits), pas une décision produit en attente. Ne pas le mettre dans le Gantt tant que ALFRED_PC/ALFRED_CPL n'ont pas atteint le seuil de maturité visé.
- Second utilisateur ALFRED (Sébastien, 47 ans) — identité seule renseignée, pas d'onboarding complet ; cohérent avec le fait qu'ARTHUR n'est pas encore engagé.

#### Epic b14 — IoT & Intégrations *(Bloc officiel 14)*
**Statut : 🔴 À réaliser, bloqué** — 100 % / 5 % (1 seul fichier structurel attendu — stub de vision). Le vrai contenu IoT est tracké sous b19 (voir ci-dessus, même blocage).

#### Finalisation V4 des epics déjà entamés
- **b17** (Visual Generation) — une fois l'anomalie résolue, compléter jusqu'à 230 fichiers.
- **b18** (Knowledge base) — pas un chantier à clôturer : flux d'enrichissement continu par design, déjà fonctionnel au seuil minimum souhaité ; la progression de 388 vers 3000 fichiers se poursuit en tâche de fond, hors séquence de finalisation.
- **b19** (Domotique) — débloquer Tuya, industrialiser la sécurité/accompagnement.
- Gouvernance IA éthique complète (AIPD, PSSI, SoA) — **mise à jour par rapport au `ROADMAP.md`** : AIPD (`docs/rgpd/aipd_donnees_sante.md`, `aipd_comptes_deploiement_public.md`) et PSSI (`docs/security/PSSI.md`) **existent déjà**, contrairement à ce que listait le backlog P1 du 05/07 comme "en attente". Statut réel : 🟢 Réalisé, à vérifier si formellement validés/signés plutôt que rédigés.

---

## 4. Synthèse des points de vigilance (à traiter avant le chiffrage Gantt)

Points clarifiés en direct par Céline le 11/08/2026 pendant la rédaction de ce document — corrigés ci-dessous plutôt que laissés comme anomalies ouvertes.

| # | Point | Gravité | Statut |
|---|---|---|---|
| 1 | ~~Bloc 17 (Visual Generation) : manifest vidé, 0 fichier sur disque~~ | — | **Clarifié** : décision produit assumée — fond neutre aligné sur l'interface existante, allège le système visuel. Pas une perte de données. Reste une action résiduelle : mettre à jour la cible du manifest (230→réduite) pour que le dashboard ne réaffiche pas un faux 0 % indéfiniment. |
| 2 | ~~ARTHUR : dossier vide, décision produit non tranchée~~ | — | **Clarifié** : séquencement assumé — ARTHUR après ALFRED_PC + ALFRED_CPL "au point". Pas un point bloquant, juste hors Gantt pour l'instant. |
| 3 | **`ROADMAP.md` obsolète** : P1 "Q01→Q09 en attente" (réalisé 18/07) et P1 "AIPD/PSSI en attente" (fichiers existants) étaient des faux retards | 🟢 Corrigé | `ROADMAP.md` mis à jour le 11/08/2026 (voir section 5) — c'était l'objectif même de cette session : une roadmap à jour et claire |
| 4 | **Bloc 23 (gouvernance/dashboard)** lui-même non entièrement validé (`update_dashboard_data.py` "codé à tester") | 🟡 Moyenne | Explique le décalage observé sur le Bloc 17 — auditer le script de génération pour que la cible manifest suive les décisions produit |
| 5 | **18 jours d'inactivité fonctionnelle** (24/07 → 11/08) sur ALFRED_PC/WEB, dépôts CPL/Android dormants depuis mi-juillet | ℹ️ Clarifié | Pause liée à un impératif de santé de Céline (plan de révision d'examens) — voir mémoire de session. Reprise du 11/08 orientée vers un projet propre et démontrable pour les soutenances FEDE d'**octobre 2026** (D42 prêt, D52 en cours — soutenance ALFRED principale —, B5 à réaliser). |
| 6 | **`config/v2/product_roadmap.json`** reste un schéma vide (`milestones: []`), non branché au code | ℹ️ Faible | Ce document Markdown + `ROADMAP.md` font office de source de vérité en attendant |
| 7 | ~~Bloc 19 Domotique : 0 fichier validé malgré 73 % de "progress"~~ | — | **Clarifié** : séquencement assumé — à développer et valider une fois V1 et V2 entièrement finalisées. Le pourcentage dashboard reste à lire avec prudence (squelette de config, pas de fonctionnalité) mais ce n'est pas un point bloquant à traiter maintenant. |

---

## 5. Corrections apportées à `ROADMAP.md` par ce document

- ❌ *"Q01→Q09 — remplissage des réponses utilisateur (en attente)"* → ✅ Fait le 18/07/2026 (onboarding complet confirmé en mémoire de session).
- ❌ *"AIPD T001 (RGPD art.35) — Obligatoire avant production"* listé en attente → les fichiers `aipd_donnees_sante.md` et `aipd_comptes_deploiement_public.md` existent déjà — à vérifier s'ils sont formellement validés, mais plus "non démarrés".
- ❌ *"PSSI formelle — docs/gouvernance/PSSI_formelle.md"* → le fichier existe sous `docs/security/PSSI.md` (chemin différent de celui noté).
- ➕ À ajouter au `ROADMAP.md` : tout ce qui s'est passé après le 05/07 et n'y figure pas — Chantier 1 Google Agenda (terminé), Chantier 1B Google Home (bloqué définitivement), Chantier 2 sécurité/Tuya (conception seule), moteur de tâches + fiabilité function-calling, synchro labiale phonème-exacte, UI hybride voix+texte, article évolution interface, fix dashboard gouvernance, page qualité-data.

---

## 6. Prochaine étape

Ce document sert de base à l'exercice suivant : **tableau de tâches détaillé** (durée estimée, statut, dépendances, ressource) pour construire un diagramme de Gantt. Granularité recommandée : une ligne de tâche par user story "🟡 En cours" ou "🔴 À réaliser" listée ci-dessus (les "✅ Finalisé" et "🟢 Réalisé" n'ont pas besoin d'entrer dans le Gantt, sauf finition ponctuelle identifiée). Point bloquant à lever en premier : anomalie Bloc 17 (section 4, #1), car elle fausse tout chiffrage de charge restante sur cet epic.
