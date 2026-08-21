# Vision — Knowledge, Training Dataset & Fine-Tuning ALFRED
## Cognitive Products Lab — ALFRED

> Version 1.0 — 2026-08-21
> Statut : CONCEPTION — rien codé, aucun commit
> Origine : document de cadrage fourni par Céline le 21/08/2026, *« ALFRED —
> Plan de mise en place Knowledge, Training Dataset & Fine-Tuning »*, étudié
> et confronté au code réel le 21/08/2026.
> Relation avec [`vision_architecture_cognitive_alfred.md`](vision_architecture_cognitive_alfred.md) :
> ce document est la suite directe du **P4 « différé »** de ce chantier
> (14/08/2026), dont le motif de report était *« aucun dataset ALFRED
> n'existe encore pour justifier un composant appris »*. Le document source
> de cette suite répond précisément à cette objection : il explique comment
> construire ce dataset avant même de parler d'entraîner quoi que ce soit.

---

## 1. Vue d'ensemble

Le document source pose trois systèmes à ne jamais confondre :

- **Knowledge** — ce qu'ALFRED sait sur le monde, destiné au RAG, modifiable
  sans réentraîner le modèle.
- **Memory** — ce qu'ALFRED retient d'un utilisateur ou d'une interaction
  (préférences, habitudes, contexte), régi par une politique
  KEEP/UPDATE/MERGE/EXPIRE/IGNORE.
- **Training Dataset** — des exemples *sélectionnés et validés* pour
  modifier le comportement d'un modèle (SFT, DPO, LoRA/QLoRA) — jamais une
  copie brute des conversations.

Principe fondamental du document, repris tel quel ici : **une information
nouvellement découverte ne doit jamais automatiquement modifier le modèle.**
Tout passe par un Quality Gate — provenance, fraîcheur, confidentialité,
qualité — avant de devenir exploitable, que ce soit comme Knowledge (RAG) ou
comme candidat d'entraînement.

Le document propose ensuite un pipeline complet : acquisition externe
(OpenAI/Anthropic/Web) quand le local échoue → Quality Gate → Knowledge Store
*ou* Training Candidate → Instruction/Preference Dataset versionné →
fine-tuning LoRA/QLoRA → évaluation contre un Golden Dataset → déploiement
avec rollback possible.

---

## 2. Constat — l'écart pilier par pilier

Un audit du code réel (`src/`) le 21/08/2026 montre un écart très inégal
selon le pilier : deux piliers sur trois ont déjà un socle réel, le
troisième n'existe pas du tout.

### 2.1 Knowledge — socle réel, mais fermé

| Élément visé (document) | État réel | Fichier |
|---|---|---|
| RAG (recherche, chunking, embeddings, ranking) | **Existe et fonctionne.** `KnowledgeLoader` → `DomainMatcher` + `TaxonomyRouter` → `KnowledgeRanker` → `ContextMerger` → `KnowledgeRetrievalEngine`. 1137 fiches JSON pré-écrites, taxonomie + registry. Corrigé le 20/08/2026 (filtrage mots-outils français, faux positifs de matching). | `src/knowledge/*.py` |
| Schéma Knowledge (provenance, source_type, acquired_at, verified_at, confidence, freshness_policy, privacy_level, training_eligible, status) | **N'existe pas.** Grep confirmé : aucun de ces champs n'apparaît nulle part dans `src/knowledge/`. Les fiches ont un `domain`/`subdomain`/`title`/`summary`/`tags`, rien de plus. | — |
| Knowledge Quality Gate | **N'existe pas.** Rien n'évalue une connaissance avant de la charger — normal, puisque rien n'est acquis dynamiquement aujourd'hui : tout est écrit à la main par Céline/Claude. | — |
| Gestion de la fraîcheur (STALE/REVALIDATION_REQUIRED) | **N'existe pas.** Aucune notion de péremption sur les fiches. | — |
| Journalisation des appels externes (OpenAI/Anthropic en fallback) | **Quasi inexistante.** `LLMRouter.generate()` se contente d'un `print()` console au moment du fallback (`"☁️ LLMRouter : utilisation OpenAI fallback"`) — rien de structuré, rien de persisté. | `src/llm/llm_router.py` |
| Gap Dataset (cas où le local échoue) | **N'existe pas** — conséquence directe du point précédent : sans journalisation structurée, aucune matière pour un Gap Dataset. | — |

