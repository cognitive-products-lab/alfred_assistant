# ALFRED Roadmap

Dernière mise à jour : 2026-07-02

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

## V1.4 — Profil IA Adaptative (en cours — branche feature)

- [x] Module `personality_adapter.py` — lecture profil → paramètres comportementaux
- [x] Module `response_generator.py` V2.3 — prompts adaptatifs + post-processing + règle tutoiement absolu
- [x] Client `llm_client_anthropic.py` — fallback Anthropic Claude
- [x] Mode recherche `recherche_on` / `recherche_off` — console commande runtime
- [x] Arborescence documentation reworkée (dossier_cadrage.html v1.1)
- [x] Upgrade hardware PC Alfred Core — Miniforum MS-S1 Max 64Go/2To + disques CORE 4To/BACKUP 5To (27/06/2026, 3127€) — nécessaire pour avancer le dev LLM local + RAG sans contrainte matérielle. Détail : `/hardware`
- [x] Migration PC Alfred Core (DESKTOP-THFV312) — environnement complet opérationnel 29/06/2026
- [x] TTS stack opérationnelle : piper-tts 1.4.2, sounddevice, soundfile, faster-whisper
- [x] `personality_celine.json` créé (minimal — onboarding complet à faire)
- [ ] Q01→Q09 — remplissage des réponses utilisateur (en attente douleur mains)
- [ ] Fusion branche feature → dev (pipeline complet Kivy + Avatar) — **prévu mercredi 02/07**
- [ ] Calques eye/mouth définitifs — patch provisoire actif (prévu vendredi 04/07)

---

## V2 — Interaction & Expérience Utilisateur

- [ ] Refonte interface principale (Kivy → UI enrichie)
- [ ] Concepts UI Figma
- [ ] Fondations design system
- [ ] Système d'expression avatar amélioré
- [ ] États d'animation simples
- [ ] Lisibilité dashboard améliorée
- [x] Exploration interface Android — PoC client compagnon (02/07/2026)
- [ ] Amélioration du flux d'interaction vocale
- [ ] Modes d'accessibilité
- [ ] Documentation des parcours utilisateurs
- [ ] Agent Arthur V2 (mémoire contextuelle avancée)

### Android — du PoC compagnon au produit complet

- [x] PoC v1 — API compagnon locale FastAPI (`interface/companion_api.py`,
      lecture seule : statut + rappels, jeton partagé `COMPANION_API_TOKEN`)
- [x] PoC v1 — app Android native Kotlin (`ALFRED_ANDROID/`, Jetpack Compose +
      MVVM + Retrofit, écran statut/rappels)
- [ ] Authentification compagnon alignée Bloc 20 (remplacer le jeton partagé
      statique par un appairage PIN/QR code, cohérent avec `src/auth/`)
- [ ] Notifications push réelles (au-delà du polling manuel du PoC)
- [ ] Mode hors-ligne / cache local (Room) pour les rappels déjà synchronisés
- [ ] Réutilisation du moteur avatar (halo/animations, cf. `src/ui/avatar_engine.py`)
      sur Android — écran avatar au lieu du simple écran statut/rappels
- [ ] Parité fonctionnelle progressive avec ALFRED desktop (conversation,
      mémoire, profil adaptatif) — dépend de l'avancement V3/V4 desktop
- [ ] Build signé + distribution interne (hors store dans un premier temps)

---

## V3 — Multi-Device & Assistant Avancé

- [ ] Upgrade hardware — Serveur Threadripper (TR 7960X 24C, 256Go DDR5 ECC, 8To NVMe) — orchestration multi-agents ALFRED V4+, hébergement CPL production Docker. Détail : `/hardware` Phase 2
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

## Backlog — En attente

| Priorité | Item | Contexte |
|----------|------|---------|
| Priorité | Item | Contexte |
|----------|------|---------|
| P1 | Merge feature branch → dev | **Mercredi 02/07** — pipeline complet Kivy + modules B |
| P1 | Pipeline voix end-to-end (STT + TTS) | **Mercredi 02/07** — faster-whisper + piper activés |
| P1 | Monter modèle Ollama (llama3.1:8b+) | **Mercredi 02/07** — nouveau PC sans contrainte |
| P1 | B02 Mémoire & RAG (ChromaDB) | **Vendredi 04/07** |
| P1 | Calques eye/mouth définitifs | **Vendredi 04/07** — patch provisoire actif |
| P1 | Remplissage Q01→Q09 utilisateur | En attente douleur mains |
| P1 | AIPD T001 (RGPD art.35) | Obligatoire avant production |
| P1 | PSSI formelle | docs/gouvernance/PSSI_formelle.md |
| ✅ | ~~Page "tous les articles" ALFRED_WEB~~ | Fait 02/07/2026 — `/articles/tous-les-articles`, persistance MongoDB (`data/articles_repository.py`) |
| P2 | Reconcilier profile_analyzer (src/core vs src/profile) | Doublon à nettoyer |
| P3 | Compléter gouvernance 360° (soa_iso27001, smsi) | Chantier audit certification |
| P3 | Mode démo public ALFRED | Après nettoyage données sensibles |
