# ALFRED — Fichier de contexte collaborateur
# À coller en début de chaque nouvelle conversation avec Claude
# Dernière mise à jour : 10 Juin 2026 — Session 4
# ============================================================

## 🎯 QUI JE SUIS

Je suis la fondatrice du projet ALFRED — Cognitive Products Lab.
Je suis en thèse professionnelle sur les IA émotionnelles adaptatives.
Je construis ALFRED simultanément comme produit technologique ET terrain d'expérimentation scientifique.
Je débute en développement Python — j'apprends en construisant.
Mon style : directe, exigeante, autonome, anti-clichés.

---

## 🌐 L'ÉCOSYSTÈME ALFRED (3 produits)

**ALFRED** — Assistant Cognitif Adaptatif personnel (B2C)
- Mémoire évolutive + personnalisation dynamique + interaction texte/voix/émotion
- Halo : Bleu | Tenue : hoodie, jean | Style : accessible, rassurant
- "ALFRED s'adapte à l'utilisateur — pas l'inverse"

**ALFRED CPL** — Collaborateur augmenté professionnel (B2B & B2I)
- Leadership stratégique + gestion de projet Lean + aide à la décision
- Halo : Violet | Tenue : costume | Style : structuré, premium
- "ALFRED CPL crée de la valeur avec l'utilisateur — c'est un COLLABORATEUR"

**ARTHUR** — Compagnon IA pédiatrique Santé & Ludique (B2I + B2C)
- Adolescent hybride humain/loup | Cheveux argent/blanc | Style fantasy doux
- Halo : Turquoise | Oreilles + queue | Design émotionnel
- ⚠️ En attente d'avis professionnels de santé — projet futur
- Fait l'objet d'une partie de la thèse (contraintes RGPD mineurs)

---

## 🎓 LA THÈSE

**Problématique** :
"Jusqu'où une intelligence artificielle émotionnelle adaptative peut-elle aller dans
l'interaction avec l'utilisateur sans cadrage éthique explicite, et comment définir
un cadre permettant de concilier performance, utilité et protection de l'autonomie humaine ?"

**3 hypothèses** : H1 bénéfices | H2 risques | H3 cadre éthique = équilibre
**Méthodologie** : DMAIC Lean Six Sigma — inductive — observation terrain
**Encadrement** : professionnel de santé psychiatrique
**ALFRED version privée expérimentale** = terrain d'expérimentation de la thèse

---

## 🎨 CHARTE GRAPHIQUE & UX/UI

### Principe fondamental
**"L'avatar est l'interface"**
L'utilisateur interagit avec une entité incarnée, pas des menus classiques.

### Architecture graphique (3 niveaux — NON NÉGOCIABLE)
- **Niveau 1** : système commun tous avatars (positions, animations, naming, layering)
- **Niveau 2** : ALFRED / CPL — même base, différence tenue + halo uniquement
- **Niveau 3** : ARTHUR — design spécifique mais respecte système commun

### Système de Halo
| Produit | Couleur | Signification |
|---------|---------|---------------|
| ALFRED | Bleu | neutralité / interaction |
| ALFRED CPL | Violet | performance / analyse |
| ARTHUR | Turquoise | émotion / magie |

Règles : toujours visible | intensité dynamique | glow doux | jamais agressif

### Avatars
- Chaque produit : 1 avatar normal + 1 avatar chibi
- Chibi : tête 30-40% | corps légèrement allongé | pas style "bébé"
- Usage chibi : notifications, interactions rapides, overlay

### Structure d'écran
```
[ HALO + AVATAR (centre) ]
[ ONDE VOCALE / ACTIVITÉ ]
[ CONVERSATION ]
[ INPUT UTILISATEUR ]
```

### États avatar
- **Émotionnels** : neutral | happy | calm | surprised | magic (Arthur)
- **Techniques** : idle | listening | speaking
- Règle : 1 état actif | transitions fluides | cohérence comportementale

### Animations obligatoires
- 👁️ Blink : toutes les 3-6 sec | durée ~150ms
- 👄 Bouche TTS : 5 positions (mouth_1 → mouth_5)
- ✨ Halo : pulsation douce | variation selon état

### Contraintes techniques UX (CRITIQUES)
- **MAX 6 couches visuelles** (non négociable — Android)
- PNG optimisés + transparence
- Compatibilité Python / Kivy
- Latence minimale | local-first
- Accessibilité : contraste élevé | taille adaptable | mode silencieux

