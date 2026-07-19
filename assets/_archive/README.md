# Archive assets — évolution interface graphique (2026-07-18)

Dossiers archivés lors du passage à l'avatar `avatar_medium` :

- `no_active_avatar_normal/` — ancien système d'avatar (base_normal), remplacé par
  `assets/avatars/avatar_medium/`. Le fallback correspondant a été retiré de
  `src/ui/avatar_renderer.py` (les sprites medium couvrent désormais tous les états).
- `avatar/` — ancien dossier `assets/avatar` (singulier), non référencé par le code actif.
- `backgrounds/` — décors de fond archivés sans remplacement actif pour l'instant ;
  `tests/b17_tests/test_smoke_backgrounds_batch1.py` est mis en pause (skip) en attendant
  un nouveau système de backgrounds.

Ne pas restaurer sans mettre à jour en parallèle `src/ui/avatar_renderer.py`,
les smoke tests concernés et `config/v2/module_mapping.json`.
