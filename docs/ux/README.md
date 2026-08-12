# UX Documentation — ALFRED

Ce dossier sert de socle textuel aux principes UX du projet ALFRED. Il n'existe pas
(encore) d'outil de maquettage dédié (pas de fichier Figma réel à référencer) : ce
document remplace, en attendant, les wireframes par une description écrite des
décisions d'expérience utilisateur déjà prises et implémentées.

## Principes UX du projet

- **Avatar unique multi-produits** — un seul système de rendu d'avatar (calques
  F/G/BL/SP/M/V00-14, cf. `assets/avatars/avatar_medium/`) sert l'ensemble des
  produits ALFRED (ALFRED PC, ALFRED CPL, interface hybride). Pas de duplication
  d'identité visuelle par produit à ce stade.
- **UI hybride voix + texte** — fusion des modes d'interaction (plus de toggle
  exclusif voix/texte depuis le 22/07/2026) : l'utilisateur bascule librement
  entre les deux dans la même conversation, sans perte de contexte.
- **Synchro labiale phonème-exacte** — le retour visuel de l'avatar est
  synchronisé avec la sortie vocale (PiperTTS → table phonème→visème), pas une
  animation générique de bouche.
- **Design émotionnel** — l'interface adapte son ton et ses réponses au profil
  psychométrique de l'utilisateur (`personality_adapter.py`,
  `response_generator.py`) plutôt que d'imposer un ton unique.
- **Accessibilité dès la conception (WCAG / neurodiversité)** — modes
  d'accessibilité posés (voice_output_manager, text_reader, WCAG checker,
  Bloc 22) ; reste à couvrir : accessibilité Android, conformité WCAG formelle,
  neurodiversité avancée (cf. `dashboard/dashboard_data/dashboard_data.json`,
  bloc b22, items 22.12/22.13/22.15).
- **Local-first et transparence** — l'utilisateur doit pouvoir comprendre ce que
  fait l'assistant ; pas d'action silencieuse non explicable.

## Personas connus

- **Céline** — utilisatrice principale. Profil MBTI EXFP, dimension émotionnelle
  et onboarding santé complétés le 18/07/2026 (Q01→Q09 + HEXACO-24). C'est le
  profil pour lequel le comportement adaptatif d'ALFRED est aujourd'hui calibré.
- **Sébastien** — second utilisateur (47 ans, concubin de Céline, sécurité
  incendie). Identité seule renseignée à ce jour, pas d'onboarding complet — état
  cohérent avec le fait que le Chantier 2 (sécurité/accompagnement, qui le
  concerne comme contact de confiance) n'est encore qu'à l'état de vision écrite.

## Modules concernés

Ce document n'est pas une spécification technique ; il pointe vers les modules
où les décisions UX ci-dessus sont réellement implémentées :

- `interface/` — logique d'interface (hybride voix/texte, bascule de mode).
- `templates/` — gabarits HTML/CSS de l'UI desktop et des dashboards.
- `assets/avatars/avatar_medium/` — système avatar en calques.
- `src/ui/` — composants applicatifs (`alfred_app.py`, `webcam_widget.py`).
- `src/output/` — pipeline de sortie vocale (TTS) lié à la synchro labiale.
- Voir aussi `docs/architecture/README.md` pour la vue d'ensemble technique
  correspondante.

## Ce que ce document n'est pas

Pas de wireframes, pas de maquettes Figma, pas de parcours utilisateur formalisés
graphiquement — ALFRED est un projet solo (une seule développeuse) sans outil de
design dédié à ce stade. Ce texte sert de référence UX jusqu'à ce qu'un outil de
maquettage soit introduit dans le flux de travail, si le besoin s'en fait sentir.
