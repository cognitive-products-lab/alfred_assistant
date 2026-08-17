# Module profil système — CLI manuel (Bloc 04.01)

`src/core/profile_analyzer.py` (classe `ProfileAnalyzer`) est un outil **CLI manuel** de scoring psychométrique : calcule les scores normalisés à partir de réponses déjà collectées, fusionne avec un profil AssessFirst, chiffre les réponses sensibles (Fernet). Usage documenté dans [`guide_utilisateur.md`](guide_utilisateur.md) (`python src/core/profile_analyzer.py --report-only`, `--decrypt`, etc.).

**Ce n'est pas la même chose que** `src/health/onboarding.py::OnboardingSession`, qui est le flux **conversationnel réellement branché dans l'app live** (`main.py`) — celui utilisé pour l'onboarding réel de Céline le 18/07/2026 (santé, personnalité MBTI, émotionnel).

**Ce n'est pas non plus** `src/profile/profile_analyzer.py::QuestionnaireSession` (instruments HEXACO-24/SWLS/PANAS/ERQ/PSS/SDT, passation Q00-Q09), documenté dans [`docs/module_profil_ia_adaptative/`](../module_profil_ia_adaptative/README.md) — un module de profilage plus riche, conçu et testé, mais lui non plus jamais branché dans `main.py`.

**Trois pipelines de profilage distincts coexistent volontairement dans le projet** (clarifié le 17/08/2026, l'ancien backlog les qualifiait à tort de "doublon à nettoyer") :

| Pipeline | Fichier | Branché en live ? | Documentation |
|---|---|---|---|
| Onboarding conversationnel | `src/health/onboarding.py` | **Oui** — via `main.py` | — |
| Scoring CLI manuel + chiffrement | `src/core/profile_analyzer.py` | Non | `docs/profil_systeme/` (ce dossier) |
| Questionnaires HEXACO/SWLS enrichis | `src/profile/profile_analyzer.py` | Non | `docs/module_profil_ia_adaptative/` |

Aucun des trois n'est du code mort : chacun a sa propre suite de tests et, pour les deux non branchés, sa propre documentation utilisateur complète. Décision (re)confirmée : ne rien fusionner/supprimer sans un chantier dédié qui statuerait explicitement sur l'intégration ou l'abandon de l'un des deux pipelines non branchés.
