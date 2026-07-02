# Archive — fichiers obsolètes

Fichiers déplacés ici le 02/07/2026 lors de la réconciliation de la numérotation des blocs (voir `docs/ALFRED_BLOCS_REFERENCE.md`).

## `dashboard_manifest.json`

Ancien manifeste de suivi par bloc (`dashboard/dashboard_manifest.json`). Confirmé **non lu par aucun script actif** du pipeline dashboard — la source réelle est `dashboard/dashboard_data/dashboard_data_manifest.json`. Utilisait sa propre numérotation de blocs, différente à la fois du "Dashboard ancien" et du "Bloc officiel", source de confusion.

## `patch_manifest.py`

Script ad hoc à usage unique qui patchait `dashboard_manifest.json` ci-dessus (ajout de fichiers à b01/b02). Devenu sans objet puisque le fichier qu'il patchait est lui-même obsolète.

**Pourquoi conservés plutôt que supprimés** : traçabilité et référence si jamais un besoin similaire (manifeste alternatif) se représente. Historique complet également disponible via `git log --follow`.
