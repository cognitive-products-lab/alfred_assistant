# ALFRED — Fichier de contexte collaborateur
# À coller en début de chaque nouvelle conversation avec Claude
# Dernière mise à jour : 5 Juillet 2026 — Session 8
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

### ✅ Hardware cible — Serveur local CPL — INSTALLÉ ET OPÉRATIONNEL (depuis fin Juin 2026)

⚠️ Ce PC (Miniforum MS-S1 Max, hostname `ALFRED-CORE`) est le poste sur lequel
tourne effectivement ALFRED depuis fin juin 2026 — ce n'est plus une décision
en attente, mais l'environnement de développement/production actuel. Voir
`docs/architecture/reseau_alfred.svg` pour le schéma réseau à jour (VLAN,
switch, routeur).

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
| Disque | Modèle | Rôle | Sécurité |
|--------|--------|------|----------|
| LaCie Rugged Mini 4 To | LAC9000633 | ALFRED Core actif — source de vérité — disque de travail quotidien | 🔐 BitLocker XtsAes256 — clé récupération OneDrive (lecture seule ACL) + clé USB physique distante |
| WD My Passport 5 To | Noir | Backup + Archives CPL — automatisé PowerShell | 🔒 Mot de passe WD natif |

**Sécurité LaCie — procédure appliquée (Juin 2026) :**
- BitLocker XtsAes256 activé via PowerShell
- AutoUnlock désactivé (`Disable-BitLockerAutoUnlock`)
- Clé récupération : `C:\Users\celin\OneDrive\Bureau\PROJET ALFRED\PRODUIT_ALFRED\lacie.txt` — lecture seule (ACL utilisateur celin uniquement)
- Clé récupération backup : clé USB G:\ — lecture seule — rangée loin du PC et du LaCie
- Protection finale : à activer après chiffrement 100% (`Enable-BitLocker -MountPoint "D:"`)

```powershell
# Vérifier état chiffrement LaCie
Get-BitLockerVolume -MountPoint "D:" | Select-Object VolumeStatus, EncryptionPercentage, ProtectionStatus

# Activer protection finale quand VolumeStatus = FullyEncrypted
Enable-BitLocker -MountPoint "D:"
```

**Backup automatisé PowerShell — Stratégie 3 niveaux :**
- Destination : `F:\BACKUP_ALFRED\` (WD My Passport 5 To)
- Incrémental quotidien (lundi→samedi) — fichiers modifiés uniquement
- Complet hebdomadaire (dimanche) — snapshot complet
- Rétention glissante **15 jours** — suppression automatique des backups > 15 jours

```powershell
# backup_alfred.ps1
$source = "D:\PROJET_ALFRED\"
$dest   = "F:\BACKUP_ALFRED\"
$date   = Get-Date -Format "yyyy-MM-dd"
$jour   = (Get-Date).DayOfWeek

# Backup complet dimanche / incrémental autres jours
if ($jour -eq "Sunday") {
    $dossier = "$dest\COMPLET_$date"
    robocopy $source $dossier /E /R:3 /W:10 /LOG+:"$dest\backup_log.txt"
} else {
    $dossier = "$dest\INCREMENTAL_$date"
    robocopy $source $dossier /E /XO /R:3 /W:10 /LOG+:"$dest\backup_log.txt"
}