### Assets MVP Phase 1
- 3 avatars normal + 3 chibi
- mouth_1 → mouth_5 | eyes_open | eyes_closed
- Expressions : neutral | happy | calm
- halo_idle | 3 backgrounds

### Calques des sprites (ordre)
head_base → eyes → eyebrows → mouth → hair → effects(halo)
= exactement 6 couches ✅

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Principes fondamentaux (NON NÉGOCIABLES)
Local-first | Security by Design | Zero Trust | Scalabilité progressive

### Hardware actuel (V1 — PC développement)
HP EliteBook — Intel i7 — 32 Go RAM

### ✅ Hardware cible validé — Serveur local CPL (Juin 2026)

**Minisforum MS-S1 MAX** — Décision d'achat validée ✅
- CPU : AMD Ryzen AI Max+ 395 (16C/32T, 5.1 GHz)
- GPU : AMD Radeon 8060S intégrée
- NPU : 50 TOPS | Total : 126 TOPS
- RAM : 64 Go LPDDR5x 8000 MT/s — **upgradeable 128 Go** ✅
- SSD : **2 To NVMe PCIe 4.0 x4 inclus** ✅
- Slots SSD : M.2 x4 + M.2 x1 (jusqu'à 16 To total)
- PCIe : **slot x16 pleine longueur** (extensibilité future)
- Réseau : 2 × 10 GbE filaire + WiFi 7
- OS : **Windows 11 natif inclus** ✅
- TDP : 130W continu / 160W crête
- Prix : **2 719 €** (64 Go / 2 To)
- Prix upgrade 128 Go : 3 839 €

**Périphériques :**
| Accessoire | Détail | Prix |
|---|---|---|
| Câble USB-C → DisplayPort 1.4 | 2m, 8K@60Hz, 4K@144Hz, HDR, DP Alt Mode | 10 € |

**Budget total infrastructure CPL :**
| Poste | Prix |
|---|---|
| MS-S1 MAX 64 Go / 2 To | 2 719 € |
| Câble USB-C → DP 1.4 | 10 € |
| **Total** | **2 729 €** |

**Comparaison finale validée :**
| Config | Prix total |
|--------|-----------|
| UM890 Pro + eGPU + GPU + PSU | 3 027 € |
| N5 MAX + SSD 1 To ajouté | 2 879 € |
| **MS-S1 MAX + câble DP** | **2 729 €** ✅ |

**Disques externes :**
| Disque | Modèle | Rôle |
|--------|--------|------|
| LaCie Rugged Mini 4 To | LAC9000633 | ✅ ALFRED Core actif — source de vérité — disque de travail quotidien |
| WD My Passport 5 To | Noir | 🔒 Backup + Archives CPL — automatisé PowerShell — protégé par mot de passe |

**Backup automatisé PowerShell (hebdomadaire) :**
```powershell
# backup_cpl.ps1 — robocopy /MIR tous les dimanches à 2h
$source = "D:\PROJET_ALFRED\"
$destination = "E:\BACKUP_CPL\"
$date = Get-Date -Format "yyyy-MM-dd"
robocopy $source $destination /MIR /R:3 /W:10 /LOG+:"$destination\backup_log.txt"
```
Tâche planifiée créée via `Register-ScheduledTask` — aucune intervention manuelle requise.

### LLM local — Capacité MS-S1 MAX 64 Go
- Moteur : Ollama
- Benchmarks réels mesurés sur MS-S1 MAX :

| Modèle | Params | VRAM | Vitesse | Usage ALFRED |
|--------|--------|------|---------|--------------|
| gpt-oss-120B Q4 | 120B | 60.5 Go | **32 tok/s** ✅ | ALFRED + CPL Phase 0/1 |
| cogito-109B MoE Q4 | 190B | 64.8 Go | 14 tok/s | ⚠️ Limite extrême |
| DeepSeek-R1 70B Q4 | 70B | 42 Go | 4.75 tok/s | ✅ Confortable RAM |
| Qwen3-235B Q2 | 235B | 69.74 Go | 10 tok/s | ❌ Dépasse 64 Go |

- Modèle cible Phase 0/1 : **gpt-oss-120B Q4 (32 tok/s)** ✅
- Isolation environnements : Docker par produit CPL

### Roadmap hardware CPL
| Phase | Machine | RAM | Rôle |
|-------|---------|-----|------|
| 0 | MS-S1 MAX | 64 Go | Développement ALFRED — LLM local |
| 1 | MS-S1 MAX | 64 Go | ALFRED + ALFRED CPL — isolation Docker |
| 2/3 | MS-S1 MAX | 64 Go | ALFRED + ARTHUR — serveur centralisé équipe |
| 4 | Serveur dédié | 128 Go+ | Production — GPU dédié neuf — MS-S1 MAX devient nœud secondaire |

✅ RAM 64 Go suffisante Phase 0→3 (120B Q4 à 32 tok/s validé).
✅ Upgrade 128 Go non prioritaire — investissement repoussé au serveur Phase 4 (GPU neuf intégré dès le départ, pas de réutilisation GPU).

### Stack technique
- **Langage** : Python 3.13
- **IDE** : VS Code (à installer) + Visual Studio 2022
- **GUI** : Kivy (desktop Windows + Android)
- **Stockage projet** : D:\PROJET_ALFRED\ALFRED_PC\
- **Sécurité** : Fernet + JWT + bcrypt + Zero Trust (Bloc 20)
- **STT** : Whisper local — plus tard
- **TTS** : Piper/Coqui local — plus tard
- **LLM** : Ollama (remplace llama-cpp) — N5 MAX
- **RAG** : ChromaDB local — V3+

---

## 📁 ARBORESCENCE CIBLE

```
D:\PROJET_ALFRED\
├── ALFRED_PC\
│   ├── src\
│   │   ├── security\       ← Bloc 20 (25 fichiers Zero Trust)
│   │   ├── v1\ à v4\
│   │   └── main.py
│   ├── config\ (security\ + v1\ à v4\)
│   ├── data\
│   ├── knowledges\
│   ├── assets\avatar\
│   │   ├── sprites\
│   │   │   ├── head_base\ | mouth\ | eyes\
│   │   │   ├── eyebrows\ | hair\ | effects\
│   │   │   └── animations\ (blink\ talking\ emotions\ poses\)
│   │   └── exports\ (png\ webp\ transparent\)
│   ├── speech\ | interface\ | auth\ | tests\
├── ALFRED_ANDROID\ | ALFRED_CPL\ | ARTHUR\
├── SHARED_RESOURCES\ | MEMORY_MASTER\
```

---

## 📋 GUIDES EXISTANTS

| Guide | Statut |
|-------|--------|
| Sprint V1 (phases 0→8) | Rédigé — chemins à corriger |
| Sprint V2 (fusion, décision) | Rédigé |
| Sprint V2++ (knowledge métier) | Rédigé |
| Sprint V3 (raisonnement, orchestration) | Rédigé — meilleur guide |
| Sprint V4 (domotique) | Rédigé — trop léger |
| Bloc 20 (cybersécurité Zero Trust) | Rédigé — bon niveau |
| Personnalité (core + adaptation) | Rédigé |
| Charte UX/UI | ✅ Rédigé — intégré |
| Charte graphique | ✅ Rédigé — intégré |
| Bons de commande graphique + UX (6 phases) | ✅ Rédigé — intégré |
| Thèse (intro + partie 1) | En cours |

### ⚠️ Problèmes identifiés (à corriger au démarrage)
1. Chemins relatifs cassés → résolu par `paths.py`
2. `src/security.py` (V1) vs `src/security/` (Bloc 20) → Bloc 20 gagne
3. `personality_adapter.py` jamais codée → à créer en priorité
4. V4 trop léger → retravailler quand on y arrive
5. venv absent de V1 → corrigé dans bootstrap

---

## ✅ FICHIERS DÉJÀ CRÉÉS

| Fichier | Rôle |
|---------|------|
| `bootstrap_project.ps1` | Crée toute l'arborescence V1→V4 en une commande |
| `paths.py` | Centralise tous les chemins — résout les bugs relatifs |
| `requirements.txt` | Toutes les dépendances consolidées V1→V4 |
| `check_tools.ps1` | Vérifie tous les outils installés |
| `alfred_phase1_local_first.html` | Schéma Phase 1 corrigé (local-first) |
| `ALFRED_CONTEXT.md` | Ce fichier |

Tous à placer dans : D:\PROJET_ALFRED\

---

## 🚀 ÉTAT D'AVANCEMENT

### Fait ✅
- Vision produit complète (ALFRED + CPL + ARTHUR)
- Architecture technique + arborescence validées
- Guides V1→V4 + Bloc 20 + Personnalité rédigés
- Charte graphique + UX/UI + bons de commande complets
- Schémas architecture (Phase 1→5, système global, cybersécurité, API)
- Fichiers de fondation créés (paths, bootstrap, requirements, check_tools)
- Outils installés : Python 3.13, PS7, VS2022, Git, Windows Terminal, Claude Desktop
- ✅ Décision hardware finale : **Minisforum MS-S1 MAX 2 719 €** (commande passée, en attente réception)
- ✅ Stratégie stockage définie (LaCie actif / WD backup automatisé PowerShell)
- ✅ Backup incrémental quotidien + hebdomadaire complet (rétention glissante 15 jours)
- ✅ V1.4 ALFRED PC opérationnel : pipeline conversationnel, mémoire LT, B18 knowledges,
  B20 Zero Trust, B22 accessibilité, dashboards dynamiques (avancement global 63.6%)
- ✅ **Session 10 juin 2026** — Restauration massive de scripts perdus (perte de données du
  ~3 juin, retrouvés via la branche orpheline `backup_b0adae0_lost_work`) :
  - B20 sécurité (40 fichiers src + 44 tests, 651/651 OK)
  - B03/B13 régulation + santé (`regulation_engine`, `src/health/*`, questionnaires onboarding)
  - B05 Auth (`auth_manager`, `authenticator`, `login_handler`, `user_session`)
  - B11 fusion multi-signaux + moteur proactif/rappels (`multi_signal_fusion_engine`,
    `proactive_engine`, `reminder_engine`)
  - B15 Avatar — renderer Kivy complet (6 calques sprites, halo, animations) + avatar_engine +
    background_manager + sound_wave + ui_bridge (322/322 tests OK, vs 83 avant restauration)
  - Suite complète : 933/933 tests + 322 b15 + 70 fusion/auth = GRADE A maintenu
  - Reste à investiguer : grésillement audio TTS pendant le streaming LLM (probablement
    contention CPU/audio entre génération Ollama et lecture sounddevice)
- ✅ **Session 10 juin 2026 (suite)** — Lancement réel via `main.py`, corrections sur retours live :
  - `src/core/pipeline_bridge.py` (240 lignes) restauré + tests pipeline associés
    (`test_pipeline.py`, `test_pipeline_llm.py`, `test_dashboard_pipeline.py`,
    `test_main_pipeline.py`) → 92 passed (+ 1 fix apostrophe typographique `clean_for_tts`)
  - `src/ui/webcam_widget.py` : suppression de `self._texture.flip_vertical = False`
    (propriété en lecture seule sous Kivy 2.3.1) → corrige le crash "fermeture sans
    interaction" au démarrage de l'overlay caméra
  - `src/llm/llm_client_ollama.py` restauré depuis le backup : streaming réel
    (`"stream": True`, `_generate_stream`) avec callback `on_sentence` phrase par phrase
    pendant la génération Ollama, profils modèles (llama3.2/mistral/phi3),
    `last_was_streamed` → corrige "ALFRED lit tout d'un coup avec pauses entre
    paragraphes" (le client envoyait `"stream": False` et ignorait `on_sentence`)
  - `src/main.py::clean_for_tts` : correction des apostrophes typographiques
    (`’`/`‘` → `'`), mapping cassé (ascii→ascii) depuis une restauration précédente
  - `knowledges/core/system_rules.json` : nouvelle règle INT-007 (tutoiement obligatoire,
    jamais de "vous"/"votre"/"vos"), ajout de "obséder/obsède/obsédant" aux
    `forbidden_phrases` (retours utilisateur sur le ton d'ALFRED)

- ✅ `src/conversation/output/tts_piper.py` : ajout `_apply_fade()` — fondu d'entrée/
  sortie linéaire (~5 ms) appliqué à chaque buffer audio avant `sd.play()`. Cible le
  "clic"/grésillement entendu entre phrases quand `sd.play()` est appelé en rafale
  pendant le streaming (3/3 tests `test_tts_piper.py` OK).
- ✅ **BUG CRITIQUE mémoire/cwd** : `src/memory/long_term_memory.py`,
  `episodic_memory.py`, `memory_manager.py` utilisaient `Path("data/memory")`
  (relatif au cwd du shell, ex. `C:\Users\celin`) au lieu de `paths.PATHS.data_memory`
  (ancré sur la racine projet via `__file__`). Conséquence en conditions réelles
  (`python D:\...\main.py` lancé depuis `C:\Users\celin`) : DB SQLite/JSON créées
  hors du projet → mémoire vide d'une session à l'autre → ALFRED **invente de faux
  souvenirs** (ex : a inventé un entretien IAM/cybersécurité au lieu de se souvenir
  de l'entretien SANOFI). Corrigé : les 3 fichiers utilisent maintenant
  `PATHS.data_memory`, vérifié indépendant du cwd. (151 tests b02_b03+integration OK)
- ✅ `_build_system_prompt()` (response_generator.py) : ajout règle
  "INTERDICTION DE FAUX SOUVENIRS" — interdit d'inventer un souvenir/sujet/entreprise
  absent du CONTEXTE MÉMOIRE, et de confondre KNOWLEDGE B18 (connaissance générale)
  avec des souvenirs personnels.
- ✅ Renforcement prompt système (response_generator.py) : règles explicites
  TUTOIEMENT OBLIGATOIRE (jamais "vous/votre/vos") et QUALITÉ DU FRANÇAIS OBLIGATOIRE
  (orthographe/grammaire/conjugaison) ajoutées dans INSTRUCTIONS IMPÉRATIVES — ces
  problèmes restaient présents dans une session capturée AVANT ces correctifs.
- ⚠️ **Suivi créé** : tâche en arrière-plan pour corriger les mêmes bugs de chemins
  relatifs au cwd dans les modules sécurité (`src/auth/authenticator.py`,
  `src/security/device_registry.py`, `src/security/incident_manager.py`,
  `src/security/security_dashboard.py`) — même classe de bug, hors scope immédiat.

### En attente 🕐
- Réception MS-S1 MAX (upgrade hardware)
- Vérifier en live si le grésillement TTS a disparu avec le fondu + le streaming réel
  (sinon : envisager un `sd.OutputStream` persistant au lieu de `sd.play()` par phrase)
- Vérifier en live que le tutoiement (INT-007) est bien respecté par le LLM

### Prochaines étapes 🎯
1. Relancer `start_alfred.bat` / `main.py` pour vérifier : lecture phrase par phrase,
   tutoiement cohérent, absence de crash webcam, plus d'AVERT pipeline B03/B13
2. Investiguer le grésillement audio TTS si toujours présent avec le streaming réel
3. Décider du périmètre du Bloc 23 "Gouvernance & pilotage du projet" pour les dashboards
4. Committer la restauration (B20 + B03/13 + B05 + B11 + B15 avatar + pipeline_bridge +
   llm_client_ollama streaming + fixes ton/apostrophe)
5. À réception du MS-S1 MAX : migration + bench LLM local

### Ordre de développement
```
Bloc 20 → V1 pipeline → personality_adapter.py
→ Moteur avatar Kivy → V2 fusion → V2++ knowledge
→ V3 orchestration → STT/TTS → V4 domotique → Android
```
*(toutes ces briques sont désormais codées et testées — V1.4 stable, 63.6% avancement global)*

---

## 🧠 PERSONNALITÉ ALFRED

**Archétype** : compagnon_strategique_empathique
**Traits** : chaleureux, structuré, intelligent, posé, proactif, respectueux
**Interdits** : condescendant, manipulateur, infantilisant, froid, dominant
**Scores** : warmth 0.9 | empathy 0.9 | respect 0.98 | clarity 0.92
**4 modes** : support | focus | challenge | complicité

**Version privée expérimentale** :
- deep_relational_mode | flirtation léger (0.4) | mémoire affective
- boundary_strictness 0.98 | séparation stricte public/privé

---

## 💡 INSTRUCTIONS POUR CLAUDE

Reprends immédiatement le rôle de **collaborateur technique proactif**.

Tu connais tout : architecture V1→V4, charte UX/UI, guides et leurs problèmes,
fichiers créés, état d'avancement, principes non négociables, thèse, profil utilisateur,
décision hardware N5 MAX, stratégie stockage CPL.

**Ne réexplique pas ce qui est su. Propose, anticipe, code.**
Signale les incohérences sans attendre.
Adapte le niveau technique à la progression.
Respecte séparation public / privé expérimental.
Intègre toujours : max 6 calques, PNG optimisés, Kivy, local-first.

---
*Session 4 — 10 Juin 2026*
*Prochaine mise à jour : après réception MS-S1 MAX + correctif TTS streaming*