# ALFRED Roadmap

Dernière mise à jour : 2026-06-18

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
- [x] Module `response_generator.py` V2.3 — prompts adaptatifs + post-processing
- [x] Client `llm_client_anthropic.py` — fallback Anthropic Claude
- [x] Mode recherche `recherche_on` / `recherche_off` — console commande runtime
- [x] Arborescence documentation reworkée (dossier_cadrage.html v1.1)
- [ ] Q01→Q09 — remplissage des réponses utilisateur (en attente)
- [ ] Fusion branche feature → dev (pipeline complet Kivy + Avatar)

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

## Backlog — En attente

| Priorité | Item | Contexte |
|----------|------|---------|
| P1 | Remplissage Q01→Q09 utilisateur | Main bloquée par douleur mains |
| P1 | AIPD T001 (RGPD art.35) | Obligatoire avant production |
| P1 | PSSI formelle | docs/gouvernance/PSSI_formelle.md |
| P2 | Reconcilier profile_analyzer (src/core vs src/profile) | Doublon à nettoyer |
| P2 | Merge feature branch → dev | Pipeline complet Kivy + modules B |
| P3 | Compléter gouvernance 360° (soa_iso27001, smsi) | Chantier audit certification |
| P3 | Mode démo public ALFRED | Après nettoyage données sensibles |