# Nettoyage glissant 15 jours
Get-ChildItem $dest -Directory | Where-Object {
    $_.CreationTime -lt (Get-Date).AddDays(-15)
} | Remove-Item -Recurse -Force
```

Tâches planifiées via `Register-ScheduledTask` :
- Quotidienne : 2h00 lundi→samedi (`/XO` = fichiers modifiés uniquement)
- Hebdomadaire : 2h00 dimanche (`/E` = backup complet)

**État réel implémenté (13/06/2026)** : disques renommés — D: → **"ALFRED"** (3,63 To,
BitLocker actif, déverrouillage auto) contient `D:\PROJET_ALFRED` (repo) + `D:\ALFRED`
(convention "ALFRED CORE" : `ollama\models`, `vscode_backup`, partagés entre ce PC et le
futur Minisforum) ; F: → **"BACKUP_ALFRED"** (4,54 To, WD My Passport 5 To). Le script de
backup ci-dessus était un brouillon — un script plus complet existait déjà en place :
`F:\BACKUP_ALFRED\SCRIPTS\alfred_backup.ps1` (modes Full hebdo / Incremental quotidien
`/M` / Assets+knowledges hebdo, couvre ALFRED_PC **et** ALFRED_WEB, rétention 15j,
déjà automatisé via tâche planifiée). Bug corrigé ce jour : `$BACKUP_ROOT`/`$LOG_DIR`
référençaient encore `E:\BACKUP_ALFRED\...` (ancienne lettre du disque WD, E: est
maintenant le lecteur virtuel "WD Unlocker" 10 Mo) → corrigés en `F:\BACKUP_ALFRED\...`.

### 🖥️ Setup bureau CPL

#### Écrans (4)
| Écran | Port | Support | Notes |
|-------|------|---------|-------|
| Gauche | HDMI | Commun aligné avec Centre | |
| Centre | DP (USB-C→DP) | Commun aligné avec Gauche | |
| Droit | HDMI → KVM | Individuel | Orientable H/V |
| Supérieur | HDMI → KVM | Individuel | |

#### Machines (ordre gauche → droite — cohérent disposition physique réelle)
| Position | Machine | Station d'accueil | Réseau |
|----------|---------|-------------------|--------|
| **Gauche** | PC Pro (futur) + PC visiteur | LaGreen (DP + Ethernet) — **active dès maintenant** | SG108E port 3 |
| **Centre** | MS-S1 MAX | Direct | SG108E port 1 |
| **Droite** | HP EliteBook | Dell (HDMI + Ethernet) | SG108E port 2 |

#### Commutateurs (ordre identique gauche → droite)
| Équipement | Ports | Rôle |
|-----------|-------|------|
| KVM HDMI 2×2 | PC Pro/visiteur ↔ EliteBook | Bascule écran Droit + Supérieur |
| Commut. USB 4/4 | P1: MS-S1 MAX / P2: St.Dell / P3: St.LaGreen / P4: libre | Webcam · Souris centrale · Clavier · Pavé numérique — P4 → PC visiteur futur |

#### Chaînes vidéo complètes
```
MS-S1 MAX ──USB-C→DP──────────────→ Écran Centre
MS-S1 MAX ──HDMI──────────→ KVM ──→ Écran Droit + Supérieur
EliteBook ──→ Station Dell ──→ KVM → Écran Droit + Supérieur
Station LaGreen ──────────────────→ Écran Gauche (HDMI) — active dès maintenant
  └── PC Pro / PC visiteur (futur)
```

#### Audio
| Équipement | Connexion | Usage |
|-----------|-----------|-------|
| Jabra dédiée | USB direct MS-S1 MAX | ALFRED permanent |
| Jabra BT | Bluetooth | EliteBook + PC Pro/visiteur |

#### Périphériques audio/vidéo
| Équipement | Quantité | Usage | Connexion |
|-----------|---------|-------|-----------|
| Webcam | 1 | Partagée 3 PC | Commutateur USB |
| Station Jabra | 1 | EliteBook + PC Pro partagée | À préciser |
| Station Jabra | 1 | **Dédiée MS-S1 MAX / ALFRED** | USB direct MS-S1 MAX |
| Lecteur empreinte | 1 | Authentification ALFRED | USB MS-S1 MAX (modèle à préciser) |

#### Webcam dédiée ALFRED (futur)
Specs cibles :
- 4K@30fps | AI face tracking | FOV 90°+ | HDR
- USB-C | OpenCV compatible | SDK Python
- Candidats : Logitech Brio 4K (~200€) / Insta360 Link 2 (~180€)

#### Réseau TP-Link — ✅ Segmentation VLAN opérationnelle (05/07/2026)

| Équipement | Modèle | Rôle | Statut |
|-----------|--------|------|--------|
| Box FAI | Bbox Must (Bouygues) | Modem — pas de vrai mode bridge sur ce modèle | `192.168.1.254`, DMZ active → ER605 |
| Routeur | ER605 (Omada) | Routeur + VLAN + pare-feu, sans WiFi (volontaire) | WAN `192.168.1.120` (réservé DHCP côté Bbox), LAN `192.168.0.1` |
| Switch | SG108E | 8 ports Gigabit manageable, 802.1Q | IP `192.168.0.101`, mdp admin changé |

```
Box Bouygues (192.168.1.254, DMZ→.120) ↔ CPL ↔ CPL ↔ ER605 (WAN .120 / LAN 192.168.0.1)
                                                          └── SG108E (192.168.0.101)
                                                                ├── Port 2 (PVID 20/ADMIN) : poste Dell
                                                                └── Port 3 (PVID 10/PC_ALFRED) : MS-S1 MAX — 192.168.10.100