**Lecture** : le RAG existe, mais c'est un système **fermé** — uniquement ce
qu'on y écrit à la main. Le document décrit un système **ouvert** qui
s'auto-enrichit à partir de ses propres échecs et de ses recherches
externes. C'est tout ce périmètre-là (acquisition, provenance, fraîcheur,
Quality Gate, Gap Dataset) qui manque, pas le RAG lui-même.

### 2.2 Memory — socle réel, écart déjà identifié et documenté

`MemoryEngine` (JSON, `dialogue_history.json`, `retention_days` depuis le
P3 du 14/08) et `LongTermMemory` (SQLite) existent et sont **réellement
utilisés en production** — confirmé de nouveau le 20/08/2026 (continuité de
session après redémarrage complet d'ALFRED). La séparation Knowledge/Memory
que demande le document (section 3.2 : *« Memory et Knowledge doivent
rester logiquement séparés »*) est déjà respectée dans le code : deux
systèmes distincts, aucun mélange constaté.

Écart résiduel, déjà noté dans `vision_architecture_cognitive_alfred.md` et
toujours vrai : les règles KEEP/UPDATE/MERGE/EXPIRE/IGNORE existent en JSON
(`memory_decay_rules.json`, `memory_prioritization.json`) mais ne sont
branchées à aucun code exécutable. Ce n'est pas un chantier nouveau, c'est
une dette déjà répertoriée — pas la priorité de ce document.

### 2.3 Training Dataset / Fine-Tuning — n'existe pas du tout

Grep exhaustif sur `src/` : aucune trace de `training_dataset`,
`training_candidate`, `instruction_dataset`, `preference_dataset`,
`golden_dataset`, `gap_dataset`, `lora`, `qlora`, `fine-tuning`, ou
`adapter_registry`. Aucun dossier `ALFRED_DATA/`. C'est un départ à zéro
absolu, cohérent avec le statut « P4 différé » du 14/08/2026.

---

## 3. Plan d'action retenu

Le document source structure lui-même son plan en P0→P3 (section 28) et en
10 étapes de roadmap (section 27). L'ordre proposé ici **suit cette
structure sur le fond**, mais l'ancre précisément dans le code réel plutôt
que de la traiter comme une liste abstraite — même logique que celle déjà
appliquée dans `vision_architecture_cognitive_alfred.md` : ne pas construire
en parallèle ce qui peut se greffer sur l'existant, et ne pas aller plus
loin que ce que l'usage réel justifie.

### P0 — Le socle : provenance + Quality Gate + Gap Dataset

C'est le seul point sans lequel **rien d'autre** dans le document ne peut
exister : sans journalisation avec provenance, ni le Gap Dataset (section 9)
ni les Training Candidates (section 10-11) n'ont de matière première.

1. **Journaliser structurellement les fallbacks cloud.** Remplacer le
   `print()` de `LLMRouter.generate()` par un événement structuré
   (`query`, `local_route`, `local_success`, `failure_reason`,
   `external_source`, `external_success`) — format JSONL append-only,
   même esprit que `src/security/audit_trail.py` (déjà utilisé par
   `retrieval_engine.py` pour tracer les consultations knowledge), sans
   forcer ce cas dedans : le schéma de `write_audit_event()` est pensé pour
   des décisions d'accès (ALLOW/DENY par rôle+ressource), pas pour un
   échec/succès de recherche — le détourner serait le même anti-pattern déjà
   évité pour `policy_engine.py` le 14/08 (*« détourner aurait été plus
   complexe et moins lisible qu'un petit module dédié »*). On réutilise donc
   le **pattern** (JSONL, rotation) sans réutiliser le **fichier**.
2. **Gap Dataset** — alimenté directement par (1). C'est le premier
   livrable utile en soi, même sans aller plus loin : le document le dit
   explicitement (section 9), *« devient un outil de pilotage de la roadmap
   ALFRED »*.
3. **Schéma Knowledge enrichi, additif et rétrocompatible.** Ne pas
   réécrire les 1137 fiches existantes (risque mécanique inutile sur un
   corpus stable et fonctionnel). À la place : les nouveaux champs
   (`source_type`, `acquired_at`, `confidence`, `freshness_policy`,
   `training_eligible`, `status`...) sont lus avec une valeur par défaut
   quand absents (`status="VALIDATED"`, `source_type="document"` pour tout
   le corpus actuel, écrit à la main et déjà validé par Céline) — seule la
   connaissance acquise dynamiquement, à l'avenir, porte le schéma complet
   dès sa création.
4. **Knowledge Quality Gate** — nouveau module, même famille que
   `src/security/safety_gate.py` (classification par mots-clés déjà
   éprouvée dans ce repo, pas de ML). Point de vigilance identifié : le
   document propose une échelle de confidentialité à 5 niveaux
   (PUBLIC/INTERNAL/PRIVATE/SENSITIVE/SECRET, section 5), alors que
   `safety_gate.py` n'en a que 2 aujourd'hui (`LOCAL_ONLY`/`STANDARD`).
   Recommandation : garder les 2 niveaux existants pour le Quality Gate
   plutôt qu'introduire une taxonomie à 5 niveaux que rien d'autre dans le
   code n'utilise encore — cohérent avec le principe déjà appliqué dans ce
   projet de ne pas construire au-delà de ce que l'usage réel justifie.
   L'échelle à 5 niveaux reste une option ouverte si le besoin se confirme
   plus tard.

### P1 — Constitution du Training Dataset (structure seule, pas d'entraînement)

Une fois P0 en place (le Gap Dataset commence à s'alimenter en usage réel),
créer la zone intermédiaire décrite section 10 : `RAW INTERACTIONS →
TRAINING CANDIDATES → QUALITY/PRIVACY/DUPLICATE CHECK → TRAINING DATASET`,
avec l'arborescence `ALFRED_DATA/{intent,routing,memory,knowledge,gaps,
instructions,preferences,users}/` proposée section 12. Zéro dépendance sur
un modèle particulier à ce stade — c'est de la donnée, pas de
l'entraînement. Dataset versionné dès le premier fichier (section 17).

### P2 — Golden Dataset + pipeline d'évaluation

Corpus de référence (section 22) et pipeline de comparaison
BASE vs candidat (section 21) — nécessaire **avant** tout fine-tuning réel,
pas après, pour avoir un point de comparaison. Peut se construire en
parallèle de P1 une fois quelques dizaines de cas représentatifs
disponibles.

### P3 — Premier fine-tuning expérimental (LoRA/QLoRA)

Volontairement en dernier, comme dans le document (étape 6 sur 10). Deux
préalables non négociables avant d'y toucher :
- Un volume minimal de Training Dataset réellement validé (P1) — pas de
  fine-tuning sur un dataset vide ou jouet.
- Une mesure réelle de ce que le matériel (Miniforum MS-S1 Max) supporte en
  entraînement local — jamais fait à ce jour, contrairement à l'inférence
  (déjà mesurée et documentée sur `hardware.html`).

### Différé, hors périmètre de ce document

DPO (préférences), User Adapter par utilisateur (ALFRED Adaptive),
apprentissage périodique automatisé (section 20) — tout ce que le document
lui-même place en P3 (section 28) reste conditionné à la réussite de P0-P2
ci-dessus, pas engagé maintenant.

---

## 4. Étude — Mesure matérielle pour le fine-tuning (préalable P3)

> Étudié le 21/08/2026, à la demande explicite de Céline, en session d'étude
> pure (aucun code exécuté, aucune mesure réelle lancée). Objectif : préparer
> le terrain avant de lancer la mesure réelle mentionnée en P3, pas la
> remplacer.

### 4.1 Ce qui est déjà su vs ce qui reste à mesurer

Le matériel est bien documenté côté **inférence** (`hardware.html`,
`ALFRED_CONTEXT.md`), jamais côté **entraînement** :

| | Inférence (Ollama) | Entraînement (LoRA/QLoRA) |
|---|---|---|
| Mesuré ? | Oui — table de benchmarks réels dans `ALFRED_CONTEXT.md` (gpt-oss-120B Q4 → 32 tok/s / 60,5 Go ; DeepSeek-R1 70B Q4 → 4,75 tok/s / 42 Go ; cogito-109B MoE Q4 → 64,8 Go, limite) | Non — jamais fait |
| Pile logicielle | Ollama (llama.cpp), backend GPU non confirmé explicitement (Vulkan probable sur Windows) | Inconnue et **non vérifiée** — voir 4.2 |
| Charge | Rafales courtes (une requête chat) | Sessions longues et soutenues (minutes à heures) |

Machine : Minisforum MS-S1 Max — CPU AMD Ryzen AI Max+ 395 (16C/32T,
5,1 GHz), GPU intégré AMD Radeon 8060S, NPU 50 TOPS, 64 Go LPDDR5x unifiés
(upgradeable 128 Go, non fait), TDP 130 W continu / 160 W crête. Disque
interne D: ("ALFRED", NVMe 4 To réutilisé, 3,63 To utiles, BitLocker) déjà
occupé par le repo + les modèles Ollama (70-120B = 150-300 Go). Disque
externe F: ("BACKUP_ALFRED", WD My Passport 5 To, 4,54 To utiles) — c'est ce
disque, sauf indication contraire de Céline, que désigne « le disque dur
externe » : c'est le seul disque externe attaché en usage régulier au poste.

### 4.2 Le vrai inconnu n'est pas la puissance brute, c'est la pile logicielle

Le point le plus important de cette étude : **la mesure a un préalable
bloquant, avant même de parler de débit ou de mémoire.** Ollama fait
tourner l'inférence sur ce GPU intégré (32 tok/s sur un 120B, donc le
matériel *peut* travailler avec ce GPU) — mais l'inférence via llama.cpp et
l'entraînement via PyTorch/PEFT ne sollicitent pas la même pile :

- **PyTorch a besoin d'un backend GPU explicite** (ROCm/HIP côté AMD, ou
  CUDA — non applicable ici). Le support ROCm de la puce de ce GPU (codename
  `gfx1151`, famille Strix Halo) est récent et sa maturité **sous Windows**
  spécifiquement (ce poste tourne Windows, pas Linux) reste à vérifier — le
  support ROCm historique d'AMD est né et reste le plus mûr sous Linux.
- **QLoRA dépend de `bitsandbytes`** pour la quantization 4-bit — bibliothèque
  historiquement pensée pour CUDA, avec un support ROCm plus expérimental.
- Si le GPU n'est pas exploitable pour l'entraînement sous Windows, les
  options de repli sont, par ordre de simplicité décroissante : WSL2 +
  ROCm Linux (revient à réintroduire la question du support `gfx1151`, plus
  une couche de virtualisation) ; entraînement CPU-only (16C/32T Zen5 —
  fonctionnellement possible pour du LoRA sur petit modèle, mais probablement
  lent au point de limiter les itérations) ; louer du calcul cloud pour la
  seule étape d'entraînement en gardant tout le reste local-first (rupture
  ponctuelle et assumée du principe local-first, uniquement si les deux
  options précédentes échouent).
- **Conséquence pour la suite** : la « mesure du matériel » n'est pas une
  seule expérience (« combien de tokens/s en training ? ») mais une
  **question binaire à trancher en premier** (« PyTorch voit-il ce GPU, et
  avec quel backend, sous Windows ? ») — le reste (débit, mémoire pic,
  température) n'a de sens qu'une fois ce préalable positif.

### 4.3 Budget mémoire : l'inférence mesurée ne prédit pas l'entraînement

Les 64 Go sont une mémoire **unifiée** (CPU et GPU se la partagent), ce que
confirme déjà le comportement observé en inférence (60-65 Go alloués pour
les plus gros modèles testés). Pour l'entraînement, même en LoRA/QLoRA (qui
gèle les poids du modèle de base et n'entraîne qu'un petit adaptateur), le
pic mémoire est structurellement différent de l'inférence : il faut ajouter
aux poids gelés les activations de la passe forward *et* backward, les
gradients de l'adaptateur, et l'état de l'optimiseur — un poste que
l'inférence pure ne connaît pas du tout. Rien dans les benchmarks existants
ne permet d'extrapoler ce chiffre : c'est une inconnue complète, distincte du
point 4.2.

Point opérationnel à trancher, indépendant de la mesure elle-même : ALFRED
tourne en production sur cette machine. Un entraînement ne peut
vraisemblablement pas cohabiter avec l'assistant en usage réel (contention
mémoire + GPU) — la mesure doit donc se faire dans une fenêtre de
maintenance dédiée, à définir avec Céline, pas en tâche de fond.

### 4.4 Stockage : quel disque, pour quel usage — un conflit à lever

Le disque F: (BACKUP_ALFRED, WD My Passport, disque dur mécanique — pas un
SSD, cohérent avec le terme « disque dur externe » employé par Céline) a
déjà un rôle : cible de la tâche planifiée de backup quotidien/hebdomadaire
(`F:\BACKUP_ALFRED\SCRIPTS\alfred_backup.ps1`, rétention 15 jours). Deux
points de vigilance avant de l'utiliser aussi comme stockage actif pour le
Training Dataset (`ALFRED_DATA/`, structure P1) :

- **Contention d'usage** : écrire/lire activement dessus pendant les
  fenêtres de backup automatisées (2h00 quotidien) créerait une compétition
  avec un système déjà en place et fiable — à éviter plutôt qu'à découvrir
  en production.
- **Nature mécanique** : un disque dur (rotationnel) est fait pour du débit
  séquentiel, pas pour de l'accès aléatoire répété. Pour du LoRA/QLoRA,
  l'usage réel du disque reste probablement léger une fois le dataset chargé
  et tokenizé en mémoire (les checkpoints d'adaptateur LoRA sont petits — Mo,
  pas Go, contrairement à une sauvegarde de modèle complet) — mais la phase
  de préparation/tokenization d'un gros dataset, elle, bénéficierait d'un
  disque rapide.

**Piste à confirmer, pas encore tranchée** : garder F: comme *archive*
long terme du Training Dataset (lecture séquentielle = point fort d'un HDD,
et cohérent avec son rôle actuel de sauvegarde), mais faire tout traitement
actif (tokenization, cache, checkpoints pendant l'entraînement) sur D: (NVMe
interne) ou C:, malgré l'espace déjà réduit par les modèles Ollama
(150-300 Go) — à vérifier avec l'espace réellement libre sur D: au moment de
la mesure.

### 4.5 Charge thermique soutenue — angle mort des benchmarks existants

Les benchmarks d'inférence existants mesurent des rafales courtes (une
réponse de chat). Un entraînement, même court, sature le CPU/GPU en continu
sur des minutes voire des heures — un régime thermique jamais testé sur ce
boîtier mini-PC (130 W continu / 160 W crête annoncés par le constructeur,
non vérifiés en charge soutenue longue). Risque à mesurer explicitement :
throttling (baisse de fréquence) après quelques minutes de charge continue,
qui fausserait toute mesure de débit prise sur une fenêtre trop courte.

### 4.6 Méthode de mesure proposée (à exécuter dans une session ultérieure, pas aujourd'hui)

1. Vérifier le préalable 4.2 : PyTorch détecte-t-il le GPU sur ce poste, et
   avec quel backend ? Résultat binaire go/no-go avant tout le reste.
2. Si non disponible : mesurer un baseline CPU-only (16C/32T) comme repli
   documenté, pas comme solution cible.
3. Choisir un modèle de base représentatif de la pile réelle d'ALFRED
   (cohérence avec le modèle d'outils déjà en usage, cf.
   `vision_architecture_cognitive_alfred.md`), petit assez pour qu'un essai
   échoue vite si la pile ne tient pas.
4. Dataset jouet (quelques dizaines d'exemples) — but : caractériser la
   courbe mémoire/débit, pas produire un adaptateur réellement utile.
5. Mesurer : pic mémoire (RAM unifiée), tokens/s en entraînement, temps par
   epoch, taille et temps d'écriture d'un checkpoint d'adaptateur,
   température/fréquence après 15-30 min de charge continue.
6. Produire un tableau symétrique à celui de `hardware.html`
   (modèle/rang LoRA/mémoire pic/débit/temps par epoch) — c'est ce tableau,
   une fois rempli, qui documente enfin la case restée vide depuis le
   14/08/2026.

### 4.7 Vers quel matériel se diriger — au-delà du MS-S1 Max

Point tranché par Céline le 21/08/2026 : P3 ne se fera pas sur ce poste.
Cette étude sert à savoir **vers quoi se diriger**, pas à forcer le
fine-tuning sur le matériel actuel. Deux constats de la section 4.2
orientent directement ce qu'il faudra viser :

- Ce n'est pas seulement une question de puissance (cœurs, RAM) mais
  d'**écosystème logiciel** : CUDA + PyTorch + bitsandbytes sur GPU NVIDIA
  est aujourd'hui l'environnement de fine-tuning de très loin le plus mûr et
  le mieux documenté, très au-devant de ROCm côté AMD — a fortiori de ROCm
  *sous Windows*, le point faible identifié en 4.2 sur le MS-S1 Max. Une
  cible « réellement adaptée au besoin » n'élimine pas cette question, elle
  la referme : GPU NVIDIA dédié (VRAM dédiée, pas de mémoire unifiée
  partagée avec le CPU), et très probablement un environnement Linux plutôt
  que Windows pour l'entraînement.
- Le serveur Phase 2 déjà sur la roadmap (`hardware.html`, TR 7960X 24C,
  256 Go DDR5 ECC, M+18→M+36) était jusqu'ici pensé pour l'orchestration
  multi-agents et l'hébergement CPL en Docker — **pas** explicitement pour
  l'entraînement, et sa fiche ne mentionnait aucun GPU dédié.
  **Mise à jour le 21/08/2026, le jour même** : plutôt que de laisser ce
  besoin en attente d'un futur dimensionnement, la fiche Phase 2 a été
  ajustée directement — RTX 4090 24 Go (VRAM dédiée, écosystème CUDA) et
  stockage porté de 8 à 16 To NVMe pour absorber Training Dataset et
  checkpoints en plus des modèles déjà stockés. Budget Phase 2 ~4 650 € →
  **~7 050 €**, total roadmap ~7 777 € → **~10 177 €**. Toujours pas une
  décision d'achat exécutée — la Phase 2 reste à M+18→M+36 — mais le besoin
  fine-tuning n'est plus une case vide à redécouvrir plus tard.

Rien de tout cela n'est une décision d'achat : c'est la direction à garder
en tête pour que le prochain arbitrage hardware (Phase 2) intègre le besoin
fine-tuning dès le dimensionnement, plutôt que de le découvrir après coup
comme ça a été le cas pour la mesure d'entraînement sur le MS-S1 Max.

### 4.8 Questions ouvertes pour Céline

- Confirmer que « disque dur externe » désigne bien F: (BACKUP_ALFRED, WD My
  Passport 5 To) et pas un autre disque non encore inventorié ici.
- Arbitrer le conflit d'usage 4.4 (archive dataset vs disque de backup actif)
  avant que P1 ne commence à écrire dans `ALFRED_DATA/`.
- Valider le principe d'une fenêtre de maintenance dédiée (4.3) plutôt qu'une
  mesure en tâche de fond pendant qu'ALFRED tourne en production.

---

## 5. Suivi

| Point | Statut | Commit |
|---|---|---|
| P0 — Journalisation fallback cloud + Gap Dataset + schéma Knowledge additif + Quality Gate | **Fait** (`gap_dataset.py`, `knowledge_quality_gate.py`, `knowledge_schema.py`, 30 tests, suite complète 1666 verts) — le constat de la section 2.1 décrit l'état *avant* ce commit, volontairement laissé tel quel comme photo du point de départ | `e95a3f87` |
| P1 — Constitution Training Dataset (structure) | **En cours** (démarré le 21/08/2026, `src/knowledge/gap_dataset.py` en cours de modification) | — |
| P2 — Golden Dataset + évaluation | Pas commencé | — |
| P3 — Premier fine-tuning LoRA/QLoRA | Pas commencé — étude préalable matériel faite le 21/08/2026 (section 4), mesure réelle non lancée | — |
| DPO / User Adapter / apprentissage automatisé | Différé, pas de date | — |

Ce document sert de source de vérité pour ce chantier, sur le même modèle
que `vision_architecture_cognitive_alfred.md`. Le suivi macro (pourcentages,
epics) reste à rattacher à `docs/roadmap/ROADMAP_MASTER_V0_VFINALE.md` une
fois le premier point engagé.
