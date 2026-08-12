# Architecture Documentation

Vue d'ensemble simplifiée de l'architecture technique d'ALFRED. Pour le détail
exhaustif module par module, voir `dossier_cadrage.html` (1 300+ lignes) et le
dashboard technique `dashboard/dashboard_data/dashboard_data.json`.

## Grands modules du dépôt (`src/`)

| Module | Rôle |
|---|---|
| `core/` | Noyau applicatif, orchestration générale |
| `conversation/`, `dialogue/` | Pipeline conversationnel (gestion des échanges, function-calling, TaskEngine) |
| `memory/` | Mémoire épisodique/longue, RAG (`rag/`) |
| `regulation/` | Régulation émotionnelle et adaptation comportementale (`personality_adapter.py`, `response_generator.py`) |
| `profile/` | Profil psychométrique utilisateur (9 dimensions, Q01-Q09 + HEXACO-24) |
| `security/`, `auth/` | Sécurité applicative, authentification, Zero Trust |
| `knowledge/` | Base de connaissances et routeur de connaissances |
| `ui/`, `output/`, `input/`, `vision/` | Interface utilisateur, sortie (TTS/avatar), entrée (STT), rendu visuel |
| `accessibility/` | Modes d'accessibilité (voice_output_manager, text_reader, WCAG checker) |
| `assistant_actions/` | Actions concrètes de l'assistant (agenda, tâches, intégrations) |
| `integrations/` | Connecteurs externes (Google Agenda, Outlook, etc.) |
| `health/` | Volet santé/bien-être (support, pas de diagnostic) |
| `v1/`, `v2/`, `v2pp/`, `v3/`, `v4/` | Versions successives des règles et moteurs de config, montée en version progressive (cf. `config/vX/`) |

Points d'entrée principaux : `src/main.py` (pipeline principal), `src/main_v3.py`,
`src/alfred_desktop.py`, `src/alfred_with_ui.py`.

## Réseau

[reseau_alfred.svg](reseau_alfred.svg) — Architecture réseau domestique ALFRED :
Internet → Bbox Must → ER605 (segmentation VLAN 10/PC_ALFRED, 20/ADMIN,
30/IOT) → switch TL-SG108E → postes finaux. État au 2026-07-05 : DMZ et
pare-feu WAN réalisés et testés, ACL inter-VLAN restantes. Détails et
procédures : `../smsi/vlan_config.md`, `../smsi/acces_distant_durcissement_wan.md`.

Confidentiel interne (IP et topologie détaillées) — ne pas publier tel quel.

## Sécurité / SMSI

Le système de management de la sécurité de l'information (SMSI, démarche ISO
27001) est documenté séparément :

- `../security/PSSI.md` — Politique de Sécurité des Systèmes d'Information.
- `../smsi/` — procédures détaillées : gestion des incidents
  (`procedure_incidents.md`), notification de violation RGPD 72h
  (`procedure_notification_violation.md`), signalement NIS2
  (`procedure_signalement_nis2.md`), déclaration d'applicabilité
  (`declaration_applicabilite.md`), inventaire des actifs
  (`inventaire_actifs.json`), plan de continuité d'activité (`pca.md`), et
  autres procédures opérationnelles (chiffrement disque, antimalware,
  durcissement accès distant, revue de code, audit interne).
- `../rgpd/` — volet RGPD (AIPD données de santé, AIPD comptes déploiement
  public, DPA sous-traitants).

## Périmètre de ce document

Ce README reste une vue d'ensemble d'orientation, pas une spécification
exhaustive : en cas de divergence avec le code ou avec `dossier_cadrage.html`,
ces derniers font foi.