```
⚠️ Ne pas empiler ER605 et SG108E — chaleur + vibrations. Poser côte à côte.

**Segmentation VLAN — réalisée et testée le 05/07/2026 :**
- VLAN 10 `PC_ALFRED` (`192.168.10.0/24`) — PC Alfred isolé, Internet + dashboard local validés
- VLAN 20 `ADMIN` (`192.168.20.0/24`) — poste Dell, accès SSH/RDP prévu vers VLAN10
- VLAN 30 `IOT` (`192.168.30.0/24`) — créé, aucun équipement branché pour l'instant
- **Double NAT résolu** via DMZ côté Bbox (le modèle Bbox Must n'a pas de vrai mode
  bridge total, seul le mode DMZ est disponible) → SSH externe validé fonctionnel
- **Pare-feu WAN ER605 vérifié conforme** : mdp admin changé, UPnP désactivé, gestion
  à distance WAN vide, aucune redirection de port superflue
- **Faille trouvée et corrigée** : l'adaptateur Wi-Fi du PC Alfred était actif et
  connecté directement à la Bbox (hors VLAN), contournant toute la segmentation —
  désactivé (`Disable-NetAdapter`)
- **Restant à faire** (reporté explicitement, ne pas relancer sans demande) : règles
  ACL inter-VLAN (actuellement tous les VLAN se joignent librement — la segmentation
  existe mais l'isolation n'est pas active), test d'isolation VLAN_DEFAULT, VPN
  OpenVPN scopé à VLAN_ADMIN, vérifs WAN restantes (ping ICMP, SPI, logs)
- **Point d'accès Wi-Fi Omada EAP610** — achat prévu **août 2026**, le Wi-Fi reste
  sur la Bbox en attendant (à couper une fois l'AP en place)
- Doc complète : `docs/smsi/vlan_config.md`, `docs/smsi/acces_distant_durcissement_wan.md`,
  schéma `docs/architecture/reseau_alfred.svg`

#### Alimentation
- Multiprise parafoudre 16A obligatoire
- Charge estimée : ~520W (MS-S1 MAX + écrans + stations + TP-Link)
- Stations Dell et LaGreen : alimentation secteur dédiée sur multiprise

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
- **LLM** : Ollama (remplace llama-cpp) — MS-S1 MAX
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
- ✅ Décision hardware finale : **Minisforum MS-S1 MAX 2 719 €** (commande passée,
  en attente réception)
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
    (`'`/`'` → `'`), mapping cassé (ascii→ascii) depuis une restauration précédente
  - `knowledges/core/system_rules.json` : nouvelle règle INT-007 (tutoiement obligatoire,
    jamais de "vous"/"votre"/"vos"), ajout de "obséder/obsède/obsédant" aux
    `forbidden_phrases` (retours utilisateur sur le ton d'ALFRED)
- ✅ `src/conversation/output/tts_piper.py` : ajout `_apply_fade()` — fondu d'entrée/
  sortie linéaire (~5 ms) appliqué à chaque buffer audio avant `sd.play()`. Cible le
  "clic"/grésillement entendu entre phrases quand `sd.play()` est appelé en rafale
  pendant le streaming (3/3 tests `test_tts_piper.py` OK).
- ✅ **BUG CRITIQUE mémoire/cwd** : `src/memory/long_term_memory.py`,
  `episodic_memory.py`, `memory_manager.py` utilisaient `Path("data/memory")`
  (relatif au cwd du shell) au lieu de `paths.PATHS.data_memory` (ancré sur la racine
  projet via `__file__`). Conséquence en conditions réelles (`python D:\...\main.py`
  lancé depuis `C:\Users\celin`) : DB SQLite/JSON créées hors du projet → mémoire vide
  d'une session à l'autre → ALFRED **invente de faux souvenirs**. Corrigé : les 3
  fichiers utilisent maintenant `PATHS.data_memory` (151 tests b02_b03+integration OK).
- ✅ Renforcement prompt système (response_generator.py) : règles explicites
  TUTOIEMENT OBLIGATOIRE (jamais "vous/votre/vos") et QUALITÉ DU FRANÇAIS OBLIGATOIRE
  + interdiction de faux souvenirs (CONTEXTE MÉMOIRE vs connaissance générale B18).
- ✅ **Session 13 juin 2026** — Fix bugs cwd-relatifs dans les modules sécurité
  (`src/auth/authenticator.py`, `src/security/device_registry.py`,
  `src/security/incident_manager.py`, `src/security/security_dashboard.py`) — même
  classe de bug que le fix mémoire ci-dessus, désormais corrigée partout.
- ✅ **Session 13 juin 2026** — Préparation matériel/poste de travail :
  - Convention **"ALFRED CORE"** sur `D:\ALFRED` (ollama models, vscode backup), disques
    renommés D:→"ALFRED" et F:→"BACKUP_ALFRED" (cf. section Architecture)
  - Migration modèles Ollama vers `D:\ALFRED\ollama\models` + `OLLAMA_MODELS` configuré
  - Backup VS Code (settings/keybindings/snippets/extensions) → `D:\ALFRED\vscode_backup`
  - `scripts/install_cpl_workstation_tools.ps1` + `scripts/setup_minisforum_ms_s1_max.ps1`
    créés pour l'installation à neuf du futur Minisforum (idempotents, via winget)
  - `src/llm/llm_client_ollama.py` : nouveaux profils `MODEL_PROFILES` pour modèles
    lourds (llama3.3:70b, qwen2.5:72b, command-r-plus:104b, gpt-oss:120b), support
    `keep_alive`/`timeout` configurables — préparation bascule LLM local 70-120B
  - Tri logiciels PC perso : 50 Go libérés sur C: (désinstallation VS2022, Apache
    Tomcat, Discord, SQL Server/MySQL, Unity Hub, Odoo, dossier Android orphelin)
  - 8 scripts PowerShell obsolètes supprimés (`git rm`) : scaffolding/migrations
    one-shot déjà exécutées et scripts redondants (cf. `scripts/` nettoyé)
  - Fix backup réel (`F:\BACKUP_ALFRED\SCRIPTS\alfred_backup.ps1`, bug drive E:→F:)
  - Schéma "Bureau CPL" prévisionnel documenté (4 écrans, KVM HDMI 2×2, réseau
    TP-Link, audio Jabra) + recommandation webcam ALFRED (Logitech Brio 4K /
    Obsbot Tiny 2 pour AI tracking)

### En attente 🕐
- MS-S1 MAX reçu et installé (fin juin 2026) — setup bureau CPL en cours d'affinage
- Vérifier en live si le grésillement TTS a disparu avec le fondu + le streaming réel
  (sinon : envisager un `sd.OutputStream` persistant au lieu de `sd.play()` par phrase)
- Vérifier en live que le tutoiement (INT-007) est bien respecté par le LLM
- Décision finale Docker Desktop sur ce PC (désinstallation actée, pas encore exécutée)
- ACL inter-VLAN, VPN VLAN_ADMIN, achat AP Wi-Fi Omada EAP610 (août 2026) — cf. section
  Réseau TP-Link ci-dessus, reportés explicitement par Céline
- ⚠️ **Trou de périmètre dashboards/manifest découvert le 08/07/2026** : `dashboard_data.json`
  (manifest 1362 fichiers, blocs `b01`→`b22`) et `dashboard_test.json` (généré par
  `ALFRED_PC/tests/run_all_tests.py`) sont scopés **exclusivement à ALFRED_PC**
  (`SCAN_DIRS = ["src", "tests", "tools", "scripts", "dashboard"]` dans
  `tools/apply_headers.py`, `TEST_GROUPS` fixes dans `run_all_tests.py`). Ils ne
  détecteront jamais les fichiers d'**ALFRED_WEB** (ex : `auth/`, `models/`,
  `data/postgres.py`, `migrations/` ajoutés ce jour pour les comptes utilisateurs
  PostgreSQL, Bloc 21.23) même une fois régénérés à jour. ALFRED_WEB a sa propre
  suite pytest (`ALFRED_WEB/tests/`) mais aucun système de manifest/statut fichier
  équivalent. Pas de correctif appliqué — juste consigné pour éviter de supposer à
  tort qu'un dashboard "à jour" couvre aussi ALFRED_WEB.

