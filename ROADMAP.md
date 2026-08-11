# ALFRED Roadmap

Dernière mise à jour : 2026-08-11

> Voir aussi `docs/roadmap/ROADMAP_MASTER_V0_VFINALE.md` — vue complète Epic/Sprint/User story/Livrable
> (26 Blocs officiels), statuts croisés avec `dashboard/dashboard_data/dashboard_data.json` et anomalies
> détectées. Ce fichier-ci reste la version courte/chronologique ; l'autre est la version détaillée.

---

## V1 — Foundation ✅

- [x] Définir la vision produit ALFRED
- [x] Définir les principes local-first
- [x] Créer le système de mémoire épisodique
- [x] Organiser la base de connaissances (knowledges/)
- [x] Construire le premier dashboard de suivi
- [x] Explorer l'identité visuelle avatar
- [x] Implémenter la logique de réponse émotionnelle
- [x] Créer le pipeline conversationnel V1 (STT Whisper + LLM + TTS Piper)
- [x] Implémenter le routeur LLM local-first (Ollama → OpenAI → Anthropic)
- [x] Construire le module profil psychométrique (9 dimensions, Q01-Q09 + HEXACO-24)
- [x] Implémenter le pipeline de scoring psychométrique (40 règles → 9 paramètres ALFRED)
- [x] Créer la suite de tests d'intégration profil (35/35 ✅)
- [x] Implémenter le mode recherche (liberté interactionnelle élevée)
- [x] Documenter l'architecture technique (dossier_cadrage.html, 1 300+ lignes)
- [x] Créer la documentation gouvernance 360° (RGPD, EU AI Act, ISO 27001)
- [x] Mettre en place la politique de sécurité des données psychologiques (Fernet, .gitignore)

---

## V1.x — Modules actifs (session 18/06)

- [x] Improve avatar expression system (B15 — renderer 6 calques, halo, sprites par état)
- [x] Add simple animation states (idle/listening/thinking/speaking/support/focus + blink)
- [x] Improve dashboard readability (dashboards dynamiques B01-B22, avancement 63.6%)
- [x] Dashboard Conformité Réglementaire dynamique (B20 — 7 normes, score 97% A+)
- [x] RGPD complet — consentement Art.9, AIPD, DPA sous-traitants, procédure notification 72h CNIL
- [x] ISO 27001 SMSI — procédure incidents (P1→P4), post-incident analysis, KPI MTTD/MTTR
- [x] NIS2 — procédure signalement ANSSI/CERT-FR (H+24/H+72/J+30)
- [x] ALFRED Web — dossier cadrage intégré `/projet/cadrage` (sous-onglet)
- [x] Add accessibility modes (B22 — voice_output_manager, text_reader, WCAG checker)

---

## V1.4 — Sécurité réseau physique (session 05/07)

- [x] Résolution double NAT Bbox Must ↔ ER605 (DMZ, SSH externe validé)
- [x] Pare-feu WAN ER605 vérifié conforme (mdp, UPnP, remote management, port forwarding)
- [x] Micro-segmentation VLAN 10/20/30 opérationnelle (switch TL-SG108E + ER605) — Internet et dashboard local validés depuis VLAN10
- [x] Faille Wi-Fi PC Alfred (hors VLAN) trouvée et corrigée
- [x] Schéma réseau `docs/architecture/reseau_alfred.svg` + section publique `hardware.html`
- [ ] Règles ACL inter-VLAN — reporté explicitement, ne pas relancer sans demande
- [ ] VPN OpenVPN scopé VLAN_ADMIN
- [ ] Point d'accès Wi-Fi Omada EAP610 — achat prévu août 2026

---

## V1.4 — Profil IA Adaptative (en cours — branche feature)

- [x] Module `personality_adapter.py` — lecture profil → paramètres comportementaux
- [x] Module `response_generator.py` V2.3 — prompts adaptatifs + post-processing
- [x] Client `llm_client_anthropic.py` — fallback Anthropic Claude
- [x] Mode recherche `recherche_on` / `recherche_off` — console commande runtime
- [x] Arborescence documentation reworkée (dossier_cadrage.html v1.1)
- [x] Q01→Q09 — remplissage des réponses utilisateur (fait le 18/07/2026, onboarding complet MBTI EXFP + émotionnel + santé)
- [x] Fusion branche feature → dev (superseded — développement repris directement sur `main`, modules livrés et validés)

---

## V1.4 — Chantiers post-05/07 (sessions 22-24/07/2026)