### Prochaines étapes 🎯
1. Relancer `start_alfred.bat` / `main.py` pour vérifier : lecture phrase par phrase,
   tutoiement cohérent, absence de crash webcam, plus d'AVERT pipeline B03/B13
2. Investiguer le grésillement audio TTS si toujours présent avec le streaming réel
3. Décider du périmètre du Bloc 23 "Gouvernance & pilotage du projet" pour les dashboards
4. Committer la restauration (B20 + B03/13 + B05 + B11 + B15 avatar + pipeline_bridge +
   llm_client_ollama streaming + fixes ton/apostrophe + fixes cwd sécurité + nettoyage
   scripts/contexte)
5. À réception du MS-S1 MAX : lancer `setup_minisforum_ms_s1_max.ps1`, migration +
   benchmark des profils LLM lourds (70B-120B), câblage bureau CPL

### Ordre de développement
```
Bloc 20 → V1 pipeline → personality_adapter.py
→ Moteur avatar Kivy → V2 fusion → V2++ knowledge
→ V3 orchestration → STT/TTS → V4 domotique → Android
```
*(toutes ces briques sont désormais codées et testées — V1.4 stable, 63.6% avancement global)*

---

## ✅ SESSION 9 — 08-09/07/2026 — Récapitulatif

**Extension architecture données (relationnel avancé + NoSQL + Big Data PoC) — demande référent thèse D52**

Séquence complète implémentée et testée sur ALFRED_WEB + ALFRED_PC (voir mémoire projet
`project_bdd_extension_deploiement_public` pour le détail complet) :

1. **PostgreSQL — comptes utilisateurs (Bloc 21.23, ALFRED_WEB)** : `data/postgres.py`,
   `models/user.py` (SQLAlchemy), Alembic (migrations versionnées), `auth/routes.py`
   (register/login/logout, bcrypt, CSRF). 11 tests pytest, tous verts contre PostgreSQL
   réel (Docker). Aucun système de comptes n'existait avant — ce n'était pas une
   "migration" SQLite→Postgres mais une création nette.

2. **MongoDB — préférences (Bloc 21.24) puis conversations (Bloc 21.25), ALFRED_WEB** :
   préférences (langue, police OpenDyslexic — les 2 seules préférences réellement
   existantes dans le code, vérifié avant de coder), consentement séparé de celui du
   compte (décision explicite de Céline). Scaffolding `conversations/` anticipatoire
   (aucun chat web n'existe encore), isolation stricte par `user_id`, index TTL 90 jours
   marqué placeholder (à confirmer via AIPD T001). 20 tests pytest supplémentaires.

3. **PoC Hadoop ciblé (Bloc B29, ALFRED_PC)** : anonymisation des vrais logs de
   sécurité (`scripts/anonymize_logs_for_hadoop.py`, 1399 lignes/~300 Ko réels),
   job MapReduce classique (`hadoop_poc/mapper.py`+`reducer.py`, validé en local avant
   toute infra), cluster Hadoop pseudo-distribué réel (`docker-compose.hadoop.yml`,
   5 conteneurs, référentiel communautaire big-data-europe/docker-hadoop, RAM/vCPU
   réduits). Bilan critique assumé (sobriété numérique) : `docs/hadoop_poc_bilan.md`.

**Tests & dashboards — trou de périmètre trouvé et partiellement comblé** :
- `tests/b29_tests/` créé (1 script = 1 test), intégré à `tests/run_all_tests.py`
  (nouveau groupe `b29`). Suite complète hors tests vocaux lents : **1289/1289, Grade A**.
- ⚠️ Découverte du 08/07/2026 (toujours vraie) : `dashboard_data.json`/`dashboard_tests.json`
  sont scopés à ALFRED_PC — les fichiers ALFRED_WEB n'y apparaissent que si explicitement
  listés dans `dashboard_data_manifest.json` (mécanisme `EXTERNAL_ROOTS` déjà présent mais
  jusque-là inutilisé pour les nouveaux fichiers). Comblé le 09/07/2026 : les 16 fichiers
  Phase 1/2 ALFRED_WEB ajoutés au bloc `b21` du manifest (tous `validated`). Nouveau bloc
  `b29` créé pour le PoC Hadoop (13 fichiers).
- `dashboard_security_manifest.json` / `dashboard_conformite/_manifest.json` /
  `dashboard_gouvernance/_manifest.json` : vérifiés — ce sont des référentiels d'exigences
  réglementaires (RGPD/ISO/AI Act) ou de modules sécurité Bloc 20, pas des registres de
  fichiers de code. Volontairement non modifiés (pas la même nature que
  `dashboard_data_manifest.json`) — à décider explicitement si une ligne de conformité
  doit être ajoutée pour l'anonymisation Hadoop.
- `sync_dashboards.py` **volontairement pas relancé** (auto-push GitHub + déploiement
  Render — toujours prévenir avant, cf. mémoire `feedback` dédiée).

**Rappel gate RGPD inchangé** : ne pas ouvrir d'inscription publique réelle avant que
l'AIPD T001 (backlog, toujours pas commencée) couvre le traitement des comptes/préférences/
conversations. Durée de rétention TTL des conversations (90j) et du Hadoop PoC restent
des placeholders à valider avec une vraie politique de rétention.

---

## ✅ SESSION 8 — 05/07/2026 — Récapitulatif

**Nettoyage dashboards + sécurisation réseau physique (Bloc 20)**

**Dashboards & git :**
- Sync ALFRED_PC/ALFRED_WEB nettoyé (doublons rapports gouvernance supprimés,
  ~30 anciens rapports fantômes purgés de git, fast-forward propre)
- Commits : ALFRED_PC `91981d2` puis `16333a5`, ALFRED_WEB `c6b60ce` puis `fe3c774`

**Réseau physique — VLAN 10/20/30 opérationnels :**
- Double NAT (Bbox Must ↔ ER605) résolu via DMZ côté Bbox — SSH externe validé
- Pare-feu WAN de l'ER605 vérifié conforme (mdp, UPnP, remote management, port
  forwarding — tous OK)