- [x] UI hybride voix+texte — fusion des modes (plus de toggle exclusif), refus vocal figé supprimé, heure ancrée Europe/Paris
- [x] Article "Évolution de l'interface" publié (ALFRED_WEB, commit `18bbef4`)
- [x] Fix dashboard `/dashboard-gouvernance` — servait le mauvais contenu (doublon Conformité) depuis le 18/06, corrigé
- [x] Page "Qualité & Data" publiée avec contenu réel (registre RGPD 7 traitements, traçabilité, KPIs)
- [x] Système avatar en calques (F/G/BL/SP/M/V00-14) — tous créés, couture V-series/f00 corrigée (cv2.seamlessClone)
- [x] **Synchro labiale phonème-exacte** — PiperTTS→API Python, table phonème→visème, testée en conditions réelles (23/07)
- [x] **Chantier 1 — Google Agenda** : lecture + écriture confirmées sur le vrai compte (create/list/delete/modify event depuis le chat), commit `dac0a4f`
- [x] Function-calling réel branché au chat — corrige une hallucination d'UI (ALFRED CPL inventé)
- [x] Moteur de tâches complet (TaskEngine) + garde-fou anti-hallucination outils — ~35-40 % des appels d'outils llama3.2 n'aboutissaient à rien de réel avant le correctif, 0 fausse confirmation sur 8 essais après
- [x] Fixes TTS (élision "de X"→"d'X", lecture des balises entre crochets, double lecture heure/date)
- [x] Décision produit : fond visuel de l'avatar **neutre**, aligné sur l'interface existante (allège le système visuel, remplace la génération contextuelle de fonds prévue au Bloc 17)
- [ ] **Chantier 1B — Google Home/Nest : bloqué définitivement.** Code écrit (commit "feat(v4): intégration Google Home/Nest + vision sécurité domestique", 24/07) mais Céline n'a que des enceintes Nest, non supportées par l'API SDM (seuls thermostat/caméra/sonnette/Hub Max le sont). **Ne pas redépanner l'OAuth Google Home** — voir Tuya à la place.
- [ ] **Chantier 2 — Sécurité chute/accompagnement (Tuya)** : vision complète rédigée (`docs/module_securite_accompagnement/vision_securite_accompagnement_360.md`), Sébastien confirmé comme contact de confiance, caméras RTSP + audio bidirectionnel prévues. **3 inconnues Tuya non résolues bloquent tout début de code.**

---

## V2 — Interaction & Expérience Utilisateur

- [ ] Refonte interface principale (Kivy → UI enrichie)
- [ ] Concepts UI Figma
- [ ] Fondations design system
- [ ] Système d'expression avatar amélioré
- [ ] États d'animation simples
- [ ] Lisibilité dashboard améliorée
- [ ] Exploration interface Android
- [ ] Amélioration du flux d'interaction vocale
- [ ] Modes d'accessibilité
- [ ] Documentation des parcours utilisateurs
- [ ] Agent Arthur V2 (mémoire contextuelle avancée)

---

## V3 — Multi-Device & Assistant Avancé

- [ ] Architecture multi-appareils
- [ ] Stratégie de synchronisation locale
- [ ] Animation avatar avancée
- [ ] Améliorations offline-first
- [ ] Architecture plugin/module
- [ ] Modèle de confidentialité renforcé
- [ ] Documentation gouvernance IA éthique complète (AIPD, PSSI, SoA)
- [ ] Adaptation contextuelle avancée
- [ ] Mode démo public
- [ ] Showcase contributeurs

---

## Objectif de la reprise (11/08/2026)

Reprise après une pause de développement liée à un impératif de santé de Céline (plan de révision d'examens).
Objectif explicite : **un projet propre et démontrable pour les soutenances FEDE d'octobre 2026** (Mastère Expert IT
— IA & Big Data), pas seulement l'avancement brut vers V-finale.

- **UC D42** (mémoire projet tutoré ALFRED) — Prêt.
- **UC D52** (thèse pro "du cadrage méthodologique à la mise en œuvre technique") — En cours. **Soutenance principale pour laquelle ALFRED doit être démontrable.**
- **UC B5** (synthèse en anglais de la thèse D52) — À réaliser.

Voir `docs/roadmap/ROADMAP_MASTER_V0_VFINALE.md` pour le détail complet par Epic/Bloc, et l'exercice suivant
(tableau de tâches → Gantt) pour la mise en séquence vers cette échéance.

## Backlog — En attente

| Priorité | Item | Contexte |
|----------|------|---------|
| P1 | Mettre à jour la cible manifest du Bloc 17 (dashboard) | Cible encore à 230 fichiers alors que le fond visuel neutre a été tranché — affiche un faux 0 % sinon |
| P2 | Reconcilier profile_analyzer (src/core vs src/profile) | Doublon à nettoyer |
| P2 | Débloquer les 3 inconnues Tuya | Condition pour démarrer le code du Chantier 2 (sécurité/accompagnement) |
| P3 | Compléter gouvernance 360° (soa_iso27001, smsi) | Chantier audit certification |
| P3 | Mode démo public ALFRED | Après nettoyage données sensibles |
| P3 | ARTHUR | Volontairement non engagé — après ALFRED_PC et ALFRED_CPL "au point" (V4) |

*(Q01→Q09, AIPD T001 et PSSI formelle retirés de ce backlog le 11/08/2026 — déjà réalisés, cf. ci-dessus et `docs/roadmap/ROADMAP_MASTER_V0_VFINALE.md` section 5.)*