- Switch TL-SG108E et ER605 configurés en 802.1Q : VLAN 10 `PC_ALFRED`
  (`192.168.10.0/24`), VLAN 20 `ADMIN` (`192.168.20.0/24`), VLAN 30 `IOT`
  (`192.168.30.0/24`) — PC Alfred confirmé isolé sur `192.168.10.100`, Internet
  et dashboard local validés
- Faille de sécurité trouvée et corrigée en cours de test : adaptateur Wi-Fi de
  PC Alfred actif hors VLAN (connecté directement à la Bbox), désactivé
- Nouveaux docs SMSI : `docs/smsi/acces_distant_durcissement_wan.md` (VPN +
  durcissement WAN), `vlan_config.md` mis à jour (v1.2, procédure détaillée +
  réalisation), schéma `docs/architecture/reseau_alfred.svg` + section
  "Architecture réseau" simplifiée sur `hardware.html` (public)
- **Restant, reporté explicitement par Céline** ("un autre jour") : règles ACL
  inter-VLAN — ne pas relancer sans qu'elle le demande
- Achat point d'accès Wi-Fi Omada **EAP610** prévu **août 2026**

---

## ✅ SESSION 7 — 18/06/2026 — Récapitulatif

**B20 Gouvernance — Sprint conformité réglementaire (42% → 97% A+)**

Traitement exhaustif de toutes les priorités HAUTE et MOYENNE de l'audit gouvernance 2026-06-18.

**Livrables :**
- 24 documents de preuve créés dans `docs/smsi/` (RACI, AIPD, DPA, PCA, SSDLC, HITL, DdA…)
- `docs/gouvernance/consentement_art9.md` — procédure consentement RGPD Art.9
- `config/security/network_policy.json` — politique réseau ISO A.8.20
- Manifest gouvernance V1.1 — 28 exigences `todo → done`
- Headers CPL (bloc `PROJECT/BLOCK/VERSION/STATUS`) ajoutés à tous les docs/smsi
- Roadmap `update_gouvernance_data.py` mise à jour (jalons RGPD/ISO/AI Act/NIS2 terminés)
- Sync dashboards + push ALFRED_WEB

**Scores après sprint :**
| Norme | Avant | Après |
|---|---|---|
| RGPD | 68% (B) | 95.5% (A+) |
| ISO 27001 | 34% (C) | 98.4% (A+) |
| AI Act | 33% (C) | 91.7% (A+) |
| NIS2 | 50% (B) | 100% (A+) |
| **Global** | **42% (C)** | **97% (A+)** |

**3 partials légitimes restants :**
1. `RGPD-09` — DPA OpenAI : doc prête, acceptation portail platform.openai.com à faire
2. `ISO-20` — VLAN PC Alfred : architecture documentée, implémentation physique Q3 2026
3. `AIACT-06` — Registre UE IA : veille documentée, obligation non applicable (risque limité)

**Commits :** `feeee9d` (dev, 33 fichiers +2701 lignes) → merge main

---

## ✅ SESSION 6 — 15/06/2026 — Récapitulatif

1. **B05 — Tests authentification (FAIT)** — création de `tests/test_b05_auth.py`
   (32 tests) couvrant `auth_manager`, `login_handler`, `user_session`,
   `authenticator` (0 → 32 tests, gap sécurité comblé). Bug réel trouvé/corrigé :
   `user_session.get_session_profile()` faisait un `.copy()` superficiel
   (préférences mutables partagées) → passage en `copy.deepcopy`.
   Les 4 fichiers passent en `validated` (registry + dashboards + BACKLOG +
   `pilotage_projet_alfred.xlsm`). Suite complète : 1558/1558 tests OK.
   Commits ALFRED_PC `ffede3e` / `f28d468` (dev), ALFRED_WEB `79b64e4` (main).

2. **Promotion 15 fichiers testés → validés** (B01/B03/B11/B15/B18) — dashboards
   data/security/tests régénérés et synchronisés vers le site web.
   Commit ALFRED_PC `3682b6e` (dev), ALFRED_WEB `19c8ec3` (main).

3. **Corrections suite aux retours de test réel `python main.py`** :
   - Crash `AttributeError: HybridInputManager.get_voice_nowait` en mode
     vocal hybride (corrigé, puis remplacé par une approche `get_input()`
     bloquant clavier+voix dans une session parallèle).
   - Lecture TTS Piper mal encodée (caractères accentués) → forçage
     `PYTHONIOENCODING=utf-8` / `PYTHONUTF8=1` sur le subprocess Piper CLI.
   - `tools/sync_dashboards.py` manquant (seul le `.pyc` existait) — recréé
     depuis le bytecode, corrige aussi 2 bugs latents (comparaison de statut
     `"OK [sanitisé]"` qui annulait le push, et `SRC_TESTS` qui pointait vers
     un JSON obsolète). Script testé en live : sync + push OK vers ALFRED_WEB
     (commits `3567797`, `76135a4`).
   - ⚠️ En parallèle (autre session) : refonte de `main.py`/`input_manager.py`
     pour le mode vocal + ajout de `PiperTTS.last_amplitude` (RMS du buffer
     audio) transmis à `AvatarController` pour synchroniser le rythme de la
     bouche au volume réel — `tts_piper.py` passé en V1.2.

4. **Audit isolation tests `tests/security_tests/`** — `test_compliance_manager.py`
   appelait `delete_user_data(confirm=True)` sur `compliance_manager._ROOT` réel,
   supprimant à chaque run `data/user_memory.json`, `data/memory/episodic/
   dialogue_history.json` et `logs/security/security.log` → corrigé en
   monkeypatchant `_ROOT` vers `tmp_path`. Audit étendu à tout `tests/security_tests/` :
   `test_backup_security.py` écrivait/supprimait aussi dans le vrai `backup/security/`
   (`cleanup_old_backups` + `.manifest.json` via la constante séparée `MANIFEST_FILE`)
   → fixture autouse monkeypatchant `BACKUP_DIR` et `MANIFEST_FILE` vers `tmp_path`,
   18 fichiers `.bak` réels + dossier `backup/` nettoyés. Suite confirmée 651/651 OK,
   plus aucune écriture réelle. `dashboard/dashboard_data/validation_registry.json`
   mis à jour : 25 entrées `src/security/*` promues `validated`/`automated`
   (2026-06-15) + 17 nouvelles entrées ajoutées (api_security, asset_classifier,
   data_flow_mapper, data_protection, html_report, key_rotation_scheduler,
   disaster_recovery, network_security, pentest_report, rate_limiter, risk_engine,
   security_dashboard, security_governance, session_anomaly_detector, soc_monitor,
   tls_manager, unicode_sanitizer) — toutes couvertes par la suite pytest 651 tests.

---

## 📌 TÂCHES PRÉVUES — PROCHAINE SESSION

**Gouvernance (résiduel) :**
1. **DPA OpenAI (RGPD-09)** — Se connecter platform.openai.com → Settings → Data Processing Addendum → accepter → passer RGPD-09 `status: done` dans `_manifest.json` → relancer `update_gouvernance_data.py` → score ~98%
2. **VLAN PC Alfred (ISO-20)** — ✅ Segmentation réalisée et testée le 05/07/2026 (VLAN 10/20/30 actifs). Restant : règles ACL inter-VLAN (reportées, ne pas relancer sans demande). Détails dans `docs/smsi/vlan_config.md`

**Développement :**
3. **Test réel `python main.py`** — valider mémoire, tutoiement, français, streaming TTS + sync avatar/amplitude
4. **B08 — Trancher `data/personality.json`** (placeholder `{"core": {}, "adaptation": {}}`) — supprimer ou documenter son rôle futur
5. **UI `alfred_app.py`** — popup Réglages, caméra live, onboarding, fix Markdown
6. **Sprint "Fichiers codés à tester"** — blocs les plus faibles (B07 1.6%, B10 0%, B14 4%)

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
décision hardware MS-S1 MAX, stratégie stockage CPL, setup bureau complet.

**Ne réexplique pas ce qui est su. Propose, anticipe, code.**
Signale les incohérences sans attendre.
Adapte le niveau technique à la progression.
Respecte séparation public / privé expérimental.
Intègre toujours : max 6 calques, PNG optimisés, Kivy, local-first.

---
*Session 9 — 9 Juillet 2026*
*Prochaine mise à jour : après finalisation du bilan PoC Hadoop (résultat job réel), AIPD T001, ou ACL inter-VLAN/VPN VLAN_ADMIN/achat AP Wi-Fi Omada (août 2026)*
